#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: May 12, 2020

This script checks if a WLAN profile exists within a specific Mist Site based on the SSID name
All the configuration details are coming from the 'config.json' file
"""


import argparse
import time
import json
import requests


def does_wlan_exist(configs):
    """
    This function checks if a WLAN profile exists within a specific Mist Site based on its SSID name
    API Call Used:
        - GET https://api.mist.com/api/v1/sites/:site_id/wlans

    Parameters:
        - configs: Dictionary containing all configurations information

    Returns:
        - The ID of the WLAN profile if it exists
    """
    api_url = f"{configs['api']['mist_url']}sites/{configs['site']['id']}/wlans"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Token {configs['api']['token']}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        wlans = json.loads(response.content.decode('utf-8'))
        # print(json.dumps(wlans, indent=4, sort_keys=True))
        for wlan in wlans:
            if wlan['ssid'] == configs['wlan']['ssid']:
                print(f"YES - {wlan['ssid']} WLAN already exists.\t\t\tWLAN ID={wlan['id']}")
                return(wlan['id'])
    else:
        print(f"Something went wrong: {response.status_code}")

    print(f"NO - {configs['wlan']['ssid']} WlAN does NOT currently exists within this Site.")
    return()


def main():
    """
    This function validates if a WLAN profile already exists based on its name
    """
    parser = argparse.ArgumentParser(
        description='Validate if a Mist WLAN already exists or not within a Mist Site')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    wlan_id = does_wlan_exist(configs)


if __name__ == '__main__':
    start_time = time.time()
    print('** Is this WLAN already configured for your Site?\n')
    main()
    run_time = time.time() - start_time
    print(f"\n** Time to run: {round(run_time, 2)} sec")
