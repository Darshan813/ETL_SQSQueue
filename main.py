import boto3
import json
import hashlib
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

def extract_data():
    transformed_data = []
    while True:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
        if "Messages" in response:
            data = transform_data(response)
            transformed_data.extend(data)
        else:
            return transformed_data

def transform_data(response):
    all_messages = []
    messages_list = response["Messages"]  # list of message_body
    created_date = response["ResponseMetadata"]["HTTPHeaders"]["date"]
    date_object = datetime.strptime(created_date, '%a, %d %b %Y %H:%M:%S %Z')
    response_date = date_object.date()
    for message in messages_list:
        message_body = json.loads(message["Body"])
        try:
            data = {
                "user_id": message_body["user_id"],
                "device_type": message_body["device_type"],
                "ip": mask_value(message_body["ip"]),
                "device_id": mask_value(message_body["device_id"]),
                "locale": message_body["locale"],
                "app_version": message_body["app_version"],
                "create_date": response_date
            }
            all_messages.append(data)

        except Exception as e:
            print("Raising Exception:", message_body["foo"])

    return all_messages

def load_data(data, db_params):
    data_to_insert = [
        (
            item["user_id"],
            item["device_type"],
            item["ip"],
            item["device_id"],
            item["locale"],
            item["app_version"],
            item["create_date"]

        )
        for item in data
    ]

    insert_query = """
    INSERT INTO user_logins 
    (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
    VALUES %s
    """

    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    execute_values(cur, insert_query, data_to_insert)
    conn.commit()

    print("Data Inserted Successfully!!")

def mask_value(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()

sqs = boto3.client('sqs',
                   endpoint_url='http://localhost:4566',
                   region_name='us-east-1',
                   aws_access_key_id='test',
                   aws_secret_access_key='test')

db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Darshan12345",
    "host": "localhost",
    "port": 5432
}

queue_url = "http://localhost:4566/000000000000/login-queue"
sqs_messages = extract_data()
print("SQS_Messages", sqs_messages)
load_data(sqs_messages, db_params)