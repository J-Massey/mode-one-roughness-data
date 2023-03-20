#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import warnings
import numpy as np


def new_f90_res(zeta: float, lam: float, N=6):
    with open("lotus.f90","r") as fileSource:
        fileLines = fileSource.readlines()

    fileLines[19] = f"    real, parameter    :: A = 0.1*c, St_d = 0.3, k_x={1/lam}, k_z={1/lam}, h_roughness=0.01\n"
    fileLines[23] = f"                          k_coeff = {1/zeta}, &\n"
    fileLines[27] = f"    integer            :: n(3), ndims=3\n"
    fileLines[51] = f"      z = {closest_a_n(N*lam*1024/4)/1024}\n"
    fileLines[57] = f"    if(ndims==3) xg(3)%h = {delta_z(lam, N)}\n"

    with open("lotus.f90","w") as fileOutput:
        fileOutput.writelines(fileLines)


def delta_z(lam, N):
    """
    Find the appropriate grid spacing for the given wavelength and number.
    """
    z = 1024*N*lam
    closest = closest_a_n(N*lam*1024/4)
    dz = z/closest
    return dz


def closest_a_n(num):
    # Populate search space
    a_guess = np.array([2, 3, 5, 7])
    n = 2**np.arange(1, 10, 1)
    search_space = a_guess*n.reshape(n.shape[0],1)
    diff = (search_space - num)
    diff[diff>0] = -np.inf
    idx = np.unravel_index(np.argmax(diff, axis=None), diff.shape)
    return a_guess[idx[1]]* 2 ** np.log2(n[idx[0]])


def new_f90_2d(zeta: float, lam: float):
    with open("lotus.f90","r") as fileSource:
        fileLines = fileSource.readlines()

    fileLines[19] = f"    real, parameter    :: A = 0.1*c, St_d = 0.3, k_x={0.}, k_z={1/lam}, h_roughness=0.0\n"
    fileLines[23] = f"                          k_coeff = {1/zeta}, &\n"
    fileLines[27] = f"    integer            :: n(3), ndims=2\n"

    with open("lotus.f90","w") as fileOutput:
        fileOutput.writelines(fileLines)


if __name__ == "__main__":
    lam, N = 1/18, 6
    print(closest_a_n(N*lam*1024/4)/1024,delta_z(lam, N))

