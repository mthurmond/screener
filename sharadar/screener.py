import pandas as pd
from dotenv import load_dotenv
load_dotenv()

pd.options.display.float_format = '{:,}'.format

# get fundamentals
fund = pd.read_pickle('fundamentals.pkl')
fin_pivot = fund.pivot(columns=["year"],values=["revenueusd", "opincusd", "netinccmnusd"])

# add company info
info = pd.read_pickle('company_info.pkl')
fund_and_info = fin_pivot.merge(info, how='left', on='ticker')

# add market caps
daily = pd.read_pickle('daily.pkl')
merged = fund_and_info.merge(daily, how='left', on='ticker')

# add valuation metrics
merged['p-opinc2010'] = merged['marketcap'] / merged[('opincusd', 2010)]
merged['p-opinc2021'] = merged['marketcap'] / merged[('opincusd', 2021)]
merged['p-netinc2021'] = merged['marketcap'] / merged[('netinccmnusd', 2021)]
merged['avginc17-21'] = (
    merged[('netinccmnusd', 2017)] + 
    merged[('netinccmnusd', 2018)] +
    merged[('netinccmnusd', 2019)] + 
    merged[('netinccmnusd', 2020)] +
    merged[('netinccmnusd', 2021)]
) / 5
merged['p-5yravginc'] = merged['marketcap'] / merged['avginc17-21']
merged = merged.round(0)

# run screen
screen = merged[
    (merged['p-opinc2010'] < 10) &
    (merged['p-opinc2010'] > 0) &
    (merged['p-opinc2021'] < 8) &
    (merged['p-opinc2021'] > 0) &
    (merged['p-netinc2021'] < 10) &
    (merged['p-netinc2021'] > 0) &
    (merged['p-5yravginc'] < 10) &
    (merged['p-5yravginc'] > 0)
]
screen = screen.sort_index()
screen.to_excel('../output/financials_screen.xlsx')