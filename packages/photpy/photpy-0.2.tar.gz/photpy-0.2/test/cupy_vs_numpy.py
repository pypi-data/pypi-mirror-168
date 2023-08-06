from deprecated import phot
import numpy as np
import time


def cpu_func(a):
    start = time.time()
    a = np.matmul(a, a)
    end = time.time()
    print('CPU Time: {:.3f}s'.format(end - start))


def gpu_func(a):
    start = time.time()
    a = phot.to_gpu(a)
    a = np.matmul(a, a)
    a = phot.to_cpu(a)
    end = time.time()
    print('GPU Time: {:.3f}s'.format(end - start))


if __name__ == '__main__':
    size = 15000
    array = np.random.random((size, size))
    cpu_func(array)
    gpu_func(array)
