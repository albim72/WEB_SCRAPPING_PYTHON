import numpy as np

a = np.array([1, 2, 3])
print(f"tablica np: {a}")
print(f"typ tablicy: {type(a)}")
print(f"rozmiar tablicy: {a.size}")
print(f"rozmiar pierwszego elementu: {a.itemsize}")
print(f"typ elementu: {a.dtype}")

print("_"*60)

b = np.arange(0,10,2)
print(f"arange: {b}")

c = np.linspace(0,1,5)
print(f"linspace: {c}")

#operacje wektorowe (zamiast pętli)
x = np.array([1,2,3])
y = np.array([11,21,31])
print(x+y)
print(x-y)
print(x*y)
print(x/y)
print(y//x)

a = np.array([[1,2,3],[4,5,6]])
b = np.array([[11,21,31],[41,51,61]])
c = np.array([[111,211,311],[411,511,611]])
print(a)
print(a+b+c)
