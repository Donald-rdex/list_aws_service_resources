## List_Service_* Scripts

A couple of python scripts that use the Boto3 library to retrieve a list of AWS resources available to a user via their configured AWS profile.

**STATUS: WORK IN PROGRESS**

### list_service_resources.py - uses Boto3 Resources

This uses the Boto3 resources implementation to retrieve the resources available to the account. Boto3 creates objects for the service, those objects are the resources. Only some services in the Boto3 library can use this implementation. 

### list_service_resources_using_clients.py - uses the Boto3 client specific calls.

As boto3 clients map to AWS SDK API calls, every service supports them. This uses clients for each service to get a list of running instances of the services. 

