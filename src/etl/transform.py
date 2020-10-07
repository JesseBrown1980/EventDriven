import pandas as pd
import notification


def modify(nyt_url, jh_url):
    # read data from both sources into a dataframe
    # remove unwanted data, formats, and filters
    # join dataframes on index
    try:
        nyt_df = pd.read_csv(nyt_url,
                             header=0,
                             names=['Date', 'Cases', 'Deaths'],
                             dtype={'Cases': 'Int64', 'Deaths': 'Int64'})
        nyt_df['Date'] = pd.to_datetime(nyt_df['Date'], format="%Y-%m-%d")
    except:
        alert = "Error with NYT link"
        notification.send_sns(alert)
        print(alert)

    try:
        jh_df = pd.read_csv(jh_url,
                            usecols=['Date', 'Country/Region', 'Recovered'],
                            dtype={'Recovered': 'Int64'},
                            encoding='utf8').dropna()
        jh_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
        jh_df['Date'] = pd.to_datetime(jh_df['Date'], format="%Y-%m-%d")
    except:
        alert = "Error with JH link"
        notification.send_sns(alert)
        print(alert)

    try:
        jh_us_filter = jh_df[jh_df.Country == 'US']
        covid_df = nyt_df.set_index('Date').join(
            jh_us_filter.set_index('Date')).dropna()
        covid_df.reset_index(inplace=True)
        covid_df['Date'] = covid_df['Date'].dt.strftime('%Y-%m-%d')
        return covid_df
    except:
        alert = "Error joining data"
        notification.send_sns(alert)
        print(alert)
