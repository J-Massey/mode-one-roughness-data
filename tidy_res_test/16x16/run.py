#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lotus import run
from itscript import new_f90
from pathlib import Path
import numpy as np


def extract_k():
    with open("lotus.f90", "r") as fileSource:
        fileLines = fileSource.readlines()
    txt = fileLines[24]
    return float([s for s in txt.split(" ")][-2][:-1])


def run_lotus():
    k = extract_k()
    for c in cs:
        new_f90(3, 8, c, k, la_x, la_z)
        run(1024, f"{cwd}/{c}")


if __name__ == "__main__":
    cwd = Path.cwd()
    la_x, la_z = 16.5, 16.0
    cs = np.array([128, 256, 512, 1024, 2048])
    run_lotus()
