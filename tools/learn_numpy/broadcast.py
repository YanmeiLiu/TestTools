import numpy as np

# 标量计算

a = np.array([10, 20, 30, 40])
print(a)
print(a + 2)
print(a * 2)
print('#' * 30)
b = np.array([[1, 2, 3], [4, 5, 6]])
print(b + 2)
print('#' * 30)
#
a = np.array([10, 20, 30, 40])
b = np.arange(1, 5)
print(a)
print(b)
print(a + b)
print('#' * 30)
# 利用广播计算
a = np.array([[1, 2], [3, 4], [5, 6]])
b = np.array([10, 20])
print(a + b)
c = np.array([[1], [2], [3]])
d = np.array([10, 20, 30])
print(c + d)
print('#' * 30)

# 无法实现广播的例子
# a = np.array([10, 20, 30])
# b = np.arange(1, 5)
# print(a + b)
# c = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
# d = np.array([[10, 20], [20, 30]])
# print(c + d)

# resize & reshape
a = np.array([[10, 20, 30], [40, 50, 60]])
print(a.shape)
print(a)
b = a.reshape(3, 2, order='F')
#
print(b.shape)
print(b)
print('#' * 30)
# resize 用原来的值填充，灵活性比reshape大
a = np.arange(8)
b = np.resize(a, (3, 6))
print(a)
print(b)
print(b.shape)
