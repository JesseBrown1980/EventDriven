import json
import transform
import load
from dashboard import graph
from dashboard import save


def lambda_handler(event, context):
    nyt_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    jh_url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'

    covid_df = transform.modify(nyt_url, jh_url)

    # create dashboard data
    save.df_to_s3(covid_df)
    covid_csv = save.get_s3()
    to_dash = graph.transform(covid_csv)
    comparison = graph.by_month(to_dash)
    save.graph_to_s3(comparison)

    # push data to DynamoDB
    covid_dynamo = load.to_dynamo(covid_df)


def main():
    lambda_handler()


if __name__ == '__main__':
    main()
