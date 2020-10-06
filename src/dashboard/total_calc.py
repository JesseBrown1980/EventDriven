import pandas as pd


def transform(covid_csv):
    to_dash = pd.read_csv(covid_csv,
                          usecols=['Cases', 'Recovered', 'Deaths'])
    cols = ['Cases', 'Recovered', 'Deaths']
    for i in cols:
        to_dash[i] = to_dash[i].astype(int).apply(lambda x: f'{x:,}')
    return to_dash


def total_numbers(to_dash):
    cases = to_dash.Cases.iat[-1]
    recovered = to_dash.Recovered.iat[-1]
    deaths = to_dash.Deaths.iat[-1]
    items = [{'cases': cases}, {'recovered': recovered}, {'deaths': deaths}]
    return items
