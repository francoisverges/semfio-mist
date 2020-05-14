#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: May 8, 2020

This script creates a new WLAN profile within a specific Mist Site
All the configuration details are coming from the 'config.json' file
"""


import argparse
import time
import json
import requests


def create_new_wlan(configs):
    """
    This function creates a new WLAN profile based on the information located in config file
    API Call Used: POST https://api.mist.com/api/v1/sites/:site_id/wlans

    Parameters:
        - configs: Dictionary containing all configurations information

    Returns:
        - The ID of the newly created WLAN
    """
    wlan = {}
    wlan['enabled'] = 'true'
    wlan['apply_to'] = 'site'

    wlan['auth'] = {'type': configs['wlan']['type'], 'psk': configs['wlan']['psk']}
    wlan['hostname_ie'] = configs['wlan']['hostname_ie']
    wlan['ssid'] = configs['wlan']['ssid']
    wlan['band'] = configs['wlan']['band']

    data_post = json.dumps(wlan)
    api_url = '{0}sites/{1}/wlans'.format(configs['api']['mist_url'], configs['site']['id'])
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['api']['token'])}

    response = requests.post(api_url, data=data_post, headers=headers)
    new_wlan = json.loads(response.content.decode('utf-8'))

    if response.status_code == 200:
        print(json.dumps(new_wlan, indent=4, sort_keys=True))
        print('{0} WLAN was created.\t\t\t\tWLAN ID={1}'.format(new_wlan['ssid'], new_wlan['id']))
    else:
        print('Something went wrong: {}'.format(response.status_code))

    return (new_wlan['id'])


def main():
    """
    This function configures a Mist WLAN profile within a specific site
    """
    parser = argparse.ArgumentParser(
        description='Creates a Mist WLAN profile within a specific site')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    new_wlan_id = create_new_wlan(configs)


if __name__ == '__main__':
    start_time = time.time()
    print('** Creating a Mist Site\n')
    main()
    run_time = time.time() - start_time
    print("")
    print("** Time to run: %s sec" % round(run_time, 2))
