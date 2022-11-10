import nasdaqdatalink
import os
import pandas as pd
# import active u.s. stock symbols
from symbols_list import symbols

nasday_data_link_api_key = os.environ['NASDAQ_DATA_LINK_API_KEY']
nasdaqdatalink.ApiConfig.api_key = nasday_data_link_api_key
pd.options.display.float_format = '{:,}'.format

# COMPANY INFO
# info = nasdaqdatalink.get_table('SHARADAR/TICKERS', table='SF1', qopts={"columns":['ticker', 'name', 'exchange', 'famaindustry', 'sector', 'companysite', 'isdelisted']}, paginate=True)
# # filter out delisted stocks, then format table
# info = info[
#     (info['isdelisted'] == 'N')
# ]
# info = info.set_index(['ticker'])
# info['name'] = info['name'].str.title()
# # export to excel
# info.to_excel('company_info.xlsx')

# save tickers that aren't delisted to list, then try 'not in' filter


# FUNDAMENTALS
# import data for listed symbols, format, then export

# fund = nasdaqdatalink.get_table('SHARADAR/SF1', dimension='MRY', ticker=symbols, qopts={"columns":['ticker', 'calendardate', 'revenueusd', 'opinc', 'netinccmnusd', 'fxusd']}, paginate=True)
fund = pd.read_pickle('fundamentals.pkl')
fund = fund.set_index(['ticker'])
fund['year'] = fund['calendardate'].dt.year
fund['revenueusd'] = fund['revenueusd'] / 1000000
fund['opinc'] = fund['opinc'] / 1000000
fund['netinccmnusd'] = fund['netinccmnusd'] / 1000000
fund['opincusd'] = fund['opinc'] / fund['fxusd']
fund.to_pickle('fundamentals.pkl')