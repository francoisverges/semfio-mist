#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: August 5, 2020

This script batch rename a group of AP based on the content of a CSV file containing
the AP Mac address and the new AP name.

The format of the MAC address part of this CSV file has to be the following:
    aabbccddeeff
"""

import argparse
import time
import json
import requests
import csv
from pprint import pprint


def is_ap_in_site(configs: dict, ap_mac: str):
    """
    This function check if an AP is already assigned to a site

    Parameters:
        - configs: Dictionary containing all configurations information
        - site_id: ID of the site we would like to assign the AP to

    Returns:
        - the ID of the AP if the AP is assign to the site
        - the current name of the AP
    """
    api_url = f"{configs['api']['mist_url']}sites/{configs['site']['id']}/devices"
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        devices = json.loads(response.content.decode('utf-8'))
        for device in devices:
            if device['mac'] == ap_mac:
                return (device['id'], device['name'])
    else:
        print('Something went wrong: {}'.format(response.status_code))
    return (None, None)


def rename_ap(configs: dict, ap_id: str, new_ap_name: str, ap_old_name: str):
    """
    This function renames an AP

    Parameters:
        - configs: Dictionary containing all configurations information
        - ap_id: ID of the AP device object
        - new_ap_name: Name to apply to the AP
        - ap_old_name: Current Name of the AP
    """
    api_url = f"{configs['api']['mist_url']}sites/{configs['site']['id']}/devices/{ap_id}"
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['api']['token'])}
    body = {}
    body['name'] = new_ap_name
    response = requests.put(api_url, headers=headers, data=json.dumps(body))

    if response.status_code == 200:
        device = json.loads(response.content.decode('utf-8'))
        print(f"{device['mac']} renamed from {ap_old_name} to {device['name']}")
    else:
        print(f"AP ID: {ap_id}\tSomething went wrong: {response.status_code}")


def retreive_ap_mac_list(csv_filename: str) -> dict:
    """
    This function convert the content of the CSV file to a python dictionary

    Parameters:
        - csv_filename: The name of the CSV File

    Returns:
        - A dictionary containing the content of the CSV file
    """
    ap_csv = csv.DictReader(csv_filename)
    ap_list = []
    for line in ap_csv:
        ap_list.append(line)
    return ap_list


def main():
    """
    This script batch rename the APs listed in a CSV file
    """
    parser = argparse.ArgumentParser(description='Configures a Mist AP for an APoS site survey')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    parser.add_argument('ap_list', metavar='aps_names', type=argparse.FileType(
        'r'), help='csv file containing new AP names')
    args = parser.parse_args()
    configs = json.load(args.config)
    ap_mac_list = retreive_ap_mac_list(args.ap_list)

    for ap in ap_mac_list:
        ap_id, ap_old_name = is_ap_in_site(configs, ap['mac'])
        if ap_id:
            rename_ap(configs, ap_id, ap['name'], ap_old_name)
        else:
            print(f"AP {ap['name']} is not part of site {configs['site']['id']}")


if __name__ == '__main__':
    start_time = time.time()
    print('** Batch renaming APs...\n')
    main()
    run_time = time.time() - start_time
    print("\n** Time to run: %s sec" % round(run_time, 2))
