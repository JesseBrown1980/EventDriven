import boto3
import botocore
import os
import sys


sns_arn = os.environ['sns_topic_arn']


def send_sns(text):
    sns = boto3.client('sns')
    try:
        sns.publish(
            TopicArn=sns_arn,
            Subject=("Covid Table Update"),
            Message=text,
        )
    except:
        print("Error sending alert")
