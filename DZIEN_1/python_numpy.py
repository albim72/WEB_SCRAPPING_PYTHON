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

#statystyki
print(f"_"*70)
z = np.array([12,87,90,2,0,24,-23,-45,16,78,92,3,3,121,-324,563,2])
print(f"tablica z: {z}:.3f")
print(f"średnia: {np.mean(z):.3f}")
print(f"odchylenie standardowe: {np.std(z):.3f}")
print(f"wariancja: {np.var(z):.3f}")
print(f"max: {np.max(z)}")
print(f"min: {np.min(z)}")

#operacje na macierzach
M = np.array([[1,2,3],[4,5,6],[7,8,9]])

print(f"Transpozycja: {M.T}")
print(f"Determinanta: {np.linalg.det(M)}")
print(f"iloczyn macierzy: {np.dot(M,M)}")
