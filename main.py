import boto3
from extract_data import extract_data
from load_data import load_data


db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Darshan12345",
    "host": "localhost",
    "port": 5432
}

queue_url = "http://localhost:4566/000000000000/login-queue"
sqs_messages = extract_data(queue_url)
load_data(sqs_messages, db_params)

