import pandas as pd
from dotenv import load_dotenv
load_dotenv()

pd.options.display.float_format = '{:,}'.format

# get fundamentals
fund = pd.read_pickle('./import/fundamentals.pkl')

# add company info
info = pd.read_pickle('./import/company_info.pkl')
fund_and_info = fund.merge(info, how='left', on='ticker')

# add market caps
daily = pd.read_pickle('./import/daily.pkl')
merged = fund_and_info.merge(daily, how='left', on='ticker')

# add valuation metrics
merged['p-opinc2010'] = merged['marketcap'] / merged[('opincusd', 2010)]
merged['p-opinc2021'] = merged['marketcap'] / merged[('opincusd', 2021)]
merged['p-netinc2021'] = merged['marketcap'] / merged[('netinccmnusd', 2021)]
merged['p-5yravginc'] = merged['marketcap'] / merged['avginc17-21']
merged['p-5yravgfcf'] = merged['marketcap'] / merged['avgfcf17-21']
merged = merged.round(0)

# value screen
screen = merged[
    (merged['p-opinc2010'] < 10) &
    (merged['p-opinc2010'] > 0) &
    (merged['p-opinc2021'] < 8) &
    (merged['p-opinc2021'] > 0) &
    (merged['p-netinc2021'] < 10) &
    (merged['p-netinc2021'] > 0) &
    (merged['p-5yravginc'] < 10) &
    (merged['p-5yravginc'] > 0) &
    (merged['p-5yravgfcf'] < 10) &
    (merged['p-5yravgfcf'] > 0) &
    (merged['intexp-ebit'] < 40)
]
screen = screen.sort_index()
screen.to_excel('./output/value_screen.xlsx')

# quality screen
quality = merged[
    (merged['p-opinc2010'] < 30) &
    (merged['p-opinc2010'] > 0) &
    (merged['p-opinc2021'] < 30) &
    (merged['p-opinc2021'] > 0) &
    (merged['p-netinc2021'] < 30) &
    (merged['p-netinc2021'] > 0) &
    (merged['p-5yravginc'] < 30) &
    (merged['p-5yravginc'] > 0) &
    (merged['p-5yravgfcf'] < 30) &
    (merged['p-5yravgfcf'] > 0) &
    (merged['intexp-ebit'] < 30) &
    (merged['avgroic17-21'] > 30)
]
quality = quality.sort_index()
quality.to_excel('./output/quality_screen.xlsx')