try:
    # this works for python 3.7 and lower
    from importlib.metadata import version, PackageNotFoundError
except (ModuleNotFoundError, ImportError):
    # this works for python 3.8 and higher
    from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("brep_part_finder")
except PackageNotFoundError:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)

__all__ = ["__version__"]


from .core import (
    get_part_properties_from_shapes,
    get_part_properties_from_shape,
    get_part_properties_from_file,
    get_matching_part_id,
    get_matching_part_ids,
    convert_shape_to_iterable_of_shapes,
)
