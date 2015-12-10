#!/usr/bin/env python
__author__ = 'andrii.kudriashov@gmail.com'

import roslib
import rospy
import tf
import geometry_msgs.msg
import time

def laser_pose():
    robotname = "spacedrill"
    r = rospy.Rate(100)
    br = tf.TransformBroadcaster()

    while not rospy.is_shutdown():
        br.sendTransform((0.0, 0.0, 0.2), (0, 0, 0, 1),\
                     rospy.Time.now(), "laser", "base_link")
        time.sleep(0.25)

if __name__ == '__main__':
    rospy.init_node('tf_laser')
    laser_pose()

