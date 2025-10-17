import numpy as np
import pandas as pd
import pyvista as pv
import cmocean


df = pd.read_csv('data/KohlerPopeSmith.csv')
vel_mag = np.sqrt(df['velx']**2 + df['vely']**2)

x_unique = np.unique(df['x'])
y_unique = np.unique(df['y'])
xx, yy = np.meshgrid(x_unique, y_unique)
shape = xx.shape

zz = np.nan_to_num(df['surf'].values.reshape(shape), nan=0.0)
vel_grid = vel_mag.values.reshape(shape)

xx = xx.astype(np.float32)
yy = yy.astype(np.float32)
zz = zz.astype(np.float32)

z_exaggeration = 10
zz_exag = zz * z_exaggeration

# Extend grid in x-direction
extra_x = np.full((xx.shape[0], 1), xx.min() - 40000, dtype=np.float32)
xx_ext = np.hstack([extra_x, xx])
yy_ext = np.hstack([yy[:, 0:1], yy])
zz_ext = np.hstack([np.zeros((zz_exag.shape[0], 1), dtype=np.float32), zz_exag])
vel_ext = np.hstack([np.zeros((vel_grid.shape[0], 1), dtype=np.float32), vel_grid])

grid_ext = pv.StructuredGrid(xx_ext, yy_ext, zz_ext)
grid_ext['Velocity'] = vel_ext.ravel(order='F')

# Plot
p = pv.Plotter()

# Mesh with vertical color bar
p.add_mesh(
    grid_ext,
    scalars='Velocity',
    cmap=cmocean.cm.dense,
    show_edges=False,
    scalar_bar_args={
        "title": "Velocity Magnitude (m/yr)",
        "vertical": True,
        "title_font_size": 18,
        "label_font_size": 14,
        "color": "black",
        "fmt": "%.2f",
        "position_x": 0.88,
        "position_y": 0.1,
        "height": 0.8,
        "width": 0.04
    }
)

# Grid and axis labels
p.show_grid(
    location='outer',
    xtitle='Polar Stereographic Easting (m)',
    ytitle='Polar Stereographic Northing (m)',
    ztitle=f'Surface Elevation * {z_exaggeration} (m)',
    n_zlabels=2,
    n_ylabels=4,
    fmt="%.0f",
    use_3d_text=False,
    padding=0.05,
)

# Use saved camera position as starting point
saved_camera = [
    (-1968892.882139573, -237129.68811485582 + 100000, 312324.56602184003),
    (-1492000.0, -635750.0, 17670.0),
    (0.325983774305665, -0.2779328938107925, 0.9035971920205331)
]
p.camera_position = saved_camera

p.show()
