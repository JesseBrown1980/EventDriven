import pandas as pd
import boto3
import os
from io import StringIO

s3 = boto3.resource('s3')
bucketName = os.environ['bucket']
bucket = s3.Bucket('bucketName') #create s3 bucket
key = 'CovidData.csv'
key2 = 'comparison.jpeg'

def df_to_s3(covid_df):
    csv_buffer = StringIO()
    covid_df.to_csv(csv_buffer)
    s3.Object(bucketName, key).put(Body=csv_buffer.getvalue())
    

def graph_to_s3(comparison):
    s3.Object(bucketName, key2).upload_file('/tmp/comparison.jpeg')

def get_s3():
    covid_csv = s3.Object(bucketName, key).get()['Body']
    return covid_csv
