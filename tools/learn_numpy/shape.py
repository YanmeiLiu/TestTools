import numpy as np

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
print(a)
print(a.shape)
# 拍扁变一维b,flatten不会影响原来的数据，ravel会影响原来的数据
b = a.flatten()
b[0] = 99
print(a)
print(b)
print(b.ndim)
c = a.ravel()
c[0] = 99
print(a)
print(c)
print(c.ndim)
print('#' * 60)
# transpose 多维转，swapaxes 两维转
a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
b = a.transpose()
c = a.T
print(a)
print(b)
print(c)
a = np.array([[1, 2], [3, 4], [5, 6]])
print(np.swapaxes(a, 0, 1))
