# -*- coding: utf-8 -*-

import glob
import json
import logging.handlers
import os
import sys
import time
from datetime import datetime

import cv2
import picamera
import picamera.array
import serial
from flask import Flask, request
import requests


from train import Train
from web.config import DevConfig
from web.serial_tool import SerialTool

# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
logger = logging.getLogger("main")

app.config.from_object(DevConfig)

serial_tool = SerialTool()
# train = Train()



@app.route('/')
def root():
    return "<h1>Hello world</h1>"


@app.route("/api/v1/get_key")
def get_key():
    logger.info(request.args["key_id"])
    return "he"


@app.route("/api/v1/serial/get_serial")
def get_serial():
    ports = serial_ports()

    return json.dumps(ports)


@app.route("/api/v1/serial/initial")
def get_init_serial():
    result = {}
    port = request.args["port"]
    baud_rate = request.args["baud_rate"]

    # serial_tool = SerialTool()
    status = serial_tool.init_serial(port, baud_rate)
    result["os_flag"] = "0" if status else "1"

    return json.dumps(result)


@app.route("/api/v1/serial/close")
def get_close_serial():
    result = {}
    status = serial_tool.close_serial()
    result["os_flag"] = "0" if status else "1"

    return json.dumps(result)

@app.route("/api/v1/serial/send")
def get_send():
    result = {}
    if "data" in request.args:
        data = request.args["data"]
        logger.info("Get data: {}".format(data))
        status = serial_tool.send_data(data)
        result["os_flag"] = "0" if status else "1"
    elif "key" in request.args:
        key = request.args["key"]
        logger.info("Get key: {}".format(key))
        if key in key_map:
            status = serial_tool.send_data(key_map[key])

            result["os_flag"] = "0" if status else "1"
        else:
            result["os_flag"] = "1"
    else:
        result["os_flag"] = "1"
    return json.dumps(result)


@app.route("/api/v1/ocr/recognise")
def get_recognise():
    result = {}
    try:
        with picamera.PiCamera() as camera:
            # camera.start_preview()
            camera.resolution = (800, 600)
            camera.rotation = 180
            time.sleep(0.1)
            tim = datetime.now().strftime("%Y%m%d_%H%M%S")
            for i in range(1):
                logger.info("Processing {}:".format(i))
                with picamera.array.PiRGBArray(camera) as stream:
                    camera.capture(stream, format='rgb')
                    # At this point the image is available as stream.array
                    image = stream.array
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    ori_file = os.path.join(os.path.curdir, "{}_{}_ori.png".format(tim, i))
                    label_file = os.path.join(os.path.curdir, "{}_label.png".format(tim))
                    cv2.imwrite(ori_file, image)

                    files = {'file': open(ori_file, 'rb')}
                    ret = requests.post('http://192.168.43.185:10086/api/v1/recognise_image', files = files)
                    print(ret.text)
                    time.sleep(2)
                    # ocr_py = OcrPy(logger)
                    # ocr_py.recognize(image)
                    # train.get_object(image, label_file)








            result["os_flag"] = "0"
    except Exception as e:
        logger.exception("Error ")
        result["os_flag"] = "1"
    return json.dumps(result)

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    # print(serial_ports())
    logger.info(serial_ports())
    # serial_tool = None

    key_map = {
        "keyboard_arrow_up": "1", # 正常前进
        "keyboard_arrow_left": "D",
        "keyboard_arrow_right": "E",
        "keyboard_arrow_down": "4",  #正常后退
        "fast_rewind": "5",  #正常后退
        "fast_forward": "2",  #正常后退
        "stop": "3",                 # 停
        "send": "8",
        "refresh": "9"
    }


    # 1 正常前进
    # 2 缓慢前进
    # 3 停
    # 4 正常后退
    # 5 缓慢后退
    # 6 抓 7 举 8 放 9 恢复
    # A profile 1
    # B profile 2
    # C profile 3
    # D 左转
    # E 右转

    app.run(host="0.0.0.0")
