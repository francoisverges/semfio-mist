#!/usr/bin/env python3

import time
import argparse
import os

from semfio_mist import Config
from semfio_mist import logger
from semfio_mist import API


def script_args_parser() -> Config:
    """PARSE THE ARGUMENTS AND RETURNS A CONFIG INSTANCE."""
    parser = argparse.ArgumentParser(
        description='Monitor client and Mist RSSI Value for a client device')
    parser.add_argument('--config', metavar='config_file', type=argparse.FileType(
        'r'), default='config.json', help='file containing all the configuration information')
    parser.add_argument("-v", "--verbose", help="See DEBUG level messages", action="store_true")
    args = parser.parse_args()

    # Create a config object based on the config filename
    config = Config(args.config.name)

    # Configure the logger based on the level of verbose
    if args.verbose:
        logger.setLevel("DEBUG")

    return config


def main():
    """COMPARE CLIENT RSSI VALUES TO MIST CLOUD RSSI VALUES."""
    config = script_args_parser()

    api = API(config)
    logger.info(f"\tClient MAC:\t{config.data['clients']['mac']}")

    # Monitoring Client Data until interupted by user
    try:
        local_rssi = 0
        local_tx_rate = 0
        ch_util = 0
        mist_tx_rate = 0
        while True:
            # Retreiving Client Wi-Fi data from local NIC (macOS)
            stream = os.popen("airport -I")
            lines = stream.read().split('\n')
            new_rssi = int(lines[0].split(": ")[1])
            mcs = int(lines[13].split(": ")[1])
            new_local_tx_rate = int(lines[6].split(": ")[1])

            # Retreiving Client Wi-Fi data from Mist Cloud
            response_client_stats = api.get(
                f"sites/{config.data['site']['id']}/stats/clients/{config.data['clients']['mac']}")
            response_ap_stats = api.get(
                f"sites/{config.data['site']['id']}/stats/devices/{response_client_stats['ap_id']}")
            new_ch_util = response_ap_stats['radio_stat']['band_5']['util_all']
            new_mist_tx_rate = response_client_stats['tx_rate']
            new_mist_rssi = response_client_stats['rssi']

            # Display updated data if any of the metric changed
            if (new_local_tx_rate != local_tx_rate) or (new_mist_tx_rate != mist_tx_rate) or (new_ch_util != ch_util) or (new_rssi != local_rssi):
                logger.info(
                    f"\tLocal MCS: {mcs}\tLocal RSSI: {new_rssi}dBm\tLocal Tx-Rate: {new_local_tx_rate}\t\tMist RSSI: {new_mist_rssi}dBm\tMist Tx Rate: {new_mist_tx_rate}\t\tCh. Utilization: {new_ch_util}%")
                local_tx_rate = new_local_tx_rate
                mist_tx_rate = new_mist_tx_rate
                ch_util = new_ch_util
                local_rssi = new_rssi
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    api.__exit__()


if __name__ == '__main__':
    start_time = time.time()
    print('** Retreiving Client RSSI...\n')
    main()
    run_time = time.time() - start_time
    print(f"\n** Time to run: {round(run_time, 2)} sec")
