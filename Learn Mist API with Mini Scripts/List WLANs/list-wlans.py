#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: May 12, 2020

This script list all WLAN profiles within a specific Mist Site
All the configuration details are coming from the 'config.json' file
"""


import argparse
import time
import json
import requests
from tabulate import tabulate


def list_wlans(configs):
    """
    This function list all WLAN profiles of a specific Mist Site
    API Call Used:
        - GET https://api.mist.com/api/v1/sites/:site_id/wlans

    Parameters:
        - configs: Dictionary containing all configurations information

    Returns:
        - Dictionary of WLAN SSID name and WLAN ID existing within the Site
    """
    api_url = f"{configs['api']['mist_url']}sites/{configs['site']['id']}/wlans"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Token {configs['api']['token']}"}
    response = requests.get(api_url, headers=headers)

    my_wlans = []
    if response.status_code == 200:
        wlans = json.loads(response.content.decode('utf-8'))
        # print(json.dumps(wlans, indent=4, sort_keys=True))
        for wlan in wlans:
            my_wlans.append([wlan['ssid'], wlan['id'], wlan['enabled'], wlan['band']])
        print(tabulate(my_wlans, headers=['SSID', 'ID', 'ACTIVE', 'BAND']))
        return(my_wlans)
    else:
        print(f"Something went wrong: {response.status_code}")

    print(f"{configs['site']['name']} Site does NOT currently have any WLAN Profile configured.")
    return(my_wlans)


def main():
    """
    This function list all WLANs configured for a specific Site
    """
    parser = argparse.ArgumentParser(description='List all WLANS within a specific Mist Site')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    my_wlans = list_wlans(configs)


if __name__ == '__main__':
    start_time = time.time()
    print('** Listing WLAN Profiles...\n')
    main()
    run_time = time.time() - start_time
    print("")
    print("** Time to run: %s sec" % round(run_time, 2))
