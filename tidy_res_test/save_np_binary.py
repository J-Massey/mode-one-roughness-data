#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np

from lotusvis.decompositions import Decompositions


def save_phase_avg():
    cwd = os.getcwd()
    
    for idx, c in enumerate(cs):
        fns = os.listdir(f"{cwd}/{case}/{str(c)}")
        if 'phase_average.npy' in fns:
            print(f'{case} has a np binary')
        else:
            phase_av = Decompositions(f"{cwd}/{case}/{str(c)}", "fluid", length_scale=c).phase_average(4)
            np.save(f"{cwd}/{case}/{str(c)}/phase_average.npy", phase_av)
            print(f'Saved phase_average.npy for {case}')
            del phase_av


def save_phase_avg_2d():
    for idx, c in enumerate(cs):
        fns = os.listdir(f"{cwd}/{case}/2D")
        if 'phase_average.npy' in fns:
            print(f'{case} has a np binary')
        else:
            phase_av = Decompositions(f"{cwd}/{case}/2D", "fluid", length_scale=c).phase_average(4)
            np.save(f"{cwd}/{case}/2D/phase_average.npy", phase_av)
            print(f'Saved phase_average.npy for {case}')
            del phase_av


def main():
    save_phase_avg()
    save_phase_avg_2d()


if __name__ == "__main__":
    cwd = os.getcwd()
    case = '16x16'
    cs = np.array([128, 256, 512, 1024, 2048])
    case = '52x52'
    cs = np.array([520, 1040, 2080])
    main()
