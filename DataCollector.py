#coding:utf-8
import tushare as ts
import pandas as pd
import datetime
from datetime import date
import os
import threading
import time

class DataCollector:
	def __init__(self):
		df = ts.get_stock_basics()
		download_lock = threading.Lock()

		stock_info = pd.read_csv('stock_info.csv')
		self.stock_industry_dict = dict()
		num_stock = len(stock_info)
		print num_stock
		for i in range(0,num_stock):
			download_lock.acquire()
			print("now thread lock")
			stock_dict = dict()
			industry = stock_info['industry'][i]
	#if not industry
			totals = stock_info['totals'][i]
			outstanding = stock_info['outstanding'][i]
			code = int(stock_info['code'][i])
			print("stock code is:")
			print code
			if code <= 10000:
				download_lock.release()
				continue
				print("code less than 10000, now release")
			if not os.path.isfile("TradeData/"+str(code)+".csv"):
				print code
				date_to_market = df.ix[str(code)]['timeToMarket'] #上市日期YYYYMMDD
				date_to_market_string = str(date_to_market)
				date_to_market_slash = date_to_market_string[0:4]+"-"+date_to_market_string[4:6]+"-"+date_to_market_string[6:8]
				print("time to market:")
				print type(date_to_market_slash)
				print date_to_market_slash
				data_of_this_stock = ts.get_h_data(str(code),index=True,start="2003-01-01",end="2017-11-13")
				data_of_this_stock.to_csv("TradeData/"+str(code)+'.csv',encoding='utf-8')

				#不复权数据
				data_of_this_stock_bfq = ts.get_hist_data(str(code),start="2003-01-01",end="2017-11-13")
				data_of_this_stock_bfq.to_csv("TradeData/"+str(code)+'bfq.csv',encoding='utf-8')
				time.sleep(60)
			download_lock.release()
			print("download completed, now release")










if __name__ == "__main__":
    DC = DataCollector()