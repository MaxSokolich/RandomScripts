
"""
you will probabily need to install the yfinance module and the pandas module
    just type in the command prompt: "pip3 install yfinance"
    once that is complete type: "pip3 install pandas"


once the yfinance module and the pandas module is installed: run the code by doing the following:

    In the python IDLE, on the top left of screen click run, and then run module

    A new window will appear and a line will be printed: " Type Ticker Symbol Here"

    type in the ticker in all caps and press enter
"""



import yfinance as yf
import pandas as pd



q1 = input('Type Ticker Symbol Here:')

stock = yf.Ticker(q1)

#print(stock.info)
for key, value in stock.info.items():
    print(key, ' : ', value)

pd.options.display.width=None
print('FINANCIALS\n\n',stock.financials) # get all basic financial values i.e. net income, total revenue
print('BALANCE SHEET\n\n',stock.quarterly_balance_sheet) #gets more financial values
print('CASHFLOW\n\n',stock.cashflow)
print('EARNINGS\n\n',stock.earnings)#or quarterly
print('SUSTAINABILITY\n\n',stock.sustainability)
print('RECOMMENDATIONS\n\n',stock.recommendations)
