import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from pandas.plotting import scatter_matrix
from pandas import Series, DataFrame
import pandas_datareader.data as web
from pandas.plotting import scatter_matrix
from datetime import datetime
from datetime import timedelta
import numpy as np
import math as math
from sklearn import preprocessing
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import yfinance as yf


style.use('ggplot')
now= datetime.now()
today = now.strftime('%Y-%m-%d')
start_date = '2011-11-10'
end_date  = today



#--------STOCK CURRENTLY TRYING TO PREDICT-------
s1 = 'NIO'
stock = yf.Ticker(s1)
q1 = input('stock statements?')
if q1 == 'yes':
    print(stock.info)
    print('FINANCIALS\n\n',stock.financials) # get all basic financial values i.e. net income, total revenue
    print('BALANCE SHEET\n\n',stock.quarterly_balance_sheet) #gets more financial values
    print('CASHFLOW\n\n',stock.cashflow)
    print('EARNINGS\n\n',stock.earnings)#or quarterly
    print('SUSTAINABILITY\n\n',stock.sustainability)
    print('RECOMMENDATIONS\n\n',stock.recommendations)
else:
    print('ight')





#scrape yahoo
data1 = web.DataReader(s1 ,'yahoo',start_date, end_date)
dfreg = data1.loc[:,['Adj Close','Volume']]
dfreg['HL_PCT'] = (data1['High'] - data1['Low']) / data1['Close'] * 100.0
dfreg['PCT_change'] = (data1['Close'] - data1['Open']) / data1['Open'] * 100.0

q2 = input('HL PCT?')
if q2 == 'yes':
    print(dfreg)
else:
    print('ight')

#HL_PCT === high low precentage

dfreg.fillna(value=-99999, inplace=True)
forecast_out = int(math.ceil(0.01 * len(dfreg)))
forecast_col = 'Adj Close' #predict the AdjClose
dfreg['label'] = dfreg[forecast_col].shift(-forecast_out)
X = np.array(dfreg.drop(['label'], 1))
# Scale the X so that everyone can have the same distribution for linear regression
X = preprocessing.scale(X)
# Finally We want to find Data Series of late X and early X (train) for model generation and evaluation
X_lately = X[-forecast_out:]
X = X[:-forecast_out]
# Separate label and identify it as y
y = np.array(dfreg['label'])
y = y[:-forecast_out]


#-----BEGIN TRAINING MODEL USING SKIKIT LEARN-----
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Linear regression
clfreg = LinearRegression(n_jobs=-1)
clfreg.fit(X_train, y_train)
# Quadratic Regression 2
clfpoly2 = make_pipeline(PolynomialFeatures(2), Ridge())
clfpoly2.fit(X_train, y_train)

# Quadratic Regression 3
clfpoly3 = make_pipeline(PolynomialFeatures(3), Ridge())
clfpoly3.fit(X_train, y_train)

# K Nearest Neighbor
# KNN Regression
clfknn = KNeighborsRegressor(n_neighbors=2)
clfknn.fit(X_train, y_train)

#finds mean accuracy of self.predict(X) with y of the data set
confidencereg = clfreg.score(X_test, y_test)
confidencepoly2 = clfpoly2.score(X_test,y_test)
confidencepoly3 = clfpoly3.score(X_test,y_test)
confidenceknn = clfknn.score(X_test, y_test)

print('The linear regression confidence is \n\n', confidencereg)
print('The quadratic regression 2 confidence is \n\n', confidencepoly2)
print('The quadratic regression 3 confidence is \n\n', confidencepoly3)
print('The knn regression confidence is \n\n',confidenceknn)


#-------FORCASTING-------

forecast_set = clfreg.predict(X_lately)
dfreg['Forecast'] = np.nan

print('FORCAST\n\n',forecast_set)

last_date = dfreg.iloc[-1].name
last_unix = last_date
next_unix = last_unix + timedelta(days=1)

for i in forecast_set:
    next_date = next_unix
    next_unix += timedelta(days=3)
    dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns)-1)]+[i]
dfreg['Adj Close'].tail(500).plot()
dfreg['Forecast'].tail(500).plot()
plt.legend(loc='upper left')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

