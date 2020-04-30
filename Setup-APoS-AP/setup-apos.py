#!/usr/bin/env python3

"""
Written by Francois Verges (@VergesFrancois)
Created on: April 30, 2020

This script configured a Mist AP for an AP-on-a-Stick site survey
"""

from optparse import OptionParser
import time
import json
import requests
from pprint import pprint
import MistSite
import MistWlan
import MistAp


def main():
    parser = OptionParser(usage='usage: %prog config-file')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('Wrong number of arguments')
    with open(args[0], 'r') as f:
     configs = json.load(f)

    site_id = MistSite.does_site_exist(configs)                                          # Validate if the APoS site already exist
    if site_id is None:
        site_id = MistSite.create_new_site(configs)                                      # Create a new site
        MistSite.enable_config_persistence(site_id, configs)                             # Enable the AP Config Persistence for this APoS site

    wlan_24ghz_id = MistWlan.does_wlan_exist(configs, site_id, '24')                     # Validate if the 2.4GHz WLAN already exist
    if wlan_24ghz_id is None:
        wlan_24ghz_id = MistWlan.create_wlan(site_id, configs, '24')                     # Create a new 2.4GHz WLAN

    wlan_5ghz_id = MistWlan.does_wlan_exist(configs, site_id, '5')                       # Validate if the 5Hz WLAN already exist
    if wlan_5ghz_id is None:
        wlan_5ghz_id = MistWlan.create_wlan(site_id, configs, '5')                       # Create a new 5GHz WLAN

    if MistAp.has_been_claimed(configs) is False:
        MistAp.claim_ap(configs)                                                       # Claim AP to Org if necessary

    survey_ap_id = MistAp.is_ap_in_site(configs, site_id)                              # Validate if the AP is already assign to site
    if survey_ap_id is None:
        survey_ap_id = MistAp.provision_ap(configs, site_id)                           # Assigns the AP to the APoS Site

    survey_ap_id = MistSite.get_device_id(configs, configs['ap']['mac'], site_id)
    MistAp.config_radio(configs, site_id, survey_ap_id, '24')                          # Configure 2.4GHz Radio of the APoS survey AP
    MistAp.config_radio(configs, site_id, survey_ap_id, '5')                           # Configure 5GHz Radio of the APoS survey AP


if __name__ == '__main__':
    start_time = time.time()
    print('** Setting up APoS AP')
    main()
    run_time = time.time() - start_time
    print("** Time to run: %s sec" % round(run_time,2))
