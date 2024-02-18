
import os
from tkinter import Tcl

import numpy as np

def bmask():
    fnsu, fnsv, fnsb = fns()
    for idx, (fnu, fnv, fnb) in enumerate(zip(fnsu, fnsv, fnsb)):
        u = np.load(os.path.join("./data", fnu))
        v = np.load(os.path.join("./data", fnv))
        b = np.load(os.path.join("./data", fnb))
        bmask = np.where(b <= 1, False, True)
        u = np.where(bmask, u, 0)
        print(u.shape)
        np.save(os.path.join("./data", f"u_{idx+20}"), u)
        v = np.where(bmask, v, 0)
        np.save(os.path.join("./data", f"v_{idx+20}"), v)
        # Now remove the files
        print(f"Removing {fnu}, {fnv}, {fnb}")
        try:
            os.remove(os.path.join("./data", fnu))
            os.remove(os.path.join("./data", fnv))
            os.remove(os.path.join("./data", fnb))
        except FileNotFoundError:
            pass


def fns():
    fnsu = [
        fn
        for fn in os.listdir("./data")
        if fn.startswith("fluid_u") and fn.endswith(f".npy")
    ]
    fnsu = Tcl().call("lsort", "-dict", fnsu)
    fnsv = [
        fn
        for fn in os.listdir("./data")
        if fn.startswith("fluid_v") and fn.endswith(f".npy")
    ]
    fnsv = Tcl().call("lsort", "-dict", fnsv)
    fnsb = [
        fn
        for fn in os.listdir("./data")
        if fn.startswith('bodyF') and fn.endswith(f".npy")
    ]
    fnsb = Tcl().call("lsort", "-dict", fnsb)
    return fnsu, fnsv, fnsb

if __name__ == "__main__":
    bmask()