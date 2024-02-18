#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from collections import deque


def new_f90(c, k, st=0.3, lambda_x=0.0, lambda_z=0.0, h=0.01):
    with open("lotus.f90", "r") as fileSource:
        fileLines = fileSource.readlines()

    fileLines[14] = f"    real,parameter     :: c={float(c)}, nu=c/Re\n"
    fileLines[
        20
    ] = f"    real, parameter    :: A = 0.1*c, St_d = {st}, k_x={lambda_x}, k_z={lambda_z}, h_roughness={h}\n"
    fileLines[24] = f"                          k_coeff = {k}, &\n"

    with open("lotus.f90", "w") as fileOutput:
        fileOutput.writelines(fileLines)


def read_forces(force_file, interest="p"):
    names = ["t", "dt", "px", "py", "pz", "cpx", "cpy", "cpz", "vx", "vy", "vz"]
    fos = np.transpose(np.genfromtxt(force_file))

    forces_dic = dict(zip(names, fos))
    t = forces_dic["t"]
    u = np.array((forces_dic[interest + "x"], forces_dic[interest + "y"]))

    ux, uy = np.squeeze(np.array(u[0])), np.squeeze(np.array(u[1]))

    ux, uy = ux * 0.2 / 2.12, uy * 0.2 / 2.12

    return t, ux, uy


def get_thrust(folder, c):
    t, ux, _ = read_forces(os.path.join(folder, "fort.9"))
    # t, vx, _ = read_forces(os.path.join(folder, 'fort.9'), interest='v')
    return np.mean(ux[t > 4])  # + np.mean(vx[t > 4])


def get_power(folder):
    t, _, cpy = read_forces(os.path.join(folder, "fort.9"), interest="cp")
    # print(f'Mean Cp={np.mean(cpy)}, RMS={np.sqrt(np.mean((cpy-np.mean(cpy))**2))}')
    return np.mean(abs(cpy[t > 4]))


def get_power_rms(folder):
    t, _, cpy = read_forces(os.path.join(folder, "fort.9"), interest="cp")
    cp = cpy[t > 59.5]
    cp_rms = np.sqrt(np.mean((cp - np.mean(cp)) ** 2))
    return cp_rms


def vertical_rms(folder):
    t, ux, uy = read_forces(os.path.join(folder, "fort.9"))
    cy = uy[t > 4]
    cy_rms = np.sqrt(np.mean((cy - np.mean(cy)) ** 2))
    return cy_rms


def thrust_rms(folder, c):
    t, ut, uy = read_forces(os.path.join(folder, "fort.9"), c)
    ct = ut[t > 4]
    ct_rms = np.sqrt(np.mean((ct - np.mean(ct)) ** 2))
    return ct_rms


def extract_zet(fp):
    with open(fp, "r") as fileSource:
        file_lines = fileSource.readlines()
    txt = file_lines[24]
    return float([s for s in txt.split(' ')][-2][:-1])

