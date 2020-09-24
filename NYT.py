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
  

  dataNYT = pd.read_csv(urlNYT, header=0, names=['Date', 'Cases', 'Deaths'], dtype={'Cases':'Int64','Deaths':'Int64'})
  dataNYT['Date'] = pd.to_datetime(dataNYT['Date'], format = "%Y-%m-%d")
  bufferNYT = StringIO()
  dataNYT.to_csv(bufferNYT)
  print(dataNYT.dtypes)

  #dataJH = pd.read_csv(urlJH, usecols=['Date', 'Country/Region', 'Recovered'], encoding='utf8').dropna()
  #dataJH.rename(columns={"Country/Region": "Country"}, inplace=True)
  #dataJH['Date'] = pd.to_datetime(dataJH['Date'], format = "%Y-%m-%d")
  #dataJH['Recovered'] = dataJH['Recovered'].astype('Int64')
  #data_JH_US_FILTER = dataJH[dataJH.Country == 'US']
  
  #data_JH_US = StringIO()
  #data_JH_US_FILTER.to_csv(data_JH_US)
  #print(data_JH_US_FILTER.dtypes)
  
  #print(dataJH.loc[4:, 'Confirmed'].head(10))
  #s3.Bucket('logantoler').put_object(Key= 'hello.csv', Body=data_JH_US.getvalue())


def main():
    extract()


if __name__ == '__main__':
    main()