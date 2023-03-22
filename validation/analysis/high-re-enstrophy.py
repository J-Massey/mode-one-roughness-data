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


def plot_enstrophy():
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    ax.set_xlabel(r"$\lambda$")
    ax.set_ylabel(r"E")

    lam = np.arange(4, 56, 4)
    ax.plot(
        1 / lam,
        get_enstrophy(lam, 6000) / (1024 * 0.25 / 4),
        markerfacecolor="None",
        marker="^",
        color="k",
        ls="-.",
    )

    ax.plot(
        1 / lam,
        get_enstrophy(lam, 6000, "-2d"),
        markerfacecolor="None",
        marker="^",
        color="grey",
        ls="-.",
    )

    ax.plot(
        1 / lam,
        get_enstrophy(lam, 24000) / (1024 * 0.25 / 4),
        markerfacecolor="None",
        marker="o",
        color="k",
        ls="--",
    )

    ax.plot(
        1 / lam,
        get_enstrophy(lam, 24000, "-2d"),
        markerfacecolor="None",
        marker="o",
        color="grey",
        ls="--",
    )
    lam = np.arange(4, 36, 4)

    ax.plot(
        1 / lam,
        get_enstrophy(lam, 48000) / (1024 * 0.25 / 4),
        markerfacecolor="None",
        marker="s",
        color="k",
        ls=":",
    )

    ax.plot(
        1 / lam,
        get_enstrophy(lam, 48000, "-2d"),
        markerfacecolor="None",
        marker="s",
        color="grey",
        ls=":",
    )

    legend_elements = [
        Line2D(
            [0],
            [0],
            ls="-.",
            label=r"$Re=6,000$",
            c="k",
            marker="^",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="--",
            label=r"$Re=24,000$",
            c="k",
            marker="o",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls=":",
            label=r"$Re=48,000$",
            c="k",
            marker="s",
            markerfacecolor="none",
        ),
    ]
    legend1 = plt.legend(handles=legend_elements, loc=2)
    ax.add_artist(legend1)

    legend_elements = [
        Line2D([0], [0], ls="-", label=r"Rough", c="black", markerfacecolor="none"),
        Line2D([0], [0], ls="-", label=r"Smooth", c="grey", markerfacecolor="none"),
    ]
    legend2 = plt.legend(handles=legend_elements, loc=4)
    ax.add_artist(legend2)

    plt.savefig(f"{os.getcwd()}/figures/enstrophy.pdf", bbox_inches="tight", dpi=300)


def plot_enstrophy_diff():
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    ax.set_xlabel(r"$\lambda/\delta$")
    ax.set_ylabel(r"$\Delta E/E_{s}$")

    lam = np.append(np.arange(4, 20, 4), np.arange(20, 56, 8))
    ax.scatter(
        1 / lam / 0.06,
        (get_enstrophy(lam, 6000) / (1024 * 0.25 / 4) - get_enstrophy(lam, 6000, "-2d"))
        / get_enstrophy(lam, 6000, "-2d"),
        facecolor="None",
        marker="^",
        color="k",
        # ls="-.",
    )

    lam = np.arange(4, 52, 4)

    ax.scatter(
        1 / lam / 0.06,
        (
            get_enstrophy(lam, 24000) / (1024 * 0.25 / 4)
            - get_enstrophy(lam, 24000, "-2d")
        )
        / get_enstrophy(lam, 24000, "-2d"),
        facecolor="None",
        marker="o",
        color="k",
        # ls="None",
    )

    lam = np.arange(4, 36, 4)

    ax.scatter(
        1 / lam / 0.06,
        (
            get_enstrophy(lam, 48000) / (1024 * 0.25 / 4)
            - get_enstrophy(lam, 48000, "-2d")
        )
        / get_enstrophy(lam, 48000, "-2d"),
        facecolor="None",
        marker="s",
        color="k",
        # ls="None",
    )

    legend_elements = [
        Line2D(
            [0],
            [0],
            ls="None",
            label=r"$Re=6,000$",
            c="k",
            marker="^",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="None",
            label=r"$Re=24,000$",
            c="k",
            marker="o",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="None",
            label=r"$Re=48,000$",
            c="k",
            marker="s",
            markerfacecolor="none",
        ),
    ]
    legend1 = ax.legend(handles=legend_elements, loc=4)
    # ax.add_artist(legend1)

    plt.savefig(
        f"{os.getcwd()}/figures/enstrophy-diff.pdf", bbox_inches="tight", dpi=300
    )


def print_convergence(lam):
    thrust = get_thrust_avg(lam, 6000)
    print(thrust)
    thrust = get_thrust_avg(lam, 6000, "-2d")
    print(thrust, "\n")
    thrust = get_thrust_avg(lam, 24000)
    print(thrust)
    thrust = get_thrust_avg(lam, 24000, "-2d")
    print(thrust)


def get_enstrophy(lam, re, d=""):
    thrust = np.empty(len(lam))
    for idx in range(len(lam)):
        t, p = read_forces(
            f"/scratch/ml4n17/jm/{re}/{lam[idx]}{d}/fort.9",
            interest="E",
            direction="",
        )
        thrust[idx] = np.mean(p[t > 4])
    return thrust


def get_thrust_avg(lam, re, d=""):
    thrust = np.empty(len(lam))
    for idx in range(len(lam)):
        t, p = read_forces(
            f"/scratch/ml4n17/jm/{re}/{lam[idx]}{d}/fort.9",
            interest="p",
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


def main():
    plot_enstrophy()
    plot_enstrophy_diff()
    # print_convergence(np.arange(4, 24, 4))


if __name__ == "__main__":
    cwd = os.getcwd()
    main()
