#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from tkinter import Label
import numpy as np
import csv
from inout import read_forces, extract_zet
from scipy.interpolate import interp1d

from scipy.optimize import curve_fit

import seaborn as sns
from cProfile import label
from matplotlib import pyplot as plt
import scienceplots
from matplotlib.lines import Line2D
from matplotlib import ticker

plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"

formatter = ticker.ScalarFormatter()
formatter.set_powerlimits((-1, 1))


def process_forces(t, ux, uy):
    t, ux, uy = t[t > 3], ux[t > 3], uy[t > 3]
    t = t % 1
    fx = interp1d(t, ux, fill_value="extrapolate")
    fy = interp1d(t, uy, fill_value="extrapolate")
    t = np.linspace(0.001, 0.999, 300)
    return t, fx(t), fy(t)


def plot_ctp():
    colors = sns.color_palette("colorblind", 6)

    fig, ax = plt.subplots(1,2,figsize=(5, 3))
    ax[1].set_xlabel(f"$ t $")
    ax[1].set_ylabel(r"$ C_{T} $")

    st = 0.3
    cs = np.array([128, 256, 512, 1024, 2048])
    for idx, case in enumerate(cs):
        t, ux, uy = read_forces(f"{cwd}/16x16/{str(case)}/fort.9", interest="p")
        t, ux, uy = process_forces(t, ux, uy)
        ax[1].plot(t, ux, color=colors[idx], label=f"${4/case:.3f}$")

    ax[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax[1].yaxis.set_major_formatter(formatter)
    plot_ctp_av(ax[0])
    plt.savefig(f"{cwd}/figures/figure10.pdf", bbox_inches="tight", dpi=300)


def plot_ctp_av(ax):
    ax.set_xlabel(f"$ \Delta x $")
    ax.set_ylabel(r"$ \overline{C_{T}^2} $ error ")

    cs52 = np.array([520, 1040, 2080])
    cs = np.array([256, 512, 1024, 2048])

    thrust16 = np.empty(len(cs))
    for idx, case in enumerate(cs):
        t, vx, vy = read_forces(f"{cwd}/16x16/{str(case)}/fort.9", interest="p")
        t, ux, uy = process_forces(t, vx, vy)
        thrust16[idx] = np.mean(ux**2)

    thrust52 = np.empty(len(cs52))
    for idx, case in enumerate(cs52):
        t, vx, vy = read_forces(f"{cwd}/52x52/{str(case)}/fort.9", interest="p")
        t, ux, uy = process_forces(t, vx, vy)
        thrust52[idx] = np.mean(ux**2)

    ax.plot(
        4 / cs[:-1],
        abs((thrust16 - thrust16[-1]) / thrust16[-1])[:-1],
        color="k",
        ls="-",
        label=r"$\lambda = 1/16$",
    )

    ax.plot(
        4 / cs52[:-1],
        abs((thrust52 - thrust52[-1]) / thrust52[-1])[:-1],
        color="k",
        ls="-.",
        label=r"$\lambda = 1/52 \Delta x$",
    )

    ax.legend(loc="lower right")
    ax.loglog()
    formatter = ticker.LogFormatter()
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_minor_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_formatter(formatter)
    # ax.yaxis.set_minor_locator(plt.MaxNLocator(2))
    # plt.savefig(f"{cwd}/figures/ctp_av.pdf", bbox_inches="tight", dpi=300)


def main():
    plot_ctp()
    # plot_ctp_av()
    # plot_ctf()
    # plot_ctf_av()


if __name__ == "__main__":
    cwd = os.getcwd()
    main()
