import roslib
import rospy
from geometry_msgs.msg import Twist
from controller import Controller
from threading import Thread, Event
from math import sin, cos, pi
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster


class ROSBaseControl(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.controller = Controller('/dev/ttyS0')
        print "%s is created!" % self.__class__.__name__

    def convert_twist(self, twist):
        # TODO: converter from vector3 linear & vector3 angular to (direction, speed)
        # Twist(v_linear, v_angular) -> cmd (forward/back/right/left/stop, velocity, distance)

        cmd = {}
        # from m/s to controller velocity
        coef = 58823530
        l_vel = twist.linear.x*coef
        r_vel = twist.angular.z*coef

        cmd['rad'] = self.parse_radial(r_vel)
        cmd['x'] = self.parse_linear(l_vel)

        return cmd

    def send_to_controller(self, cmd):
        pass

    def parse_linear(self, l_vel):
        if l_vel != 0:
            return ('F', abs(l_vel))
        else:
            return ('S', )

    def parse_radial(self, r_vel):
        if r_vel > 0:
            return ('R', abs(r_vel))
        elif r_vel < 0:
            return ('L', abs(r_vel))
        else:
            return ('S', )


class OdometryPublisher(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.finished = Event()

        self.base_control = ROSBaseControl()

        # Parameters
        self.rate = float(rospy.get_param("~base_controller_rate", 10))
        now = rospy.Time.now()

        self.t_delta = rospy.Duration(1.0/self.rate)
        self.t_next = now + self.t_delta
        self.then = now     # time for determining dx/dy

        # internal data
        self.x = 0          # position in xy plane
        self.y = 0
        self.th = 0         # rotation in radians

        # Set up the odometry broadcaster
        self.odomPub = rospy.Publisher('odom', Odometry)
        self.odomBroadcaster = TransformBroadcaster()

        rospy.loginfo("Started Odometry simmulator " + name)

    def publish_odom(self, twist):

        # TODO: Odometry publisher
        # TODO: odometry must be REAL, generated from motor moving.
        # publish on /odom

        rosRate = rospy.Rate(self.rate)
        rospy.loginfo("Publishing Odometry data at: " + str(self.rate) + " Hz")

        vx = twist.linear.x
        vy = twist.linear.y
        vth = twist.angular.z

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
