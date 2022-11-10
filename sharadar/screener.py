import nasdaqdatalink
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

nasday_data_link_api_key = os.environ['NASDAQ_DATA_LINK_API_KEY']
nasdaqdatalink.ApiConfig.api_key = nasday_data_link_api_key
pd.options.display.float_format = '{:,}'.format

# get base info; to refresh, see import file
fund = pd.read_pickle('fundamentals.pkl')
fin_pivot = fund.pivot(columns=["year"],values=["revenueusd", "opincusd", "netinccmnusd"])

# add company info
info = pd.read_excel('company_info.xlsx',index_col=0)
fin_and_info = fin_pivot.merge(info, how='left', on='ticker')

# add market cap
daily = nasdaqdatalink.get_table('SHARADAR/DAILY', date='2022-11-09')
daily_output = daily[[
    'ticker',
    'marketcap'
]]
daily_output = daily_output.set_index(['ticker'])
fin_merged = fin_and_info.merge(daily_output, how='left', on='ticker')

# add valuation metrics
fin_merged['p-opinc2010'] = fin_merged['marketcap'] / fin_merged[('opincusd', 2010)]
fin_merged['p-opinc2021'] = fin_merged['marketcap'] / fin_merged[('opincusd', 2021)]
fin_merged['p-netinc2021'] = fin_merged['marketcap'] / fin_merged[('netinccmnusd', 2021)]
fin_merged['avginc17-21'] = (
    fin_merged[('netinccmnusd', 2017)] + 
    fin_merged[('netinccmnusd', 2018)] +
    fin_merged[('netinccmnusd', 2019)] + 
    fin_merged[('netinccmnusd', 2020)] +
    fin_merged[('netinccmnusd', 2021)]
) / 5
fin_merged['p-5yravginc'] = fin_merged['marketcap'] / fin_merged['avginc17-21']
fin_merged = fin_merged.round(0)

# run screen
fin_screen = fin_merged[
    (fin_merged['p-opinc2010'] < 10) &
    (fin_merged['p-opinc2010'] > 0) &
    (fin_merged['p-opinc2021'] < 8) &
    (fin_merged['p-opinc2021'] > 0) &
    (fin_merged['p-netinc2021'] < 10) &
    (fin_merged['p-netinc2021'] > 0) &
    (fin_merged['p-5yravginc'] < 10) &
    (fin_merged['p-5yravginc'] > 0)
]
fin_screen = fin_screen.sort_index()
fin_screen.to_excel('financials_screen.xlsx')
# https://data.nasdaq.com/tables/SHARADAR-SF1/export?dimension=MRY&qopts.columns=ticker,calendardate,revenue,opinc&api_key=Za66XwxKqwNL-heRFEep