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
    fig, ax = plt.subplots(figsize=(5, 1.))
    # ax.set_xlabel(f"$ t $")
    # ax.set_ylabel(r"$ C_{T} $")
    ax.set_xticklabels([])

    ax.set_xlim(0, 1)

    # domain_set(ax, 5000, sns.color_palette("Reds",2)[1], 0)
    # domain_set(ax, 12000, sns.color_palette("Greens",2)[1], 0.)
    domain_set(ax, 24000, sns.color_palette("Blues",2)[1], 0)

    legend_elements = [
        Line2D([0], [0], ls="-", label=r"$Re=5,000$", c=sns.color_palette("Reds",2)[1]),
        Line2D([0], [0], ls="-", label=r"$Re=12,000$", c=sns.color_palette("Greens",2)[1]),
        Line2D([0], [0], ls="-", label=r"$Re=24,000$", c=sns.color_palette("Blues",2)[1]),
    ]
    # legend_elements = [
    #     Line2D([0], [0], ls="-", label="Domain 1", c="k"),
    #     Line2D([0], [0], ls=":", label="Domain 2", c="k"),
    # ]
    # ax.legend(handles=legend_elements)
    plt.savefig(f"{os.getcwd()}/figures/24.pdf", bbox_inches="tight", dpi=200)


def domain_set(ax, re, color, offset):
    t_sample = np.linspace(0.01, 0.99, 300)

    f = interp_cycle(
        1024,
        f"domain-test/{re}/grid-2",
        "p",
        "x",
    )

    ax.plot(
        t_sample,
        f(t_sample) - offset,
        color=color,
        ls="-",
    )

    f = interp_cycle(
        1024,
        f"domain-test/{re}/grid-3",
        "p",
        "x",
    )

    ax.plot(
        t_sample,
        f(t_sample) - offset,
        color=color,
        ls=":",
    )


def interp_cycle(
    L,
    crit_str="3d-check",
    interest="v",
    direction="x",
):
    t, ux, *_ = read_forces(
        f"/ssdfs/users/jmom1n15/rough-plate-revisions/{crit_str}/{L}/fort.9",
        interest=interest,
        direction=direction,
    )
    t, ux = t[t > 3], ux[t > 3]

    ux = savgol_filter(
        ux,
        int(len(ux)/(7*4)),
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
