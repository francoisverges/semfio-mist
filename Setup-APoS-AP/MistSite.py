"""
Written by Francois Verges (@VergesFrancois)
Created on: April 30, 2020

This file is a module that defines functions used for Mist Site operations
"""

import requests
import json


# Check if the APoS site already exist
def does_site_exist(configs):
    api_url = '{0}orgs/{1}/sites'.format(configs['api']['mist_url'],configs['api']['org_id'])
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        sites = json.loads(response.content.decode('utf-8'))
        for site in sites:
            if site['name'] == configs['site']['name']:
                print('{0} site already exist.\t\t\t\tSITE ID={1}'.format(configs['site']['name'], site['id']))
                return (site['id'])
    else:
        print('Something went wrong: {}'.format(response.status_code))


# This function creates a new Site
def create_new_site(configs):
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
        print('{0} site was created.\t\t\t\tSITE ID={1}'.format(new_site['name'], new_site['id']))
    else:
        print('Something went wrong: {}'.format(response.status_code))

    return (new_site['id'])


# This function Enable the AP Config Persistence feature of a site
def enable_config_persistence(new_site_id, configs):
    data_put = '{"persist_config_on_device": true}'
    api_url = '{0}sites/{1}/setting'.format(configs['api']['mist_url'], new_site_id)
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.put(api_url, data=data_put, headers=headers)
    if response.status_code != 200:
        print('Something went wrong: {}'.format(response.status_code))


# This function returns the device ID based on the device MAC address
def get_device_id(configs, device_mac, site_id):
    api_url = '{0}sites/{1}/devices'.format(configs['api']['mist_url'],site_id)
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        devices = json.loads(response.content.decode('utf-8'))
        for device in devices:
            if device['mac'] == device_mac:
                return (device['id'])
    else:
        print('Error: {}'.format(response.status_code))

    return ()
