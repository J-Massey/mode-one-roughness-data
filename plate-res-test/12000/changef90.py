#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def new_f90_res(L: float):
    with open("lotus.f90","r") as fileSource:
        fileLines = fileSource.readlines()

    fileLines[13] = f"    real,parameter     :: c={L}, nu=c/Re\n"

    with open("lotus.f90","w") as fileOutput:
        fileOutput.writelines(fileLines)

