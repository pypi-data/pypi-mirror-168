#!/usr/bin/python3

"""checks ansible configuration"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import os

from rich import print
from logging import debug

from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.template import Templar

import nb2an.netbox


def parse_args():
    "Parse the command line arguments."
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: ")

    parser.add_argument("-i", "--inventory-file", default="hosts", type=str,
                        help="The name of the inventory/hosts list file")

    parser.add_argument("-H", "--hosts", default=None, type=str, nargs="*",
                        help="A specific set of hosts to check")

    parser.add_argument("--log-level", "--ll", default="warning",
                        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).")

    parser.add_argument("-d", "--ansible-directory",
                        type=str, help="The ansible directory to verify")

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level,
                        format="%(levelname)-10s:\t%(message)s")
    return args


def main():
    args = parse_args()

    nb = nb2an.netbox.Netbox()
    config = nb.get_config()

    ansible_directory = args.ansible_directory
    if not ansible_directory:
        ansible_directory = config.get("ansible_directory")

    if not ansible_directory or not os.path.exists(ansible_directory):
        error("Failed to find expansible directory")
        exit(1)

    hosts = os.path.join(ansible_directory, args.inventory_file)
    if not os.path.exists(hosts):
        error("Failed to find the path to the inventory file")
        exit(1)

    # setup ansible
    dl = DataLoader()
    im = InventoryManager(loader=dl, sources=[hosts])
    vm = VariableManager(loader=dl, inventory=im)

    check_interfaces(vm, dl, im, nb, args.hosts)


def check_interfaces(vm, dl, im, nb, hosts=None):
    # set up ansible config grabber

    # get netbox devices
    netbox_addrs = nb.get_addresses()

    host_list = netbox_addrs.keys()
    if hosts:
        host_list = hosts
    for host in host_list:

        try:
            # get ansible config for this host
            search_host = host
            if not host.endswith(nb.suffix):
                search_host = search_host + nb.suffix
            ansible_host = im.get_host(search_host)
            vars = vm.get_vars(host=ansible_host)
            templar = Templar(loader=dl, variables=vars)

            if 'net_config' not in vars:
                warning(f"{search_host} does not have \"net_config\" in ansible")
                continue

            netconf = templar.template(vars['net_config'])

            # compare each interface on the host
            if len(netbox_addrs[host]) == 0:
                warning(f"{host}: no interfaces in netbox")
                continue

            for interface in netbox_addrs[host]:
                debug(f"starting {host} {interface}")

                for i in netconf:
                    if 'ipaddr' in i and i['name'] == interface:
                        debug(i)
                        debug(netbox_addrs[host][interface])

                        label = host + "/" + interface + ":"
                        # check v4
                        if 'IPv4' in netbox_addrs[host][interface]:
                            netbox_addr = netbox_addrs[host][interface]['IPv4']
                            netbox_addr = netbox_addr[0:netbox_addr.find("/")]
                            if netbox_addr != i['ipaddr']:
                                warning(f"{label:<25} netbox={netbox_addr:<25} ansible={i['ipaddr']:<25}")
                            else:
                                info(f"{label:<25} IPv4 values match")

                        # check v6
                        if 'IPv6' in netbox_addrs[host][interface]:
                            netbox_addr = netbox_addrs[host][interface]['IPv6']
                            if i['ipv6addr'].rfind("/") == -1:
                                netbox_addr = netbox_addr[0:netbox_addr.find("/")]
                            if netbox_addr != i['ipv6addr']:
                                warning(f"{label:<25} netbox={netbox_addr:<25} ansible={i['ipv6addr']:<25}")
                            else:
                                info(f"{label:<25} IPv6 values match")

                        # stop on match
                        break
                else:
                    debug(f"  no {interface} found in netbox")

        except Exception as exp:
            warning(f"failed with stack trace for host {host}")
            warning("  " + str(exp))


if __name__ == "__main__":
    main()



