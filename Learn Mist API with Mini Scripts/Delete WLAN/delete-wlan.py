#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: May 12, 2020

This script deletes WLAN profile within a specific Mist Site
All the configuration details are coming from the 'config.json' file
"""


import argparse
import time
import json
import requests


def delete_wlan(configs):
    """
    This function deletes a new WLAN profile based on the information located in config file
    API Call Used:
        - GET https://api.mist.com/api/v1/sites/:site_id/wlans
        - DELETE https://api.mist.com/api/v1/sites/:site_id/wlans/:wlan_id

    Parameters:
        - configs: Dictionary containing all configurations information

    Returns:
        - True if the site is deleted, False if not
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
                api_url_del = f"{configs['api']['mist_url']}sites/{configs['site']['id']}/wlans/{wlan['id']}"
                response_del = requests.delete(api_url_del, headers=headers)
                if response_del.status_code == 200:
                    print(f"{wlan['ssid']} WLAN was deleted.\t\t\t\tWLAN ID={wlan['id']}")
                    return(True)
                else:
                    print(f"Something went wrong: {response_del.status_code}")
    else:
        print(f"Something went wrong: {response.status_code}")

    print(f"{configs['wlan']['ssid']} was NOT deleted. Reason: WLAN does not exist in this site.")
    return(False)


def main():
    """
    This function deletes a Mist WLAN profile within a specific site
    """
    parser = argparse.ArgumentParser(description='Deletes a Mist site within your site')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    delete_wlan(configs)


if __name__ == '__main__':
    start_time = time.time()
    print('** Deleting a Mist Site...\n')
    main()
    run_time = time.time() - start_time
    print(f"\n** Time to run: {round(run_time, 2)} sec")
