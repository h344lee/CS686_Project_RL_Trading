from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd


def get_data(stock_code, date_from, date_to, ver='v1'):
    yf.pdr_override()
    # download dataframe

    date_from = "{}-{}-{}".format(date_from[:4], date_from[4:6], date_from[6:])
    date_to = "{}-{}-{}".format(date_to[:4], date_to[4:6], date_to[6:])

    # print(stock_code)
    # print(date_from)
    # print(date_to)
    # print(fpath)

    data = pdr.get_data_yahoo(stock_code, start=date_from, end=date_to)
    del data['Adj Close']

    for col in ['Open','High','Low','Close','Volume']:
        data[col] = data[col].astype(float)

    data.columns = ['open','high','low','close','volume']

    #print(data)
    data.to_csv('./data/v1/{}.csv'.format(stock_code, header=None), mode='w')

#get_data('MSFT', './data/v1/MSFT.csv', '20190101', '20191230')