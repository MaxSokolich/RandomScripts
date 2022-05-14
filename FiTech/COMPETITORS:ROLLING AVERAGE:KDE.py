from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from pandas.plotting import scatter_matrix
from pandas import Series, DataFrame
import pandas_datareader.data as web
from pandas.plotting import scatter_matrix


style.use('ggplot')
now= datetime.now()
today = now.strftime('%Y-%m-%d')
start_date = '2018-10-10'
end_date  = today


#INDUSTRY CURRENTLY LOOKING AT
#my stocks
s1 = 'umc'
s2 = 'cetv'
s3 = 'rvp'
s4 = 'gsat'
s5 = 'aapl'
s6 = 'spy'

data1 = web.DataReader(s1 ,'yahoo',start_date, end_date)
data2 = web.DataReader(s2 ,'yahoo',start_date, end_date)
data3 = web.DataReader(s3 ,'yahoo',start_date, end_date)
data4 = web.DataReader(s4 ,'yahoo',start_date, end_date)
data5 = web.DataReader(s5 ,'yahoo',start_date, end_date)
data6 = web.DataReader(s6 ,'yahoo',start_date, end_date)


#rolling mean analysis - smooths out price data by creating a
#constantly updated average price. cut down on noise in price chart
close1 = data1['Adj Close']
close2 = data2['Adj Close']
close3 = data3['Adj Close']
close4 = data4['Adj Close']
close5 = data5['Adj Close']
close6 = data6['Adj Close']
mavg1 = close1.rolling(window=60).mean()
mavg2 = close2.rolling(window=60).mean()
mavg3 = close3.rolling(window=60).mean()
mavg4 = close4.rolling(window=60).mean()
mavg5 = close5.rolling(window=60).mean()
mavg6 = close6.rolling(window=60).mean()

plt.subplot(6, 2, 1)
close1.plot(label = s1)
mavg1.plot(label = 'MAVG')
plt.legend()
plt.subplot(6, 2, 3)
close2.plot(label = s2)
mavg2.plot(label = 'MAVG')
plt.legend()
plt.subplot(6, 2, 5)
close3.plot(label = s3)
mavg3.plot(label = 'MAVG')
plt.legend()
plt.subplot(6, 2, 7)
close4.plot(label = s4)
mavg4.plot(label = 'MAVG')
plt.legend()
plt.subplot(6, 2, 9)
close5.plot(label = s5)
mavg5.plot(label = 'MAVG')
plt.legend()
plt.subplot(6, 2, 11)
close6.plot(label = s6)
mavg6.plot(label = 'MAVG')
plt.legend()

#return deviation = determine risk and return
#mulitply eight of each asset by its expected return and adding the values for each investment
plt.subplot(6, 2, 2)
returns1 = close1/close1.shift(1)-1
returns1.plot(label='return') # want high and stable
plt.legend()
plt.subplot(6, 2, 4)
returns2 = close2/close2.shift(1)-1
returns2.plot(label='return') # want high and stable
plt.legend()
plt.subplot(6, 2, 6)
returns3 = close3/close3.shift(1)-1
returns3.plot(label='return') # want high and stable
plt.legend()
plt.subplot(6, 2, 8)
returns4 = close4/close4.shift(1)-1
returns4.plot(label='return') # want high and stable
plt.legend()
plt.subplot(6, 2, 10)
returns5 = close5/close5.shift(1)-1
returns5.plot(label='return') # want high and stable
plt.legend()
plt.subplot(6, 2, 12)
returns6 = close6/close6.shift(1)-1
returns6.plot(label='return') # want high and stable
plt.legend()
plt.show()





