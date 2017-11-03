#!/usr/bin/env python

import numpy
import stl

def get_bounding_box(mesh):
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
    geom_center = ((maxx-minx) / 2.0, (maxy-miny)/2.0, (maxz-minz)/2.0)
    bounding_box = (maxx-minx, maxy-miny, maxz-minz)
    extrema = ((minx, maxx), (miny, maxy), (minz, maxz))
    return geom_center, bounding_box, extrema

def mesh(name, mesh_path, rpy="0 0 0", scale="0.001 0.001 0.001"):
    scale_vector = map(float, scale.split(" "))
    rpy_vector = map(float, rpy.split(" "))

    mesh = stl.mesh.Mesh.from_file(mesh_path)

    mesh.x *= scale_vector[0]
    mesh.y *= scale_vector[1]
    mesh.z *= scale_vector[2]

    mesh.rotate([1,0,0], rpy_vector[0])
    mesh.rotate([0,1,0], rpy_vector[1])
    mesh.rotate([0,0,1], rpy_vector[2])

    volume, cog, inertia = mesh.get_mass_properties()
    geom_center, bounding_box, extrema = get_bounding_box(mesh)

    # Take absolute value of extrema
    extrema = numpy.absolute(extrema)

    # TODO Save bounding box sizes and extrema as properties
    # to make composing easier
    return """<link name="{name}">
    <visual>
        <origin rpy="{rpy}"/> 
        <geometry>
            <mesh filename="file://{mesh_path}" scale="{scale}"/>
        </geometry>
    </visual>
    <collision>
        <origin xyz="{geom_center[0]} {geom_center[1]} {geom_center[2]}"/> 
        <geometry>
            <box size="{bounding_box[0]} {bounding_box[1]} {bounding_box[2]}"/>
        </geometry>
    </collision>
    <inertial>
        <mass value="{mass}"/>
        <origin xyz="{com[0]} {com[1]} {com[2]}"/> 
        <inertia
            ixx="{i[0][0]}" 
            ixy="{i[1][0]}" iyy="{i[1][1]}" 
            ixz="{i[2][0]}" iyz="{i[2][1]}" izz="{i[2][2]}"
        />
    </inertial>
</link>""".format(name=name, geom_center=geom_center, bounding_box=bounding_box,
        com=cog, mass=volume, scale=scale, i=inertia, extrema=extrema, rpy=rpy, mesh_path=mesh_path)

