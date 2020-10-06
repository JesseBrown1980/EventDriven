import pandas as pd
import boto3
import os
from io import StringIO
import notification

s3 = boto3.resource('s3')
bucketName = os.environ['bucket']
key = 'CovidData.csv'
key2 = 'comparison.jpeg'



def graph_to_s3(comparison):
    try:
        s3.Object(bucketName, key2).upload_file('/tmp/comparison.jpeg')
    except:
        alert = "Error saving graph to S3"
        notification.send_sns(alert)
        print(alert)


def get_s3():
    try:
        covid_csv = s3.Object(bucketName, key).get()['Body']
        return covid_csv
    except:
        alert = "Error getting csv from S3"
        notification.send_sns(alert)
        print(alert)
