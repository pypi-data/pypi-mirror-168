#!/usr/bin/python3

"""Updates ansible YAML files with information from netbox"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import os
import nb2an.netbox

import ruamel.yaml

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: update")

    parser.add_argument("-n", "--noop", action="store_true",
                        help="Don't actually make changes")

    parser.add_argument("--log-level", "--ll", default="info",
                        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).")

    parser.add_argument("-r", "--racks", default=[], type=int, nargs="*",
                        help="Racks to update")

    parser.add_argument("ansible_directory",
                        type=str, help="The ansible directory to verify")

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level,
                        format="%(levelname)-10s:\t%(message)s")
    return args


def process_host(b: nb2an.netbox.Netbox, hostname: str, yaml_file: str, outlets: list,
                 make_changes: bool = True):
    debug(f"modifying {yaml_file}")
    with open(yaml_file) as original:
        yaml_data = original.read()

        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.preserve_quotes = True
        yaml_struct = yaml.load(yaml_data)

        if make_changes:
            # # now do modifications
            if 'host_info' not in yaml_struct:
                yaml_struct['host_info'] = {}
            # yaml_struct['host_info']['netbox_modified'] = True

            # if 'net_config' in yaml_struct:
            #     yaml_struct['net_config'].append({
            #         'name': 'nb_dummy0',
            #         'ipaddr': "127.0.0.9",
            #         'prefix': 24})

            #
            # OUTLETS
            #
            debug(f"  checking outlets for {hostname}")
            for o in outlets:
                debug(f"    checking outlet connected to {b.fqdn(o['device']['name'])}")
                if b.fqdn(o['device']['name']) == hostname:
                    debug(f"  FOUND outlet connected to {b.fqdn(o['device']['name'])}")
                    if 'outlets' not in yaml_struct['host_info']:
                        yaml_struct['host_info']['outlets'] = {}
                    yaml_struct['host_info']['outlets'][o['name']] = {
                        'label': o['label'],
                    }

            #
            # DEVICE information
            #
            d = b.get_devices_by_name(hostname)
            if len(d) > 1:
                warning(f"too many devices returned for {hostname}")
            if d:
                d = d[0]
                if 'device_type' in d and \
                   'manufacturer' in d['device_type']:
                    yaml_struct['host_info']['systype'] = d['device_type']['manufacturer']['name']
                    yaml_struct['host_info']['model'] = d['device_type']['model']

                if 'serial'in d:
                    yaml_struct['host_info']['isitag'] = d['serial'].lower()

                # netbox reference
                yaml_struct['netbox'] = {
                    'url': b.prefix + "/dcim/device/" + str(d['id']),
                    'device_id': d['id'],
                    'site': d['site']['name'],
                    'site_url': d['site']['url'],
                    'location': d['location']['name'],
                    'location_url': d['location']['url'],
                    'rack': d['rack']['name'],
                    'rack_url': d['location']['url'],
                }  # always reset everything

            # if we inserted nothing, drop it
            if yaml_struct['host_info'] == {}:
                del yaml_struct['host_info']

    with open(yaml_file, "w") as modified:
        yaml.dump(yaml_struct, modified)


def main():
    args = parse_args()
    ansible_directory = args.ansible_directory

    b = nb2an.netbox.Netbox()

    devices = b.get_devices(args.racks)
    outlets = b.get_outlets()

    for device in devices:
        name = b.fqdn(device['name'])
        debug(f"starting: {name}")

        device_yaml = os.path.join(ansible_directory, "host_vars", name + ".yml")
        if os.path.exists(device_yaml):
            process_host(b, name, device_yaml, outlets, make_changes=(not args.noop))


if __name__ == "__main__":
    main()
