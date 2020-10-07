# EventDrivenPython

## Overview
Runs an ETL job on two data sources ([NYT](https://github.com/nytimes/covid-19-data/blob/master/us.csv?opt_id=oeu1600284808955r0.2700974837928787), [John Hopkins](https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv?opt_id=oeu1600284808955r0.2700974837928787)).


### ETL Function
The ETL function performs an ETL job within memory on a single Lambda function and the resulting data is loaded into a DynamoDB table and saved as a CSV in S3. It is triggered each day at 16h00 EST using an EventBridge event and relies exclusively on Pandas and Boto3.
When loading the data, a conditional expression is used to block updating/overwriting existing records and only write new ones in the table. If a record fails to write, it will be noted and included when the job runs again.


### Dashboard Function
The dashboard function creates data that could be used to build a dashboard. It is triggered by calling the API created in the template, which pulls the CSV created by the ETL function from S3. The resulting graph is stored in an S3 bucket and the totals are returned in the API response. 
This function relies on Matplot to create a stack area chart and Pandas to extract the most recent total cases, recoveries, and deaths.

### SNS
An SNS topic is created to alert the amount of rows added when the ETL job completes and any run-time failures.

### CI/CD
GitHub Actions is used to package and deploy the SAM package to AWS when a change is detected on the master branch.

### To deploy - clone the repo and push to the master branch
```
gh repo clone tolerl1/EventDrivenPython
```

### Current Dashboard
The [current dashboard](https://app.redash.io/logan-toler/public/dashboards/bQv4OpTwd8oZ2NHjT31gtjtIFiDayXu1XPK0NbTM) is hosted on Redash. The future plan is to move this over to the Vue.js app that I am working on.

SaaS dashboard solutions are very expensive and there is the additional cost of running scans/queries against a DynamoDB table to obtain the data. Using other AWS database solutions would be overkill for this challenge and still carry a high operating cost. Therefore, DynamoDB was chosen and the intent to create a custom dashboard using Vue.js, pulling the necessary data using a lambda function, removing the need to run queries against the table.

### Unit Testing
The unit test directory contains two sample CSV files with a few malformed records and a Jupyter Notebook to run the tests. 
