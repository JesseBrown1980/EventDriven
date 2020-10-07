import json

import transform
import load
import save
import notification


def lambda_handler(event, context):
    nyt_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    jh_url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'

    covid_df = transform.modify(nyt_url, jh_url)

    try:  # save dataframe for dashboard data
        save.df_to_s3(covid_df)
    except:
        alert = "Error passing covid dataframe to S3 save module"
        notification.send_sns(alert)
        print(alert)

    try:  # pushe data to DynamoDB
        covid_dynamo = load.to_dynamo(covid_df)
    except:
        alert = "Error passing covid dataframe to_dynamo function"
        notification.send_sns(alert)
        print(alert)


def main():
    lambda_handler()


if __name__ == '__main__':
    main()
