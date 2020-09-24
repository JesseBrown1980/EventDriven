import boto3
import csv
from io import StringIO
import pandas as pd
import os
import json
import codecs

dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')
bucket = s3.Bucket('logantoler')
key = 'us.csv'
tableName = 'CovidDate'


def extract():
   urlNYT = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
   urlJH = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'

   transform(urlNYT, urlJH)


def transform(urlNYT, urlJH):
   dataNYT = pd.read_csv(urlNYT, header=0, names=['Date', 'Cases', 'Deaths'], dtype={'Cases':'Int64','Deaths':'Int64'})
   dataNYT['Date'] = pd.to_datetime(dataNYT['Date'], format = "%Y-%m-%d")

   dataJH = pd.read_csv(urlJH, usecols=['Date', 'Country/Region', 'Recovered'], dtype={'Recovered':'Int64'}, encoding='utf8').dropna()
   dataJH.rename(columns={"Country/Region": "Country"}, inplace=True)
   dataJH['Date'] = pd.to_datetime(dataJH['Date'], format = "%Y-%m-%d")
   data_JH_US_FILTER = dataJH[dataJH.Country == 'US']


   NYTtoJH = dataNYT.set_index('Date').join(data_JH_US_FILTER.set_index('Date')).dropna()
   headers = ['Country', 'Cases', 'Recovered', 'Deaths']
   sortBy = headers + [c for c in NYTtoJH.columns if c not in headers]
   NYTtoJH = NYTtoJH[sortBy]

   covidTable = StringIO()
   NYTtoJH.to_csv(covidTable)
   s3.Bucket('logantoler').put_object(Key = 'us.csv', Body=covidTable.getvalue())
   
   begin_load()

def begin_load():
   try:
      obj1 = s3.Object('logantoler', key).get()['Body']
   except:
      print("error happened at upload")
   try:
      table = dynamodb.Table(tableName)
   except:
      print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

   batch_size = 100
   batch = []

   # DictReader is a generator; not stored in memory
   for row in csv.DictReader(codecs.getreader('utf-8')(obj1)):
      if len(batch) >= batch_size:
         write_to_dynamo(batch)
         batch.clear()

      batch.append(row)

   if batch:
      write_to_dynamo(batch)
   return {
      'statusCode': 200,
      'body': json.dumps('Uploaded to DynamoDB Table')
   }


def write_to_dynamo(rows):
   try:
      table = dynamodb.Table(tableName)
   except:
      print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

   try:
      with table.batch_writer() as batch:
         for i in range(len(rows)):
            batch.put_item(Item=rows[i])
   except:
      print("Error executing batch_writer")



def main():
    extract()


if __name__ == '__main__':
    main()




#if upload to s3 == 200 continue to transform module 
#else throw error

#when transform is complete load data

