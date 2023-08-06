import os

import paramak

my_reactor = paramak.BallReactor(rotation_angle=90)

# order of parts gets mixed when saved to brep file
my_reactor.export_dagmc_h5m(
    filename="dagmc.h5m",
    min_mesh_size=5,
    max_mesh_size=10,
    exclude=[
        "plasma"
    ],  # does not mesh the plasma as not many neutron interactions occur
)

# converting for viewing geometry in Paraview / Visit using the Moab tool mbconvert
# os.system("mbconvert dagmc.h5m dagmc.vtk")
