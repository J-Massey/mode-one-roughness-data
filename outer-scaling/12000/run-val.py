# -*- coding: utf-8 -*-
from lotus import run
from changef90 import new_f90_res, new_f90_2d
from pathlib import Path
import numpy as np
from scipy.interpolate import interp1d
import numpy as np


def run_val(zeta, k_lam):
    new_f90_res(zeta, 1/k_lam)
    run(256, f'{cwd}/{k_lam}')
    # new_f90_2d(zeta, 1/k_lam)
    # run(256, f'{cwd}/{k_lam}-2d')

if __name__ == "__main__":
    cwd = Path.cwd()
    k_lams = np.array([4, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 36, 40, 44, 48, 52])
    k_lams = np.array([24, 28, 32, 36, 40, 44, 48, 52])
    zeta, lam = np.load(f'{cwd}/zeta_lambda.npy', allow_pickle=True)
    [run_val(interp1d(lam, zeta)(1/k_lam), k_lam) for k_lam in k_lams]
    
