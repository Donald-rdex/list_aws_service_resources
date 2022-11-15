
import logging

from botocore.exceptions import ClientError


def aws_services_by_resource(aws_sess):
    """Get available services as boto3 resources (that means they can be used as python objects)
    :param aws_sess: established boto3 Session object
    """
    logger = logging.getLogger()

    # https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/session.html#Session.get_available_services
    aws_resources = aws_sess.get_available_resources()

    logger.debug(aws_resources)

    # for region get services, store in dictionary of Service -> regions_where_service_is_available
    aws_service_list = dict()
    for aws_resource in aws_resources:
        aws_service_list[aws_resource] = aws_sess.get_available_regions(aws_resource)

    logger.debug('\n'.join(f'{srvc}: {rgns}' for srvc, rgns in aws_service_list.items()))

    for service_name, region_list in aws_service_list.items():
        for service_region in region_list:
            try:
                logger.info(f'{service_name}: {service_region}: ')
                # set up the service_resource as an object of service_name in a region.
                service_resource = aws_sess.resource(service_name, region_name=service_region)

                if service_name == 'cloudformation' and service_resource.stacks.all() is not None:
                    for cf_stack in service_resource.stacks.all():
                        print(f'{cf_stack.stack_id}, {cf_stack.stack_name}')

                if service_name == 'ec2' and service_resource.instances.all() is not None:
                    for ec2_instance in service_resource.instances.all():
                        print(f'{ec2_instance.id}, {ec2_instance.vpc}, {ec2_instance.subnet}')

                    # in a region we can have VPCs w/o instances though, also this allows a per VPC view of instances
                    for vpc in service_resource.vpcs.all():
                        print(f'{vpc.id}, {vpc.cidr_block}, {list(vpc.instances.all())}')

                # S3 is global, so repeated calls per region are not needed
                if service_name == 's3' and service_resource.buckets.all() is not None:
                    for bucket in service_resource.buckets.all():
                        print(f'{bucket.name}')
                    break

                # TODO there are several other boto3 resource based services, implementation left to the reader.

            except ClientError as e:
                logger.warning(f'Account may not be enabled in {service_region}. Error: {e}')
