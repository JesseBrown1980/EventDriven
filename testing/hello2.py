import boto3
import csv
from io import StringIO
import pandas as pd
import os
import json
import codecs

import hello

dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')
bucket = s3.Bucket('logantoler')
key = 'us.csv'
tableName = 'CovidDate'

def begin_load(obj):
   try:
      table = dynamodb.Table(tableName)
   except:
      print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

   batch_size = 100
   batch = []

   # DictReader is a generator; not stored in memory
   for row in csv.DictReader(codecs.getreader('utf-8')(obj)):
      if len(batch) >= batch_size:
         write_to_dynamo(batch)
         batch.clear()

      batch.append(row)

   if batch:
      write_to_dynamo(batch)
   return {
      'statusCode': 200,
      'body': json.dumps('Uploaded to DynamoDB Table')
   }


def write_to_dynamo(rows):
   try:
      table = dynamodb.Table(tableName)
   except:
      print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

   try:
      with table.batch_writer() as batch:
         for i in range(len(rows)):
            batch.put_item(Item=rows[i])
   except:
      print("Error executing batch_writer")
