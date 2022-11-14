import nasdaqdatalink
import os
import pandas as pd
from symbols_list import symbols  # all active u.s. stock symbols

nasday_data_link_api_key = os.environ['NASDAQ_DATA_LINK_API_KEY']
nasdaqdatalink.ApiConfig.api_key = nasday_data_link_api_key
pd.options.display.float_format = '{:,}'.format

def get_daily():
    daily = nasdaqdatalink.get_table('SHARADAR/DAILY', date='2022-11-11')
    daily = daily[[
        'ticker',
        'marketcap'
    ]]
    daily = daily.set_index(['ticker'])
    daily.to_pickle('daily.pkl')

def get_company_info():
    info = nasdaqdatalink.get_table('SHARADAR/TICKERS', table='SF1', qopts={"columns":['ticker', 'name', 'exchange', 'famaindustry', 'sector', 'companysite', 'isdelisted']}, paginate=True)

    # filter out delisted stocks, then format table
    info = info[
        (info['isdelisted'] == 'N')
    ]
    info = info.set_index(['ticker'])
    info['name'] = info['name'].str.title()

    info.to_pickle('company_info.pkl')

def get_fundamentals():
    # import data for listed symbols, format, then export
    fund = nasdaqdatalink.get_table('SHARADAR/SF1', dimension='MRY', ticker=symbols, qopts={"columns":['ticker', 'calendardate', 'revenueusd', 'opinc', 'netinccmnusd', 'fcf', 'fxusd']}, paginate=True) 

    fund = fund.set_index(['ticker'])
    fund['year'] = fund['calendardate'].dt.year
    fund['revenueusd'] = fund['revenueusd'] / 1000000
    fund['opinc'] = fund['opinc'] / 1000000
    fund['opincusd'] = fund['opinc'] / fund['fxusd']
    fund['netinccmnusd'] = fund['netinccmnusd'] / 1000000
    fund['fcf'] = fund['fcf'] / 1000000
    fund['fcfusd'] = fund['fcf'] / fund['fxusd']
    fund['ncfbus'] = fund['ncfbus'] / 1000000
    fund['ncfbususd'] = fund['ncfbus'] / fund['fxusd']
    fund['intexp'] = fund['intexp'] / 1000000
    fund['intexpusd'] = fund['intexp'] / fund['fxusd']
    print(fund)
    fund.to_pickle('fundamentals.pkl')

    # add these metrics for each ticker (i.e. to each row) after pivoting
    # 'ncfbus', 'intexp', 'de', 'roic'

# Read pickle files only to do specific formatting, then resave
    # info = pd.read_pickle('company_info.pkl')
    # fund = pd.read_pickle('fundamentals.pkl')

# get_daily()
# get_company_info()
get_fundamentals()