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
        # TODO: speed in m/s!!
        # forward with V m/s
        # twist.linear.x = V; forward speed, if pos - go_forward, if 0 - stop, if neg - go_back
        # twist.angular.z = 0; angle, if pos - turn_right, if neg - turn_left
        #
        # twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!
        # twist.angular.x = 0; twist.angular.y = 0;   #          or these!
        print twist

        print "forward speed: " + str(twist.linear.x)
        print "rad speed: " + str(twist.angular.z)

        coef = 20000000
        l_vel = twist.linear.x
        l_vel = l_vel*coef

        r_vel = twist.angular.z
        r_vel = r_vel*coef

        # TODO: implement case (l_vel=1, r_vel=-1)

        # TODO: fix lags, refactor
        # TODO: maybe set vel in threads?

        if l_vel > 0:
            if r_vel > 0:
                self.controller.set_global_velocity(abs(r_vel))
                self.controller.turn_right()
            elif r_vel < 0:
                self.controller.set_global_velocity(abs(r_vel))
                self.controller.turn_left()
            else:
                self.controller.stop_motor()
            self.controller.set_global_velocity(abs(l_vel))
            self.controller.go_forward()
        elif l_vel < 0:
            if r_vel > 0:
                self.controller.set_global_velocity(abs(r_vel))
                self.controller.turn_right()
            elif r_vel < 0:
                self.controller.set_global_velocity(abs(r_vel))
                self.controller.turn_left()
            else:
                self.controller.stop_motor()
            self.controller.set_global_velocity(abs(l_vel))
            self.controller.go_back()
        else:
            if r_vel > 0:
                self.controller.set_global_velocity(abs(r_vel))
                self.controller.turn_right()
            elif r_vel < 0:
                self.controller.set_global_velocity(abs(r_vel))
                self.controller.turn_left()
            else:
                self.controller.stop_motor()
            self.controller.stop_motor()

        cmd = None
        return cmd

    def publish_odom(self):
        # TODO: Odometry publisher
        # odometry must be REAL, gerenerated from motor moving..
        # publish on /odom
        pass