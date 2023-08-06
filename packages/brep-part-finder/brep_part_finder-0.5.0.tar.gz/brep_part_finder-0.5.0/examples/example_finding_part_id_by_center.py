# In this example there are two parts in the Brep file that match the specified
# center coordinates provided

import brep_part_finder as bpf


# brep file is imported
my_brep_part_properties = bpf.get_part_properties_from_file("ball_reactor.brep")

# from the printed json dictionary we know that there is are two parts with a
# volume 95467959.26023674 which is the blanket_rear_wall component
part_id = bpf.get_matching_part_id(
    brep_part_properties=my_brep_part_properties,
    center_x=0,
    center_y=0,
    center_z=0,
    center_atol=1e-6,
)

# prints the part id found
# in this case there are several parts found with this center of mass
print(f" there is {len(part_id)} with a matching volume")
print(f" the part id with a matching volume is {part_id}")
