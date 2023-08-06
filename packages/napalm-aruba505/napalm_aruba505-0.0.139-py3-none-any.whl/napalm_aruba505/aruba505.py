# -*- coding: utf-8 -*-
"""NAPALM ArubaOS Five zero five Handler."""

import copy
import functools
import os
import re
import socket
import telnetlib
import tempfile
import time
import uuid
from collections import defaultdict

from netaddr import IPNetwork
from netaddr.core import AddrFormatError
from netmiko import FileTransfer, InLineTransfer

import napalm.base.constants as C
import napalm.base.helpers
from napalm.base.base import NetworkDriver
from napalm.base.exceptions import (
    ReplaceConfigException,
    MergeConfigException,
    ConnectionClosedException,
    CommandErrorException,
    CommitConfirmException,
)
from napalm.base.helpers import (
    canonical_interface_name,
    transform_lldp_capab,
    textfsm_extractor,
    split_interface,
    abbreviated_interface_name,
    generate_regex_or,
    sanitize_configs,
)
from napalm.base.netmiko_helpers import netmiko_args
from netmiko import ConnectHandler

# Easier to store these as constants
SECONDS = 1
MINUTE_SECONDS = 60
HOUR_SECONDS = 3600
DAY_SECONDS = 24 * HOUR_SECONDS
WEEK_SECONDS = 7 * DAY_SECONDS
YEAR_SECONDS = 365 * DAY_SECONDS


class Aruba505Driver(NetworkDriver):
    """NAPALM ArubaOS [505, 505H, 515] Handler."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """NAPALM Cisco IOS Handler."""

        if optional_args is None:
            optional_args = {}
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.transport = optional_args.get('transport', 'ssh')
        self.interfaces = []
        # Netmiko possible arguments
        netmiko_argument_map = {
            'port': None,
            'secret': '',
            'verbose': False,
            'keepalive': 30,
            'global_delay_factor': 1,
            'use_keys': False,
            'key_file': None,
            'ssh_strict': False,
            'system_host_keys': False,
            'alt_host_keys': False,
            'alt_key_file': '',
            'ssh_config_file': None,
            'allow_agent': False,
        }

        # Build dict of any optional Netmiko args
        self.netmiko_optional_args = {}
        for k, v in netmiko_argument_map.items():
            try:
                self.netmiko_optional_args[k] = optional_args[k]
            except KeyError:
                pass

        default_port = {'ssh': 22}
        self.port = optional_args.get('port', default_port[self.transport])
        self.device = None
        self.config_replace = False
        self.interface_map = {}
        self.platform = "cisco_ios"
        self.profile = [self.platform]
        # self.device.enable()

    def open(self):
        """Open a connection to the device."""
        device_type = "cisco_ios"
        if self.transport == "telnet":
            device_type = "cisco_ios_telnet"
        self.device = self._netmiko_open(
            device_type, netmiko_optional_args=self.netmiko_optional_args
        )

    def close(self):
        """Close the connection to the device and do the necessary cleanup."""
        self._netmiko_close()

    def is_alive(self):
        """Returns a flag with the state of the connection."""
        null = chr(0)
        if self.device is None:
            return {'is_alive': False}
        else:
            # SSH
            try:
                # Try sending ASCII null byte to maintain the connection alive
                self.device.write_channel(null)
                return {'is_alive': self.device.remote_conn.transport.is_active()}
            except (socket.error, EOFError):
                # If unable to send, we can tell for sure that the connection is unusable
                return {'is_alive': False}

    @staticmethod
    def _send_command_postprocess(output):
        """
        Cleanup actions on send_command() for NAPALM getters.
        Remove "Load for five sec; one minute if in output"
        Remove "Time source is"
        """
        output = re.sub(r"^Load for five secs.*$", "", output, flags=re.M)
        output = re.sub(r"^Time source is .*$", "", output, flags=re.M)
        return output.strip()

    def _send_command(self, command):
        """Wrapper for self.device.send.command().
        If command is a list will iterate through commands until valid command.
        """
        try:
            if isinstance(command, list):
                for cmd in command:
                    output = self.device.send_command(cmd)
                    if "% Invalid" not in output:
                        break
            else:
                output = self.device.send_command(command)
            return self._send_command_postprocess(output)
        except (socket.error, EOFError) as e:
            raise ConnectionClosedException(str(e))

    def get_config(self, retrieve="all", full=False, sanitized=False):
        """
        Get config from device.
        Returns the running configuration as dictionary.
        The candidate and startup are always empty string for now,
        """

        configs = {
            "running": "",
            "startup": "No Startup",
            "candidate": "No Candidate"
        }

        if retrieve.lower() in ('running', 'all'):
            command = "show running-config"
            output_ = self._send_command(command)
            if output_:
                configs['running'] = output_
                data = str(configs['running']).split("\n")
                non_empty_lines = [line for line in data if line.strip() != ""]

                string_without_empty_lines = ""
                for line in non_empty_lines:
                    string_without_empty_lines += line + "\n"
                configs['running'] = string_without_empty_lines

        if retrieve.lower() in ('startup', 'all'):
            pass
        return configs

    def show_summary_sanitizer(self, data):
        """ Collects the fqdn and the serial number from the 'show summary'
        :returns a tuple with two values (hostname, fqdn, serial_number)
        """

        fqdn = ""
        serial_number = ""
        hostname_ = ""

        if data:
            data_l = data.strip().splitlines()

            for l in data_l:
                if "Name" in l and not hostname_:
                    hostname_ = f"{l.split(':')[1].lower()}"
                if "DNSDomain" in l and hostname_:
                    fqdn = f"{hostname_}.{l.split(':')[1]}"
                if "Serial Number" in l:
                    serial_number = l.split(':')[1]
        return hostname_, fqdn, serial_number

    def show_version_sanitizer(self, data):
        """ Collects the vendor, model, os version and uptime from the 'show version'
        :returns a tuple with two values (vendor, model, os version, uptime)
        """
        # Initialize to zero
        (years, weeks, days, hours, minutes, seconds) = (0, 0, 0, 0, 0, 0)
        vendor = "Hewlett Packard"
        model = ""
        os_version = ""
        uptime = ""

        if data:
            data_l = data.strip().splitlines()
            for l in data_l:
                if "MODEL" in l:
                    model, os_version = l.split(',')
                if "AP uptime is" in l:
                    tmp_uptime = l.replace("AP uptime is", "").split()
                    uptimes_records = [int(i) for i in tmp_uptime if i.isnumeric()]

                    if uptimes_records and len(uptimes_records) >= 5:
                        weeks, days, hours, minutes, seconds = uptimes_records
                        uptime = float(sum([(years * YEAR_SECONDS), (weeks * WEEK_SECONDS), (days * DAY_SECONDS),
                                            (hours * HOUR_SECONDS), (minutes * MINUTE_SECONDS), (seconds * SECONDS), ]))
                    if uptimes_records and len(uptimes_records) == 4:
                        weeks, days, hours, minutes = uptimes_records
                        uptime = float(sum([(years * YEAR_SECONDS), (weeks * WEEK_SECONDS), (days * DAY_SECONDS),
                                            (hours * HOUR_SECONDS), (minutes * MINUTE_SECONDS), (seconds * SECONDS), ]))

        return vendor, model, os_version, uptime

    def get_facts(self):
        """Return a set of facts from the devices"""
        interface_list = list(self.get_interfaces().keys())
        configs = {}
        show_version_output = self._send_command("show version")
        show_summary_output = self._send_command("show summary")

        # processing 'show version' output
        configs['show_version'] = show_version_output
        show_version_data = str(configs['show_version']).split("\n")
        show_version_non_empty_lines = [line for line in show_version_data if line.strip() != ""]

        show_version_string_ = ""
        for line in show_version_non_empty_lines:
            show_version_string_ += line + "\n"
        vendor, model, os_version, uptime = self.show_version_sanitizer(show_version_string_)

        # processing 'show summary' output
        configs['running_'] = show_summary_output
        data = str(configs['running_']).split("\n")
        non_empty_lines = [line for line in data if line.strip() != ""]

        show_summary_string_ = ""
        for line in non_empty_lines:
            show_summary_string_ += line + "\n"
        hostname_, fqdn_, serial_number_ = self.show_summary_sanitizer(show_summary_string_)

        return {
            "hostname": str(hostname_),
            "fqdn": fqdn_,
            "vendor": str(vendor),
            "model": str(model),
            "serial_number": str(serial_number_),
            "os_version": str(os_version).strip(),
            "uptime": uptime,
            "interface_list": interface_list,
        }

    def get_lldp_neighbors(self):
        """This code has been tested for HP SW, Cisco FTTX and Nokia ONT"""
        system_name = ""
        interface_description = ""
        lldp = {}

        command = "show ap debug lldp neighbor interface eth0"
        result = self._send_command(command)
        data = [line.strip() for line in result.splitlines()]
        for line in data:
            if line:
                if "System name:" in line:
                    system_name = line.split()[2]
                if "Interface description:" in line:
                    if "Interface description: Not received" in line:
                        interface_description = line.split()[5].replace(",", "")
                    else:
                        interface_description = line.split()[2].replace(",", "")
        lldp["eth0"] = [{"hostname": system_name, "port": interface_description}]
        return lldp

    def sanitize_interface_status(self, data):
        # process the show interface output
        new_data = [line.strip() for line in data.splitlines()]
        if new_data:
            for line in new_data:
                if "Admin Status" in line:
                    status = line.split(":")[1]
                    return status

    def get_interfaces_status(self):
        # This function can be used to get the status of each interface
        interface_e0_status = self.sanitize_interface_status(
            self._send_command("show wired - port - settings E0"))
        time.sleep(1)
        interface_e1_status = self.sanitize_interface_status(
            self._send_command("show wired - port - settings E1"))
        time.sleep(1)
        interface_e2_status = self.sanitize_interface_status(
            self._send_command("show wired - port - settings E2"))
        time.sleep(1)
        interface_e3_status = self.sanitize_interface_status(
            self._send_command("show wired - port - settings E3"))
        time.sleep(1)
        interface_e4_status = self.sanitize_interface_status(
            self._send_command("show wired - port - settings E4"))

        return [interface_e0_status, interface_e1_status,
               interface_e2_status, interface_e3_status, interface_e4_status]

    def get_interfaces(self):
        """
        Returns a dictionary of dictionaries. The keys for the first dictionary will be the \
        interfaces in the devices. The inner dictionary will containing the following data for \
        each interface:

         * is_up (True/False)
         * is_enabled (True/False)
         * description (string)
         * last_flapped (float in seconds)
         * speed (int in Mbit)
         * MTU (in Bytes)
         * mac_address (string)
        """
        show_interfaces = "show interface"
        data = self._send_command(show_interfaces)

        # process the show interface output
        new_data = [line.strip() for line in data.splitlines()]
        interfaces = {}
        temp_list = []

        for line in new_data:
            if line.startswith("eth"):
                temp_list.append(line.split()[0])
                if "line protocol is up" in line:
                    temp_list.append(True)
                    temp_list.append(True)
                elif "line protocol is down" in line:
                    temp_list.append(False)
                    temp_list.append(False)

            if line.startswith("bond0"):
                # For ArubaOS (MODEL: 505)
                temp_list.append(line.split()[0])
                if "line protocol is up" in line:
                    temp_list.append(True)
                    temp_list.append(True)

            if line.startswith("Hardware is"):
                temp_list.append(line.split()[-1])

            if "Speed" and 'duplex' in line:
                line = line.split()[1]
                if "unknown" in line:
                    temp_list.append("unknown")
                elif "Mb/s," in line:
                    temp_list.append(line.replace("Mb/s,", ""))
                interfaces[f"{temp_list[0]}"] = {
                    'is_up': temp_list[1],
                    'is_enabled': temp_list[2],
                    'description': '',
                    'last_flapped': -1.0,
                    'speed': temp_list[4],
                    'mtu': 0,
                    'mac_address': temp_list[3],
                }
                temp_list.clear()

        return interfaces

    def get_environment(self):
        """
        Get environment facts.
        """
        environment = {}
        mem_cmd = "sh memory"
        cpu_cmd = "show cpu"

        environment.setdefault("cpu", {})
        environment["cpu"][0] = {}
        environment["cpu"][0]["%usage"] = 0.0
        environment.setdefault("memory", {})

        cpu_output = self._send_command(cpu_cmd)
        # process cpu outputs
        data = [line.strip() for line in cpu_output.splitlines() if "system" in str(line)]
        current_cpu_usage = 0
        for line in data:
            if line:
                per = line.strip()[-2:-1]
                current_cpu_usage += int(per)

        # process the show memory output
        output_ = self._send_command(mem_cmd)
        available_ram = None
        free_ram = None
        for line in output_.splitlines():
            if "MemTotal:" in line:
                available_ram = int(line.split()[1])
            if "MemAvailable:" in line:
                free_ram = int(line.split()[1])

        environment["cpu"][0]["%usage"] = float(current_cpu_usage)
        environment["memory"]["available_ram"] = available_ram
        environment["memory"]["used_ram"] = available_ram - free_ram

        return environment

    def cli(self, commands):
        """
        Execute a list of commands and return the output or results in a dictionary format
        using the command as the key.
        """
        cli_output = dict()
        if type(commands) is not list:
            raise TypeError("\nPlease enter a valid list of commands!\n")

        for command in commands:
            output = self._send_command(command)
            if "Invalid input:" in output or "error" in output or "Invalid" in output or "invalid" in output:
                raise ValueError('Unable to execute command "{}"'.format(command))
            cli_output.setdefault(command, {})
            cli_output[command] = output

        return cli_output

    def get_vlans(self):
        data = self._send_command("show network")
        if data:
            new_data = [line.strip() for line in data.splitlines()]
            vlans = {}
            for i in new_data:
                if "employee  all   Per User" in i:
                    line = i.split()
                    vlans[f"{line[0]}"] = line[9]
            return vlans