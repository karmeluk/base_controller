#!/usr/bin/env python

import rospy

from threading import Thread, Event
from math import sin, cos, pi
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster

class base_controller(Thread):
    """ Controller to handle movement & odometry feedback for a differential drive mobile base. """
    def __init__(self, name):
        Thread.__init__ (self)
        self.finished = Event()

        # Parameters
        self.rate = float(rospy.get_param("~base_controller_rate", 10))
        now = rospy.Time.now()
        
        self.t_delta = rospy.Duration(1.0/self.rate)
        self.t_next = now + self.t_delta
        self.then = now # time for determining dx/dy

        # internal data        
        self.x = 0.                  # position in xy plane
        self.y = 0.
        self.th = 0.                 # rotation in radians

        # Set up the odometry broadcaster
        self.odomPub = rospy.Publisher('odom', Odometry)
        self.odomBroadcaster = TransformBroadcaster()
        
        rospy.loginfo("Started Odometry simmulator " + name )

    def run(self):
        rosRate = rospy.Rate(self.rate)
        rospy.loginfo("Publishing Odometry data at: " + str(self.rate) + " Hz")

        vx = 0.0
        vy = 0.0
        vth = 0.0

        while not rospy.is_shutdown() and not self.finished.isSet():
            now = rospy.Time.now()         
            if now > self.t_next:
                dt = now - self.then
                self.then = now
                dt = dt.to_sec()

                delta_x = (vx * cos(self.th) - vy * sin(self.th)) * dt
                delta_y = (vx * sin(self.th) + vy * cos(self.th)) * dt
                delta_th = vth * dt

                self.x += delta_x
                self.y += delta_y
                self.th += delta_th


                quaternion = Quaternion()
                quaternion.x = 0.0 
                quaternion.y = 0.0
                quaternion.z = sin(self.th / 2.0)
                quaternion.w = cos(self.th / 2.0)
    
                # Create the odometry transform frame broadcaster.
                self.odomBroadcaster.sendTransform(
                    (self.x, self.y, 0), 
                    (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
                    rospy.Time.now(),
                    "base_link",
                    "odom"
                    )
    
                odom = Odometry()
                odom.header.frame_id = "odom"
                odom.child_frame_id = "base_link"
                odom.header.stamp = now
                odom.pose.pose.position.x = self.x
                odom.pose.pose.position.y = self.y
                odom.pose.pose.position.z = 0
                odom.pose.pose.orientation = quaternion
                odom.twist.twist.linear.x = vx
                odom.twist.twist.linear.y = 0
                odom.twist.twist.angular.z = vth
    
                self.odomPub.publish(odom)
                
                self.t_next = now + self.t_delta
                
            rosRate.sleep()

    def stop(self):
        print "Shutting down base odom_sim"
        self.finished.set()
        self.join()

if __name__ == "__main__":

    rospy.init_node("odom_sim")
    controller = base_controller("spacedrill")
    controller.run()
    rospy.spin()
