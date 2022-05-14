import random

list(print(['Tie  -', 'You Win  -', 'You Lose  -'][((int(input("0 = Rock, 1 = Paper, 2 = Scissors?: "))-c)% 3)]+f'-Computer Played {["Rock","Paper","Scissors"][c]}') for c in [random.randint(0,2) for _ in range(100)])
