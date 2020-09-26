def transform(urlNYT, urlJH):
   dataNYT = pd.read_csv(urlNYT, header=0, names=['Date', 'Cases', 'Deaths'], dtype={'Cases':'Int64','Deaths':'Int64'})
   dataNYT['Date'] = pd.to_datetime(dataNYT['Date'], format = "%Y-%m-%d")

   dataJH = pd.read_csv(urlJH, usecols=['Date', 'Country/Region', 'Recovered'], dtype={'Recovered':'Int64'}, encoding='utf8').dropna()
   dataJH.rename(columns={"Country/Region": "Country"}, inplace=True)
   dataJH['Date'] = pd.to_datetime(dataJH['Date'], format = "%Y-%m-%d")
   data_JH_US_FILTER = dataJH[dataJH.Country == 'US']


   NYTtoJH = dataNYT.set_index('Date').join(data_JH_US_FILTER.set_index('Date')).dropna()
   headers = ['Country', 'Cases', 'Recovered', 'Deaths']
   sortBy = headers + [c for c in NYTtoJH.columns if c not in headers]
   NYTtoJH = NYTtoJH[sortBy]

   covidTable = StringIO()
   NYTtoJH.to_csv(covidTable)
   #begin_load()
   print(covidTable.getvalue())