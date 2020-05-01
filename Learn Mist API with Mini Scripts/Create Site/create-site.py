#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: May 1, 2020

This script creates a new site within your Mist Organization
All the configuration details are coming from the 'config-site.json' file
"""


import argparse
import time
import json
import requests


def create_new_site(configs):
    """
    This function creates a new Site based on the information located in configs

    Parameters:
        - configs: Dictionary containing all configurations information

    Returns:
        - The ID of the newly created site
    """
    apos_site = {}
    apos_site['name'] = configs['site']['name']
    apos_site['timezone'] = configs['site']['timezone']
    apos_site['country_code'] = configs['site']['country_code']
    apos_site['address'] = configs['site']['address']
    apos_site['latlng'] = {'lat': configs['site']['lat'], 'lng': configs['site']['lng']}

    data_post = json.dumps(apos_site)
    api_url = '{0}orgs/{1}/sites'.format(configs['api']['mist_url'],configs['api']['org_id'])
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}

    response = requests.post(api_url, data=data_post, headers=headers)
    new_site = json.loads(response.content.decode('utf-8'))

    if response.status_code == 200:
        # new_site_response = json.loads(response.content.decode('utf-8'))
        # print(json.dumps(new_site_response, indent=4, sort_keys=True))
        print('{0} site was created.\t\t\t\tSITE ID={1}'.format(new_site['name'], new_site['id']))
    else:
        print('Something went wrong: {}'.format(response.status_code))

    return (new_site['id'])


def main():
    """
    This function configures a Mist Site within your organization
    """
    parser = argparse.ArgumentParser(description='Creates a Mist site within your organization')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType('r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    new_site_id = create_new_site(configs)


if __name__ == '__main__':
    start_time = time.time()
    print('** Creating a Mist Site\n')
    main()
    run_time = time.time() - start_time
    print("")
    print("** Time to run: %s sec" % round(run_time,2))
