#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from tkinter import Label
import numpy as np
import csv
from inout import read_forces, extract_zet
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from scipy.fft import fft, fftfreq
from scipy.signal import welch

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


def process_forces(t, ux):
    t, ux = t[t > 4], ux[t > 4]
    # nsplit = 1
    # t, ux = t[:(len(t)//nsplit)*nsplit], ux[:(len(ux)//nsplit)*nsplit]
    # splitlen = len(t)//nsplit
    # t = [t[i*splitlen//2:(i+1)*splitlen//2] for i in range(nsplit+nsplit//2)]
    # ux = [ux[i*splitlen//2:(i+1)*splitlen//2] for i in range(nsplit+nsplit//2)]
    # for id in range(len(t)):
    #     # Define window function
    #     window = np.hanning(len(t[id]))
    #     # Apply window function
    #     ux[id] = ux[id] * window
    #     # take fft
    #     ux[id] = fft(ux[id])
    
    # f = np.array(t).mean(axis=0)
    # ux_hat = np.array(ux).mean(axis=0)
    # fix the sampling rate by interpolating
    ux = interp1d(t, ux, fill_value="extrapolate")
    t = np.linspace(4.01, 7.99, 300)
    ux_hat = fft(ux(t))
    St = fftfreq(len(t), d=4/len(t))*0.3
    print(St[np.argsort(-ux_hat)]/0.3)
    # t = t % 1
    # f, ux_hat = welch(ux, fs=5/len(t), nperseg=300)
    return abs(St), abs(ux_hat) 


def plot_fft():
    colors = sns.color_palette("colorblind", 6)

    fig, ax = plt.subplots(figsize=(3, 3))
    # ax.set_yscale("log")
    ax.set_xlabel(f"$ St $")
    ax.set_ylabel(r"$ \hat{C_{T}} $")

    cs = np.array([128, 256, 512, 1024, 2048])
    cs = np.array([512, 1024, 2048])
    for idx, case in enumerate(cs):
        t, ux, _ = read_forces(f"{cwd}/16x16/{str(case)}/fort.9", interest="p")
        f, ux_hat = process_forces(t, ux)
        ax.loglog(f, ux_hat, color=colors[idx+2], label=f"${4/case:.3f}$", alpha=0.8)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plot_ctp_av(ax[0])
    plt.savefig(f"{cwd}/figures/fft.pdf", bbox_inches="tight", dpi=300)


def main():
    plot_fft()
    # plot_ctp_av()
    # plot_ctf()
    # plot_ctf_av()


if __name__ == "__main__":
    cwd = os.getcwd()
    main()
