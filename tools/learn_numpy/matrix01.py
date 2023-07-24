import numpy as np

a = np.arange(1, 5).reshape(2, 2)
b = np.array([[10, 20], [30, 40]])
print(a)
print(b)
print(a + b)
print(a*b)
print(a.dot(b)) # 点乘法，矩阵乘法
print('$'*100)
a = np.matrix("1 2;3 4")
b = np.matrix("10 20;30 40")
print(a)
print(b)
print(a * b)


