import numpy as np


def vorticity_x(flow: object) -> np.array:
    dv_dz = np.gradient(flow.V, axis=2, edge_order=2)
    dw_dy = np.gradient(flow.W, axis=1, edge_order=2)
    return dw_dy - dv_dz


def vorticity_y(flow: object) -> np.array:
    du_dz = np.gradient(flow.U, axis=2, edge_order=2)
    dw_dx = np.gradient(flow.W, axis=0, edge_order=2)
    return du_dz - dw_dx


def vorticity_z(flow: object) -> np.array:
    dv_dx = np.gradient(flow.V, axis=1, edge_order=2)
    du_dy = np.gradient(flow.U, axis=0, edge_order=2)
    return dv_dx - du_dy


def vorticity_mag(flow: object) -> np.array:
    try:
        mag = np.sqrt(vorticity_x(flow) ** 2 + vorticity_y(flow) ** 2 + vorticity_z(flow) ** 2)
    except ValueError:
        mag = np.sqrt(vorticity_z(flow) ** 2)
    return mag

