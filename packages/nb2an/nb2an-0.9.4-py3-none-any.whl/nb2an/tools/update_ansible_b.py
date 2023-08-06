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

