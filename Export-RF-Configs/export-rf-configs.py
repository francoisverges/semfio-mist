"""
Written by Francois Verges (@VergesFrancois)
Created on: May 14, 2020

This script exports the RF configurations of Access Points of a Mist Site
All the configuration details are coming from the 'config.json' file
"""


import argparse
import time
import json
import requests
import csv
from tabulate import tabulate


def export_ap_rf_congs_to_file(aps_rf_configs):
    """
    This function export the AP RF configs into a csv File

    Parameters:
        - aps_rf_configs: Dictionary of all AP configs
    """
    ap_count = 0
    with open('ap-rf-config.csv', mode='w') as config_file:
        config_writer = csv.writer(config_file, delimiter=',',
                                   quotechar='"', quoting=csv.QUOTE_MINIMAL)
        config_writer.writerow(['AP Name', 'AP Model', 'MAC Address', 'IP Address', '2.4GHz Channel',
                                '2.4GHz Tx Power', '5GHz Channel', '5GHz Channel Width', '5GHz Tx Power'])

        for ap in aps_rf_configs:
            ap_count += 1
            config_writer.writerow([ap['name'], ap['model'], ap['mac'], ap['ip'],
                                    ap['band_24']['channel'],
                                    str(ap['band_24']['power']) + "dBm",
                                    ap['band_5']['channel'],
                                    str(ap['band_5']['bandwidth']) + "MHz",
                                    str(ap['band_5']['power']) + "dBm"])

    print(f"* AP RF configuration exported!\t\tNb of APs: {ap_count}")


def get_ap_rf_configs(configs):
    """
    This function retreive the RF Configs of all APs part of a Mist site
    API Call Used: GET https://api.mist.com/api/v1/sites/:site_id/stats/devices

    Parameters:
        - configs: Dictionary containing all configurations information

    Returns:
        - A dictionary containing all AP RF configurations required
    """
    aps_rf_configs = []

    api_url = f"{configs['api']['mist_url']}sites/{configs['site']['id']}/stats/devices"
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Token {configs['api']['token']}"}
    response = requests.get(api_url, headers=headers)
    devices = json.loads(response.content.decode('utf-8'))

    if response.status_code == 200:
        # print(json.dumps(devices, indent=4, sort_keys=True))
        for device in devices:
            if device['type'] == "ap":
                ap_rf_configs = {}
                ap_rf_configs['id'] = device['id']
                ap_rf_configs['name'] = device['name']
                ap_rf_configs['model'] = device['model']
                ap_rf_configs['mac'] = device['mac']
                ap_rf_configs['ip'] = device['ip']
                ap_rf_configs['band_24'] = {"channel": device['radio_stat']['band_24']['channel'],
                                            "power": device['radio_stat']['band_24']['power']}
                ap_rf_configs['band_5'] = {"channel": device['radio_stat']['band_5']['channel'],
                                           "power": device['radio_stat']['band_5']['power'],
                                           "bandwidth": device['radio_stat']['band_5']['bandwidth']}
                aps_rf_configs.append(ap_rf_configs)
    else:
        print(f"Something went wrong: {response.status_code}")

    return(aps_rf_configs)


def main():
    """
    This function configures a Mist WLAN profile within a specific site
    """
    parser = argparse.ArgumentParser(
        description='Creates a Mist WLAN profile within a specific site')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    # Retreiving the information from Mist (Using an API Call)
    aps_rf_configs = get_ap_rf_configs(configs)

    # Exporting all the RF configuration into a CSV File
    export_ap_rf_congs_to_file(aps_rf_configs)


if __name__ == '__main__':
    start_time = time.time()
    print('** Exporting AP RF Configurations...\n')
    main()
    run_time = time.time() - start_time
    print(f"\n** Time to run: {round(run_time, 2)} sec")
