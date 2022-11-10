import requests, time, string, random
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

# pull symbols from excel file
us_symbols_df = pd.read_excel('../symbols/symbols_current.xlsx')
us_symbols_list = us_symbols_df['symbol'].values.tolist()

ameritrade_instruments_url = 'https://api.tdameritrade.com/v1/instruments'
ameritrade_option_chains_url = 'https://api.tdameritrade.com/v1/marketdata/chains'
ameritrade_api_key = os.environ['AMERITRADE_API_KEY']

# pull fundamental stock data from ameritrade
def get_fundamentals(tickers):
	# ameritrade api accepts max of 500 tickers per call  
	start = 0
	end = 500
	frames = []

	# call api for each group of 500 tickers
	while start < len(tickers):  # can also use max as len(tickers) to extract data for all tickers in spreadsheet (~5k)
		tickers_short_list = tickers[start:end]

		payload = {'apikey': ameritrade_api_key,
				'symbol': tickers_short_list,
				'projection': 'fundamental'}

		results = requests.get(ameritrade_instruments_url, params=payload)
		data = results.json()
		result_df = pd.DataFrame.from_dict(data)

		# transpose data so one row per ticker
		tickers_as_rows = result_df.T
		# transform 'fundamental' json metrics into columns
		twocols = tickers_as_rows[["fundamental", 'symbol']]
		fundamentals = pd.json_normalize(twocols.fundamental)
		# store all dfs in single list
		frames.append(fundamentals)

		start = end
		end += 500 # max tickers ameritrade allows per API call

	fundamentals_df = pd.concat(frames)
	fundamentals_df = fundamentals_df.set_index('symbol')
	return fundamentals_df

# get descriptions for stock symbols: input symbols df, output descriptions df
def get_descriptions(tickers):
	start = 0
	end = 500
	frames = []

	# call api for each group of 500 tickers
	while start < len(tickers):  
		tickers_short_list = tickers[start:end]

		payload = {'apikey': ameritrade_api_key,
				'symbol': tickers_short_list,
				'projection': 'symbol-search'}

		results = requests.get(ameritrade_instruments_url, params=payload)
		data = results.json()
		result_df = pd.DataFrame.from_dict(data)

		df_descriptions = result_df.T  
		df_descriptions = df_descriptions.set_index('symbol')

		# store all dfs in single list
		frames.append(df_descriptions)

		start = end
		end += 500 # max tickers ameritrade allows per API call
		
	df_descriptions = pd.concat(frames)
	return df_descriptions

def get_options_vol(symbols):
	df = pd.DataFrame(columns=['symbol', 'put_vol'])
	count = 0
	
	for symbol in symbols:
		payload = {
			'apikey': ameritrade_api_key,
			'symbol': symbol,
			'contractType': 'PUT',
			'strikeCount': 1,
			'range': 'SNK',
			'fromDate': '2023-05-01',
			'toDate': '2023-08-01'
		}
		results = requests.get(ameritrade_option_chains_url, params=payload)
		data = results.json()

		try:
			put_map = data['putExpDateMap']
			put_date = put_map[next(iter(put_map))]
			put_info = put_date[next(iter(put_date))]
			put_vol = put_info[0]['volatility']
			print(put_vol)
		except:
			put_vol = 000

		df.loc[len(df.index)] = [symbol, put_vol]
		count += 1
		print(count)
		
	df = df.set_index('symbol')
	return df

# fundamentals_df = get_fundamentals(us_symbols_list)
# fundamentals_df.to_excel('fundamentals_11-4-2022.xlsx')

# descriptions_df = get_descriptions(us_symbols_list)
# descriptions_df.to_excel('descriptions_11-4-2022.xlsx')

# options_vol_df = get_options_vol(us_symbols_list)
# options_vol_df.to_excel('options_11-4-2022.xlsx')