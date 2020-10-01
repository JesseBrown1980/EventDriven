import boto3
import pandas as pd
import os
import json
from decimal import Decimal

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
tableName = os.environ['table']


def to_dynamo(covid_df):
    try:
        table = dynamodb.Table(tableName)
    except:
        print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")
    try:
        for index, item in covid_df.iterrows():
            item = json.loads(item.to_json(), parse_float=(
                lambda s: Decimal(str(s))))
            try:
                table.put_item(
                    Item=item, ConditionExpression=Attr('Date').not_exists())
            except ClientError as e:
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    print("ConditionalCheckFailedException: {}".format(
                        item['Date']))
                    continue
    except:
        print("Error with put/batch_writer")
