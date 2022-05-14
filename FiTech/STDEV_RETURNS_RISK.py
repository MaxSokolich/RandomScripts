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
#my stock
s1 = 'aapl'
s2 = 'btg'
s3 ='spy'
s4 = 'inpx'
s5 = 'ibio'
s6 = 'axas'


dfcomp = web.DataReader([s1,s2,s3,s4,s5,s6],'yahoo',start_date,end_date)['Adj Close']
returns_comparison = dfcomp.pct_change() #pandas built in % change function
correlation = returns_comparison.corr()

q0 = input('correlation chart?')
if q0 == 'yes':
    print(correlation)
else:
    print('ight')
    
q1 = input('scatter matrix?')
if q1 == 'yes':
    
    scatter_matrix(returns_comparison, diagonal='kde', figsize=(8,8));
else:
    print('ight')
q2 = input('heatmap?')
if q2 == 'yes':
    plt.figure()
    plt.imshow(correlation, cmap='hot', interpolation='none')
    plt.colorbar()
    plt.xticks(range(len(correlation)), correlation.columns)
    plt.yticks(range(len(correlation)), correlation.columns);
else:
    print('ight')

q3 = input('returns vs risk?')
if q3 == 'yes':
    plt.figure()
    plt.scatter(returns_comparison.mean(), returns_comparison.std())
    plt.xlabel('Expected returns')
    plt.ylabel('Risk')
    for label, x, y in zip(returns_comparison.columns, returns_comparison.mean(), returns_comparison.std()):
        plt.annotate(
            label, 
            xy = (x, y), xytext = (20, -20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
else:
    print('ight')
plt.show()
