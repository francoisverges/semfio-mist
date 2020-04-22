#!/usr/bin/env python3

from optparse import OptionParser
import time
import json
import requests

def main():
    usage = "usage: %prog AP_MAC_Address AP_New_Name"
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    if len(args) == 2:
        ap_mac = args[0]
        ap_new_name = args[1]
    else:
        print('Wrong set of arguments! Please see usage below:\n\t{0}'.format(usage))
        return

    org_id = '22bfc07a-8591-432e-8825-92593049db0d'
    site_id = '1a13f6c2-3186-418f-8ca9-016fa4ac9ee7'
    token = 'o2gT2czKAzLkHAb49oEOGB0a9ujDCChd3FbRk50jL7A9Px6PJIu6pYRa7IAmmZdwZOz5CQ5j2YqjNa1J8qZpYjNufZGj68kh'
    mist_url = 'https://api.mist.com/api/v1/'
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(token)}

    # Retreiving the list of AP deployed at one site through an API GET call
    api_url = '{0}sites/{1}/devices'.format(mist_url,site_id)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        devices = json.loads(response.content.decode('utf-8'))

        # Looping on these APs until we find the one we want to update
        for device in devices:
            if device['type'] == 'ap':                                          # Making sure that we are modifying an AP object
                if device['mac'] == ap_mac:                                     # Finding the AP we want to modify based on its MAC Address
                    old_name = device['name']
                    device['name'] = ap_new_name                                # Update the name of the AP
                    device_id = device['id']
                    data_put = json.dumps(device)

                    # Building and Sending an API call to update the AP object
                    api_url = '{0}sites/{1}/devices/{2}'.format(mist_url,site_id,device_id)
                    response = requests.put(api_url, data=data_put, headers=headers)

                    if response.status_code == 200:
                        print('{0} AP name changed from "{1}" to "{2}"'.format(device['mac'],old_name,device['name']))
                    else:
                        print('Something went wrong: {}'.format(response.status_code))

    else:
        print('Something went wrong: {}'.format(response.status_code))


if __name__ == '__main__':
    start_time = time.time()
    main()
    run_time = time.time() - start_time
    print("** Time to run: %s sec" % round(run_time,2))
