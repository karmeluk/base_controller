from pymodbus.client.sync import ModbusSerialClient
from threading import Thread, Event


class Controller(Thread):

    MOTION = {"POS": "AB", "FWD": "BB", "BCK": "CB"}
    STOP = {"Hard": 0xABFF, "Smooth": 0xCDFF, "Other": 0xCBFF}
    CMDS = {'FWD': {'LEFT': 0xBB05, 'RIGHT': 0xCB0A}, 'BCK': {'LEFT': 0xCB05, 'RIGHT': 0xBB0A}}

    def __init__(self, port='/dev/ttyS0'):
        Thread.__init__(self)
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
        print int(mode+motor, 16)
        _r = self.write_register(1, int(mode+motor, 16))
        print _r

    def start_motor_raw(self, value):
        _r = self.write_register(1, value)
        print _r

    def stop_motor(self, mode=STOP['Hard']):
        _r = self.write_register(2, mode)
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
        for motor in range(1, 5):
            self.set_velocity(motor, speed)

    def set_rwheel_velocity(self, speed):
        self.set_velocity(1, speed)
        self.set_velocity(3, speed)

    def set_lwheel_velocity(self, speed):
        self.set_velocity(2, speed)
        self.set_velocity(4, speed)

    def set_velocity(self, motor, speed):
        # TODO: speed in m/s
        velocity = speed
        low = velocity % 65536
        hi = velocity / 65536
        motor -= 1
        reg_base = 35 + (motor*7)
        _r1 = self.write_register(reg_base+2, hi)
        _r2 = self.write_register(reg_base+3, low)
        print _r1, _r2

    def set_acceleration(self, motor, acceleration):
        # TODO: acceleration in m/s^2
        low = acceleration % 65536
        hi = acceleration / 65536
        motor -= 1
        reg_base = 35 + (motor*7)
        _r1 = self.write_register(reg_base+4, hi)
        _r2 = self.write_register(reg_base+5, low)
        print _r1, _r2

    def get_velocity(self, motor, speed):
        # TODO
        pass

    def get_acceleration(self, motor, speed):
        # TODO
        pass
