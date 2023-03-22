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
    fig, ax = plt.subplots(figsize=(4.5, 2.))
    ax.set_xlabel(f"$ x $")
    ax.set_ylabel(r"$ y $")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.25, 0.25)

    legend_elements = envelope_helper(ax, "1_3", 2)

    legend1 = plt.legend(handles=legend_elements, loc=3)

    legend_elements = [
        Line2D([0], [0], ls="--", label=r"Lucas et al. 2015", c="grey"),
        Line2D([0], [0], ls="-", label=r"Fitted", c="k"),
    ]

    ax.legend(handles=legend_elements, loc=2)
    plt.gca().add_artist(legend1)

    plt.savefig(
        f"{os.getcwd()}/figures/amplitude-envelopes.pdf", bbox_inches="tight", dpi=200
    )

def envelope_helper(ax, foil: str, n: int):
    kins = FitKinematics(amplitude_envelope(foil), kinematic_trajectory(foil))

    _, amp = amplitude_envelope(foil)
    print(abs(amp.max()))
    # ax.scatter(x, amp, color='grey')
    # ax.plot(x, kins.fit_poly(n)(x), color='k', ls=':')

    x = np.linspace(0, 1, 1000)
    zeta, ts = kins.fit_sine(n)
    print(zeta)
    print(
        [round(el, 4) for el in np.flip(kins.print_poly_coeffs(n))]
         )

    h = np.empty((len(ts), len(x)))
    for idx in range(len(ts)):
        h[idx] = kins.fit_poly(n)(x)*np.sin(2*np.pi*(x/2.15-ts[idx]))
        ax.plot(x, h[idx], color='k')

    x_exp, amp = kinematic_trajectory(foil)
    amp_exp = np.empty((len(x_exp), len(x)))
    for idx in range(len(x_exp)):
        f_amp = interp1d(x_exp[idx], amp[idx], fill_value="extrapolate")
        amp_exp[idx] = f_amp(x)
        ax.plot(x, amp_exp[idx], color='grey', ls='--', alpha=0.85)

    print(np.sqrt(np.sum((h.flatten()-amp_exp.flatten())**2))/h.flatten().shape[0])
    print(np.std(amp_exp-h)/np.std(amp_exp))

    legend_elements = [
        Line2D([], [], linestyle='None', label=f"$std(y[x,t]-fit(x,t))/std(y[x,t])$ = {np.sqrt(np.sum((h.flatten()-amp_exp.flatten())**2))/h.flatten().shape[0]:.2e}",),
        # Line2D([], [], linestyle='None', label=f"$L_2$ error = {np.linalg.norm(h-amp_exp, ord=2):.3f}",),
    ]
    return legend_elements


def amplitude_envelope(foil: str):
    x, amp = np.genfromtxt(f"{os.getcwd()}/raw-data/{foil}-h-l.csv", delimiter=", ").T
    x = np.linspace(0.0, 1.0, 13)
    return x, amp


def kinematic_trajectory(foil: str):
    x = np.linspace(0, 1, 1000)
    amp = np.empty((6, len(x)))
    for loop in range(6):
        x_raw, amp_raw = np.genfromtxt(
            f"{os.getcwd()}/raw-data/{foil}-kinematic-envelope/{int(loop+1)}.csv",
            delimiter=", ",
        ).T
        f = interp1d(
            x_raw / 180, amp_raw / 180, fill_value="extrapolate"
        )  # Normalise by foil length
        amp[loop - 1] = f(x)
    return np.array((np.tile(x, (6, 1)), amp))


class FitKinematics:
    def __init__(self, amp_data, kin_data) -> None:
        self.amp_data = amp_data
        self.kin_data = kin_data
    
    def print_poly_coeffs(self, n):
        x_data, y_data = self.amp_data
        return np.polyfit(x_data, y_data, n)
    
    def fit_poly(self, n):
        x_data, y_data = self.amp_data
        return np.poly1d(np.polyfit(x_data, y_data, n))

    def fit_sine(self, n):
        x_data, y_data = self.kin_data

        igz = 2.; ts = []
        for _ in range(50):
            zetas = []
            ts = []
            for xloop, yloop in zip(x_data,y_data):
                # First fit an initial guess at the appropriate cycle time
                    def t_finder(x, t):
                        return self.fit_poly(n)(x) * np.sin(2*np.pi*(x / igz - t))
                    popt, _ = curve_fit(t_finder, xloop, yloop)
                    t = popt[0]
                    ts.append(t)
                    # Now find the wavespeed to match
                    def zeta_finder(x, zeta):
                        return self.fit_poly(n)(x) * np.sin(2*np.pi*(x / zeta - t))
                    popt, _ = curve_fit(zeta_finder, xloop, yloop)
                    zetas.append(popt[0])
            igz = np.array(zetas).mean()
        return igz,ts


if __name__ == "__main__":
    plot_envelopes()
