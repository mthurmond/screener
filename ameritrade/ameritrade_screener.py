import time
import string
import random
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

pd.options.display.float_format = '{:,}'.format

# create unique filename
def create_filename(prefix):
    letters = string.ascii_lowercase
    ran_string = ''.join(random.choice(letters) for i in range(3))
    current_time = time.localtime()
    short_time = time.strftime("%m_%d_%Y_%I_%M_%p", current_time)
    f_name = f'{prefix}_{short_time}_{ran_string}.xlsx'
    return f_name

# get screen data & format it; refresh excel by running queries in API files
fundamentals = pd.read_excel('fundamentals_12-1-2022.xlsx',index_col=0)

financials = pd.read_excel('./polygon/financials_11-1-2022.xlsx', index_col=0)
financials['opincome'] = financials['opincome'] / 1000000
financials['revenue'] = financials['revenue'] / 1000000
financials['opcashflow'] = financials['opcashflow'] / 1000000
financials['assets'] = financials['assets'] / 1000000
financials['current_assets'] = financials['current_assets'] / 1000000
financials['lt_assets'] = financials['assets'] - financials['current_assets']

descriptions = pd.read_excel('descriptions_11-4-2022.xlsx', index_col=0)

details = pd.read_excel('./polygon/details_11-3-2022.xlsx', index_col=0)

options = pd.read_excel('options_11-3-2022.xlsx', index_col=0)

# join dfs
screen_data_df = fundamentals.merge(financials, how='left',on='symbol').merge(descriptions, how='left',on='symbol').merge(details, how='left', on='symbol').merge(options, how='left', on='symbol')

# add columns
screen_data_df['currassets_over_mrktcap'] = screen_data_df['current_assets'] / screen_data_df['marketCap']

# format values
screen_data_df = screen_data_df.round(1)
screen_data_df = screen_data_df.set_index('symbol')

# run value screen
value_screen = screen_data_df[
    (screen_data_df['dividendAmount'] > 1) &
    (screen_data_df['peRatio'] > 3) &
    (screen_data_df['peRatio'] < 20) &
    (screen_data_df['prRatio'] < 5) &
    (screen_data_df['pegRatio'] < 1) &
    (screen_data_df['pbRatio'] < 5) &
    (screen_data_df['pcfRatio'] < 20) &
    (screen_data_df['grossMarginTTM'] > 30) &
    (screen_data_df['operatingMarginTTM'] > 15) &
    (screen_data_df['netProfitMarginTTM'] > 10) &
    (screen_data_df['returnOnEquity'] > 25) &
    (screen_data_df['returnOnAssets'] > 15) &
    (screen_data_df['totalDebtToCapital'] < 30)
]

value_output = value_screen[[
    'description_x',
    'sic_description',
    'marketCap',
    'prRatio', 
    'peRatio',
    'pbRatio', 
    'pegRatio', 
    'dividendAmount',
    'revenue',
    'opincome',
    'current_assets',
    'grossMarginTTM',
    'netProfitMarginTTM',
    'totalDebtToCapital',
    'description_y',
    'put_vol'
]]

if not value_screen.empty:
    value_output.to_excel(create_filename('./output/value'))
else:
    print("No companies returned for value screen.")

# run short screen
short_screen = screen_data_df[
    # (screen_data_df['opincome'] < 0) &
    # (screen_data_df['dividendAmount'] == 0) &
    (screen_data_df['prRatio'] > 15)
    # (screen_data_df['pegRatio'] > 1) &
    # (screen_data_df['pbRatio'] > 5) &
    # (screen_data_df['pcfRatio'] > 5) &
    # (screen_data_df['grossMarginTTM'] < 100) &
    # (screen_data_df['operatingMarginTTM'] < 90) &
    # (screen_data_df['netProfitMarginTTM'] < 90) &
    # (screen_data_df['returnOnEquity'] < 80) &
    # (screen_data_df['returnOnAssets'] < 80) &
    # (screen_data_df['totalDebtToCapital'] < 100)
]

short_output = short_screen[[
    'description_x',
    'sic_description',
    'marketCap',
    'put_vol',
    'prRatio', 
    'peRatio',
    'pbRatio', 
    'pegRatio', 
    'dividendAmount',
    'revenue',
    'opincome',
    'current_assets',
    'currassets_over_mrktcap',
    'grossMarginTTM',
    'netProfitMarginTTM',
    'totalDebtToCapital',
    'description_y'
]]

if not short_screen.empty:
    short_output.to_excel(create_filename('./output/short'))
else:
    print("No companies returned for short screen.")
