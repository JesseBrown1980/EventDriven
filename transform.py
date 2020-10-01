import pandas as pd


def modify(nyt_url, jh_url):
    nyt_df = pd.read_csv(nyt_url,
                         header=0,
                         names=['Date', 'Cases', 'Deaths'],
                         dtype={'Cases': 'Int64', 'Deaths': 'Int64'})
    nyt_df['Date'] = pd.to_datetime(nyt_df['Date'], format="%Y-%m-%d")
    #dataNYT['Date'] = dataNYT.Date.apply(lambda x: x.strftime('%Y-%m-%d'))

    jh_df = pd.read_csv(jh_url,
                        usecols=['Date', 'Country/Region', 'Recovered'],
                        dtype={'Recovered': 'Int64'},
                        encoding='utf8').dropna()

    jh_df.rename(columns={'Country/Region': 'Country'}, inplace=True)

    jh_df['Date'] = pd.to_datetime(jh_df['Date'], format="%Y-%m-%d")

    #jh_df['Date'] = jh_df.Date.apply(lambda x: x.strftime('%Y-%m-%d'))
    jh_us_filter = jh_df[jh_df.Country == 'US']

    covid_df = nyt_df.set_index('Date').join(
        jh_us_filter.set_index('Date')).dropna()
    
    covid_df.reset_index(inplace=True)
    covid_df['Date'] = covid_df['Date'].dt.strftime('%Y-%m-%d')

    return covid_df
