#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 14:08:58 2022

@author: bizzarohd
"""
import numpy as np

def Four_Digit_Sudoku_Combinations(DIGIT):
    combinations = []
    filtered_combinations = []
    for a in range(1,7):
        for b in range(1,7):
            for c in range(1,7):
                for d in range(1,7):
                    print(a+b+c+d)
                    if a+b+c+d == DIGIT and c!=a!=b!=c!=d!=b and a!=d:
                        test = list(np.sort([a,b,c,d]))    # add the new combination the list
                        combinations.append(test)
          
    for i in combinations:
        #If the combination does not appear in the filtered combination list; append that combination
        #otherwise do not append it
        if not i in filtered_combinations:
            filtered_combinations.append(i)
    
    print(filtered_combinations)  
    print("Count = ",len(filtered_combinations))
    
    
quad = int(input("4 SUM: "))
Four_Digit_Sudoku_Combinations(quad)