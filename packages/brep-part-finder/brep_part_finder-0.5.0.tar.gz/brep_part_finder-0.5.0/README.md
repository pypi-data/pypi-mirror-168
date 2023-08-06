[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CI with install](https://github.com/fusion-energy/brep_part_finder/actions/workflows/ci_with_install.yml/badge.svg)](https://github.com/fusion-energy/brep_part_finder/actions/workflows/ci_with_install.yml)

[![Upload Python Package](https://github.com/fusion-energy/brep_part_finder/actions/workflows/python-publish.yml/badge.svg)](https://github.com/fusion-energy/brep_part_finder/actions/workflows/python-publish.yml)
[![anaconda-publish](https://github.com/fusion-energy/brep_part_finder/actions/workflows/anaconda-publish.yml/badge.svg)](https://github.com/fusion-energy/brep_part_finder/actions/workflows/anaconda-publish.yml)

Brep-part-finder is able to search within a Brep file for parts that match user
specified properties such as volume, center of mass and bounding box. The
matching ID number of the part will be returned if found.

This is useful because the order or parts changes when exporting to Brep files.
This part finder package helps keep track of meta data within a workflow.
The [neutronics workflow](https://github.com/fusion-energy/neutronics-workshop)
makes use of this package to help correctly identify materials when making
[DAGMC](https://github.com/svalinn/DAGMC/) h5m files from 
[Paramak](https://github.com/fusion-energy/paramak) geometries for neutronics
simulations.

# Installation (Conda)

The installation instructions below create a new conda enviroment and install 

```bash
conda create --name bpf_env
conda activate bpf_env
conda install -c cadquery -c fusion-energy -c conda-forge brep_part_finder
```

# Installation (Conda + Pip)

The installation instructions below create a new conda enviroment, install CadQuery and install this package.
The master branch of CadQuery is currently required as latest features are required.
When CadQuery version 2.2 is released then install can target a stable version.

```bash
conda create --name bpf_env
conda activate bpf_env
conda install -c cadquery -c conda-forge cadquery=master
pip install brep_part_finder
```

# Usage

To view the properties of the parts in the Brep file the first stage is to import the package and make use of the ```get_brep_part_properties``` function.

```
import brep_part_finder as bpf

my_brep_part_properties = bpf.get_brep_part_properties('my_brep_file.brep')

print(my_brep_part_properties)
>>>{
    1: {
        'Center.x': 0, 'Center.y': 0, 'Center.z': 0,
        'Volume': 10,
        'BoundingBox.xmin': -20, 'BoundingBox.ymin': -20, 'BoundingBox.zmin': -20,
        'BoundingBox.xmax': 20, 'BoundingBox.ymax': 20, 'BoundingBox.zmax': 20
       },
     2: {
         'Center.x': 5, 'Center.y': 6, 'Center.z': 7,
         'Volume': 10,
         'BoundingBox.xmin': -40.0, 'BoundingBox.ymin': -40.0, 'BoundingBox.zmin': -40.0,
         'BoundingBox.xmax': 40.0, 'BoundingBox.ymax': 40.0, 'BoundingBox.zmax': 40.0
        },
     3: {
         'Center.x': 0, 'Center.y': 0, 'Center.z': 0,
         'Volume': 10,
         'BoundingBox.xmin': -10, 'BoundingBox.ymin': -10, 'BoundingBox.zmin': -10,
         'BoundingBox.xmax': 10, 'BoundingBox.ymax': 10, 'BoundingBox.zmax': 10
        } 
    }
```

From the above dictionary it is possible to identify parts from their central of mass (x,y,z coordinate), volume and bounding box. This can be done manually or one can pass the required properties into the ```find_part_id``` or ```find_part_ids``` functions to identify the part numbers of solids automatically.

A minimal example that finds the part id numbers with matching volumes
```python
import brep_part_finder as bpf

my_brep_part_properties = bpf.get_brep_part_properties('my_brep_file.brep')
part_id = bpf.find_part_id(
    brep_part_properties=my_brep_part_properties,
    volume=10,

)

print(part_id)
>> [1, 3, 4]
```

The above example found 3 part ids with matching volumes.

The follow example also specifies the center of mass which helps narrow down the part ids to just to matching parts.
```python
import brep_part_finder as bpf

my_brep_part_properties = bpf.get_brep_part_properties('my_brep_file.brep')
part_id = bpf.find_part_id(
    brep_part_properties=my_brep_part_properties,
    volume=10,
    center_of_mass=(0,0,0),
)

print(part_id)
>> [1, 3]
```

In the this example the bounding box of the part has also been specified and these three pieces of information are enough to find one part that matches all three criteria.
```python
import brep_part_finder as bpf

my_brep_part_properties = bpf.get_brep_part_properties('my_brep_file.brep')
part_id = bpf.find_part_id(
    brep_part_properties=my_brep_part_properties,
    volume=10,
    center_of_mass=(0,0,0),
    bounding_box = [[10,10,10], [-10,-10,10]]
)

print(part_id)
>> [3]
```

For more usage examples see the [examples](https://github.com/fusion-energy/brep_part_finder/tree/main/examples) folder in this repository

# Combining with Paramak

When reactor models made with Paramak are exported to Brep files it is likely that the order of parts in the Brep file does not match the order of parts within the Paramak object. Therefore this program is useful when identifying parts in the Brep file. See the [paramak_example](https://github.com/fusion-energy/brep_part_finder/blob/main/examples/paramak_example.py) file in the examples folder of this repository.
