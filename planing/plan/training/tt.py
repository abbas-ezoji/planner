import math

life_cycle = 5
data = []
for i in range(1,1000):
    data.append(life_cycle*(1- math.exp(-1/i))+1)