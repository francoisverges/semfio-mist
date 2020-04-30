"""
Written by Francois Verges (@VergesFrancois)
Created on: April 30, 2020

This file is a module that defines functions used for Mist WLAN operations
"""

import requests
import json

# Check if the WLAN already exist
def does_wlan_exist(configs, site_id, band):
    api_url = '{0}sites/{1}/wlans'.format(configs['api']['mist_url'],site_id)
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        wlans = json.loads(response.content.decode('utf-8'))
        for wlan in wlans:
            if 'ssid' in wlan:
                if band == '24':
                    if wlan['ssid'] == configs['24ghz']['ssid']:
                        print('{0} WLAN already exist.\t\t\t\tWLAN ID={1}'.format(wlan['ssid'], wlan['id']))
                        return (wlan['id'])
                if band == '5':
                    if wlan['ssid'] == configs['5ghz']['ssid']:
                        print('{0} WLAN already exist.\t\t\t\tWLAN ID={1}'.format(wlan['ssid'], wlan['id']))
                        return (wlan['id'])
    else:
        print('Something went wrong: {}'.format(response.status_code))


# This function creates a new WLAN
def create_wlan(site_id, configs, band):
    wlan = {}
    wlan['enabled'] = 'true'
    wlan['type'] = 'open'
    wlan['apply_to'] = 'site'
    wlan['hostname_ie'] = 'true'

    if band == '24':
        wlan['ssid'] = configs['24ghz']['ssid']
        wlan['band'] = '24'
    if band == '5':
        wlan['ssid'] = configs['5ghz']['ssid']
        wlan['band'] = '5'

    data_post = json.dumps(wlan)
    api_url = '{0}sites/{1}/wlans'.format(configs['api']['mist_url'],site_id)
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(configs['api']['token'])}

    response = requests.post(api_url, data=data_post, headers=headers)
    new_wlan = json.loads(response.content.decode('utf-8'))

    if response.status_code == 200:
        print('{0} WLAN was created.\t\t\t\tWLAN ID={1}'.format(new_wlan['ssid'], new_wlan['id']))
    else:
        print('Something went wrong: {}'.format(response.status_code))

    return (new_wlan['id'])
