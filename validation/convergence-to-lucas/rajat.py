import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots
import matplotlib.animation as animation
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib import colors, pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
import scienceplots

plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"
plt.rcParams['savefig.bbox'] = 'tight' 

flow = np.load('data/vort.npy')
xlims, ylims = (-0.5, 2.5), (-0.9, 0.9)
print("Loaded")
nx, ny, nt = flow.shape
pxs = np.linspace(xlims[0], xlims[1], nx)
pys = np.linspace(ylims[0], ylims[1], ny)

nframes = nt
fn = 'vortsnap'
lim=[-0.1, 0.1]

fig, ax = plt.subplots(figsize=(5, 3))
# ax.set_yticks([])
# ax.axis('off')
ax.set_xlabel(r"$x/L$")
ax.set_ylabel(r"$y/L$")

norm = colors.Normalize(vmin=lim[0], vmax=lim[1])
levels = np.linspace(lim[0], lim[1], 44)


_cmap = sns.color_palette("seismic", as_cmap=True)
cs = ax.contourf(
    pxs,
    pys,
    flow[:,:,0].T,
    levels=levels,
    norm=norm,
    cmap=_cmap,
    vmin=lim[0],
    vmax=lim[1],
    extend="both",
)
divider = make_axes_locatable(ax)
cax = divider.append_axes("top", size="7%", pad=0.2)
fig.add_axes(cax)
cb = plt.colorbar(cs, cax=cax, orientation="horizontal", ticks=[-0.1, -0.05, 0.00, 0.05, 0.1])
cax.set_title(r"$\omega_z$")
ax.set_aspect(1)

plt.savefig("figures/vortsnap.pdf")
print("Plotted")