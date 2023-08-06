#!/usr/bin/env python3

"""
RGBD camera sensor simulation for RosGymBullet base on pybullet.getCameraImage()
"""

import math
import numpy as np
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CameraInfo
import os
import yaml
from yaml.loader import SafeLoader

class RGBDCamera:
    def __init__(self, pybullet, robot, **kargs):
        # get "import pybullet as pb" and store in self.pb
        self.pb = pybullet
        # get robot from parent class
        self.robot = robot
        # create ros_rgb_image_msg placeholder for publication
        self.rgb_image_msg = Image()
        self.depth_image_msg = Image()
        # get RGBD camera parameters from ROS param server
        self.rgb_image_msg.width = rospy.get_param('~rgbd_camera/resolution/width', 640)
        self.rgb_image_msg.height = rospy.get_param('~rgbd_camera/resolution/height', 480)
        assert(self.rgb_image_msg.width > 5)
        assert(self.rgb_image_msg.height > 5)
        self.depth_image_msg.width = rospy.get_param('~rgbd_camera/resolution/width', 640)
        self.depth_image_msg.height = rospy.get_param('~rgbd_camera/resolution/height', 480)
        assert(self.depth_image_msg.width > 5)
        assert(self.depth_image_msg.height > 5)
        cam_frame_id = rospy.get_param('~rgbd_camera/frame_id', "kinect_link")
        if not cam_frame_id:
            rospy.logerr('Required parameter rgbd_camera/frame_id not set, will exit now...')
            rospy.signal_shutdown('Required parameter rgbd_camera/frame_id not set')
            return
        # get pybullet camera link id from its name
        link_names_to_ids_dic = kargs['link_ids']
        if not cam_frame_id in link_names_to_ids_dic:
            rospy.logerr('Camera reference frame "{}" not found in URDF model'.format(cam_frame_id))
            rospy.logwarn('Available frames are: {}'.format(link_names_to_ids_dic))
            rospy.signal_shutdown('required param rgbd_camera/frame_id not set properly')
            return
        self.pb_camera_link_id = link_names_to_ids_dic[cam_frame_id]
        self.rgb_image_msg.header.frame_id = cam_frame_id
        self.depth_image_msg.header.frame_id = cam_frame_id
        # create publisher
        queue_size_cfg = rospy.get_param('~rgbd_camera/queue_size_cfg', 10)
        # rgb_image
        self.pub_rgb_image = rospy.Publisher('kinect/rgb/image_raw', Image, queue_size=queue_size_cfg)
        self.rgb_image_msg.encoding = rospy.get_param('~rgbd_camera/resolution/rgb_encoding', 'rgb8')
        self.rgb_image_msg.is_bigendian = 0
        self.rgb_image_msg.step = rospy.get_param('~rgbd_camera/resolution/rgb_step', 1920)
        # depth_image
        self.pub_depth_image = rospy.Publisher('kinect/depth/image_raw', Image, queue_size=queue_size_cfg)
        self.depth_image_msg.encoding = rospy.get_param('~rgbd_camera/resolution/depth_encoding', '16UC1')
        self.depth_image_msg.is_bigendian = 0
        self.depth_image_msg.step = rospy.get_param('~rgbd_camera/resolution/depth_step', 1280)
        # projection matrix
        self.hfov = rospy.get_param('~rgbd_camera/hfov', 56.3)
        self.vfov = rospy.get_param('~rgbd_camera/vfov', 43.7)
        self.near_plane = rospy.get_param('~rgbd_camera/near_plane', 0.4)
        self.far_plane = rospy.get_param('~rgbd_camera/far_plane', 8)
        self.projection_matrix = self.compute_projection_matrix()
        # use cv_bridge ros to convert cv matrix to ros format
        self.image_bridge = CvBridge()
        # variable used to run this plugin at a lower frequency, HACK
        self.count = 0
        # publishing depth/camera_info topic
        # depth_file = os.path.join(os.path.dirname(__file__), "depth_msg.yaml")
        depth_file = rospy.get_param('~depth_cfg', "/home/saun/My_DQN_MB_model/src/dqn_mb/config/depth_msg.yaml")
        with open(depth_file, "r") as depth_file_handle:
            depth_data = yaml.load(depth_file_handle, Loader=SafeLoader)
        self.depth_camera_info_msg = CameraInfo()
        self.depth_camera_info_msg.width = depth_data["image_width"]
        self.depth_camera_info_msg.height = depth_data["image_height"]
        self.depth_camera_info_msg.K = depth_data["camera_matrix"]["data"]
        self.depth_camera_info_msg.D = depth_data["distortion_coefficients"]["data"]
        self.depth_camera_info_msg.R = depth_data["rectification_matrix"]["data"]
        self.depth_camera_info_msg.P = depth_data["projection_matrix"]["data"]
        self.depth_camera_info_msg.distortion_model = "plumb_bob"
        self.pub_depth_info_msg = rospy.Publisher('kinect/depth/camera_info', CameraInfo, queue_size=10)
        # publishing rgb/camera_info topic
        # rgb_file = os.path.join(os.path.dirname(__file__), "rgb_msg.yaml")
        rgb_file = rospy.get_param('~rgb_cfg', "/home/saun/My_DQN_MB_model/src/dqn_mb/config/rgb_msg.yaml")
        with open(rgb_file, "r") as rgb_file_handle:
            rgb_data = yaml.load(rgb_file_handle, Loader=SafeLoader)
        self.rgb_camera_info_msg = CameraInfo()
        self.rgb_camera_info_msg.width = rgb_data["image_width"]
        self.rgb_camera_info_msg.height = rgb_data["image_height"]
        self.rgb_camera_info_msg.K = rgb_data["camera_matrix"]["data"]
        self.rgb_camera_info_msg.D = rgb_data["distortion_coefficients"]["data"]
        self.rgb_camera_info_msg.R = rgb_data["rectification_matrix"]["data"]
        self.rgb_camera_info_msg.P = rgb_data["projection_matrix"]["data"]
        self.rgb_camera_info_msg.distortion_model = "plumb_bob"
        self.pub_rgb_info_msg = rospy.Publisher('kinect/rgb/camera_info', CameraInfo, queue_size=10)

    def compute_projection_matrix(self):
        return self.pb.computeProjectionMatrix(
                    left=-math.tan(math.pi * self.hfov / 360.0) * self.near_plane,
                    right=math.tan(math.pi * self.hfov / 360.0) * self.near_plane,
                    bottom=-math.tan(math.pi * self.vfov / 360.0) * self.near_plane,
                    top=math.tan(math.pi * self.vfov / 360.0) * self.near_plane,
                    nearVal=self.near_plane,
                    farVal=self.far_plane)

    def extract_frame(self, camera_image):
        bgr_image = np.zeros((self.rgb_image_msg.height, self.rgb_image_msg.width, 3))

        camera_image = np.reshape(camera_image[2], (camera_image[1], camera_image[0], 4))

        bgr_image[:, :, 2] =\
            (1 - camera_image[:, :, 3]) * camera_image[:, :, 2] +\
            camera_image[:, :, 3] * camera_image[:, :, 2]

        bgr_image[:, :, 1] =\
            (1 - camera_image[:, :, 3]) * camera_image[:, :, 1] +\
            camera_image[:, :, 3] * camera_image[:, :, 1]

        bgr_image[:, :, 0] =\
            (1 - camera_image[:, :, 3]) * camera_image[:, :, 0] +\
            camera_image[:, :, 3] * camera_image[:, :, 0]

        # return frame
        return bgr_image.astype(np.uint8)

    def extract_depth_frame(self, camera_image):
        depth_img = np.zeros((self.depth_image_msg.height, self.depth_image_msg.width, 3))

        camera_image = np.reshape(camera_image[2], (camera_image[1], camera_image[0], 4))

        depth_img[:, :, 2] =\
            (1 - camera_image[:, :, 3]) * camera_image[:, :, 2] +\
            camera_image[:, :, 3] * camera_image[:, :, 2]

        depth_img[:, :, 1] =\
            (1 - camera_image[:, :, 3]) * camera_image[:, :, 1] +\
            camera_image[:, :, 3] * camera_image[:, :, 1]

        depth_img[:, :, 0] =\
            (1 - camera_image[:, :, 3]) * camera_image[:, :, 0] +\
            camera_image[:, :, 3] * camera_image[:, :, 0]

        # return frame
        return depth_img.astype(np.uint16)

    def compute_camera_target(self, camera_position, camera_orientation):
        """
        camera target is a point 5m in front of the robot camera
        This method is used to tranform it to the world reference frame
        NOTE: this method uses pybullet functions and not tf
        """
        target_point = [5.0, 0, 0] # expressed w.r.t camera reference frame
        camera_position = [camera_position[0], camera_position[1], camera_position[2]]
        rm = self.pb.getMatrixFromQuaternion(camera_orientation)
        rotation_matrix = [[rm[0], rm[1], rm[2]],[rm[3], rm[4], rm[5]],[rm[6], rm[7], rm[8]]]
        return np.dot(rotation_matrix, target_point) + camera_position

    def execute(self):
        """this function gets called from pybullet ros main update loop"""
        # run at lower frequency, camera computations are expensive
        # self.count += 1
        # if self.count < 100:
        #     return
        # self.count = 0 # reset count
        # get camera pose
        cam_state = self.pb.getLinkState(self.robot, self.pb_camera_link_id)
        # target is a point 5m ahead of the robot camera expressed w.r.t world reference frame
        target = self.compute_camera_target(cam_state[0], cam_state[1])
        view_matrix = self.pb.computeViewMatrix(cam_state[0], target, [0, 0, 1])
        # get camera image from pybullet
        pybullet_cam_resp = self.pb.getCameraImage(self.rgb_image_msg.width,
                                                   self.rgb_image_msg.height,
                                                   view_matrix,
                                                   self.projection_matrix,
                                                   renderer=self.pb.ER_BULLET_HARDWARE_OPENGL,
                                                   flags=self.pb.ER_NO_SEGMENTATION_MASK)

        pybullet_depth_cam_resp = self.pb.getCameraImage(self.depth_image_msg.width,
                                                   self.depth_image_msg.height,
                                                   view_matrix,
                                                   self.projection_matrix,
                                                   renderer=self.pb.ER_BULLET_HARDWARE_OPENGL,
                                                   flags=self.pb.ER_NO_SEGMENTATION_MASK)
        # frame extraction function from qibullet
        frame = self.extract_frame(pybullet_cam_resp)
        depth_frame = self.extract_depth_frame(pybullet_depth_cam_resp)
        # fill pixel data array
        self.rgb_image_msg.data = self.image_bridge.cv2_to_imgmsg(frame).data
        self.depth_image_msg.data = self.image_bridge.cv2_to_imgmsg(depth_frame).data
        # update msg time stamp
        self.rgb_image_msg.header.stamp = rospy.Time.now()
        self.depth_image_msg.header.stamp = rospy.Time.now()
        # publish camera image to ROS network
        self.pub_rgb_image.publish(self.rgb_image_msg)
        self.pub_rgb_info_msg.publish(self.rgb_camera_info_msg)
        self.pub_depth_image.publish(self.depth_image_msg)
        self.pub_depth_info_msg.publish(self.depth_camera_info_msg)
