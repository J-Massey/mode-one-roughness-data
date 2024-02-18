import os
import time
from tkinter import Tcl

from lotusvis.flow_field import ReadIn


def fluid_snap(sim_dir, fn, count):
    fsim = ReadIn(sim_dir, 'fluid', 4096, ext="vti")
    fsim.u_low_memory_saver(fn, count, "./data")
    fsim.v_low_memory_saver(fn, count, "./data")


def body_snap(sim_dir, fn, count):
    bsim = ReadIn(sim_dir, 'bodyF', 4096, ext="vti")
    bsim.save_sdf_low_memory(fn, count, "./data")


# Specify the directory to monitor
directory_to_watch = "./4096"
print("Watching directory:", directory_to_watch)


bcount=0
fcount = 0
delete_count = 0
while True:
    time.sleep(1)
    for root, _, files in os.walk(directory_to_watch):
        time.sleep(1)
        # Process files
        for file in files:
            print("File created:", os.path.join(root, file))
            if root.endswith("datp"):
                # Buffer to allow finish writing
                time.sleep(1)
                # Sort the files
                dpdfs = [fp for fp in os.listdir(root)]
                dpdfs = Tcl().call("lsort", "-dict", dpdfs)
                for fn in dpdfs:
                    if fn.startswith("bodyF"):
                        path = os.path.join(root, fn)
                        body_snap(directory_to_watch, path, bcount)
                        os.remove(path)
                        bcount += 1
                    elif fn.startswith("fluid"):
                        path = os.path.join(root, fn)
                        fluid_snap(directory_to_watch, path, fcount)
                        os.remove(path)
                        fcount += 1
    for root, _, files in os.walk(directory_to_watch):
        for file in files:
            if (file.startswith("fluid") or file.startswith("bodyF")) and \
            (not file.endswith(".pvtr") and not file.endswith(".vtr") and not file.endswith("vtr.pvd")):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                delete_count += 1

# bmask(count)
    print(f"Total files deleted: {delete_count}")

    # Sleep for a certain duration before checking again
    time.sleep(2)
