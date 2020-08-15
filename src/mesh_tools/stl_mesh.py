import stl


def load(mesh_file_path, scale):
    mesh = stl.mesh.Mesh.from_file(mesh_file_path)
    mesh.x *= scale[0]
    mesh.y *= scale[1]
    mesh.z *= scale[2]
    return mesh


def bounding_box(mesh):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in mesh.points:
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    geom_center = ((maxx+minx) / 2.0, (maxy+miny)/2.0, (maxz+minz)/2.0)
    bounding_box = (maxx-minx, maxy-miny, maxz-minz)
    extrema = ((minx, maxx), (miny, maxy), (minz, maxz))
    return geom_center, bounding_box, extrema


def can_get_inertia(mesh):
    return mesh.check()


def inertia(mesh, mass):
    volume, cog, inertia = mesh.get_mass_properties()
    return cog, inertia / volume * mass
