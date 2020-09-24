import boto3
import csv
import pandas as pd
from io import StringIO
#import os

#s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')

def extract():
  urlNYT = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
  urlJH = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'

  dataNYT = pd.read_csv(urlNYT)
  dataNYT['date'] = pd.to_datetime(dataNYT['date'], format = "%Y-%m-%d")
  bufferNYT = StringIO()
  dataNYT.to_csv(bufferNYT)
  

  dataJH = pd.read_csv(urlJH, usecols=['Date', 'Country/Region', 'Province/State', 'Recovered']).dropna()
  dataJH.rename(columns={"Country/Region": "Country", "Province/State": "State"}, inplace=True)
  dataJH['Date'] = pd.to_datetime(dataJH['Date'], format = "%Y-%m-%d")
  dataJH['Recovered'] = dataJH['Recovered'].astype('Int64')
  

  #dataJH.to_csv()
  print(d)
  
  #print(dataJH.loc[4:, 'Confirmed'].head(10))
  #s3.Bucket('logantoler').put_object(Key= 'hello.csv', Body=bufferNYT.getvalue())


def main():
    extract()


if __name__ == '__main__':
    main()