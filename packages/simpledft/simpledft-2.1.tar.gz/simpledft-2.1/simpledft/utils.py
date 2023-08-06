import numpy as np


def diagprod(a, B):
    '''Efficiently calculate the expression Diag(a) * B.'''
    a_col = a[:, None]
    return a_col * B


def sqrtm(A):
    '''Calculate the matrix square root of A.'''
    evals, evecs = np.linalg.eig(A)
    return evecs @ np.diag(np.sqrt(evals)) @ np.linalg.inv(evecs)


def pseudo_uniform(size, seed=1234):
    '''Lehmer random number generator, follwoing MINSTD.'''
    U = np.zeros(size, dtype=complex)
    mult = 48271
    mod = (2**31) - 1
    x = (seed * mult + 1) % mod
    for i in range(size[0]):
        for j in range(size[1]):
            x = (x * mult + 1) % mod
            U[i, j] = x / mod
    return U
