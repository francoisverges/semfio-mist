#!/usr/bin/env python3

import time
import json
import requests

def main():
    org_id = '22bfc07a-8591-432e-8825-92593049db0d'
    site_id = '1a13f6c2-3186-418f-8ca9-016fa4ac9ee7'
    token = 'o2gT2czKAzLkHAb49oEOGB0a9ujDCChd3FbRk50jL7A9Px6PJIu6pYRa7IAmmZdwZOz5CQ5j2YqjNa1J8qZpYjNufZGj68kh'
    mist_url = 'https://api.mist.com/api/v1/'
    headers = {'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(token)}

    api_url = '{0}sites/{1}/devices'.format(mist_url,site_id)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        devices = json.loads(response.content.decode('utf-8'))

        print('--------------')
        for device in devices:
            print('AP Name      : {}'.format(device['name']))
            print('AP Model     : {}'.format(device['model']))
            print('AP MAC Adress: {}'.format(device['mac']))
            print('--------------')


if __name__ == '__main__':
    start_time = time.time()
    main()
    run_time = time.time() - start_time
    print("** Time to run: %s sec" % round(run_time,2))
