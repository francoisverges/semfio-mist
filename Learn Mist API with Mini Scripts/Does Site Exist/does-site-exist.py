#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: May 1, 2020

This script checks if a specific site exists based on its name
All the configuration details are coming from the 'config-site.json' file
"""


import argparse
import time
import json
import requests


def does_site_exist(configs):
    """
    Check if a Mist site already exist
    API Call Used: GET https://api.mist.com/api/v1/orgs/:org_id/sites

    Parameters:
        - configs: Dictionary containing all configurations information
        - verbose: Display output messages (Default = True)

    Returns:
        - The ID of the site if it exists
    """
    api_url = '{0}orgs/{1}/sites'.format(configs['api']['mist_url'], configs['api']['org_id'])
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        sites = json.loads(response.content.decode('utf-8'))
        print(json.dumps(sites, indent=4, sort_keys=True))
        for site in sites:
            if site['name'] == configs['site']['name']:
                print('{0} site already exist.\t\t\t\tSITE ID={1}'.format(
                    configs['site']['name'], site['id']))
                return (site['id'])
    else:
        print('Something went wrong: {}'.format(response.status_code))

    print('{0} site does not currently exist in your organization.'.format(configs['site']['name']))


def main():
    """
    This function checks if a specific site already exists in a Mist Organization
    """
    parser = argparse.ArgumentParser(
        description='Check if a Mist site exists within your organization')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    does_site_exist(configs)


if __name__ == '__main__':
    start_time = time.time()
    print('** Is this Mist Site already part of your Organization?\n')
    main()
    run_time = time.time() - start_time
    print("\n** Time to run: %s sec" % round(run_time, 2))
