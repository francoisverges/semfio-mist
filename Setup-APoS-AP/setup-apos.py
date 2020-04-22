#!/usr/bin/env python3

from optparse import OptionParser
import time
import json
import requests
from pprint import pprint

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


# This function check if an AP is already assigned to a site
def is_ap_in_site(configs, site_id):
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


def main():
    parser = OptionParser(usage='usage: %prog config-file')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('Wrong number of arguments')
    with open(args[0], 'r') as f:
     configs = json.load(f)

    site_id = does_site_exist(configs)                                          # Validate if the APoS site already exist
    if site_id is None:
        site_id = create_new_site(configs)                                      # Create a new site
        enable_config_persistence(site_id, configs)                             # Enable the AP Config Persistence for this APoS site

    wlan_24ghz_id = does_wlan_exist(configs, site_id, '24')                     # Validate if the 2.4GHz WLAN already exist
    if wlan_24ghz_id is None:
        wlan_24ghz_id = create_wlan(site_id, configs, '24')                     # Create a new 2.4GHz WLAN

    wlan_5ghz_id = does_wlan_exist(configs, site_id, '5')                       # Validate if the 5Hz WLAN already exist
    if wlan_5ghz_id is None:
        wlan_5ghz_id = create_wlan(site_id, configs, '5')                       # Create a new 5GHz WLAN

    if has_been_claimed(configs) is False:
        claim_ap(configs)                                                       # Claim AP to Org if necessary

    survey_ap_id = is_ap_in_site(configs, site_id)                              # Validate if the AP is already assign to site
    if survey_ap_id is None:
        survey_ap_id = provision_ap(configs, site_id)                           # Assigns the AP to the APoS Site

    survey_ap_id = get_device_id(configs, configs['ap']['mac'], site_id)
    config_radio(configs, site_id, survey_ap_id, '24')                          # Configure 2.4GHz Radio of the APoS survey AP
    config_radio(configs, site_id, survey_ap_id, '5')                           # Configure 5GHz Radio of the APoS survey AP


if __name__ == '__main__':
    start_time = time.time()
    print('** Setting up APoS AP')
    main()
    run_time = time.time() - start_time
    print("** Time to run: %s sec" % round(run_time,2))
