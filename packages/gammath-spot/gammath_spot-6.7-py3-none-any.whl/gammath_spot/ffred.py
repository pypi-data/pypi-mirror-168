import pandas as pd
import pandas_datareader.data as pdd
import datetime

try:

    fama_french_factor = 'F-F_Research_Data_5_Factors_2x3'
    fama_french_data = pdd.DataReader(fama_french_factor, 'famafrench', start='2017')[0]

    fama_french_data.to_csv('fama_french_data.csv')
except:
    print('Get FF factor data filed')

try:

    fama_french_portfolio = '17_Industry_Portfolios'
    fama_french_portfolio_data = pdd.DataReader(fama_french_portfolio, 'famafrench', start='2017')[0]
    fama_french_portfolio_data.to_csv('fama_french_portfolio_data.csv')
except:
    print('Get FF Industry portfolios failed')

start = datetime.datetime(2017, 1, 1)

try:

    gdp = pdd.DataReader('GDP', 'fred', start)
    gdp.to_csv('gdp_data.csv')
except:
    print('Get GDP data failed')

try:
    #CPI for all urban consumers
    cpi = pdd.DataReader('CPIAUCSL', 'fred', start)
    cpi.to_csv('cpi_data.csv')
except:
    print('Get CPI data failed')

try:
    #PCE excluding food and energy
    pce = pdd.DataReader('PCEPILFE', 'fred', start)
    pce.to_csv('pce_data.csv')
except:
    print('Get PCE data failed')

try:
    #University of Michigan Consumer sentiment
    consumer_sentiment_data = pdd.DataReader('UMCSENT', 'fred', start)
    consumer_sentiment_data.to_csv('consumer_sentiment_data.csv')
except:
    print('Get consumer sentiment data failed')

try:
    industrial_production_data = pdd.DataReader('IPGMFN', 'fred', start)
    industrial_production_data.to_csv('industrial_production_data.csv')
except:
    print('Get industrial production data failed')

try:
    #National financial condition
    financial_condition_data = pdd.DataReader('NFCI', 'fred', start)
    financial_condition_data.to_csv('financial_condition_data.csv')
except:
    print('Get natinoal financial condition data failed')

try:
    #National nonfinancial leverage index
    nonfinancial_leverage_data = pdd.DataReader('NFCILEVERAGE', 'fred', start)
    nonfinancial_leverage_data.to_csv('nonfinancial_leverage_data.csv')
except:
    print('Get nonfinancial leverage data failed')


try:
    # US Recession dates
    us_recession_dates = pdd.DataReader('JHDUSRGDPBR', 'fred', start)
    us_recession_dates.to_csv('us_recession_dates.csv')
except:
    print('Get US recession dates failed')

try:
    #Yield curve
    yield_curve_data = pdd.DataReader('T10Y3M', 'fred', start)
    yield_curve_data.to_csv('yield_curve_data.csv')
except:
    print('Get yield curve data failed')



