import boto3
from transform_data import transform_data

sqs = boto3.client('sqs',
                   endpoint_url='http://localhost:4566',
                   region_name='us-east-1',
                   aws_access_key_id='test',
                   aws_secret_access_key='test')

def extract_data(queue_url):
    transformed_data = []
    while True:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
        if "Messages" in response:
            data = transform_data(response)
            transformed_data.extend(data)
        else:
            return transformed_data
