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


def plot_thrust_avg():
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    ax.set_xlabel(f"$ St $", fontsize=10.5)
    ax.set_ylabel(r"$ \overline{C_T} $", fontsize=10.5)

    ax.axhline(0, ls='--', c='k', alpha=0.6)
    sts = np.array([0.10274133333333334, 0.15411199999999997, 0.20731733333333338, 0.25868800000000003, 0.31009362717481354, 0.36142933333333327, 0.4141360994200497])

    st_1_3, ct_1_3 = read_csv(f"{cwd}/lit_data/1_3-ct-f.csv")
    thrust_plot_helper(ax, sts, '1_3')
    print(ct_1_3)

    sf = lambda a: 2*(a*0.18)/0.3  # Define a scale factor to convert from frequency to Strouhal number

    ax.plot(
        st_1_3*sf(0.172),
        ct_1_3,
        ls="-.",
        color='grey',
        marker="D",
        markerfacecolor="none",
    )

    # print(list(st_1_3*sf(0.172)))

    legend_elements = [
        Line2D([0], [0], ls="-.", label=r"Lucas et al. 2015", c='grey', marker="D", markerfacecolor="none"),
        Line2D([0], [0], ls="-", marker='o', label="Simulation", c='k', markerfacecolor="none"),
        Line2D([0], [0], marker='s', label="Matched", c='red', markerfacecolor="none"),
    ]

    legend1 = plt.legend(handles=legend_elements, loc=2)
    plt.gca().add_artist(legend1)

    plt.savefig(
        f"{cwd}/figures/lucas-ct-comparison.pdf", bbox_inches="tight", dpi=300
    )

def thrust_plot_helper(ax, sts, case):
    thrust = np.empty(len(sts))
    for idx, st in enumerate(sts):
        try:
            t, ux, *_ = read_forces(
                f"/ssdfs/users/jmom1n15/rough-plate-revisions/validation/{case}/{str(st)}/fort.9",
                interest="p",
            )
            thrust[idx] = np.mean(ux[t > 4])
        except FileNotFoundError:
            thrust[idx]=np.NAN
    print(thrust)
    ax.plot(
        sts,
        thrust,
        ls="-",
        color='k',
        marker="o",
        markerfacecolor="none",
    )


def read_csv(fn):
    st, ct = [], []
    with open(fn) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            st.append(float(row[0]))
            ct.append(float(row[1]))
    return np.array(st), np.array(ct)



def get_ct(x, y):
    return (interp1d(x,y)(1.5))


def main():
    plot_thrust_avg()


if __name__ == "__main__":
    cwd = os.getcwd()
    main()
