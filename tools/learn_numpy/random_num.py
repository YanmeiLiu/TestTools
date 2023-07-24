import numpy as np

x = np.random.randint(0, 10, 5)
y = np.random.randint(0, 10, 5)
print(x)
print(y)

x_avg = x.mean()
print(x_avg)
# 方差
print(x.var())
# 标准差
print(x.std())
# 协方差
print(np.cov(x, y))
