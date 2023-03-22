#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def new_f90(l=1024, st=0.31009362717481354):
    with open("lotus.f90","r") as fileSource:
        fileLines = fileSource.readlines()

    fileLines[13] = f"  real,parameter     :: c={l}, nu=c/Re\n"
    fileLines[19] = f"  real, parameter    :: A = 0.1*c, St_d = {st}, k_x=0., k_z=16.0, h_roughness=0.0\n"
        
    with open("lotus.f90","w") as fileOutput:
        fileOutput.writelines(fileLines)


