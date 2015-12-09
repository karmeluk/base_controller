import time
from controller import Controller
from RobotHQ import RobotHQ
from ROSBaseControl import ROSBaseControl
from geometry_msgs.msg import Twist


def main():
    test = TestsRobot()
    TESTS = ['test.test_Controller()', 'test.test_RobotHQ()', 'test.test_ROSBaseControl()']
    print " 1 - Controller()\n 2 - RobotHQ()\n 3 - RosBaseControl()\n"
    choice = input("Please choose test to run:\n")
    exec TESTS[choice-1]


class TestsRobot:

    def __init__(self):
        print "TEST are ready to start!"
        self.port = '/dev/ttyS0'

    def start_info(self, obj):
        sym = '#'*100
        print "\n%s\n%s TEST\n%s\n" % (sym, obj.__class__.__name__, sym)

    def test_RobotHQ(self):
        test_object = RobotHQ(self.port)
        self.start_info(test_object)

        test_object.start_gui()

    def test_ROSBaseControl(self):
        test_object = ROSBaseControl()
        self.start_info(test_object)
        # TODO: implement test for ROSBaseControl
        TEST_MOVES=[(0.1, 0.0), (-0.1, 0.0), (0.1, 0.1), (-0.1, 0.1), (0.1, -0.1),
                    (-0.1, -0.1), (0.0, 0.0), (0.0, 0.1), (0.0, -0.1)]

        for move in TEST_MOVES:
            l_vel, r_vel = move
            twist = self.twist_generator(l_vel, r_vel)
            test_object.convert_twist(twist)
            time.sleep(2)

    def twist_generator(self, x_speed, ang_speed=0):
        twist = Twist()

        twist.linear.x = x_speed
        twist.angular.z = ang_speed

        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0

        return twist

    def test_Controller(self, vel=5000000):
        test_object = Controller(self.port)
        self.start_info(test_object)

        test_object.set_global_velocity(vel/2)
        test_object.go_forward()
        time.sleep(2)
        test_object.set_global_velocity(vel/2)
        test_object.go_back()
        time.sleep(2)
        test_object.set_global_velocity(vel/5)
        test_object.turn_right()
        time.sleep(5)
        test_object.turn_left()
        time.sleep(5)
        test_object.stop_motor()

if __name__ == '__main__':
    main()
