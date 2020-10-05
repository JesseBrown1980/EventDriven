from dashboard import save
from dashboard import total_calc
import json

def lambda_handler(event, context):
    covid_csv = save.get_s3()
    to_dash = total_calc.transform(covid_csv)
    totals = total_calc.total_numbers(to_dash)

    #expose return total values to api
    return json.dumps([{"total": total} for total in totals])