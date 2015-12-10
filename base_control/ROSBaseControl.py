import roslib
import rospy
from controller import Controller
from geometry_msgs.msg import Twist


class ROSBaseControl:

    def __init__(self):
        self.controller = Controller('/dev/ttyS0')

        rospy.loginfo("Started base_control")
        print "Started base_control2"

    def callback(self, msg):
        # TODO: from linear & radial velocities to linear vel on right/left wheel

        rospy.loginfo("Received a /cmd_vel message!")
        print "Received a /cmd_vel message2!"

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
            self.controller.set_lwheel_velocity(lwheel_vel*coef)
            self.controller.set_rwheel_velocity(rwheel_vel*coef)
            self.controller.go_forward()

    def listener(self):
        rospy.init_node('base_control')
        rospy.Subscriber('/cmd_vel', Twist, self.callback)


if __name__ == "__main__":
    base = ROSBaseControl()
    base.listener()
    rospy.spin()
