import pandas as pd
import boto3
import os
from io import StringIO
import notification

s3 = boto3.resource('s3')
bucketName = os.environ['bucket']
key = 'CovidData.csv'


def df_to_s3(covid_df):
    try:
        csv_buffer = StringIO()
        covid_df.to_csv(csv_buffer)
        s3.Object(bucketName, key).put(Body=csv_buffer.getvalue())
    except:
        alert = "Error saving csv to S3"
        notification.send_sns(alert)
        print(alert)
