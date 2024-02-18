#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lotus import run
from itscript import new_f90
from pathlib import Path

def extract_k():
    with open("lotus.f90","r") as fileSource:
        fileLines = fileSource.readlines()
    txt = fileLines[24]
    return float([s for s in txt.split(' ')][-2][:-1])


def run2d():
    k = extract_k()
    new_f90(2, 8, c, k, la_x, la_z)
    run(256, f'{cwd}/2D')


if __name__ == "__main__":
    cwd = Path.cwd()
    la_x, la_z = 0., 4.
    c = 1024
    run2d()
    

