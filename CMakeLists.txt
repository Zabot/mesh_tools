cmake_minimum_required(VERSION 2.8.3)
project(mesh_tools)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_python_setup()

catkin_package()

install(PROGRAMS scripts/mesh_macro.py
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/scripts)

