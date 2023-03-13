#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lotus import run
from itscript import new_f90
from pathlib import Path
import os
import numpy as np


def run_lotus():
    for st in sts:
        new_f90(st)
        run(64, f'{cwd}/{str(st)}')


if __name__ == "__main__":
    cwd = Path.cwd()
    sts = np.array([0.15411199999999997, 0.20731733333333338, 0.25868800000000003, 0.31009362717481354, 0.36142933333333327, 0.4141360994200497])
    run_lotus()
    

