#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def new_f90_res(zeta: float, lam: float):
    with open("lotus.f90","r") as fileSource:
        fileLines = fileSource.readlines()

    fileLines[19] = f"    real, parameter    :: A = 0.1*c, St_d = 0.3, k_x={1/lam}, k_z={1/lam}, h_roughness=0.01\n"
    fileLines[23] = f"                          k_coeff = {1/zeta}, &\n"
    fileLines[27] = f"    integer            :: n(3), ndims=3\n"
    fileLines[51] = f"      z = {6*lam/4}\n"

    with open("lotus.f90","w") as fileOutput:
        fileOutput.writelines(fileLines)


def new_f90_2d(zeta: float, lam: float):
    with open("lotus.f90","r") as fileSource:
        fileLines = fileSource.readlines()

    fileLines[19] = f"    real, parameter    :: A = 0.1*c, St_d = 0.3, k_x={0.}, k_z={1/lam}, h_roughness=0.0\n"
    fileLines[23] = f"                          k_coeff = {1/zeta}, &\n"
    fileLines[27] = f"    integer            :: n(3), ndims=2\n"

    with open("lotus.f90","w") as fileOutput:
        fileOutput.writelines(fileLines)

