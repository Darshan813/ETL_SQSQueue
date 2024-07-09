import psycopg2
from psycopg2.extras import execute_values


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
