#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

# from turtle import color
import numpy as np

from inout import read_forces, extract_zet
from scipy.interpolate import interp1d
from itertools import cycle

from scipy.optimize import curve_fit

import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import cm
import matplotlib.colors as colors
from scipy.signal import savgol_filter


plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"


def plot_phase_av_ct_ts():
    fig, ax = plt.subplots(3, figsize=(2.5, 2.5))
    ax[2].set_xlabel(f"$ t $")
    ax[1].set_ylabel(r"$ C_{T} $")
    ax[0].set_xticklabels([])
    ax[1].set_xticklabels([])

    ax[0].set_xlim(0, 1)
    ax[1].set_xlim(0, 1)
    ax[2].set_xlim(0, 1)

    domain_set(ax[0], 5000, "Blues", 0)
    domain_set(ax[1], 12000, "Greens", 0.)
    domain_set(ax[2], 24000, "Reds", 0)

    legend_elements = [
        Line2D(
            [0], [0], ls="-", label=r"$Re=6,000$", c=sns.color_palette("Blues", 4)[3]
        ),
        Line2D(
            [0], [0], ls="-", label="$Re=12,000$", c=sns.color_palette("Greens", 4)[3]
        ),
        Line2D(
            [0], [0], ls="-", label="$Re=24,000$", c=sns.color_palette("Reds", 4)[3]
        ),
    ]
    legend1 = plt.legend(handles=legend_elements, loc=2)

    legend_elements = [
        Line2D([0], [0], ls=":", label=f"$\Delta x = {4/512:.4f}$", c="k"),
        Line2D([0], [0], ls="-", label=f"$\Delta x = {4/1024:.4f}$", c="k"),
        Line2D([0], [0], ls="-.", label=f"$\Delta x = {4/2048:.4f}$", c="k"),
    ]
    ax[1].legend(handles=legend_elements)
    plt.gca().add_artist(legend1)

    plt.savefig(f"{os.getcwd()}/figures/plate-res.pdf", bbox_inches="tight", dpi=200)


def domain_set(ax, re, color, offset):
    t_sample = np.linspace(0.01, 0.99, 300)

    f = interp_cycle(
        512,
        f"{re}",
        "p",
        "x",
    )

    ax.plot(
        t_sample,
        f(t_sample) - np.min(f(t_sample) * offset),
        color=sns.color_palette(color, 4)[1],
        ls=":",
        alpha=0.8,
    )

    f = interp_cycle(
        1024,
        f"{re}",
        "p",
        "x",
    )

    ax.plot(
        t_sample,
        f(t_sample) - np.min(f(t_sample) * offset),
        color=sns.color_palette(color, 4)[2],
        ls="-",
        alpha=0.8,
    )

    f = interp_cycle(
        2048,
        f"{re}",
        "p",
        "x",
    )

    ax.plot(
        t_sample,
        f(t_sample) - np.min(f(t_sample) * offset),
        color=sns.color_palette(color, 4)[3],
        ls="-.",
        alpha=0.8,
    )


def interp_cycle(
    L,
    crit_str="3d-check",
    interest="p",
    direction="x",
):
    t, ux, *_ = read_forces(
        f"/ssdfs/users/jmom1n15/rough-plate-revisions/plate-res-test/{crit_str}/{L}/fort.9",
        interest=interest,
        direction=direction,
    )
    t, ux = t[t > 3], ux[t > 3]

    ux = savgol_filter(
        ux,
        int(len(ux) / (3 * 4)),
        3,
    )
    t = t % 1
    f = interp1d(t, ux, fill_value="extrapolate")
    return f


def main():
    plot_phase_av_ct_ts()


if __name__ == "__main__":
    marker = cycle(("^", "P", "s", "o", "X"))
    main()
