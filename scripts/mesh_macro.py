#!/usr/bin/env python

import resource_retriever

import mesh_tools


def auto_mesh(name, mesh_path, mass, rpy="0 0 0", scale="0.001 0.001 0.001"):
    scale_vector = list(map(float, scale.split(" ")))
    rpy_vector = list(map(float, rpy.split(" ")))
    mass = float(mass)

    mesh_file_path = resource_retriever.get_filename(mesh_path, False)
    mesh = mesh_tools.Mesh(mesh_file_path, rpy_vector, scale_vector, mass)

    params = mesh.get_params()
    params['name'] = name
    params['mesh_path'] = mesh_path
    params['scale'] = scale
    params['mass'] = mass
    params['rpy'] = rpy

    # TODO Save bounding box sizes and extrema as properties
    # to make composing easier
    return """<link name="{name}">
    <visual>
        <origin rpy="{rpy}"/>
        <geometry>
            <mesh filename="{mesh_path}" scale="{scale}"/>
        </geometry>
    </visual>
    <collision>
        <origin xyz="{geom_center[0]} {geom_center[1]} {geom_center[2]}" rpy="{rpy}"/>
        <geometry>
            <box size="{bounding_box[0]} {bounding_box[1]} {bounding_box[2]}"/>
        </geometry>
    </collision>
    <inertial>
        <mass value="{mass}"/>
        <origin xyz="{com[0]} {com[1]} {com[2]}" rpy="{rpy}"/>
        <inertia
            ixx="{i[0][0]}"
            ixy="{i[1][0]}" iyy="{i[1][1]}"
            ixz="{i[2][0]}" iyz="{i[2][1]}" izz="{i[2][2]}"
        />
    </inertial>
</link>""".format(**params)
