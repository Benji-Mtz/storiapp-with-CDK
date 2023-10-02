import json
import os
import boto3
import csv
import io

from helpers.functions import reading_csv, reading_dict, total_balance, transactions_for_month, average_amount, send_email

s3Client = boto3.client('s3')


EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_RECEIVER = os.environ['EMAIL_RECEIVER']


def lambda_handler(event, context):

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    s3_file_name = event["Records"][0]["s3"]["object"]["key"]
    print(s3_file_name)

    print(bucket_name)
    print(s3_file_name)

    resp = s3Client.get_object(Bucket=bucket_name, Key=s3_file_name)
    # extract body and decode using utf-8
    data = resp['Body'].read().decode('utf-8')

    # Obtaining general dict from csv
    keys_dict = reading_csv(data)
    csv_to_dict = reading_dict(data, keys_dict)
    print(csv_to_dict)

    # Balance
    tb = total_balance(csv_to_dict)
    print(tb)

    # Transactions
    transactions = transactions_for_month(csv_to_dict)
    print(transactions)

    # Average
    debit, credit = average_amount(csv_to_dict)

    print(tb, transactions, debit, credit)

    # Sending email
    data_for_email = {
        "total_balance": tb,
        "transactions": transactions,
        "avg_debit": debit,
        "avg_credit": credit
    }
    send_email(data_for_email, EMAIL_ADDRESS,  EMAIL_RECEIVER, EMAIL_PASSWORD)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data_for_email)
    }
