Vf = 141
Vb = int(input("Beginning Market Size"))
t = int(input("time"))

CAGR = ((Vf/Vb)**(1/t))-1
print(CAGR, "%")
