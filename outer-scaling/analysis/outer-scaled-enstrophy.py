#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from matplotlib.axes import Axes

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

def SA_enstrophy_scaling(span=0.03125):
    return (
        1 / 0.1             # A
        / (1 * 1024/4.)     # L
        / (span * 1024)  # span
      )


def get_enstrophy(k_lam: np.ndarray, re: int, d: str = "") -> np.ndarray:
    enstrophy = np.empty(len(k_lam))
    for idx, k_la in enumerate(k_lam):
        # Read in the enstrophy
        t, p = read_forces(
            f"{Path.cwd().parent}/{re}/{k_lam[idx]}{d}/fort.9",
            interest="E",
            direction="b",
        )
        raw_enstrophy = np.mean(p[t > 4])
        enstrophy[idx] = scale_enstrophy(raw_enstrophy, k_la, d)
    return enstrophy


def scale_enstrophy(raw_enstrophy: float, k_la: float, d: str) -> float:
    if k_la==0 or d=="-2d":
        # Scale the enstrophy using the SA_enstrophy_scaling function
        scaled_enstrophy = raw_enstrophy * SA_enstrophy_scaling(1/1024)
    elif k_la <16:
        scaled_enstrophy = raw_enstrophy * SA_enstrophy_scaling(6/k_la/4)
    else:
        scaled_enstrophy = raw_enstrophy * SA_enstrophy_scaling(0.03125)
    return scaled_enstrophy


def plot_enstrophy_3d(ax: Axes) -> None:
    ax.set_xlabel(r"$\zeta$")
    ax.set_ylabel(r"E")
    ax.set_xlim(1, 2)

    for idx, _ in enumerate(res):
        enst_plot_helper(ax, idx)


def enst_plot_helper(ax: Axes, re_idx: int) -> None:
    # Load the values of zeta (the non-dimensionalized wall distance) and
    # lambda (the non-dimensionalized Reynolds number) from the data file
    zeta, lam = np.load(f"{cwd}/zeta_lambda.npy", allow_pickle=True)

    # Use a linear interpolation to find the value of zeta for the given
    # Reynolds number
    zet = interp1d(lam, zeta)(1 / k_lams)

    # Get the enstrophy for the given Reynolds number
    enstrophy = get_enstrophy(k_lams, res[re_idx])

    # Plot the enstrophy as a function of zeta
    ax.plot(
        zet,
        enstrophy,
        markerfacecolor="None",
        marker=markers[re_idx],
        color=sns.color_palette("colorblind")[re_idx],
        ls="-",
    )


def plot_enstrophy_2d(ax: Axes) -> None:
    ax.set_xlabel(r"$\zeta$")
    ax.set_ylabel(r"E_s")
    ax.set_xlim(1, 2)

    for idx, _ in enumerate(res):
        enst_plot_helper_2d(ax, idx)


def enst_plot_helper_2d(ax: Axes, re_idx: int) -> None:
    zeta, lam = np.load(f"{cwd}/zeta_lambda.npy", allow_pickle=True)
    zet = interp1d(lam, zeta)(1 / k_lams)

    enstrophy_2d = get_enstrophy(k_lams, res[re_idx], d='-2d')

    ax.plot(
        zet,
        enstrophy_2d,
        markerfacecolor="None",
        marker=markers[re_idx],
        color='grey',
        alpha=0.8,
        ls="-.",
    )


def plot_enstrophy_diff(ax):
    # fig, ax = plt.subplots(figsize=(4.5, 2.5))
    ax.set_xlabel(r"$\lambda/\delta$")
    ax.set_ylabel(r"$\Delta E/E_{s}$")

    ax.set_xlim(0, 5)

    ax.scatter(
        1 / k_lams / 0.06,
        (get_enstrophy(k_lams, 6000) / (1024 * 0.25 / 4) - get_enstrophy(k_lams, 6000, "-2d"))
        / get_enstrophy(k_lams, 6000, "-2d"),
        facecolor="None",
        marker="^",
        color=sns.color_palette("colorblind")[0],
    )

    ax.scatter(
        1 / k_lams / 0.06,
        (
            get_enstrophy(k_lams, 12000) / (1024 * 0.25 / 4)
            - get_enstrophy(k_lams, 12000, "-2d")
        )
        / get_enstrophy(k_lams, 12000, "-2d"),
        facecolor="None",
        marker="P",
        color=sns.color_palette("colorblind")[1],
    )

    ax.scatter(
        1 / k_lams / 0.06,
        (
            get_enstrophy(k_lams, 24000) / (1024 * 0.25 / 4)
            - get_enstrophy(k_lams, 24000, "-2d")
        )
        / get_enstrophy(k_lams, 24000, "-2d"),
        facecolor="None",
        marker="o",
        color=sns.color_palette("colorblind")[2],
    )

def re_legend():
    legend_elements = [
        Line2D(
            [0],
            [0],
            ls="-",
            label=r"$Re=6,000$",
            c=sns.color_palette('colorblind')[0],
            marker="^",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="-",
            label=r"$Re=12,000$",
            c=sns.color_palette('colorblind')[1],
            marker="P",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="-",
            label=r"$Re=24,000$",
            c=sns.color_palette('colorblind')[2],
            marker="o",
            markerfacecolor="none",
        ),
    ]
    return legend_elements


def smooth_rough_legend():
    legend_elements = [
        Line2D(
            [0],
            [0],
            ls="-",
            label=r"Rough",
            c='k',
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="-.",
            label=r"Smooth",
            c="grey",
            alpha=0.8,
            markerfacecolor="none",
        ),
    ]
    return legend_elements


def print_convergence(lam):
    thrust = get_thrust_avg(lam, 6000)
    print(thrust)
    thrust = get_thrust_avg(lam, 6000, "-2d")
    print(thrust, "\n")
    thrust = get_thrust_avg(lam, 24000)
    print(thrust)
    thrust = get_thrust_avg(lam, 24000, "-2d")
    print(thrust)


def get_thrust_avg(lam, re, d=""):
    thrust = np.empty(len(lam))
    for idx in range(len(lam)):
        t, p = read_forces(
            f"{Path.cwd().parent}/{re}/{lam[idx]}{d}/fort.9",
            interest="P",
            direction="x",
        )
        thrust[idx] = np.mean(p[t > 4])
    return thrust


def read_csv(fn):
    st, ct = [], []
    with open(fn) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            st.append(float(row[0]))
            ct.append(float(row[1]))
    return np.array(st), np.array(ct)


def plot_wrapper():
    fig, axd = plt.subplot_mosaic([['upper left', 'upper right'],
                               ['lower', 'lower']],
                              figsize=(5., 5.), layout="constrained")
    plot_enstrophy_3d(axd['upper left']) # type: ignore
    plot_enstrophy_2d(axd['upper right']) # type: ignore
    # plot_enstrophy_diff(axd['lower'])  # type: ignore

    axd['lower'].legend(handles=re_legend(), loc=4) # type: ignore

    plt.savefig(
        f"{os.getcwd()}/figures/figure9.pdf", bbox_inches="tight", dpi=300
    )


def main():
    plot_wrapper()
    # plot_enstrophy()
    # plot_enstrophy_2d()
    # plot_enstrophy_diff()
    # print_convergence(np.arange(4, 24, 4))


if __name__ == "__main__":
    cwd = os.getcwd()
    markers = ['^', 'p', 'o']
    res = [6000, 12000, 24000]
    n_bump_k_lam = np.arange(4, 16, 4)
    k_lams = np.arange(4, 52, 4)
    main()
    
