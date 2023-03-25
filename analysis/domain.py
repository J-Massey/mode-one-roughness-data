#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path

import numpy as np
from inout import read_forces, extract_zet
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d

import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import scienceplots

plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"


def plot_domain_test():
    fig, axes = plt.subplots(3, figsize=(5, 3.))
    axes[-1].set_xlabel(f"$ t $")
    axes[1].set_ylabel(r"$ C_{T} $")
    [ax.set_xticklabels([]) for ax in axes[:-1]]
    [ax.set_xlim(0, 1) for ax in axes]


    domain_set(axes[0], 6000, sns.color_palette('colorblind')[1])
    domain_set(axes[1], 12000, sns.color_palette('colorblind')[0])
    domain_set(axes[2], 24000, sns.color_palette('colorblind')[2])

    legend_elements2 = [
        Line2D([0], [0], ls="-", label="Domain 1", c="k"),
        Line2D([0], [0], ls=":", label="Domain 2", c="k"),
    ]

    legend1 = axes[0].legend(handles=[Line2D([0], [0], ls="-", label=r"$Re=6,000$", c=sns.color_palette('colorblind')[1])], loc=2)
    legend2 = axes[1].legend(handles=[Line2D([0], [0], ls="-", label=r"$Re=12,000$", c=sns.color_palette('colorblind')[0])], loc=2)
    legend3 = axes[2].legend(handles=[Line2D([0], [0], ls="-", label=r"$Re=24,000$", c=sns.color_palette('colorblind')[2])], loc=2)
    legend4 = axes[0].legend(handles=legend_elements2, loc=4)
    axes[0].add_artist(legend1)
    # axes[1].add_artist(legend2)
    # axes[2].add_artist(legend3)

    plt.savefig(f"{Path.cwd()}/analysis/figures/figure12.pdf", bbox_inches="tight", dpi=200)


def domain_set(ax, re, color):
    t_sample = np.linspace(0.01, 0.99, 300)

    f = interp_cycle(
        f"{re}/grid-2",
    )

    ax.plot(
        t_sample,
        f(t_sample),
        color=color,
        ls="-",
    )

    f = interp_cycle(
        f"{re}/grid-3",
    )

    ax.plot(
        t_sample,
        f(t_sample),
        color=color,
        ls=":",
    )


def interp_cycle(
    crit_str="grid-2",
    interest="p",
    direction="x",
):
    t, ux, *_ = read_forces(
        f"{Path.cwd()}/domain-test/{crit_str}/1024/fort.9",
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
    plot_domain_test()


if __name__ == "__main__":
    main()
