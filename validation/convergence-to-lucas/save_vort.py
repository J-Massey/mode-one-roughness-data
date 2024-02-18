import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots
plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"

xlims, ylims = (-0.5, 2.5), (-0.9, 0.9)

u = np.load(f"data/u.npy")
u = np.einsum("ijk -> kji", u)
v = np.load(f"data/v.npy")
v = np.einsum("ijk -> kji", v)

print("Loaded snap")

nx, ny, nt = u.shape
pxs = np.linspace(xlims[0], xlims[1], nx)
pys = np.linspace(ylims[0], ylims[1], ny)

dvdx = np.gradient(v, 4096*np.diff(pxs).mean(), axis=0, edge_order=2)
dudy = np.gradient(u, 4096*np.diff(pys).mean(), axis=1, edge_order=2)
vort = dvdx - dudy
print(vort.shape)
np.save("data/vort.npy", vort)
print("Saved vort")

fig, ax = plt.subplots(figsize=(5, 3))
lim = [-.05, .05]
levels = np.linspace(lim[0], lim[1], 44)
_cmap = sns.color_palette("seismic", as_cmap=True)
cs = ax.contourf(
    pxs,
    pys,
    vort[:,:,0].T,
    levels=levels,
    vmin=lim[0],
    vmax=lim[1],
    # norm=norm,
    cmap=_cmap,
    extend="both",
)
ax.set_aspect(1)
plt.savefig("figures/vortsnap.pdf")
print("Plotted")

# xlims, ylims = (-0.35, 2), (-0.35, 0.35)

# # vort = np.load("vort.npy")

# # print("Loaded")

# nx, ny, nt = vort.shape
# pxs = np.linspace(xlims[0], xlims[1], nx)
# pys = np.linspace(ylims[0], ylims[1], ny)


# # Just consider the wake
# wake_u = u[pxs>1, :, :]
# wake_v = v[pxs>1, :, :]
# wake_vort = vort[pxs>1, :, :]

# print("Waked")

# xlims, ylims = (1, 2), (-0.35, 0.35)
# nx, ny, nt = wake_vort.shape
# pxs = np.linspace(xlims[0], xlims[1], nx)
# pys = np.linspace(ylims[0], ylims[1], ny)

# np.save("10k/wake_u.npy", wake_u)
# np.save("10k/wake_v.npy", wake_v)
# np.save("10k/wake_vort.npy", wake_vort)

# print("Saved wake")

# np.save("10k/wake_u_quarter.npy", wake_u[:,:,0:nt//4])
# np.save("10k/wake_v_quarter.npy", wake_v[:,:,0:nt//4])
# np.save("10k/wake_vort_quarter.npy", wake_vort[:,:,0:nt//4])

# print("Saved wake quarter")


# fig, ax = plt.subplots(figsize=(5, 3))
# lim = [-.05, .05]
# levels = np.linspace(lim[0], lim[1], 44)
# _cmap = sns.color_palette("seismic", as_cmap=True)
# cs = ax.contourf(
#     pxs,
#     pys,
#     wake_vort[:,:,50].T,
#     levels=levels,
#     vmin=lim[0],
#     vmax=lim[1],
#     # norm=norm,
#     cmap=_cmap,
#     extend="both",
# )
# ax.set_aspect(1)
# plt.savefig("figures/testplotvortwake.pdf")


print("Finished")