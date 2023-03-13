#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lotus import run
from changef90 import new_f90_res
from pathlib import Path
import numpy as np

def extract_k():
    with open("lotus.f90","r") as fileSource:
        fileLines = fileSource.readlines()
    txt = fileLines[24]
    return float([s for s in txt.split(' ')][-2][:-1])


def run_val(L):
    run(64, f'{cwd}/{L}')

if __name__ == "__main__":
    cwd = Path.cwd()
    Ls = [1024]
    [run_val(L) for L in Ls]
    
