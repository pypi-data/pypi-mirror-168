import numpy as np
import time
from numba import njit, prange


@njit(parallel=True)
def func(size):
    total = 0.0
    for i in prange(size):  # xrange is slower according
        for j in prange(1, size):  # to my test but more memory-friendly.
            total += (i / j)
    return total


def f4(num):
    x = np.ones(num - 1)
    y = np.arange(1, num)
    return np.sum(np.true_divide(x, y)) * np.sum(y)


if __name__ == '__main__':
    func(10)
    start = time.time()
    print(func(99999))
    print("numba time: {}".format(time.time() - start))
    start = time.time()
    print(f4(99999))
    print("numpy time: {}".format(time.time() - start))
