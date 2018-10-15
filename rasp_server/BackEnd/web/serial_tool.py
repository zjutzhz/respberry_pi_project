import serial
import logging


class SerialTool(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.ser = None
        self.initialed = False
        self.port = None

    def init_serial(self, port, baud_rate):
        if self.port == None:
            self.port = port
            self.init(port, baud_rate)
        else:
            self.close_serial()
            if self.port == port:
                self.init(port, baud_rate)
            else:
                self.port = port
                self.init(port, baud_rate)
        return self.initialed

    def init(self, port, baud_rate):
        if self.initialed:
            self.logger.info("Already initialed")
        else:
            if port is not None and port.find("tty") > -1:
                try:
                    self.ser = serial.Serial(port, baud_rate)
                    self.initialed = True
                except Exception as e:
                    self.logger.exception(e)

    def close_serial(self):
        if self.initialed:
            try:
                self.ser.close()
                self.initialed = False
            except Exception as e:
                self.logger.exception("Error in close")
        else:
            self.logger.info("Serial not initialed")

    def send_data(self, data):
        if self.initialed:
            try:
                self.ser.write(data.encode("utf-8"))
                return True
            except Exception as e:
                self.logger.exception("Error in send data to port {}".format(data))
        else:
            self.logger.info("Serial not initialed")
        return False