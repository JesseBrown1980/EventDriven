import pandas as pd

import notification


def transform(covid_csv):
    try:
        to_dash = pd.read_csv(covid_csv,
                              usecols=['Cases', 'Recovered', 'Deaths'])
        cols = ['Cases', 'Recovered', 'Deaths']
        for i in cols:
            to_dash[i] = to_dash[i].astype(int).apply(lambda x: f'{x:,}')
        return to_dash
    except:
        alert = "Error reading csv for calculating totals"
        notification.send_sns(alert)
        print(alert)


def total_numbers(to_dash):
    try:
        cases = to_dash.Cases.iat[-1]
        recovered = to_dash.Recovered.iat[-1]
        deaths = to_dash.Deaths.iat[-1]
        items = [{'cases': cases}, {
            'recovered': recovered}, {'deaths': deaths}]
        return items
    except:
        alert = "Error pulling total number from csv"
        notification.send_sns(alert)
        print(alert)
