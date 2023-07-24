import numpy as np

arr1 = np.array([[2, 4], [6, 8]])
arr2 = np.array([[3, 5], [7, 9]])
print(np.concatenate((arr1, arr2), axis=0))
print('@' * 50)
print(np.concatenate((arr1, arr2), axis=1))
print('@' * 50)
print(np.concatenate((arr1, arr2), axis=None))  # 拍扁成一维
print('-' * 50)
in_arr1 = np.array([1, 2, 3])
in_arr2 = np.array([4, 5, 6])
print(np.vstack((in_arr1, in_arr2)))
print('-' * 50)
print(np.hstack((in_arr1, in_arr2)))
print('-' * 50)

a = np.arange(9).reshape(3,3)
print(a)
print('-' * 50)
#

