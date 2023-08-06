#!/usr/bin/env python3

"""
plugin that is loaded one time only at the beginning
It is meant to be for you to upload your environment
"""

import rospy
import os

ENV_PATH = '/home/saun/My_DQN_MB_model/src/turtlebot3_simulations/turtlebot3_gazebo/models/training_maze/env.urdf'
class Environment:
    def __init__(self, pybullet, **kargs):
        # get "import pybullet as pb" and store in self.pb
        self.pb = pybullet
        # enable soft body simulation if needed
        if rospy.get_param('~use_deformable_world', False):
            rospy.loginfo('Using deformable world (soft body simulation)')
            self.pb.resetSimulation(self.pb.RESET_USE_DEFORMABLE_WORLD)

    def load_environment(self):
        """
        set gravity, ground plane and load URDF or SDF models as required
        """
        # set gravity
        self.pb.setGravity(0, 0, -9.81)
        # set floor
        plane_pos = rospy.get_param("~plane_pos", [0, 0, 0])
        self.pb.loadURDF('plane.urdf', basePosition=plane_pos)
        self.env = self.pb.loadURDF(ENV_PATH)
        org_env_orientation = self.pb.getQuaternionFromEuler([0,0,0])
        self.pb.resetBasePositionAndOrientation(self.env, [0,0,0],org_env_orientation)
        self.load_environment_via_code()

    def load_environment_via_code(self):
        """
        This method provides the possibility for the user to define an environment via python code
        example:
        self.pb.loadURDF(...)
        self.pb.loadSDF(...)
        self.pb.loadSoftBody(...)
        self.pb.setTimeStep(0.001)
        self.pb.setPhysicsEngineParameter(sparseSdfVoxelSize=0.25) # ? related to soft bodies
        etc...
        NOTE: is not advised to directly write code below, instead make new class and inherit from this one
              see example: environment_template.py
        """
        pass
