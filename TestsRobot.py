import time
from controller import RobotHQ, ROSBaseControl, Controller


def main():
    test = TestsRobot()
    # run tests here
    test.test_Controller()


class TestsRobot:

    def __init__(self):
        print "TEST are ready to start!"

    def start_info(self, obj):
        sym = '#'*100
        print "%\ns\n%s TEST\n%s\n" % (sym, obj.__class__.__name__, sym)

    def test_RobotHQ(self):
        test_object = RobotHQ()
        self.start_info(test_object)
        # TODO: implement test for pyQT GUI

    def test_ROSBaseControl(self):
        test_object = ROSBaseControl()
        self.start_info(test_object)
        # TODO: implement test for ROSBaseControl

    def test_Controller(self, vel=5000000):
        test_object = Controller(1)
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