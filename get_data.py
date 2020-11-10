from pandas_datareader import data as pdr
import yfinance as yf

def get_data(stock_code, date_from, date_to, ver='v1'):
    yf.pdr_override()
    date_from = "{}-{}-{}".format(date_from[:4], date_from[4:6], date_from[6:])
    date_to = "{}-{}-{}".format(date_to[:4], date_to[4:6], date_to[6:])
    data = pdr.get_data_yahoo(stock_code, start=date_from, end=date_to)
    del data['Adj Close']
    data.to_csv('./data/v1/{}.csv'.format(stock_code, header=None), mode='w')
