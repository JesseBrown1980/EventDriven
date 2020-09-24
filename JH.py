import boto3
import csv
import pandas as pd
from io import StringIO
#import os

#s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')

def extract():
  urlJH = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'
  

  dataJH = pd.read_csv(urlJH, usecols=['Date', 'Country/Region', 'Recovered'], dtype={'Recovered':'Int64'}, encoding='utf8').dropna()
  dataJH.rename(columns={"Country/Region": "Country"}, inplace=True)
  dataJH['Date'] = pd.to_datetime(dataJH['Date'], format = "%Y-%m-%d")
  data_JH_US_FILTER = dataJH[dataJH.Country == 'US']
  
  #data_JH_US = StringIO()
  #data_JH_US_FILTER.to_csv(data_JH_US)
  print(data_JH_US_FILTER)
  
  #print(dataJH.loc[4:, 'Confirmed'].head(10))
  #s3.Bucket('logantoler').put_object(Key= 'hello.csv', Body=data_JH_US.getvalue())


def main():
    extract()


if __name__ == '__main__':
    main()