#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from collections import deque


def read_forces(force_file, interest="p", direction="x"):
    names = [
        "t",
        "dt",
        "px",
        "py",
        "pz",
        "cp",
        "vx",
        "vy",
        "vz",
        "v1x",
        "v1y",
        "v1z",
        "v2x",
        "v2y",
        "v2z",
        "Eb",
        "Ew",
        "tkeb",
        "tkew",
        "E",
        "tke",
    ]
    fos = np.transpose(np.genfromtxt(force_file))

    forces_dic = dict(zip(names, fos))
    t = forces_dic["t"]
    u = forces_dic[interest + direction]

    u = np.squeeze(np.array(u))

    return t, u


def get_thrust(folder, c):
    t, u = read_forces(os.path.join(folder, "fort.9"))
    # t, vx, _ = read_forces(os.path.join(folder, 'fort.9'), interest='v')
    return np.mean(u[t > 4])  # + np.mean(vx[t > 4])


def get_power(folder):
    t, cp = read_forces(os.path.join(folder, "fort.9"), interest="cp")
    # print(f'Mean Cp={np.mean(cpy)}, RMS={np.sqrt(np.mean((cpy-np.mean(cpy))**2))}')
    return np.mean(abs(cp[t > 4]))


def get_power_rms(folder):
    t, cp = read_forces(os.path.join(folder, "fort.9"), interest="cp")
    cp = cp[t > 59.5]
    cp_rms = np.sqrt(np.mean((cp - np.mean(cp)) ** 2))
    return cp_rms


def vertical_rms(folder):
    t, u = read_forces(os.path.join(folder, "fort.9"))
    cy = u[t > 4]
    cy_rms = np.sqrt(np.mean((cy - np.mean(cy)) ** 2))
    return cy_rms


def thrust_rms(folder, c):
    t, u = read_forces(os.path.join(folder, "fort.9"), c)
    ct = u[t > 4]
    ct_rms = np.sqrt(np.mean((ct - np.mean(ct)) ** 2))
    return ct_rms


def extract_zet(fp):
    with open(fp, "r") as fileSource:
        file_lines = fileSource.readlines()
    txt = file_lines[24]
    return float([s for s in txt.split(" ")][-2][:-1])
