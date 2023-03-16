#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path

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


def plot_enstrophy_3d(ax):
    # fig, ax = plt.subplots(figsize=(2.5, 2.5))
    ax.set_xlabel(r"$\zeta$")
    ax.set_ylabel(r"E")

    ax.set_xlim(1, 2)

    for idx, _ in enumerate(res):
        enst_plot_helper(ax, idx)


def enst_plot_helper(ax, re_idx):
    zeta, lam = np.load(f"{cwd}/zeta_lambda.npy", allow_pickle=True)
    zet = np.append(1/0.94, interp1d(lam, zeta)(1 / k_lam))

    enstrophy = np.append(
        get_enstrophy(np.array([0]), res[re_idx])*SA_enstrophy_scaling(1/1024),
        get_enstrophy(k_lam, res[re_idx]) * SA_enstrophy_scaling(0.03125)
        )

    ax.plot(
        zet,
        enstrophy,
        markerfacecolor="None",
        marker=markers[re_idx],
        color=sns.color_palette("colorblind")[re_idx],
        # alpha=0.7,
        ls="-",
    )


def plot_enstrophy_2d(ax):
    ax.set_xlabel(r"$\zeta$")
    ax.set_ylabel(r"E_s")
    ax.set_xlim(1, 2)

    for idx, _ in enumerate(res):
        enst_plot_helper_2d(ax, idx)


def enst_plot_helper_2d(ax, re_idx):
    zeta, lam = np.load(f"{cwd}/zeta_lambda.npy", allow_pickle=True)
    zet = np.append(1/0.94, interp1d(lam, zeta)(1 / k_lam))

    enstrophy_2d = np.append(
        get_enstrophy(np.array([0]), res[re_idx], '-2d')*SA_enstrophy_scaling(1/1024),
        get_enstrophy(k_lam, res[re_idx], '-2d') * SA_enstrophy_scaling(1/1024)
        )

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
        1 / k_lam / 0.06,
        (get_enstrophy(k_lam, 6000) / (1024 * 0.25 / 4) - get_enstrophy(k_lam, 6000, "-2d"))
        / get_enstrophy(k_lam, 6000, "-2d"),
        facecolor="None",
        marker="^",
        color=sns.color_palette("colorblind")[0],
    )

    ax.scatter(
        1 / k_lam / 0.06,
        (
            get_enstrophy(k_lam, 12000) / (1024 * 0.25 / 4)
            - get_enstrophy(k_lam, 12000, "-2d")
        )
        / get_enstrophy(k_lam, 12000, "-2d"),
        facecolor="None",
        marker="P",
        color=sns.color_palette("colorblind")[1],
    )

    ax.scatter(
        1 / k_lam / 0.06,
        (
            get_enstrophy(k_lam, 24000) / (1024 * 0.25 / 4)
            - get_enstrophy(k_lam, 24000, "-2d")
        )
        / get_enstrophy(k_lam, 24000, "-2d"),
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



def get_enstrophy(lam, re, d=""):
    thrust = np.empty(len(lam))
    for idx in range(len(lam)):
        t, p = read_forces(
            f"{Path.cwd().parent}/{re}/{lam[idx]}{d}/fort.9",
            interest="E",
            direction="b",
        )
        thrust[idx] = np.mean(p[t > 4])
    return thrust


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
    plot_enstrophy_3d(axd['upper left'])
    plot_enstrophy_2d(axd['upper right'])
    plot_enstrophy_diff(axd['lower'])

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
    k_lam = np.arange(16, 52, 4)
    main()