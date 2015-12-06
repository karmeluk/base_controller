from pymodbus.client.sync import ModbusSerialClient
from PyQt4 import QtGui, QtCore
import sys


class RobotHQ(QtGui.QWidget):
    # TODO: 5 buttons, 2 text fields
    # GUI (forward/back/right/left/stop, velocity, distance) -> cmd
    def __init__(self):
        self.controller = Controller()
        self.app = QtGui.QApplication(sys.argv)
        super(RobotHQ, self).__init__()
        self.setGeometry(500, 500, 300, 300)
        self.setWindowTitle('Message box')
        self.init_ui()
        self.center()

    def init_ui(self):
        btn_fwd = QtGui.QPushButton('Move Forward', self)
        btn_fwd.clicked.connect(self.handleButtonFWD)
        btn_fwd.resize(btn_fwd.sizeHint())
        btn_fwd.move(115, 10)

        btn_back = QtGui.QPushButton('Back', self)
        btn_back.clicked.connect(self.handleButtonBack)
        btn_back.resize(btn_back.sizeHint())
        btn_back.move(115, 50)

        btn_stop = QtGui.QPushButton('Stop', self)
        btn_stop.clicked.connect(self.handleButtonSTP)
        btn_stop.resize(btn_stop.sizeHint())
        btn_stop.move(115, 90)

        btn_left = QtGui.QPushButton('Turn Left', self)
        btn_left.clicked.connect(self.handleButtonL)
        btn_left.resize(btn_stop.sizeHint())
        btn_left.move(10, 30)

        btn_right = QtGui.QPushButton('Turn Right', self)
        btn_right.clicked.connect(self.handleButtonR)
        btn_right.resize(btn_stop.sizeHint())
        btn_right.move(210, 30)

        lb_vel = QtGui.QLabel('Velocity', self)
        lb_vel.move(15, 120)
        le_vel = QtGui.QLineEdit('5000000', self)
        le_vel.move(10, 135)

        lb_dis = QtGui.QLabel('Distance', self)
        lb_dis.move(160, 120)
        le_dis = QtGui.QLineEdit(self)
        le_dis.move(155, 135)



    def handleButtonFWD(self):
        self.controller.go_forward()

    def handleButtonBack(self):
        self.controller.go_back()


    def handleButtonR(self):
        self.controller.turn_right()

    def handleButtonL(self):
        self.controller.turn_left()

    def handleButtonSTP(self):
        self.controller.stop_motor()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



    def start_gui(self):
        self.show()
        sys.exit(self.app.exec_())


class ROSBaseControl:

    def __init__(self):
        pass

    def convert_twist(self, twist):
        # TODO: converter from vector3 linear & vector3 angular to (direction, speed)
        # Twist(v_linear, v_angular) -> cmd (forward/back/right/left/stop, velocity, distance)
        # speed in m/s!!
        # forward with V m/s
        # twist.linear.x = V;                   # our forward speed
        # twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!
        # twist.angular.x = 0; twist.angular.y = 0;   #          or these!
        # twist.angular.z = 0;
        cmd = None
        return cmd

    def publish_odom(self):
        # TODO: Odometry publisher
        # odometry must be REAL, gerenerated from motor moving..
        # publish on /odom
        pass


class Controller:

    MOTION = {"POS":"AB", "FWD":"BB", "BCK":"CB"}
    STOP = {"Hard":0xABFF, "Smooth":0xCDFF, "Other":0xCBFF}
    CMDS = {'FWD': {'LEFT': 0xBB05, 'RIGHT': 0xCB0A}, 'BCK': {'LEFT': 0xCB05, 'RIGHT': 0xBB0A}}


    def __init__(self, port=1):
        # connect to COM
        self.client = ModbusSerialClient(method='rtu', port=port,\
                                         baudrate=115200, stopbits=1, parity='N', bytesize=8, timeout=0.1)

    def cmd_listener(self):
        # TODO: cmd input. callback?
        pass

    def read_register(self, address, size=16, unit=1):
        _r = self.client.read_holding_registers(address, size, unit)
        if _r:
            return [hex(x) for x in _r.registers]
        return None

    def write_register(self, address, value, unit=1):
        _r = self.client.write_register(address, value, unit=1)
        if _r:
            return _r
        return None

    def start_motor(self, motor, mode):
        print int(mode+motor,16)
        _r = self.write_register(1, int(mode+motor,16))
        print _r

    def start_motor_raw(self, value):
        _r = self.write_register(1, value)
        print _r

    def stop_motor(self, mode=STOP['Hard']):
        _r = self.write_register(2,mode)
        print _r

    def go_forward(self, _stop='Hard'):
        self.stop_motor(self.STOP[_stop])
        self.start_motor_raw(self.CMDS['FWD']['RIGHT'])
        self.start_motor_raw(self.CMDS['FWD']['LEFT'])

    def go_back(self, _stop='Hard'):
        self.stop_motor(self.STOP[_stop])
        self.start_motor_raw(self.CMDS['BCK']['RIGHT'])
        self.start_motor_raw(self.CMDS['BCK']['LEFT'])

    def turn_right(self, _stop='Hard'):
        self.stop_motor(self.STOP[_stop])
        self.start_motor_raw(self.CMDS['FWD']['RIGHT'])
        self.start_motor_raw(self.CMDS['BCK']['LEFT'])

    def turn_left(self, _stop='Hard'):
        self.stop_motor(self.STOP[_stop])
        self.start_motor_raw(self.CMDS['BCK']['RIGHT'])
        self.start_motor_raw(self.CMDS['FWD']['LEFT'])

    def set_global_velocity(self, speed):
        for motor in range(1,5):
            self.set_velocity(motor, speed)

    def set_velocity(self, motor, speed):
        # TODO: speed in m/s
        velocity = speed
        low = velocity % 65536
        hi = velocity / 65536
        motor -= 1
        reg_base = 35 + (motor *7)
        _r1 = self.write_register(reg_base+2, hi)
        _r2 = self.write_register(reg_base+3, low)
        print _r1, _r2

    def set_acceleration(self, motor, acceleration):
        # TODO: acceleration in m/s^2
        low = acceleration % 65536
        hi = acceleration / 65536
        motor -= 1
        reg_base = 35 + (motor *7)
        _r1 = self.write_register(reg_base+4, hi)
        _r2 = self.write_register(reg_base+5, low)
        print _r1, _r2

    def get_velocity(self, motor, speed):
        # TODO
        pass

    def get_acceleration(self, motor, speed):
        # TODO
        pass
