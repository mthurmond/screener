import requests
import pandas as pd
import os
from symbols_list_copy import symbols

polygon_key = os.environ['POLYGON_API_KEY']

polygon_key = 'lA4S9f8CnDuPhIjuBGvsKzmHdNk1ibf9'
polygon_financials_url = 'https://api.polygon.io/vX/reference/financials'
polygon_tickers_url = 'https://api.polygon.io/v3/reference/tickers/'

us_symbols_list = symbols

def get_financials(symbols):
	# pull operating income from polygon for all symbols
	df = pd.DataFrame(columns=['symbol', 'revenue', 'opincome', 'opcashflow', 'assets', 'current_assets'])
	count = 0

	for symbol in symbols:
		payload = {'apikey': polygon_key,
					'include_sources': 'false',
					'ticker': symbol}
		results = requests.get(polygon_financials_url, params=payload)
		data = results.json()
		
		try:
			revenue = data['results'][0]['financials']['income_statement']['revenues']['value']
		except:
			revenue = 000

		try:
			opincome = data['results'][0]['financials']['income_statement']['operating_income_loss']['value']
		except:
			opincome = 000
		
		try:
			opcashflow = data['results'][0]['financials']['cash_flow_statement']['net_cash_flow_from_operating_activities']['value']
		except:
			opcashflow = 000

		try:
			assets = data['results'][0]['financials']['balance_sheet']['assets']['value']
		except:
			assets = 000

		try:
			current_assets = data['results'][0]['financials']['balance_sheet']['current_assets']['value']
		except:
			current_assets = 000

		df.loc[len(df.index)] = [symbol, revenue, opincome, opcashflow, assets, current_assets]
		count += 1
		print(count)
	
	return df

def get_comp_details(symbols):
	# pull operating income from polygon for all symbols
	df = pd.DataFrame(columns=['symbol', 'description', 'sic_code', 'sic_description', 'total_employees'])
	count = 0
	payload = {'apikey': polygon_key}

	for symbol in symbols:
		results = requests.get(polygon_tickers_url + symbol, params=payload)
		data = results.json()
		
		try:
			description = data['results']['description']
		except:
			description = 'not available'

		try:
			sic_code = data['results']['sic_code']
		except:
			sic_code = 000
		
		try:
			sic_description = data['results']['sic_description']
		except:
			sic_description = 'not available'

		try:
			total_employees = data['results']['total_employees']
		except:
			total_employees = 000

		df.loc[len(df.index)] = [symbol, description, sic_code, sic_description, total_employees]
		count += 1
		print(count)
	
	return df

# refresh data by uncommenting code below
# financials_df = get_financials(us_symbols_list)
# financials_df.to_excel('financials_11-2-2022.xlsx')

# details_df = get_comp_details(us_symbols_list)
# details_df.to_excel('details_11-2-2022.xlsx')

# can refactor code above so I make fewer queries by using query parameters

def get_financials_multi_ticker():
	payload = {'apikey': 'lA4S9f8CnDuPhIjuBGvsKzmHdNk1ibf9',
				'include_sources': 'false',
				'period_of_report_date.gte': '2022-06-01',
				'period_of_report_date.lte': '2022-09-01',
				'timeframe': 'annual',
				'order': 'asc',
				'limit': '30'}
	results = requests.get(polygon_financials_url, params=payload)
	data = results.json()
	return data

# financials_resp = get_financials_multi_ticker()

# example query parameters
# https://api.polygon.io/v3/reference/tickers?ticker.gte=A&ticker.lt=B&active=true&sort=ticker&order=asc&limit=10&apiKey=lA4S9f8CnDuPhIjuBGvsKzmHdNk1ibf9

# https://api.polygon.io/vX/reference/financials?period_of_report_date.gte=2022-06-01&period_of_report_date.lte=2022-09-01&limit=30&timeframe=annual&order=asc&limit=10&apiKey=lA4S9f8CnDuPhIjuBGvsKzmHdNk1ibf9