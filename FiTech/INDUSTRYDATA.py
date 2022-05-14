from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import *
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from pandas import Series, DataFrame
from pandas.plotting import scatter_matrix
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas_datareader.data as web
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from datetime import datetime
import yfinance as yf
from yahoofinancials import YahooFinancials




style.use('ggplot')
#updates todays date autmoatically
now = datetime.now()
today = now.strftime('%Y-%m-%d')

#ibiotech
s1 = 'ctxr'
s2 = 'ntrp'
s3 = 'snna'
s4 = 'cnat'
s5 = 'gnpx'
s6 = 'cocp'

#semiconductor
s7 = 'iots'
s8 = 'atom'
s9 = 'quik'
s10 = 'fsi'
s11 = 'mosy'
s12 = 'intt'

#oil
s13 = 'swn'
s14 = 'cdev'
s15 = 'chk'
s16 = 'cpe'
s17 = 'do'
s18 = 'eca'

#gold

s19 = 'aug'
s20 = 'chnr'
s21 = 'gsv'
s22 = 'mux'
s23 = 'usau'
s24 = 'tmq'



#my stocks

s25 = 'cetv'
s26 = 'gsat'
s27 = 'wisa'
s28 = 'umc' 
s29 = 'axas'
s30 = 'jasn'

#internet
s31 = 'idex'
s32 = 'ftr'
s33 = 'wtrh'
s34 = 'renn'
s35 = 'ent'
s36 = 'taop'

#next_stock


start_date = '2019-10-10'
end_date  = today

#price to earnings ratios
'''
stock = YahooFinancials(['cetv','bdr','gsat','wisa','umc','rvp','axas','jasn'])
print(stock.get_pe_ratio())
'''



#biotech shit
q1 = input('biotech charts?')
if q1 == 'yes':
    print('biotech shit')

    d1 = web.DataReader(s1 ,'yahoo',start_date, end_date)
    d2 = web.DataReader(s2 ,'yahoo',start_date, end_date)
    d3 = web.DataReader(s3 ,'yahoo',start_date, end_date)
    d4 = web.DataReader(s4 ,'yahoo',start_date, end_date)
    d5 = web.DataReader(s5 ,'yahoo',start_date, end_date)
    d6 = web.DataReader(s6 ,'yahoo',start_date, end_date)

    fig2, ax = plt.subplots()
    ax.plot(d1['Adj Close'],color = 'yellow',label = s1)
    ax.plot(d2['Adj Close'],color = 'blue',label = s2)
    ax.plot(d3['Adj Close'],color = 'red',label = s3)
    ax.plot(d4['Adj Close'],color = 'black',label = s4)
    ax.plot(d5['Adj Close'],color = 'pink',label = s5)
    ax.plot(d6['Adj Close'],color = 'green',label = s6)
    ax.set_title('biotech stocks')
    legend = ax.legend(loc='upper left')
else:
    print('ight')


#semi conductor shit
q2 = input('semiconductor charts?')
if q2 == 'yes':
    print('semiconductor shit')

    d7 = web.DataReader(s7 ,'yahoo',start_date, end_date)
    d8 = web.DataReader(s8 ,'yahoo',start_date, end_date)
    d9 = web.DataReader(s9 ,'yahoo',start_date, end_date)
    d10 = web.DataReader(s10 ,'yahoo',start_date, end_date)
    d11 = web.DataReader(s11 ,'yahoo',start_date, end_date)
    d12 = web.DataReader(s12 ,'yahoo',start_date, end_date)

    fig3, ax3 = plt.subplots()
    ax3.plot(d7['Adj Close'],color = 'red',label = s7)
    ax3.plot(d8['Adj Close'],color = 'blue',label = s8)
    ax3.plot(d9['Adj Close'],color = 'green',label = s9)
    ax3.plot(d10['Adj Close'],color = 'yellow',label = s10)
    ax3.plot(d11['Adj Close'],color = 'black',label = s11)
    ax3.plot(d12['Adj Close'],color = 'pink',label = s12)

    ax3.set_title('semiconductor stocks')
    legend = ax3.legend(loc='upper left')
else:
    print('ight')


#oil shit
q3 = input('oil charts?')
if q3 == 'yes':
    print('oil shit')

    d13 = web.DataReader(s13 ,'yahoo',start_date, end_date)
    d14 = web.DataReader(s14 ,'yahoo',start_date, end_date)
    d15 = web.DataReader(s15 ,'yahoo',start_date, end_date)
    d16 = web.DataReader(s16 ,'yahoo',start_date, end_date)
    d17 = web.DataReader(s17 ,'yahoo',start_date, end_date)
    d18 = web.DataReader(s18 ,'yahoo',start_date, end_date)

    fig3, ax3 = plt.subplots()
    ax3.plot(d13['Adj Close'],color = 'red',label = s13)
    ax3.plot(d14['Adj Close'],color = 'blue',label = s14)
    ax3.plot(d15['Adj Close'],color = 'green',label = s15)
    ax3.plot(d16['Adj Close'],color = 'yellow',label = s16)
    ax3.plot(d17['Adj Close'],color = 'black',label = s17)
    ax3.plot(d18['Adj Close'],color = 'pink',label = s18)

    ax3.set_title('oil stocks')
    legend = ax3.legend(loc='upper left')
else:
    print('ight')

#gold shit
q4 = input('gold charts?')
if q4 == 'yes':
    
    print('gold shit')

    d19 = web.DataReader(s19 ,'yahoo',start_date, end_date)
    d20 = web.DataReader(s20 ,'yahoo',start_date, end_date)
    d21 = web.DataReader(s21 ,'yahoo',start_date, end_date)
    d22 = web.DataReader(s22 ,'yahoo',start_date, end_date)
    d23 = web.DataReader(s23 ,'yahoo',start_date, end_date)
    d24 = web.DataReader(s24 ,'yahoo',start_date, end_date)

    fig4, ax4 = plt.subplots()
    ax4.plot(d19['Adj Close'],color = 'red',label = s19)
    ax4.plot(d20['Adj Close'],color = 'blue',label = s20)
    ax4.plot(d21['Adj Close'],color = 'green',label = s21)
    ax4.plot(d22['Adj Close'],color = 'yellow',label = s22)
    ax4.plot(d23['Adj Close'],color = 'black',label = s23)
    ax4.plot(d24['Adj Close'],color = 'pink',label = s24)

    ax4.set_title('gold stocks')
    legend = ax4.legend(loc='upper left')

else:
    print('ight')

#my stocks
q4 = input('my charts?')
if q4 == 'yes':
    print('my shit')
    d25 = web.DataReader(s25 ,'yahoo',start_date, end_date)
    d26 = web.DataReader(s26 ,'yahoo',start_date, end_date)
    d27 = web.DataReader(s27 ,'yahoo',start_date, end_date)
    d28 = web.DataReader(s28 ,'yahoo',start_date, end_date)
    d29 = web.DataReader(s29 ,'yahoo',start_date, end_date)
    d30 = web.DataReader(s30 ,'yahoo',start_date, end_date)

    fig5, ax5 = plt.subplots()
    ax5.plot(d25['Adj Close'],color = 'red',label = s25)
    ax5.plot(d26['Adj Close'],color = 'blue',label = s26)
    ax5.plot(d27['Adj Close'],color = 'green',label = s27)
    ax5.plot(d28['Adj Close'],color = 'yellow',label = s28)
    ax5.plot(d29['Adj Close'],color = 'black',label = s29)
    ax5.plot(d30['Adj Close'],color = 'pink',label = s30)

    ax5.set_title('my stocks')
    legend = ax5.legend(loc='upper left')
    
else:
    print('ight')

#internet
q5 = input('internet charts?')
if q5 == 'yes':
    print('internet shit')
    d31 = web.DataReader(s31 ,'yahoo',start_date, end_date)
    d32 = web.DataReader(s32 ,'yahoo',start_date, end_date)
    d33 = web.DataReader(s33 ,'yahoo',start_date, end_date)
    d34 = web.DataReader(s34 ,'yahoo',start_date, end_date)
    d35 = web.DataReader(s35 ,'yahoo',start_date, end_date)
    d36 = web.DataReader(s36 ,'yahoo',start_date, end_date)

    fig6, ax6 = plt.subplots()
    ax6.plot(d31['Adj Close'],color = 'red',label = s31)
    ax6.plot(d32['Adj Close'],color = 'blue',label = s32)
    ax6.plot(d33['Adj Close'],color = 'green',label = s33)
    ax6.plot(d34['Adj Close'],color = 'yellow',label = s34)
    ax6.plot(d35['Adj Close'],color = 'black',label = s35)
    ax6.plot(d36['Adj Close'],color = 'pink',label = s36)

    ax6.set_title('internet')
    legend = ax6.legend(loc='upper left')
    
else:
    print('ight')
plt.show()
