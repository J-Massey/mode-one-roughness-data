#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
import csv
from inout import read_forces
from scipy.interpolate import interp1d

from matplotlib.lines import Line2D
import seaborn as sns
from matplotlib import pyplot as plt
import scienceplots
plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"

def print_convergence(ls):
    thrust = np.empty(len(ls))
    for idx in range(len(ls)):
        t, ux = read_forces(
                    f"/scratch/ml4n17/jm/lucas-res-test-high-zeta/{ls[idx]}/fort.9",
                    interest="p",
                    direction='x',
                )
        thrust[idx] = np.mean(ux[((t > 4)&(t<10))])
    print(thrust)

    # _, ct_1_3 = read_csv(f"{cwd}/lit_data/1_3-ct-f.csv")
    # print(ct_1_3[-3])
    print((thrust-0.162)/0.162)
    print(4/ls)


def read_csv(fn):
    st, ct = [], []
    with open(fn) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            st.append(float(row[0]))
            ct.append(float(row[1]))
    return np.array(st), np.array(ct)


def main():
    print_convergence(np.array([512, 1024, 2048, 4096]))


if __name__ == "__main__":
    cwd = os.getcwd()
    main()
