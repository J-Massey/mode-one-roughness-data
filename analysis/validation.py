#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np
import csv
from inout import read_forces

def print_convergence(ls):
    thrust = np.empty(len(ls))
    for idx in range(len(ls)):
        t, ux = read_forces(
                    f"{Path.cwd().parent}/validation/convergence-to-lucas/{ls[idx]}/fort.9",
                    interest="p",
                    direction='x',
                )
        thrust[idx] = np.mean(ux[((t > 4)&(t<10))])

    print(thrust)
    print((thrust-0.162)/0.162)
    print("Delta x", 4/ls)


def read_csv(fn):
    st, ct = [], []
    with open(fn) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            st.append(float(row[0]))
            ct.append(float(row[1]))
    return np.array(st), np.array(ct)


def main():
    print_convergence(np.array([1024, 2048, 4096]))


if __name__ == "__main__":
    main()
