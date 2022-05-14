# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Zerodur = pd.read_excel(r"file:///C:/Users/msokolic/Desktop/Riley Project/CTE_Data_Test.xlsx", sheet_name="test1", index_col=False) 




TempULE = Zerodur['Temp [C]'].to_numpy()
LowULE = Zerodur['Low'].to_numpy()
HighULE = Zerodur['High'].to_numpy()
NominalULE = Zerodur['Nominal'].to_numpy()


       
        
    
fig, ax = plt.subplots(facecolor = "#A0F0CC")


                       
                       
ax.plot(TempULE,NominalULE, color = 'r',label = 'NominalULE')
ax.plot(TempULE, LowULE, color = 'b',label = 'LowULE')
ax.plot(TempULE, HighULE, color = 'g', label = 'HighULE')
plt.xlabel("Temp [C]")
plt.ylabel("CTE [ppb/C]")
ax.set_xlim(0)
ax.set_ylim(0)
plt.legend()
plt.show()


