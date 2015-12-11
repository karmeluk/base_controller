import zmq
import time
import sys
import json
from controller import Controller

class HQControlServer():

    def __init__(self):
        self.controller = Controller()
        self.coef = 58823530
        self.port = "50060"
        if len(sys.argv) > 1:
            self.port = sys.argv[1]
            int(self.port)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % self.port)

    def listen_commands(self):
        print "server is ready for commands"
        while True:
            #  Wait for next request from client
            message = self.socket.recv()

            direction, velocity = json.loads(message)

            if direction == 'forward':
                self.handleButtonFWD(velocity)
            if direction == 'back':
                self.handleButtonBack(velocity)
            if direction == 'left':
                self.handleButtonL(velocity)
            if direction == 'right':
                self.handleButtonR(velocity)
            if direction == 'stop':
                self.handleButtonSTP()
            self.socket.send("OK")

    def from_real_to_drive_vel(self, real):
            return float(real) * self.coef

    def handleButtonFWD(self, vel):
        self.controller.set_global_velocity(self.from_real_to_drive_vel(vel))
        self.controller.go_forward()

    def handleButtonBack(self, vel):
        self.controller.set_global_velocity(self.from_real_to_drive_vel(vel))
        self.controller.go_back()

    def handleButtonR(self, vel):
        self.controller.set_global_velocity(self.from_real_to_drive_vel(vel))
        self.controller.turn_right()

    def handleButtonL(self, vel):
        self.controller.set_global_velocity(self.from_real_to_drive_vel(vel))
        self.controller.turn_left()

    def handleButtonSTP(self):
        self.controller.stop_motor()

if __name__ == '__main__':
    server = HQControlServer()
    server.listen_commands()