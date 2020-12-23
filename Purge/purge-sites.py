import time
import argparse

from pymist.config import Config
from pymist.mist_api import API
from pymist.logger import logger


def script_args_parser() -> Config:
    """Parse the Arguments and returns a Config instance."""
    parser = argparse.ArgumentParser(description='Configures a Mist AP for an APoS site survey')
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
    """Delete all sites of an organization but the Primary Site."""
    config = script_args_parser()
    api = API(config)

    # Retreive sites
    sites = api.get(f"orgs/{config.data['org_id']}/sites")

    # Delete all but Primary Site
    for site in sites:
        if site['name'] != "Primary Site":
            api.delete(f"sites/{site['id']}")
            logger.info(f"Site deleted:\t{site['name']}")

    # Retreive rf rf_templates
    rf_templates = api.get(f"orgs/{config.data['org_id']}/rftemplates")

    # Delete all RF rf_templates
    for rf_template in rf_templates:
        api.delete(f"orgs/{config.data['org_id']}/rftemplates/{rf_template['id']}")
        logger.info(f"RF Template deleted:\t{rf_template['name']}")

    api.__exit__()


if __name__ == '__main__':
    start_time = time.time()
    print('** Purging sites...\n')
    main()
    run_time = time.time() - start_time
    print("\n** Time to run: %s sec" % round(run_time, 2))
