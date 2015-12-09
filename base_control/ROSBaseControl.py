import roslib
import rospy
from geometry_msgs.msg import Twist
from controller import Controller
import thread

class ROSBaseControl:

    def __init__(self):
        self.controller = Controller('/dev/ttyS0')
        print "%s is created!" % self.__class__.__name__

    def convert_twist(self, twist):
        # TODO: converter from vector3 linear & vector3 angular to (direction, speed)
        # Twist(v_linear, v_angular) -> cmd (forward/back/right/left/stop, velocity, distance)

        cmd = {}
        # from m/s to controller velocity
        coef = 17000
        l_vel = twist.linear.x*coef
        r_vel = twist.angular.z*coef


        # TODO: implement case (l_vel=1, r_vel=-1)
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


    def publish_odom(self):
        # TODO: Odometry publisher
        # odometry must be REAL, gerenerated from motor moving..
        # publish on /odom
        pass