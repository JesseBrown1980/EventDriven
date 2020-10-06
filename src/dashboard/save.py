import pandas as pd
import boto3
import os
from io import StringIO

s3 = boto3.resource('s3')
bucketName = os.environ['bucket']
key = 'CovidData.csv'
key2 = 'comparison.jpeg'


def graph_to_s3(comparison):
    s3.Object(bucketName, key2).upload_file('/tmp/comparison.jpeg')


def get_s3():
    covid_csv = s3.Object(bucketName, key).get()['Body']
    return covid_csv
