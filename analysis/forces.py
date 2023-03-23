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


def get_forces(k_lam: np.ndarray, re: int, f : str = "p", d: str = "x", dim: str = "") -> np.ndarray:
    force = np.empty(len(k_lam))
    for idx, k_la in enumerate(k_lam):
        # Read in the force
        t, p = read_forces(
            f"{Path.cwd()}/outer-scaling/{re}/{k_lam[idx]}{dim}/fort.9",
            interest=f,
            direction=d,
        )
        force[idx] = np.mean(p[t > 4])
    return force


def get_rms(k_lam: np.ndarray, re: int, f : str = "p", d: str = "x", dim: str = "") -> np.ndarray:
    force = np.empty(len(k_lam))
    for idx, k_la in enumerate(k_lam):
        # Read in the force
        t, p = read_forces(
            f"{Path.cwd()}/outer-scaling/{re}/{k_lam[idx]}{dim}/fort.9",
            interest=f,
            direction=d,
        )
        force[idx] = np.std(p[t > 4])
    return force


def plot_thrust(ax: Axes) -> None:
    ax.set_xlabel(r"$\zeta$")
    ax.set_ylabel(r"$\overline{C_T}$")
    ax.set_xlim(1, 2.35)
    # ax.set_ylim(-0.01, 0.085)

    for idx, _ in enumerate(res):
        thrust_plt_helper(ax, idx)


def thrust_plt_helper(ax: Axes, re_idx: int) -> None:
    # Load the values of zeta (the wave speed) and
    # lambda (the roughness wavelength) from the data file

    # Use a linear interpolation to find the value of zeta for the given
    # roughness wavelength
    zet = interp1d(lam, zeta)(1 / k_lams)
    # Get the force for the given roughness wavelength
    force = get_forces(k_lams, res[re_idx])
    # [print(f"${f:.4f}$") for f in force]

    # Plot the force as a function of zeta
    ax.plot(
        zet,
        force,
        markerfacecolor="None",
        marker='d',
        color=sns.color_palette("colorblind")[re_idx],
        ls="-",
    )
    force = get_forces(k_lams, res[re_idx], dim="-2d")
    # [print(f"${f:.4f}$") for f in force]

    # Plot the force as a function of zeta
    ax.plot(
        zet,
        force,
        markerfacecolor="None",
        marker='s',
        color='grey',
        ls="-.",
    )


def plot_thrust_rms(ax: Axes) -> None:
    ax.set_xlabel(r"$\zeta$")
    ax.set_ylabel(r"$RMS(C_T)$")
    ax.set_xlim(1, 2.35)
    # ax.set_ylim(-0.01, 0.085)

    for idx, _ in enumerate(res):
        rms_thrust_plt_helper(ax, idx)


def rms_thrust_plt_helper(ax: Axes, re_idx: int) -> None:

    zet = interp1d(lam, zeta)(1 / k_lams)
    force = get_rms(k_lams, res[re_idx])

    # Plot the force as a function of zeta
    ax.plot(
        zet,
        force,
        markerfacecolor="None",
        marker='d',
        color=sns.color_palette("colorblind")[re_idx],
        ls="-",
    )
    force = get_rms(k_lams, res[re_idx], dim="-2d")

    # Plot the force as a function of zeta
    ax.plot(
        zet,
        force,
        markerfacecolor="None",
        marker='s',
        color='grey',
        ls="-.",
    )


def plot_lift_rms(ax: Axes) -> None:
    ax.set_xlabel(r"$\zeta$")
    ax.set_ylabel(r"$RMS(C_L)$")
    ax.set_xlim(1, 2.35)
    # ax.set_ylim(-0.01, 0.085)

    for idx, _ in enumerate(res):
        rms_lift_plt_helper(ax, idx)


def rms_lift_plt_helper(ax: Axes, re_idx: int) -> None:

    zet = interp1d(lam, zeta)(1 / k_lams)
    force = get_rms(k_lams, res[re_idx], d="y")

    # Plot the force as a function of zeta
    ax.plot(
        zet,
        force,
        markerfacecolor="None",
        marker='d',
        color=sns.color_palette("colorblind")[re_idx],
        ls="-",
    )
    force = get_rms(k_lams, res[re_idx], d="y", dim="-2d")

    # Plot the force as a function of zeta
    ax.plot(
        zet,
        force,
        markerfacecolor="None",
        marker='s',
        color='grey',
        ls="-.",
    )


def plot_power(ax: Axes) -> None:
    ax.set_xlabel(r"$\zeta$")
    ax.set_ylabel(r"$\overline{C_P}$")
    ax.set_xlim(1, 2.35)
    # ax.set_ylim(0, 0.5)

    for idx, _ in enumerate(res):
        power_plt_helper(ax, idx)


def power_plt_helper(ax: Axes, re_idx: int) -> None:
    # Load the values of zeta (the wave speed) and
    # lambda (the roughness wavelength) from the data file

    # Use a linear interpolation to find the value of zeta for the given
    # roughness wavelength
    zet = interp1d(lam, zeta)(1 / k_lams)
    # Get the force for the given roughness wavelength
    force = get_forces(k_lams, res[re_idx], f="cp", d="")
    [print(f"${f:.3f}$") for f in force]

    # Plot the force as a function of zeta
    ax.plot(
        zet,
        force,
        markerfacecolor="None",
        marker='d',
        color=sns.color_palette("colorblind")[re_idx],
        ls="-",
    )
    force = get_forces(k_lams, res[re_idx], f="cp", d="", dim="-2d")
    [print(f"${f:.3f}$") for f in force]

    # Plot the force as a function of zeta
    ax.plot(
        zet,
        force,
        markerfacecolor="None",
        marker='s',
        color='grey',
        ls="-.",
    )


def re_legend():
    legend_elements = [
        Line2D(
            [0],
            [0],
            ls="-",
            label=r"$Re=24,000$",
            c=sns.color_palette('colorblind')[2],
            marker="o",
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
            label=r"$Re=6,000$",
            c=sns.color_palette('colorblind')[0],
            marker="^",
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
            f"{Path.cwd()}/outer-scaling/{re}/{lam[idx]}{d}/fort.9",
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
            try:
                st.append(float(row[0]))
                ct.append(float(row[1]))
            except ValueError:
                continue
    return np.array(st), np.array(ct)


def plot_wrapper():
    fig, axd = plt.subplot_mosaic([[0, 1],
                               [2, 3]],
                              figsize=(5., 5.), layout="constrained")
    plot_power(axd[0]) # type: ignore
    plot_lift_rms(axd[1]) # type: ignore
    plot_thrust(axd[2]) # type: ignore
    plot_thrust_rms(axd[3]) # type: ignore

    # legend1 = axd['lower'].legend(handles=re_legend(), loc=4) # type: ignore
    # legend2 = axd['lower'].legend(handles=smooth_rough_legend(), loc=1) # type: ignore
    # axd['lower'].add_artist(legend1) # type: ignore

    plt.savefig(
        f"{os.getcwd()}/analysis/figures/figure7.pdf", bbox_inches="tight", dpi=300
    )


def main():
    plot_wrapper()


if __name__ == "__main__":
    cwd = os.getcwd()
    zeta, lam = np.load(f"{Path.cwd()}/analysis/zeta_lambda.npy", allow_pickle=True)
    markers = ['^', 'p', 'o']
    res = [6000, 12000, 24000]
    res = [12000]
    k_lams = np.arange(0, 56, 4)
    main()
    
