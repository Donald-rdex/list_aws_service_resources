
import logging

from botocore.exceptions import ClientError


def aws_services_using_clients(aws_sess):
    """Get available services using boto3 clients, these are low level calls to AWS APIs
    :param aws_sess: established boto3 Session object
    """
    logger = logging.getLogger()

    services_as_clients_list = aws_sess.get_available_services()

    logger.info(f'service clients: {services_as_clients_list}')

    for service_name in services_as_clients_list:
        for service_region in aws_sess.get_available_regions(service_name):
            try:
                service_client = aws_sess.client(service_name, region_name=service_region)
                service_client_methods = [meth_name for meth_name in dir(service_client)
                                          if callable(getattr(service_client, meth_name))
                                          and meth_name.startswith('list_')]

                logger.debug(f'service client list_* methods for {service_client}: {service_client_methods}')

            except ClientError as e:
                logger.error(f'Account may not be enabled in {service_region}. Error: {e}')

    # for service get list_* calls

    # run list_* calls
    # header of Region -> Service -> list_* call
    # table of results.
