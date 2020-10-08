import time
import argparse

from semfio_mist import Config
from semfio_mist import logger
from semfio_mist import API
from prettytable import PrettyTable


def script_args_parser() -> Config:
    """PARSE THE ARGUMENTS AND RETURN CONFIGS."""
    parser = argparse.ArgumentParser(
        description='Monitor Channel Utilization of all APs part of a site')
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
    """MONITOR CHANNEL UTILIZATION OF ALL APS OF A SITE."""
    config = script_args_parser()
    api = API(config)

    # Retrieve list of APs and their current stats
    aps = api.get(f"sites/{config.data['site']['id']}/stats/devices")

    # Creation of the table header (for printing results)
    table = PrettyTable(['AP Name', '2.4 Ch.', '2.4 Util.',
                         '2.4 Clts', '5 Ch.', '5 Util.', '5 Clts'])

    # Looping on each APs to retreive relevant stats (channel utilizations)
    for ap in aps:
        if ap['type'] == 'ap':
            ap_mon_data = []
            ap_mon_data.append(ap['name'])

            if ap['status'] == 'connected':
                ap_mon_data.append(ap['radio_stat']['band_24']['channel'])
                ap_mon_data.append(f"{ap['radio_stat']['band_24']['util_all']}%")
                ap_mon_data.append(ap['radio_stat']['band_24']['num_clients'])
                ap_mon_data.append(
                    f"{ap['radio_stat']['band_5']['channel']}({ap['radio_stat']['band_5']['bandwidth']})")
                ap_mon_data.append(f"{ap['radio_stat']['band_5']['util_all']}%")
                ap_mon_data.append(ap['radio_stat']['band_5']['num_clients'])
                table.add_row(ap_mon_data)

    # Displaying the results sorting them by 5GHz channel utilization
    print(table.get_string(sortby="5 Util.", reversesort=True))

    api.__exit__()


if __name__ == '__main__':
    start_time = time.time()
    print('** MONITORING CHANNEL UTILIZATION...\n')
    main()
    run_time = time.time() - start_time
    print(f"\n** Time to run: {round(run_time, 2)} sec")
