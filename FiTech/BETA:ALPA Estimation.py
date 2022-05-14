import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader as web
from scipy import stats
import seaborn as sns
from datetime import datetime
style.use('ggplot')

now = datetime.now()
today = now.strftime('%Y-%m-%d')

start_date = '2019-1-10'
end_date  = today


#----------BETA AND ALPHA CALULATION/ESTIMATION--------------
#water
water = ['awr','cwco','cwt','yorw','awk','msex','sbs','pcyo']
#oil
oil = ['altm','swn','cdev','chk','cpe','do','eca','mdr']
#gold
gold = ['aug','chnr','gsv','mux','usau','tmq']
#penny
penny = ['inpx', 'uec', 'ensv', 'quik', 'ntrp', 'teum', 'ctxr', 'cocp', 'dffn', 'bioc', 'umrx', 'aveo', 'hos', 'trch', 'gsv', 'usau', 'ctst', 'fgp', 'trq', 'royt', 'qhc', 'ttnp', 'phio', 'wtrh' ,'ocgn', 'ontx']
#single stock
stock = ['inpx','ibio','axas','btg']

#next stock
next_stock = ['inpx','ibio','axas','btg']
tickers = next_stock

price_data = web.get_data_yahoo(tickers,start_date,end_date)
price_data = price_data['Adj Close']
ret_data = price_data.pct_change()[1:]
port_ret = ret_data.sum(axis=1)

benchmark_price = web.get_data_yahoo('spy',start_date,end_date)
benchmark_ret = benchmark_price["Adj Close"].pct_change()[1:]
sns.regplot(benchmark_ret.values,port_ret.values)
plt.xlabel("Benchmark Returns")
plt.ylabel("Portfolio Returns")
plt.title("Portfolio Returns vs Benchmark Returns")


(beta, alpha) = stats.linregress(benchmark_ret.values,port_ret.values)[0:2]
print("The portfolio beta is", round(beta, 4))
print("The portfolio alpa is", round(alpha, 5))

plt.show()
