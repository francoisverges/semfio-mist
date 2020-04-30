"""
Written by Francois Verges (@VergesFrancois)
Created on: April 30, 2020

This file is a module that defines functions used for Mist AP operations
"""

import requests
import json


def is_ap_in_site(configs, site_id):
    """
    This function check if an AP is already assigned to a site

    Parameters:
        - configs: Dictionary containing all configurations information
        - site_id: ID of the site we would like to assign the AP to

    Returns:
        - the ID of the AP if the AP is assign to the site
    """
    api_url = '{0}sites/{1}/devices'.format(configs['api']['mist_url'],site_id)
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        devices = json.loads(response.content.decode('utf-8'))
        for device in devices:
            if device['mac'] == configs['ap']['mac']:
                print('{0} AP is already assigned to site.\t\tSITE ID={1}'.format(device['name'], site_id))
                return (device['id'])
    else:
        print('Something went wrong: {}'.format(response.status_code))


# This function check if an AP has been claimed
def has_been_claimed(configs):
    api_url = '{0}installer/orgs/{1}/devices'.format(configs['api']['mist_url'], configs['api']['org_id'])
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        devices = json.loads(response.content.decode('utf-8'))
        for device in devices:
            if device['mac'] == configs['ap']['mac']:
                print('{0} AP has already be claimed to org.\t\tORG ID={1}'.format(device['mac'], configs['api']['org_id']))
                return (True)
    else:
        print('Something went wrong: {}'.format(response.status_code))

    return (False)


# This function claims an AP to an organization
def claim_ap(configs):
    data_post = '["{}"]'.format(configs['ap']['claim-code'])
    api_url = '{0}orgs/{1}/inventory'.format(configs['api']['mist_url'], configs['api']['org_id'])
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}

    response = requests.post(api_url, data=data_post, headers=headers)

    if response.status_code == 200:
        print('{0} AP has been claimed to org.\t\tORG ID={1}'.format(configs['ap']['mac'], configs['api']['org_id']))
    else:
        print('Something went wrong: {}'.format(response.status_code))


# This function configure radio settings of an AP
def config_radio(configs, site_id, device_id, band):
    radio_configs = {}
    radio_configs['radio_config'] = {}

    if band == '24':
        radio_configs['radio_config']['band_24'] = {}
        radio_configs['radio_config']['band_24']['power'] = configs['24ghz']['tx-power']
        radio_configs['radio_config']['band_24']['channel'] = configs['24ghz']['channel']
    elif band == '5':
        radio_configs['radio_config']['band_5'] = {}
        radio_configs['radio_config']['band_5']['power'] = configs['5ghz']['tx-power']
        radio_configs['radio_config']['band_5']['bandwidth'] = configs['5ghz']['bandwidth']
        radio_configs['radio_config']['band_5']['channel'] = configs['5ghz']['channel']

    data_put = json.dumps(radio_configs)

    api_url = '{0}sites/{1}/devices/{2}'.format(configs['api']['mist_url'], site_id, device_id)
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.put(api_url, data=data_put, headers=headers)

    if response.status_code == 200:
        if band == '24':
            print('2.4GHz Radio Configured:\t\t\t\tCHANNEL={0}\tTX-POWER={1}'.format(configs['24ghz']['channel'], configs['24ghz']['tx-power']))
        elif band == '5':
            print('5GHz   Radio Configured:\t\t\t\tCHANNEL={0}/{1}\tTX-POWER={2}'.format(configs['5ghz']['channel'], configs['5ghz']['bandwidth'], configs['5ghz']['tx-power']))
    else:
        print('Something went wrong: {}'.format(response.status_code))


# This function assigns an AP to a site
def provision_ap(configs, site_id):
    ap_provision = {}
    ap_provision['name'] = configs['ap']['name']
    ap_provision['site_id'] = site_id
    data_put = json.dumps(ap_provision)

    api_url = '{0}installer/orgs/{1}/devices/{2}'.format(configs['api']['mist_url'],
                                                         configs['api']['org_id'],
                                                         configs['ap']['mac'])
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.put(api_url, data=data_put, headers=headers)

    if response.status_code == 200:
        print('{0} has been assigned to APoS site.\t\tSITE ID={1}'.format(ap_provision['name'], site_id))
    else:
        print('Something went wrong: {0} - {1} AP has not claimed'.format(response.status_code, configs['ap']['mac']))
