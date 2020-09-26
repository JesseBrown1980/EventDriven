def begin_load(covidTable):
   # get() does not store in memory
   try:
      obj1 = covidTable
      #obj2 = s3.Object(BucketName, key2).get()['Body']
   except:
      print("S3 Object could not be opened. Check environment variable.")
   try:
      table = dynamodb.Table(tableName)
   except:
      print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

   batch_size = 100
   batch = []

   # DictReader is a generator; not stored in memory
   for row in csv.DictReader(codecs.getreader('utf-8')(obj1)):
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
