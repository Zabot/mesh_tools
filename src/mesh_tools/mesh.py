import numpy
import math

from mesh_tools import collada_mesh, stl_mesh


class Mesh:
    def __init__(self, filepath, rpy, scale, mass):
        self.scale = scale
        self.mass = mass
        self.rpy = self.rpy_to_matrix(rpy)

        supported_extensions = {
            'dae': 'collada',
            'stl': 'stl',
        }
        try:
            self.type = supported_extensions[filepath.split('.')[-1]]
        except KeyError as e:
            raise ValueError("Unsupported file extensions", e)

        if self.type == 'collada':
            self.mesh = collada_mesh.load(filepath)
        elif self.type == 'stl':
            self.mesh = stl_mesh.load(filepath, scale)

    def get_params(self):
        geom_center, bounding_box, extrema = self.bounding_box()

        # If we can, compute the real inertial properties of the mesh
        if self.can_get_inertia():
            cog, inertia = self.inertia()

        else:
            # Otherwise, use the geometric center and assume cuboid
            cog = geom_center
            inertia = numpy.eye(3)
            inertia[0][0] = 1/12.0 * (bounding_box[1] ** 2
                                      + bounding_box[2]**2)
            inertia[1][1] = 1/12.0 * (bounding_box[0] ** 2
                                      + bounding_box[2]**2)
            inertia[2][2] = 1/12.0 * (bounding_box[0] ** 2
                                      + bounding_box[1]**2)
            inertia = inertia * self.mass

        return {
                'geom_center': self.rpy.dot(geom_center),
                'bounding_box': bounding_box,
                'i': inertia,
                'com': self.rpy.dot(cog),
            }

    def bounding_box(self):
        if self.type == 'collada':
            (geom_center,
             bounding_box,
             extrema) = collada_mesh.bounding_box(self.mesh)

            return (geom_center * self.scale,
                    bounding_box * self.scale,
                    extrema * self.scale)

        elif self.type == 'stl':
            return stl_mesh.bounding_box(self.mesh)

    def can_get_inertia(self):
        if self.type == 'collada':
            return collada_mesh.can_get_inertia(self.mesh)

        elif self.type == 'stl':
            return stl_mesh.can_get_inertia(self.mesh)

    def inertia(self):
        if self.type == 'stl':
            return stl_mesh.inertia(self.mesh, self.mass)

    def rpy_to_matrix(self, rpy):
        r = numpy.array([
                [1,                0,                 0],
                [0, math.cos(rpy[0]), -math.sin(rpy[0])],
                [0, math.sin(rpy[0]),  math.cos(rpy[0])],
        ])
        p = numpy.array([
                [ math.cos(rpy[1]), 0, math.sin(rpy[1])],
                [                0, 1,                0],
                [-math.sin(rpy[1]), 0, math.cos(rpy[1])],
        ])
        y = numpy.array([
                [math.cos(rpy[2]), -math.sin(rpy[2]), 0],
                [math.sin(rpy[2]),  math.cos(rpy[2]), 0],
                [               0,                 0, 1],
        ])

        return r * p * y
