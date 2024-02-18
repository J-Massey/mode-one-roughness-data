#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
import seaborn as sns
from get_vort import vorticity_x
from matplotlib import pyplot as plt
from lotusvis.assign_props import AssignProps

import matplotlib.colors as colors
import numpy as np
import seaborn as sns
import scienceplots

plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{txfonts}')


def save_total_int():
    for idx, case in enumerate(cases):
        total_int = []
        for _, c in enumerate(cs[idx]):
            cell_volume = 4 / c * 2 / c
            phase_average = np.load(f"{cwd}/{case}x{case}/{str(c)}/phase_average.npy")
            temp = []
            for loop in phase_average:
                flow = AssignProps(loop)
                vortx = vorticity_x(flow) * cell_volume
                mag = np.sqrt((vortx) ** 2)

                temp.append(np.trapz(mag.flat))
                del flow
            total_int.append(temp)
            del phase_average
            print(f'Saved for {c}')

    total_int = np.array(total_int)
    total_int = total_int.T
    np.save(f"{cwd}/{case}x{case}/vortx.npy", total_int)

def plot_vortx_integral():
    fig, ax = plt.subplots(figsize=(4, 3.5))

    ax.set_ylabel(r"$ \int |\overline{\omega_x}| dV $")
    ax.set_xlabel(r"$ \Delta x $")
    ax.set_xlim(1e-3, 4e-2)
    lines = ['-', '-.']

    for idx, case in enumerate(cases):
        total_int = np.load(f"{cwd}/tidy_res_test/{case}x{case}/vortx.npy", allow_pickle=True)
        vort = np.mean(total_int, axis=0)
        dx = np.array([4 / c for c in cs[idx]])
        ax.plot(
            dx,
            vort,
            linestyle=lines[idx],
            color='k',
            markerfacecolor='none',
            label=f"$\lambda=1/{case}$",
        )

    # ax.set_xscale("log")
    ax.loglog()
    ax.legend()
    plt.savefig(
        f"{cwd}/tidy_res_test/figures/figure11.pdf",
        dpi=300,
        transparent=False,
    )
    plt.close()

if __name__ == "__main__":
    cwd = os.getcwd()
    cases = [16, 52]
    cs = np.array([[128, 256, 512, 1024, 2048], [520, 1040, 2080]], dtype=object)
    plot_vortx_integral()

