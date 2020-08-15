import collada
import numpy
import itertools


def load(mesh_file_path):
    return collada.Collada(mesh_file_path)


def bounding_box(mesh):
    # Find the extrema of each components
    min_bounds = []
    max_bounds = []

    for geometry in mesh.scene.objects('geometry'):
        for primitive in geometry.primitives():
            v = primitive.vertex
            min_bounds.append(v.min(axis=0))
            max_bounds.append(v.max(axis=0))

    # Find the global extrema
    min_bounds = numpy.array(min_bounds)
    max_bounds = numpy.array(max_bounds)

    mesh_min = min_bounds.min(axis=0)
    mesh_max = max_bounds.max(axis=0)

    # Calculate geometric properties
    geom_center = (mesh_min + mesh_max) / 2.0
    bounding_box = mesh_max - mesh_min
    extrema = numpy.array([mesh_min, mesh_max])
    return geom_center, bounding_box, extrema


def can_get_inertia(mesh):
    return False
