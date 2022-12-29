import nasdaqdatalink
import os
import pandas as pd
from symbols_list import symbols  # all active u.s. stock symbols
# from symbols_portfolio import portfolio  # all active u.s. stock symbols

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
    info = nasdaqdatalink.get_table('SHARADAR/TICKERS', table='SF1', qopts={"columns":['ticker', 'name', 'exchange', 'famaindustry', 'sector', 'location', 'companysite', 'isdelisted']}, paginate=True)

    # filter out delisted stocks, then format table
    info = info[
        (info['isdelisted'] == 'N')
    ]
    info = info.set_index(['ticker'])
    info['name'] = info['name'].str.title()

    info.to_pickle('company_info.pkl')

def get_fundamentals():
    # import data for listed symbols, format, then export
    fund = nasdaqdatalink.get_table('SHARADAR/SF1', dimension='MRY', ticker=symbols, qopts={"columns":['ticker', 'calendardate', 'revenueusd', 'opinc', 'netinccmnusd', 'fcf', 'roic', 'fxusd']}, paginate=True) 

    fund = fund.set_index(['ticker'])
    fund['year'] = fund['calendardate'].dt.year
    fund['revenueusd'] = fund['revenueusd'] / 1000000
    fund['opinc'] = fund['opinc'] / 1000000
    fund['opincusd'] = fund['opinc'] / fund['fxusd']
    fund['netinccmnusd'] = fund['netinccmnusd'] / 1000000
    fund['fcf'] = fund['fcf'] / 1000000
    fund['fcfusd'] = fund['fcf'] / fund['fxusd']
    fund['roic'] = fund['roic'] * 100
    fund = fund.pivot(columns=["year"],values=["revenueusd", "opincusd", "netinccmnusd", 'fcfusd', 'roic'])

    # add metrics where only most recent datapoint needed
    recent = nasdaqdatalink.get_table('SHARADAR/SF1', dimension='MRY', ticker=symbols, qopts={'latest':1, "columns":['ticker', 'intexp', 'ebit']}, paginate=True)
    recent = recent.set_index(['ticker'])
    recent['intexp-ebit'] = recent['intexp'] / recent['ebit']
    recent['intexp-ebit'] = recent['intexp-ebit'] * 100
    recent = recent[[
        'intexp-ebit'
    ]]

    # merge recent point metrics into pivot table and export
    fund = fund.merge(recent, how='left', on='ticker')

    # add average metrics
    fund['avginc02-06'] = (
        fund[('netinccmnusd', 2002)] + 
        fund[('netinccmnusd', 2003)] +
        fund[('netinccmnusd', 2004)] + 
        fund[('netinccmnusd', 2005)] +
        fund[('netinccmnusd', 2006)]
    ) / 5
    fund['avginc07-11'] = (
        fund[('netinccmnusd', 2007)] + 
        fund[('netinccmnusd', 2008)] +
        fund[('netinccmnusd', 2009)] + 
        fund[('netinccmnusd', 2010)] +
        fund[('netinccmnusd', 2011)]
    ) / 5
    fund['avginc12-16'] = (
        fund[('netinccmnusd', 2012)] + 
        fund[('netinccmnusd', 2013)] +
        fund[('netinccmnusd', 2014)] + 
        fund[('netinccmnusd', 2015)] +
        fund[('netinccmnusd', 2016)]
    ) / 5
    fund['avginc17-21'] = (
        fund[('netinccmnusd', 2017)] + 
        fund[('netinccmnusd', 2018)] +
        fund[('netinccmnusd', 2019)] + 
        fund[('netinccmnusd', 2020)] +
        fund[('netinccmnusd', 2021)]
    ) / 5

    fund['avgfcf02-06'] = (
        fund[('fcfusd', 2002)] + 
        fund[('fcfusd', 2003)] +
        fund[('fcfusd', 2004)] + 
        fund[('fcfusd', 2005)] +
        fund[('fcfusd', 2006)]
    ) / 5
    fund['avgfcf07-11'] = (
        fund[('fcfusd', 2007)] + 
        fund[('fcfusd', 2008)] +
        fund[('fcfusd', 2009)] + 
        fund[('fcfusd', 2010)] +
        fund[('fcfusd', 2011)]
    ) / 5
    fund['avgfcf12-16'] = (
        fund[('fcfusd', 2012)] + 
        fund[('fcfusd', 2013)] +
        fund[('fcfusd', 2014)] + 
        fund[('fcfusd', 2015)] +
        fund[('fcfusd', 2016)]
    ) / 5
    fund['avgfcf17-21'] = (
        fund[('fcfusd', 2017)] + 
        fund[('fcfusd', 2018)] +
        fund[('fcfusd', 2019)] + 
        fund[('fcfusd', 2020)] +
        fund[('fcfusd', 2021)]
    ) / 5

    fund['avgroic02-06'] = (
        fund[('roic', 2002)] + 
        fund[('roic', 2003)] +
        fund[('roic', 2004)] + 
        fund[('roic', 2005)] +
        fund[('roic', 2006)]
    ) / 5
    fund['avgroic07-11'] = (
        fund[('roic', 2007)] + 
        fund[('roic', 2008)] +
        fund[('roic', 2009)] + 
        fund[('roic', 2010)] +
        fund[('roic', 2011)]
    ) / 5
    fund['avgroic12-16'] = (
        fund[('roic', 2012)] + 
        fund[('roic', 2013)] +
        fund[('roic', 2014)] + 
        fund[('roic', 2015)] +
        fund[('roic', 2016)]
    ) / 5
    fund['avgroic17-21'] = (
        fund[('roic', 2017)] + 
        fund[('roic', 2018)] +
        fund[('roic', 2019)] + 
        fund[('roic', 2020)] +
        fund[('roic', 2021)]
    ) / 5

    fund.to_pickle('fundamentals.pkl')

# Read pickle files only to do specific formatting, then resave
    # info = pd.read_pickle('company_info.pkl')
    # fund = pd.read_pickle('fundamentals.pkl')

# # get_daily()
# get_company_info()
get_fundamentals()