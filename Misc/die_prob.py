#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 18:32:21 2021

@author: bizzaro
"""
import matplotlib.pyplot as plt
import random as random
import numpy as np

p1_wins = 0
p2_wins = 0


#could keep going add another while loop here for continued games

p1_data = []
p2_data = []


while True:

    print("----------Player 1 Throw-------------")
    
    p1_die1 = input("Player 1 die 1?  ")#random.randint(1,6)
    p1_die2 = input("Player 1 die 2?  ")
    print("\n\n")
    
    p1_roll = [int(p1_die1),int(p1_die2)]
    p1_data.append(p1_roll)
    
    print("----------Player 2 Throw:------------")
    
    p2_die1 = input("Player 2 die 1?  ")
    p2_die2 = input("Player 2 die 2?  ")
    
    p2_roll = [int(p2_die1),int(p2_die2)]
    
    
    p2_data.append(p2_roll)
    status = input("Gameover?")
    print(status)
    
    if status == 'y':
        winner = input("who won? (p1 or p2)")
        if winner == 'p1':
            p1_wins +=1
        else:
            p2_wins +=1
        break
    
    
print("player 1 wins = " , p1_wins)





print("player 2 wins = " , p2_wins)
    


###########  PLAYER ONE ANALYSIS  ###############
#doubles

num_doubles1 = 0 
for i in range(len(p1_data)):
    if p1_data[i][0] == p1_data[i][1]:
        num_doubles1 +=1
        
    

# extend out rolls
turn_player_1 = []
total_rolls_player_1 = []

for i in range(len(p1_data)):
    turn_player_1.append(i)
    turn_player_1.append(i)
       
    
    total_rolls_player_1.append(p1_data[i][0])
    total_rolls_player_1.append(p1_data[i][1])


#create bar chart
    


one1 = 0
two1 = 0
three1 = 0
four1 = 0
five1 = 0
six1 = 0
for i in total_rolls_player_1:
    if i == 1:
        one1 +=1
    if i == 2:
        two1+=1
    if i == 3:
        three1 +=1
    if i == 4:
        four1 +=1
    if i == 5:
        five1 +=1
    if i == 6:
        six1 +=1
        
num_rolled1 = [one1,two1,three1, four1, five1, six1]









  
###########  PLAYER TWO ANALYSIS  ###############

#doubles

num_doubles2 = 0 
for i in range(len(p2_data)):
    if p2_data[i][0] == p2_data[i][1]:
        num_doubles2 +=1
        
        
        
        
# extend out rolls
turn_player_2 = []
total_rolls_player_2 = []

for i in range(len(p2_data)):
    turn_player_2.append(i)
    turn_player_2.append(i)
       
    
    total_rolls_player_2.append(p2_data[i][0])
    total_rolls_player_2.append(p2_data[i][1])


#create bar chart
    


one2 = 0
two2 = 0
three2 = 0
four2 = 0
five2 = 0
six2 = 0
for i in total_rolls_player_2:
    if i == 1:
        one2 +=1
    if i == 2:
        two2+=1
    if i == 3:
        three2 +=1
    if i == 4:
        four2 +=1
    if i == 5:
        five2 +=1
    if i == 6:
        six2 +=1
        
num_rolled2 = [one2,two2,three2, four2, five2, six2]
  

#plot
die= [1,2,3,4,5,6]


x = np.arange(1,7)
width = 0.35

#fig1 = plt.figure(figsize = (10,10))
fig1, ax1 = plt.subplots()



ax1.bar(x-width/2, num_rolled1, width, label = "Player 1")
ax1.bar(x+width/2, num_rolled2, width, label = "Player 2")
ax1.set_xticks(die)
ax1.legend()
plt.show()

print("Player 1 Number of Doubles = ",num_doubles1)
print("Player 2 Number of Doubles = ",num_doubles2)

#

 
