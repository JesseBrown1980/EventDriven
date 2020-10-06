import boto3
import pandas as pd
import os
import json
from decimal import Decimal

import notification


from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
tableName = os.environ['table']


def to_dynamo(covid_df):
    try:
        table = dynamodb.Table(tableName)
    except:
        alert = "Error loading DynamoDB table. Check if table was created correctly and environment variable."
        notification.send_sns(alert)
        print(alert)

    try:
        count = 0
        for index, item in covid_df.iterrows():
            item = json.loads(item.to_json(), parse_float=(
                lambda s: Decimal(str(s))))
            try:
                table.put_item(
                    Item=item, ConditionExpression=Attr('Date').not_exists())
                count += 1
            except ClientError as e:
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    print("ConditionalCheckFailedException: {}".format(
                        item['Date']))
                    continue
        alert = ("{} row(s) have been added".format(count))
        print(alert)
        if count > 0:
            notification.send_sns(alert)
    except:
        alert = "Error with adding item(s) to table"
        notification.send_sns(alert)
        print(alert)
