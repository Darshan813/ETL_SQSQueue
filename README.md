# User Login Data - ETL Pipeline

The Python script implements an ETL (Extract, Transform, Load) pipeline for processing user login data from an AWS SQS queue and storing it in a PostgreSQL database.

## Overview

The script performs the following operations:
1. Extracts messages from an AWS SQS queue
2. Transforms the data, including masking sensitive information
3. Loads the transformed data into a PostgreSQL database

## Requirements

- Python 3.9
- AWS CLI version 1.20.50
- Docker
- pgAdmin

## Dependencies

The script requires the following Python packages:
- boto3==1.21.50
- psycopg2 == 2.9.9

## Configuration

The script uses the following configurations:

1. AWS SQS:
   - Endpoint URL: http://localhost:4566
   - Region: us-east-1
   - Queue URL: http://localhost:4566/000000000000/login-queue
   - aws_access_key_id='test'
   -  aws_secret_access_key='test'

2. PostgreSQL Database:
   - Database parameters are stored in the `db_params` dictionary in the script
   - Can be managed and monitored using pgAdmin

## How to Run

1. Ensure Docker is installed and running on your system.
2. Ensure LocalStack and postgres containers are running.
3. Update the `db_params` in the script with the correct database credentials.
4. Install the Python dependencies
5. Ensure the `user_logins` table in PostgreSQL has the correct schema, particularly:
- `app_version` column should be of type VARCHAR(10)
6. Run the script:

## Error Handling

The script includes basic error handling for message processing. Errors are printed to the console.

## Notes

Sensitive data (IP and device ID) is masked using MD5 hashing for privacy protection.
The `app_version` field is stored as VARCHAR(10) in the database

## Key Implementation Details

### Reading Messages from the Queue

 Messages are read from the SQS queue using boto3's `receive_message` method.
- The script uses a loop to continuously poll the queue, processing up to 10 messages at a time.

Data Structures

The script primarily uses Python dictionaries and lists to handle the data.
Extracted messages are stored in a list of dictionaries, where each dictionary represents a single message.

Masking PII Data 

- Personally Identifiable Information (PII) such as IP addresses and device IDs are masked using MD5 hashing.
- This approach ensures that duplicate values can be identified while maintaining data privacy.
- For enhanced security, we can use SHA-256 hashing instead of MD5. Additionally, we can implement tokenization to replace sensitive data with unique tokens

Connecting and Writing to Postgres

The script uses the psycopg2 library to connect to and interact with the PostgreSQL database.

## Deploying in Production

- We can package the application in a Docker container for consistent deployment across environments.
- Deploying on a cloud platform like AWS, GCP, or Azure can provide scalability.
- We can implement monitoring and logging tools, such as CloudWatch, for better application oversight.
- We can use a managed database service like AWS RDS for PostgreSQL, with proper scaling and backup configurations.
- For Large Datasets, we can use Apache Spark for processng.

## PII Recovery
Instead of one-way hashing, use reversible encryption (e.g., AES) for PII data that needs to be recovered.
AES ensures that data remains confidential and is only accessible to authorized parties with the decryption key.

Reference: [GeeksforGeeks - Advanced Encryption Standard (AES)](https://www.geeksforgeeks.org/advanced-encryption-standard-aes/#)
