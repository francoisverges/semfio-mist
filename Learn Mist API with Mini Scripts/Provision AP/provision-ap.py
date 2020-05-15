#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: May 14, 2020

This script provision an AP into a specific Mist Site based on its name
All the configuration details are coming from the 'config.json' file
"""


import argparse
import time
import json
import requests


def provision_ap(configs):
    """
    This function provision an AP into a specific Mist Site
    API Call Used: PUT https://api.mist.com/api/v1/installer/org/:org_id/devices/:device_id

    Parameters:
        - configs: Dictionary containing all configurations information

    Returns:
        - Status: True if the AP has been provisioned properly, False if not
    """
    ap_provision = {}
    ap_provision['mac'] = configs['ap']['mac']
    ap_provision['name'] = configs['ap']['name']
    ap_provision['site_id'] = configs['site']['id']
    data_put = json.dumps(ap_provision)

    api_url = f"{configs['api']['mist_url']}installer/orgs/{configs['api']['org_id']}/devices/{configs['ap']['mac']}"
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Token {configs['api']['token']}"}

    response = requests.put(api_url, data=data_put, headers=headers)
    provision_response = json.loads(response.content.decode('utf-8'))
    # print(json.dumps(provision_response, indent=4, sort_keys=True))

    if response.status_code == 200:
        print(
            f"{provision_response['name']} has been assigned to the following site: {provision_response['site_name']}")
        return (True)
    else:
        print(f"Something went wrong: {response.status_code} - {configs['ap']['mac']} \
        AP has not been provisioned\t\tREASON: {provision_response['detail']}")

    return (False)


def main():
    """
    This function provision an AP into a specific Mist Site
    """
    parser = argparse.ArgumentParser(description='Provision an AP to a Mist Site')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    is_provisioned = provision_ap(configs)


if __name__ == '__main__':
    start_time = time.time()
    print('** Provisioning Mist AP...\n')
    main()
    run_time = time.time() - start_time
    print(f"\n** Time to run: {round(run_time, 2)} sec")
