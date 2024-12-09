import os

import boto3
from context import Context
from botocore.exceptions import ClientError


def create_dax_table(table_name, dyn_resource=None):
    endpoint_url = os.getenv('ENDPOINT_URL')
    # Retrieve credentials from environment variables (configured by Kubernetes)
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_DEFAULT_REGION')
    operating_system = os.getenv('OPERATING_SYSTEM')

    try:
        if operating_system.lower() == "minikube":
            dyn_resource = boto3.resource('dynamodb', endpoint_url=endpoint_url)  # Run in minikube
        elif operating_system.lower() == "kubernetes":
            dyn_resource = boto3.resource(
                'dynamodb',
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )  # Run in kubernetes
        else:
            dyn_resource = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')  # locally

        print(f'created boto3 client {dyn_resource}')

        table_names = [table.name for table in dyn_resource.tables.all()]
        Context.dynamodb_local = dyn_resource

        if table_name in table_names:
            print(f"Table {table_name} already exist")
            Context.dynamodb_table = table_name
            return table_name
        else:
            print('table', table_name, 'does not exists')
            print('creating table started')
            table_name = table_name
            params = {
                'TableName': table_name,
                'KeySchema': [
                    {'AttributeName': 'id', 'KeyType': 'HASH'},  # partition_key
                    {'AttributeName': 'name', 'KeyType': 'RANGE'}  # sort_key
                ],
                'AttributeDefinitions': [
                    {'AttributeName': 'id', 'AttributeType': 'N'},
                    {'AttributeName': 'name', 'AttributeType': 'S'}
                ],
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            }
            table = dyn_resource.create_table(**params)
            print(f"Creating {table_name}...")
            table.wait_until_exists()
            Context.dynamodb_table = table_name
            print(f"Table {table_name} creating complete")
    except ClientError as ex:
        print(f'Error creating table: {ex.response}')
    return table_name
