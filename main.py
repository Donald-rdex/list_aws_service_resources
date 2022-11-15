import argparse
import logging
import sys

import boto3

from list_service_resources_using_clients import aws_services_using_clients
from list_service_resources import aws_services_by_resource


def main(aws_profile, aws_region, retrieval_method):
    # setup Session for our connection
    aws_session = boto3.session.Session(region_name=aws_region, profile_name=aws_profile)

    # first list by resource
    if retrieval_method == 'resource':
        aws_services_by_resource(aws_session)
    elif retrieval_method == 'client':
        aws_services_using_clients(aws_session)
    else:
        logger.error("Unknown method of retrieving AWS resources. Given: %s, please use '--help' to see options. "
                     "Exiting...", retrieval_method)
        sys.exit(1)


if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='turn on debugging by setting logging.DEBUG, otherwise logging.INFO')
    parser.add_argument('-p', '--profile', default='default',
                        help='use a specific AWS profile section instead of default')
    parser.add_argument('-r', '--region', default='us-east-1',
                        help='AWS region to start collecting resources from.')
    parser.add_argument('-m', '--method', default='resource',
                        choices=['resource', 'client'],
                        help='use either resource methods or low-level clients for accessing objects.')
    args = parser.parse_args()

    logging_format = f'%(asctime)s list_service_resources [%(levelname)s] %(module)s:%(lineno)d :: %(message)s '
    logging_level = logging.INFO

    if args.debug:
        logging_level = logging.DEBUG

    logging.basicConfig(
        level=logging_level,
        format=logging_format
    )

    logger = logging.getLogger()
    logger.debug('Starting...')

    main(args.profile, args.region, args.method)
