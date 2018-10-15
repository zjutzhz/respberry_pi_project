from flask import Flask, request

from config import DevConfig
import logging
import os
import cv2
import glob
from load.train import Train


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("main")

app = Flask(__name__)

app.config.from_object(DevConfig)

train = Train()

@app.route('/')
def root():
    # return "<h1>Hello world</h1>"
    return app.send_static_file('index.html')

@app.route("/api/v1/recent_capture_image_name", methods=["GET"])
def get_recent_capture_image_name():
    upload_path = app.config['UPLOAD_FOLDER']
    latest_upload_file = max(glob.iglob(os.path.join(upload_path, "*.png")), key=os.path.getctime)
    logger.info(latest_upload_file)
    return latest_upload_file


@app.route("/api/v1/recognise_image"  ,methods=['GET', 'POST'])
def get_key():

    result = ""
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            file_name = "default.png"
        else:
            file_name = file.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(image_path)
        result = train.recognise_cup(image_path)
    else:
        result = "Hello"
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10086)
