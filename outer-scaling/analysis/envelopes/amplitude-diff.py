import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots
from matplotlib.lines import Line2D

import os

plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"


def plot_envelopes():
    fig, ax = plt.subplots(2, figsize=(4.5, 3.))
    ax[0].set_xticklabels([])
    ax[1].set_xlabel(f"$ x $")
    ax[0].set_ylabel(r"$ y $")
    ax[1].set_ylabel(r"$ y $")
    ax[0].set_xlim(0, 1)
    ax[1].set_xlim(0, 1)
    ax[0].set_ylim(-0.15, 0.15)
    ax[1].set_ylim(-0.15, 0.15)

    ts = np.arange(0,1, 0.25)
    x = np.linspace(0,1)
    for t in ts:
        h1 = env1(x)*np.sin(2*np.pi*(x/1- t))
        ax[0].plot(x, h1, color=sns.color_palette('Reds', 3)[1])
        h1 = env1(x)*np.sin(2*np.pi*(x/2- t))
        ax[1].plot(x, h1, color=sns.color_palette('Reds', 3)[2])

        h2 = env_sant(x)*np.sin(2*np.pi*(x/1- t))
        ax[0].plot(x, h2, color=sns.color_palette('Blues', 3)[1])
        h2 = env_sant(x)*np.sin(2*np.pi*(x/2- t))
        ax[1].plot(x, h2, color=sns.color_palette('Blues', 3)[2])

    legend_elements = [
        Line2D([0], [0], ls="-", label=r"$\zeta=1$", c="grey"),
    ]
    legend1 = ax[0].legend(handles=legend_elements, loc=1)
    ax[0].add_artist(legend1)

    legend_elements = [
        Line2D([0], [0], ls="-", label=r"$0.28 x^2+0.13 x+0.05$", c=sns.color_palette('Reds', 3)[2]),
        Line2D([0], [0], ls="-", label=r"$0.28 x^2-0.13 x+0.05$", c=sns.color_palette('Blues', 3)[2]),
    ]

    legend2 = ax[0].legend(handles=legend_elements, loc=3)
    ax[0].add_artist(legend2)

    legend_elements = [
        Line2D([0], [0], ls="-", label=r"$\zeta=2$", c="k"),
    ]
    legend1 = ax[1].legend(handles=legend_elements, loc=1)
    ax[1].add_artist(legend1)

    plt.savefig(
        f"{os.getcwd()}/figures/trajectory-diff.png", bbox_inches="tight", dpi=200
    )

def env1(x):
    return 0.1*(0.28*x**2+0.13*x+0.05)/(0.28+0.13+0.05)

def env_sant(x):
    return 0.14*x**2-0.065*x+0.025


if __name__ == "__main__":
    plot_envelopes()
