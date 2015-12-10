from controller import Controller
from PyQt4 import QtGui, QtCore
import sys


class RobotHQ(QtGui.QWidget):
    # TODO: 5 buttons, 2 text fields
    # GUI (forward/back/right/left/stop, velocity, distance) -> cmd
    def __init__(self, port=1):
        self.controller = Controller(port)
        self.app = QtGui.QApplication(sys.argv)
        super(RobotHQ, self).__init__()
        self.setGeometry(500, 500, 300, 200)
        self.setWindowTitle('Mobile Robot control')
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
        lb_vel.move(15, 135)
        self.le_vel = QtGui.QLineEdit('1000000', self)
        self.le_vel.move(10, 150)

        lb_dis = QtGui.QLabel('Position', self)
        lb_dis.move(160, 135)
        self.le_pos = QtGui.QLineEdit(self)
        self.le_pos.move(155, 150)

    def handleButtonFWD(self):
        self.controller.set_global_velocity(int(self.le_vel.text()))
        if self.le_pos.text() != '':
            # TODO: implement self.controller.set_possition(int(self.le_pos.text()))
            pass
        self.controller.go_forward()


    def handleButtonBack(self):
        self.controller.set_global_velocity(int(self.le_vel.text()))
        self.controller.go_back()

    def handleButtonR(self):
        self.controller.set_global_velocity(int(self.le_vel.text()))
        self.controller.turn_right()

    def handleButtonL(self):
        self.controller.set_global_velocity(int(self.le_vel.text()))
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