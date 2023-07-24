import numpy as np
import time
import sys

# list1 = [1, 2, 3, 4, 5]
# arr = np.array(list1)
# print(arr)
# print(arr.dtype)
# print(type(arr))
# print(list(arr))
# 0D scalars
arr = np.array(43)
print(arr)
# 1D
arra = np.array([1, 2, 3])

print(arra)

# 2D
arr2 = np.array([[1, 2, 3], [2, 3, 4]])

print(arr2)
# 3D
arr3 = np.array([[[1, 2, 3], [4, 5, 6]], [[11, 22, 33], [44, 55, 66]]])
print(arr3.ndim)

# nD
arr4 = np.array([1.1, 2, 3, 4, 5], ndmin=5, dtype=np.int0)
print(arr4)

arr5 = np.arange(1, 8, 3)
print(arr5)
arr6 = np.arange(7, 0, -3)

print(arr6)
print(np.arange(start=1, stop=10.1, step=3))
print(np.arange(1, 10))
print(np.arange(3))
print(np.arange(-5, -1))
print(np.arange(-8, -18, -9))
# slicing
print(type(np.arange(1, 8, 3)))
print(np.arange(1, 80, 3)[::-1])
# 空数组
print(np.arange(2, 2))
# 数据类型
x = np.arange(5, dtype=np.float32)
print(x, type(x))
print(x.dtype)
print(x.itemsize)

# ---------------------
x = np.arange(5)
print(x)
print(2 ** x)
y = np.arange(-1, 1.1, 0.5)
print(y)
print(np.abs(y))
print(np.sin(y))
# arrange vs np.arange 性能对比
# import timeit
#
# n = 1
# print(timeit.timeit(f'x=[x**2 for x in range({n})]'))
# print(timeit.timeit(f'x = np.arange({n})**2', setup='import numpy as np'))

# zeros
help(np.zeros)
print(np.zeros(5))
print(np.zeros(5, dtype=np.int0))
print('#' * 20)
print(np.zeros((2, 3)))
print('#' * 20)
print(np.zeros([2, 3]))
print('#' * 50)

# one
print(np.ones(2))
print(np.ones((2, 3), dtype=int))
print('#' * 50)

# empty
print(np.empty(2))
print(np.empty((2, 3)))

# eye
print(np.eye(4))
print(np.eye(4, 5, k=2))
print('#' * 50)

# linspace 头尾中间等分切割n份
print(np.linspace(2.0, 3.0, num=5))
print(np.linspace(1, 100, num=16, retstep=True))

from matplotlib import pylab as p
# xa = np.linspace(0,2,10)
# y1 = np.ones(10)
# print(xa)
# print(y1)

# random
print(np.random.randn(3, 4))
print('#' * 50)

# shape
a = np.array([1, 2, 3])
a2 = np.array([[1, 3, 5, 7], [2, 4, 6, 8]])
print(a)
print('当前数组是 ' + str(a.ndim), '维')
print(a2)
print(f'当前数组是 {a2.shape}的')

# index
list1 = [1, 2, 3, 4, 5, 6]
list2 = [10, 9, 8, 7, 6, 5]
a1 = np.array(list1)
a2 = np.array(list2)
print(a1 * a2)

a = np.arange(10, 1, -2)
print(a)
print(a[np.array([3, 1, 2])])
print('---' * 10)
a = np.arange(20)
print(a)
print(a[:7])

print(a[4:])

print('---' * 10)
a = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
print(a)
print(a[2, 0:])
print(a[2, ::2])

#
print('---' * 10)
a = np.array([[1, -2, 3], [4, -2, 3]])
print(a)
print(a.shape)
print(a.ndim)
print(a[a<0])
