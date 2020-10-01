#import boto3
#import os
import transform
import load

#dynamodb = boto3.resource('dynamodb')
#tableName = os.environ['table']
#bucket = os.environ['bucket']

def app():

    nyt_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    jh_url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'

    covid_df = transform.modify(nyt_url, jh_url)
    covid_dynamo = load.to_dynamo(covid_df)
    return covid_dynamo


def main():
    app()


if __name__ == '__main__':
    main()
