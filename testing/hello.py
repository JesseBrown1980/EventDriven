import boto3
import csv
from io import StringIO
import pandas as pd
import os
import json
import codecs
import hello2

dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')
bucket = s3.Bucket('logantoler')
key = 'us.csv'
tableName = 'CovidDate'
table = dynamodb.Table(tableName)

def transform(urlNYT, urlJH):
   dataNYT = pd.read_csv(urlNYT, header=0, names=['Date', 'Cases', 'Deaths'], dtype={'Cases':'Int64','Deaths':'Int64'})
   dataNYT['Date'] = pd.to_datetime(dataNYT['Date'], format = "%Y-%m-%d")
   #dataNYT['Date'] = dataNYT.Date.apply(lambda x: x.strftime('%Y-%m-%d'))
   
   dataJH = pd.read_csv(urlJH, usecols=['Date', 'Country/Region', 'Recovered'], dtype={'Recovered':'Int64'}, encoding='utf8').dropna()
   dataJH.rename(columns={"Country/Region": "Country"}, inplace=True)
   dataJH['Date'] = pd.to_datetime(dataJH['Date'], format = "%Y-%m-%d")
   #dataJH['Date'] = dataJH.Date.apply(lambda x: x.strftime('%Y-%m-%d'))
   data_JH_US_FILTER = dataJH[dataJH.Country == 'US']

   
   NYTtoJH = dataNYT.set_index('Date').join(data_JH_US_FILTER.set_index('Date')).dropna()

   covidTable = StringIO()
   NYTtoJH.to_csv(covidTable)
   
   s3.Bucket('logantoler').put_object(Key = 'us.csv', Body=covidTable.getvalue())
   obj = s3.Object('logantoler', key).get()['Body']
   
   hello2.begin_load(obj)

   #module to filter dates, but need logic to compare what is in table and not to only update added records

   