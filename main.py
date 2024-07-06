import boto3
import json

sqs = boto3.client('sqs',
                   endpoint_url='http://localhost:4566',
                   region_name='us-east-1',
                   aws_access_key_id='test',
                   aws_secret_access_key='test')

queue_url = "http://localhost:4566/000000000000/login-queue"

all_messages = []
while True:
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
    if "Messages" in response:
        messages_list = response["Messages"] #list of message_body
        for message in messages_list:
            message_body = json.loads(message["Body"])
            data = {
                "user_id": message_body["user_id"],
                "device_type": message_body["device_type"],
                "ip": message_body["ip"],
                "device_id": message_body["device_id"],
                "locale": message_body["locale"],
                "app_version": message_body["app_version"],
            }
            all_messages.append(data)
    else:
        break
        print("No more messages")

