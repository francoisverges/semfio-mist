#!/usr/bin/env python3
import time
import argparse
import csv
import geocoder

from semfio_mist import Config
from semfio_mist import logger
from semfio_mist import API
from semfio_mist import Site


def retreive_csv_data(csv_filename: str) -> dict:
    """Convert the content of the CSV file to a python dictionary."""
    data = []
    for line in csv.DictReader(csv_filename):
        data.append(line)
    return data


def script_args_parser() -> Config:
    """PARSE THE ARGUMENTS AND RETURNS A CONFIG INSTANCE."""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--config', metavar='config_file', type=argparse.FileType(
        'r'), default='config.json', help='file containing all the configuration information')
    parser.add_argument('site_list', metavar='site_info', type=argparse.FileType(
        'r'), help='csv file containing new sites names')
    parser.add_argument("-v", "--verbose", help="See DEBUG level messages", action="store_true")
    args = parser.parse_args()

    # Create a config object based on the config filename
    config = Config(args.config.name)

    # Configure the logger based on the level of verbose
    if args.verbose:
        logger.setLevel("DEBUG")

    # Extract the information from the CSV fiel into a Python dictionary
    site_list = retreive_csv_data(args.site_list)

    return config, site_list


def validate_site_group(site_group_name: str, api: API, config: Config) -> str:
    """Validate if a Site Group exists and creates it if not."""
    logger.debug(f"Validating if the following site group exists: {site_group_name}")
    site_groups = api.get(f"orgs/{config.data['org_id']}/sitegroups")
    sitegroup_id = None

    site_group_exists = False
    for site_group in site_groups:
        if site_group_name == site_group['name']:
            site_group_exists = True
            sitegroup_id = site_group['id']
            break

    if site_group_exists is False:
        logger.debug(f"Site Group {site_group_name} does not exist. Creating site group...")
        create_new_site_group_body = {}
        create_new_site_group_body['name'] = site_group_name
        response_post = api.post(
            f"orgs/{config.data['org_id']}/sitegroups", create_new_site_group_body)
        sitegroup_id = response_post['id']
    else:
        logger.debug(f"Site Group {site_group_name} already exists.")

    return sitegroup_id


def validate_rf_template(rf_template_name: str, address: str, api: API, config: Config) -> str:
    """Validate if an RF template exists and creates a barebone one if not."""
    logger.debug(f"Validating if the following rf tempalte exists: {rf_template_name}")
    rf_templates = api.get(f"orgs/{config.data['org_id']}/rftemplates")
    rf_template_id = None

    rf_template_exists = False
    for rf_template in rf_templates:
        if rf_template_name == rf_template['name']:
            rf_template_exists = True
            rf_template_id = rf_template['id']
            break

    if rf_template_exists is False:
        logger.debug(f"RF Template {rf_template_name} does not exist. Creating site group...")
        create_new_rf_template_body = {}
        create_new_rf_template_body['name'] = rf_template_name
        try:
            glocation = geocoder.google(address, key=config.data['google_api_key'])
        except Exception:
            raise
        create_new_rf_template_body['country_code'] = glocation.country
        response_post = api.post(
            f"orgs/{config.data['org_id']}/rftemplates", create_new_rf_template_body)
        rf_template_id = response_post['id']
    else:
        logger.debug(f"RF Template {rf_template_name} already exists.")

    return rf_template_id


def main():
    """Create Mist sites based on CSV list."""
    config, site_list = script_args_parser()
    api = API(config)

    for site in site_list:
        logger.debug(f"Adding following site: {site['site_name']}")

        # Validate that the Site Group exists
        sitegroup_ids = []
        sitegroup_id = validate_site_group(site['site_group'], api, config)
        sitegroup_ids.append(sitegroup_id)

        # Validate that the RF template exists
        rf_template_id = validate_rf_template(
            site['rf_template'], site['site_address'], api, config)

        # Create the new site
        new_site = Site(site['site_name'], site['site_address'],
                        api, config, rf_template_id=rf_template_id, sitegroup_ids=sitegroup_ids)
        new_site.create()

    api.__exit__()


if __name__ == '__main__':
    start_time = time.time()
    print('** Creating sites from CSV...\n')
    main()
    run_time = time.time() - start_time
    print(f"\n** Time to run: {round(run_time, 2)} sec")
