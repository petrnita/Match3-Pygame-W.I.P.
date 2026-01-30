import numpy as np

a = 20
arr = np.full(a, True)
rng = np.random.default_rng()
r = rng.integers(2, size=a)
print(arr)
print(r)

ls = np.linspace(0, 80, 13, retstep=True)
print(ls)

# Creating dataset
a = np.random.randint(100, size =(50))

# Creating histogram
hist, bins = np.histogram(a, bins = [0, 20, 40, 60, 80, 100]) 

# printing histogram
print(a)
print (hist) 
print (bins) 
print()

