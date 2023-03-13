#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lotus import run
from itscript import new_f90
from pathlib import Path
import os
import numpy as np


def run_lotus():
    for l in ls:
        new_f90(l)
        run(128, f'{cwd}/{str(l)}')


if __name__ == "__main__":
    cwd = Path.cwd()
    sts = np.array([0.31009362717481354])
    ls = np.array([4096])
    run_lotus()
    

