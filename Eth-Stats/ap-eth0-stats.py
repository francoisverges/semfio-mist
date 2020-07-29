import argparse
import time
import json
import requests
from pprint import pprint
from tabulate import tabulate
from datetime import datetime


def humanbytes(B):
    """
    Return the given bytes as a human friendly KB, MB, GB, or TB string
    """
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)
    TB = float(KB ** 4)

    if B < KB:
        return '{0} {1}'.format(B, 'B' if 0 == B > 1 else 'B')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B/KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B/MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B/TB)


def uptime(time_in_sec):
    """
    Returns a human friendly time expressed in days, hours and minutes
    """
    uptime_days = time_in_sec // (24 * 3600)
    uptime_hours = (time_in_sec - (uptime_days * (24 * 3600))) // 3600
    uptime_minutes = (time_in_sec - (uptime_days *
                                     (24 * 3600)) - (uptime_hours * 3600)) // 60
    return (str(uptime_days) + "d " + str(uptime_hours) + "h " + str(uptime_minutes) + "m")


def main():
    """
    Script to find out the speed of an Eth0 port
    """
    parser = argparse.ArgumentParser(description='Configures a Mist AP for an APoS site survey')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType(
        'r'), help='file containing all the configuration information')
    args = parser.parse_args()
    configs = json.load(args.config)

    # GET /api/v1/sites/:site_id/stats/devices
    api_url = f"{configs['api']['mist_url']}sites/{configs['site']['id']}/stats/devices"
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['api']['token'])}
    response = requests.get(api_url, headers=headers)

    aps_eth_stats = []
    if response.status_code == 200:
        devices = json.loads(response.content.decode('utf-8'))
        # Loop on each APs
        for device in devices:
            # Loading relevant AP stats into a dictionary
            aps_eth_stats.append([
                device['name'],
                device['model'],
                uptime(int(device['uptime'])),
                datetime.fromtimestamp(device['last_seen']).time(),
                humanbytes(int(device['tx_bps'])),
                humanbytes(int(device['rx_bps'])),
                device['port_stat']['eth0']['speed'],
                humanbytes(int(device['port_stat']['eth0']['tx_bytes'])),
                humanbytes(int(device['port_stat']['eth0']['rx_bytes'])),
                device['port_stat']['eth0']['rx_errors']
            ])
        # Print the AP stats in a table fashion
        print(tabulate(aps_eth_stats,
                       headers=[
                           'AP Name',
                           'AP Model',
                           'Up Time',
                           'Last Seen',
                           'Tx Bps',
                           'Rx Bps',
                           'Eth0 Speed',
                           'Eth0 Tx',
                           'Eth0 Rx',
                           'Eth0 Errors'],
                       numalign="left"))
    else:
        print('Something went wrong: {}'.format(response.status_code))


if __name__ == '__main__':
    start_time = time.time()
    print('** Getting Eth0 Stats...\n')
    main()
    run_time = time.time() - start_time
    print("\n** Time to run: %s sec" % round(run_time, 2))
