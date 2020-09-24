import boto3
import csv
import pandas as pd
from io import StringIO
import codecs
#import os

#s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')

def extract():
  urlNYT = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
  urlJH = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'

  dataNYT = pd.read_csv(urlNYT, header=0, names=['Date', 'Cases', 'Deaths'], dtype={'Cases':'Int64','Deaths':'Int64'})
  dataNYT['Date'] = pd.to_datetime(dataNYT['Date'], format = "%Y-%m-%d")
  #hello = dataNYT
  #dataNYT.set_index('Date')
  #bufferNYT = StringIO()
  #dataNYT.to_csv(bufferNYT)
  #hello.reset_index()
  #print(hello)
  #print(dataNYT)
  

  dataJH = pd.read_csv(urlJH, usecols=['Date', 'Country/Region', 'Recovered'], dtype={'Recovered':'Int64'}, encoding='utf8').dropna()
  dataJH.rename(columns={"Country/Region": "Country"}, inplace=True)
  dataJH['Date'] = pd.to_datetime(dataJH['Date'], format = "%Y-%m-%d")
  data_JH_US_FILTER = dataJH[dataJH.Country == 'US']
  
  
  NYTtoJH = dataNYT.set_index('Date').join(data_JH_US_FILTER.set_index('Date')).dropna()
  headers = ['Country', 'Cases', 'Recovered', 'Deaths']
  sortBy = headers + [c for c in NYTtoJH.columns if c not in headers]
  NYTtoJH = NYTtoJH[sortBy]
  #print(NYTtoJH)
  buffer = StringIO()
  NYTtoJH.to_csv(buffer)
  #print(buffer.getvalue())

  #print(data_JH_US_FILTER.set_index('Date'))
  #data_JH_US = StringIO()
  #data_JH_US_FILTER.to_csv(data_JH_US)
  #print(data_JH_US_FILTER.dtypes)
  
  #print(dataJH.loc[4:, 'Confirmed'].head(10))
  #s3.Bucket('logantoler').put_object(Key= 'hello.csv', Body=data_JH_US.getvalue())


def main():
    extract()


if __name__ == '__main__':
    main()