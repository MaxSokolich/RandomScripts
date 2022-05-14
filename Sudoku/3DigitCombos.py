#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:06:15 2022

@author: bizzarohd
"""
import numpy as np


def Three_Digit_Sudoku_Combinations(DIGIT):
    combinations = []
    filtered_combinations = []
    for a in range(1,10):
        for b in range(1,10):
            for c in range(1,10):
                if a+b+c == DIGIT and a != b !=c !=a:
                    test = list(np.sort([a,b,c]))    # add the new combination the list
                    combinations.append(test)
    
    for i in combinations:
        #If the combination does not appear in the filtered combination list; append that combination
        #otherwise do not append it
        if not i in filtered_combinations:
            filtered_combinations.append(i)
    
    print(filtered_combinations)  
    print("Count = ",len(filtered_combinations))


tre = int(input("3 SUM: "))
Three_Digit_Sudoku_Combinations(tre)

