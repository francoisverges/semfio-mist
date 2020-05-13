#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: May 12, 2020

This script claims an AP within your Mist Organization of choice
All the configuration details are coming from the 'config.json' file
"""


import argparse
import time
import json
import requests


def claim_ap(configs):
    """
    This function claims an AP to an organization
    API Call Used: POST https://api.mist.com/api/v1/orgs/:org_id/inventory

    Parameters:
        - configs: Dictionary containing all configurations information

    Returns:
        - ID of the AP
    """
    data_post = f"[\"{configs['ap']['claim-code']}\"]"
    api_url = f"{configs['api']['mist_url']}orgs/{configs['api']['org_id']}/inventory"
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Token {configs['api']['token']}"}

    response = requests.post(api_url, data=data_post, headers=headers)
    claim_response = json.loads(response.content.decode('utf-8'))
    # print(json.dumps(claim_response, indent=4, sort_keys=True))

    if claim_response['error']:
        print(f"ERROR: The AP was NOT claimed.\t\t Reason: {claim_response['reason'][0]}")
    elif claim_response['inventory_added']:
        print(f"{configs['ap']['mac']} AP has been claimed to organization {configs['api']['org_id']}")
    elif claim_response['duplicated']:
        print(f"{configs['ap']['mac']} AP has already been claimed to this organization.")

    return()


def main():
    """
    This function claims a Mist AP to a specific Organization
    """
    parser = argparse.ArgumentParser(description='Creates a Mist site within your organization')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    claim_ap(configs)


if __name__ == '__main__':
    start_time = time.time()
    print('** Claiming Mist AP...\n')
    main()
    run_time = time.time() - start_time
    print("")
    print("** Time to run: %s sec" % round(run_time, 2))
