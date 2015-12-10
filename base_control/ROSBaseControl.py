import roslib
import rospy
from threading import Thread, Event
from controller import Controller
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster
from math import sin, cos, pi
from geometry_msgs.msg import Quaternion


class ROSBaseControl:

    def __init__(self):
        rospy.init_node('base_control')
        self.finished = Event()
        self.controller = Controller('/dev/ttyS0')

        rospy.loginfo("Started base_control")
        print "Started base_control"

        # odom...
        self.rate = float(rospy.get_param("~base_controller_rate", 20))
        now = rospy.Time.now()

        self.t_delta = rospy.Duration(1.0/self.rate)
        self.t_next = now + self.t_delta
        self.then = now # time for determining dx/dy

        # internal data
        self.x = 0                  # position in xy plane
        self.y = 0
        self.th = 0                 # rotation in radians
        self.vx = 0.0
        self.vy = 0.0
        self.vth = 0.0

        # Set up the odometry broadcaster
        self.odomPub = rospy.Publisher('odom', Odometry)
        self.odomBroadcaster = TransformBroadcaster()

    def callback_cmd(self, msg):
        # TODO: from linear & radial velocities to linear vel on right/left wheel

        rospy.loginfo("Received a /cmd_vel message!")
        print "Received a /cmd_vel message!"

        # from m/s to controller velocity
        coef = 58823530
        # L = distance between wheels
        L = 0.495

        if msg.linear.x == 0 and msg.angular.z == 0:
            self.controller.stop_motor()
        else:
            rwheel_vel = (2*msg.linear.x - L*msg.angular.z)/2
            lwheel_vel = (2*msg.linear.x + L*msg.angular.z)/2
            print rwheel_vel, lwheel_vel
            self.controller.set_lwheel_velocity(abs(lwheel_vel*coef))
            self.controller.set_rwheel_velocity(abs(rwheel_vel*coef))
            self.controller.go_forward()

        self.vx = msg.linear.x
        #self.vth = msg.angular.z

    def listener(self):
        rospy.Subscriber('/cmd_vel', Twist, self.callback_cmd)

        rosRate = rospy.Rate(self.rate)

        while not rospy.is_shutdown() and not self.finished.isSet():
            now = rospy.Time.now()
            if now > self.t_next:
                dt = now - self.then
                self.then = now
                dt = dt.to_sec()

                delta_x = (self.vx * cos(self.th) - self.vy * sin(self.th)) * dt
                delta_y = (self.vx * sin(self.th) + self.vy * cos(self.th)) * dt
                delta_th = self.vth * dt

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
                odom.twist.twist.linear.x = self.vx
                odom.twist.twist.linear.y = 0
                odom.twist.twist.angular.z = self.vth

                self.odomPub.publish(odom)

                self.t_next = now + self.t_delta

            rosRate.sleep()

if __name__ == "__main__":
    base = ROSBaseControl()
    base.listener()
    rospy.spin()
