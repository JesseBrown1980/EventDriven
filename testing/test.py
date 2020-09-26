import boto3
import csv
from io import StringIO
import pandas as pd
import os
import json
import codecs

import hello


dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')
bucket = s3.Bucket('logantoler')
key = 'us.csv'
tableName = 'CovidDate'


def extract():
   urlNYT = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
   urlJH = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'

   #extractNYT = pd.read_csv(urlNYT)
   #s3NYT = StringIO()
   #extract.to_csv(s3NYT)

   #s3.Bucket('logantoler').put_object(Key = 'us.csv', Body=s3NYT.getvalue())
   hello.transform(urlNYT, urlJH)




def main():
    extract()


if __name__ == '__main__':
    main()




#if upload to s3 == 200 continue to transform module 
#else throw error

#when transform is complete load data

