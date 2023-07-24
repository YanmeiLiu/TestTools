#比较List和numpyarray的性能
import numpy as np
import time

size_of_ven = 100000000


def pure_python():
    t1 = time.time()
    x = range(size_of_ven)
    y = range(size_of_ven)
    z = []

    for i in range(len(x)):
        z.append(x[i] + y[i])
    return time.time() - t1


def numpy_version():
    t1 = time.time()
    x = np.arange(size_of_ven)
    y = np.arange(size_of_ven)
    z = x + y
    print(z)
    return time.time() - t1


ts2 = numpy_version()
ts1 = pure_python()
print('ts1:', ts1)
print('ts2:', ts2)

print('Numpy is ', str(ts1 / ts2), ' faster')
