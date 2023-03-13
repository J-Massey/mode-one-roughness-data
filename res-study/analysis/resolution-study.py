#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path

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
    fig, ax = plt.subplots(len(res), figsize=(5., 3.))
    ax[-1].set_xlabel(f"$ t $")
    ax[1].set_ylabel(r"$ C_{T} $")

    [a.set_xticklabels([]) for a in ax[:-1]]
    [a.set_xlim(0, 1) for a in ax]

    for idx, _ in enumerate(res):
        domain_set(ax[idx], idx)

    legend_elements1 = [
        Line2D(
            [0], [0], ls="-", label=r"$Re=6,000$", c=sns.color_palette('colorblind')[0]
        ),
        Line2D(
            [0], [0], ls="-", label="$Re=12,000$", c=sns.color_palette('colorblind')[1]
        ),
        Line2D(
            [0], [0], ls="-", label="$Re=24,000$", c=sns.color_palette('colorblind')[2]
        ),
    ]
    legend_elements2 = [
        Line2D([0], [0], ls=":", label=f"$\Delta x = {4/512:.4f}$", c="k"),
        Line2D([0], [0], ls="-", label=f"$\Delta x = {4/1024:.4f}$", c="k"),
        Line2D([0], [0], ls="-.", label=f"$\Delta x = {4/2048:.4f}$", c="k"),
    ]

    legend1 = ax[0].legend(handles=legend_elements1, loc=2)
    legend2 = ax[0].legend(handles=legend_elements2, loc=4)
    ax[0].add_artist(legend1)
    ax[0].add_artist(legend2)

    plt.savefig(f"{Path.cwd()}/figures/plate-res.pdf", bbox_inches="tight", dpi=200)


def domain_set(ax, re_idx: int):
    re = res[re_idx]
    for idx, l in enumerate(Ls):
        f = interp_cycle(
            l,
            f"{re}",
        )

        print(f(t_sample).mean())

        ax.plot(
            t_sample,
            f(t_sample),
            color=sns.color_palette('colorblind')[re_idx],
            ls=lss[idx],
            alpha=0.8,
        )


def interp_cycle(
    L,
    crit_str="12000",
    interest="p",
    direction="x",
):
    t, ux, *_ = read_forces(
        f"{Path.cwd().parent}/{crit_str}/{L}/fort.9",
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
    lss = [":", "-", "-.", "--"]

    t_sample = np.linspace(0.01, 0.99, 300)
    Ls = np.array([512, 1024, 2048])
    # res = np.array([6000, 12000, 24000, 48000])
    res = np.array([6000, 12000, 24000])
    main()
