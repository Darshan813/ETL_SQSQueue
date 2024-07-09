import json
from datetime import datetime
from mask_data import mask_data


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
                "ip": mask_data(message_body["ip"]),
                "device_id": mask_data(message_body["device_id"]),
                "locale": message_body["locale"],
                "app_version": message_body["app_version"],
                "create_date": response_date
            }
            all_messages.append(data)

        except Exception as e:
            print("Raising Exception:", message_body["foo"])

    return all_messages