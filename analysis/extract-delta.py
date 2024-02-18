import os
from pathlib import Path
from matplotlib.lines import Line2D
import numpy as np


from lotusvis.plot_flow import Plots
from lotusvis.flow_field import ReadIn
from lotusvis.assign_props import AssignProps

from matplotlib import pyplot as plt
import seaborn as sns
import scienceplots
plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"



def extract_delta(re):
    # Extract the delta profiles for a given Reynolds number
    sim_dir = f"{Path.cwd()}/analysis/visualise-outer-scale/{re}k/0-2d"
    vel = ReadIn(sim_dir, 'fluid', 1024, ext='vti')
    snaps = vel.snaps
    profiles = np.zeros((np.shape(snaps)[0], np.shape(snaps)[2]))
    ys = np.zeros((np.shape(snaps)[0], np.shape(snaps)[2])) 
    for idx, s in enumerate(snaps):
        snap = AssignProps(s)
        index = np.argmin(abs(np.mean(snap.X, axis=2)-1))
        profiles[idx] = np.ravel(np.mean(snap.U, axis=2)[:, index])
        ys[idx] = np.ravel(np.mean(snap.Y, axis=2)[:, index])
    return profiles, ys


def delta(profs):
    '''
    Compute the mean positive and negative bl thickness.
    '''

    # Unpack the profiles
    u, y = profs

    # Preallocate the arrays
    positive, negative = np.empty(len(u)), np.empty(len(u))

    # Loop through the profiles
    for idx in range(len(u)):
        u = profs[0][idx]
        y = profs[1][idx]

        # Find the indices where u>0
        pos = np.where(u>0.)[0]

        # Split the profiles at the indices where the difference between indices is not equal to 1
        # This identifies the body and splits either side
        yout = np.split(y[pos],np.where(np.diff(pos)!=1)[0]+1)
        uout = np.split(u[pos],np.where(np.diff(pos)!=1)[0]+1)

        bl = []
        for jdx in range(2):
            # Get the maximum and minimum values from each top and bottom half 
            maxi, mini = np.max(uout[jdx]), np.min(uout[jdx])
            # Find the indices where the maximum and minimum values are
            pos_max, pos_min = np.where(uout[jdx]==maxi)[0], np.where(uout[jdx]==mini)[0]
            if pos_max.size > 1 or pos_min.size > 1:
                bls = abs(yout[jdx][pos_max]-yout[jdx][pos_min]).mean()
            else:
                bls = abs(yout[jdx][pos_max]-yout[jdx][pos_min])
            bl.append(bls)
        # print(bl, np.shape(bl))

        # Distinguish between pos and neg pressure gradients
        positive[idx] = min(bl)
        negative[idx] = max(bl)

    return positive, negative


def get_bl(profs):
    u, y = profs
    us, ys = [], []
    for idx in range(len(u)):
        u = profs[0][idx]
        y = profs[1][idx]

        pos = np.where(u>0.)[0]
        us.append(u[pos])
        ys.append(y[pos])
    return us, ys


def plot_re(ax, col, re):
    us, ys = get_bl(extract_delta(re))

    for idx in range(0, len(us)//2, 2):
        ax.plot(
            us[idx], ys[idx],
            color=col,
            ls='-.',
            alpha=0.7,
        )


def re_legend():
    legend_elements = [
        Line2D(
            [0],
            [0],
            ls="-.",
            label=r"$Re=6,000$",
            c=sns.color_palette('colorblind')[1],
            # marker="^",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="-.",
            label=r"$Re=12,000$",
            c=sns.color_palette('colorblind')[0],
            # marker="P",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="-.",
            label=r"$Re=24,000$",
            c=sns.color_palette('colorblind')[2],
            # marker="o",
            markerfacecolor="none",
        ),
    ]
    return legend_elements

        
def plot_bl_ontop():
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlabel(r"$u$")
    ax.set_ylabel(r"$y$")

    plot_re(ax, sns.color_palette('colorblind')[1], 6)
    plot_re(ax, sns.color_palette('colorblind')[0], 12)
    plot_re(ax, sns.color_palette('colorblind')[2], 24)

    ax.legend(handles=re_legend(), loc=2)
    
    plt.savefig(f"{Path.cwd()}/analysis/figures/bl-on-top.pdf", dpi=200, transparent=True)


def plot_bl_seperated():
    fig, ax = plt.subplots(3, figsize=(4,4))
    ax[2].set_xlabel(r"$u$")
    ax[1].set_ylabel(r"$y$")
    [ax.set_xticks([]) for ax in ax[:-1]]

    plot_re(ax[0], sns.color_palette('colorblind')[1], 6)
    plot_re(ax[1], sns.color_palette('colorblind')[0], 12)
    plot_re(ax[2], sns.color_palette('colorblind')[2], 24)

    for idx, ax in enumerate(ax):
        l2 = ax.legend(labels=[f"$\delta={delta(extract_delta(res[idx]))[0]:.3f}$"], loc=4)
        l1 = ax.legend(handles=[re_legend()[idx]], loc=2)
        ax.add_artist(l2)

    
    plt.savefig(f"{Path.cwd()}/analysis/figures/bl.pdf", dpi=200, transparent=True)

def plot_bl_time():
    fig, ax = plt.subplots(2, figsize=(4,4))
    ax[1].set_xlabel(r"$t$")
    ax[0].set_ylabel(r"$\delta_{pos}$")
    ax[1].set_ylabel(r"$\delta_{neg}$")
    [ax.set_xticks([]) for ax in ax[:-1]]

    res = [12, 6, 24]
    for idx, re in enumerate(res):
        pos = np.load(f"{Path.cwd()}/analysis/visualise-outer-scale/pos_{re}.npy")
        neg = np.load(f"{Path.cwd()}/analysis/visualise-outer-scale/neg_{re}.npy")
        t = np.linspace(0, 3, len(pos))
        ax[0].plot(t, pos, color=sns.color_palette('colorblind')[idx])
        print(np.std(pos))
        ax[1].plot(t, neg, color=sns.color_palette('colorblind')[idx])

    # for idx, ax in enumerate(ax):
    #     l2 = ax.legend(labels=[f"$\delta={delta(extract_delta(res[idx]))[0]:.3f}$"], loc=4)
    #     l1 = ax.legend(handles=[re_legend()[idx]], loc=2)
    #     ax.add_artist(l2)

    
    plt.savefig(f"{Path.cwd()}/analysis/figures/bl_t.pdf", dpi=200, transparent=True)


if __name__ == "__main__":
    res = [6, 12, 24]
    # plot_bl_seperated()
    # plot_bl_ontop()
    # for re in res:
    #     pos, neg = delta(extract_delta(re))
    #     np.save(f"{Path.cwd()}/analysis/visualise-outer-scale/pos_{re}.npy", pos, allow_pickle=True)
    #     np.save(f"{Path.cwd()}/analysis/visualise-outer-scale/neg_{re}.npy", neg, allow_pickle=True)
    plot_bl_time()
    # print(np.linspace(0,1, len(pos)), pos)