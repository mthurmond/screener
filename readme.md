# Fundamentals-based stock screener

This screener pulls data on over 6,000 companies listed on the NYSE and NASDAQ. It reviews financial, valuation, and ROIC information for over 30 years, and then applies screening criteria to output a value, quality, and short list of companies that are exported to excel.

## APIs

The ameritrade API key is free. You will need to purchase the other two. The primary paid API is "shardar", purchased via nasdaq data link, for historic financials. I also used the "polygon" API for company descriptions and options data. 