from flask import Flask, jsonify
from nxlib import NxLibItem
from nxlib.constants import *
from nxlib.context import NxLib
import os


basePath = os.environ.get('BASE_PATH', '/')
app = Flask(__name__)

def check_true(item):
    return item.exists() and item.as_bool() is True


def check_false(item):
    return item.exists() and item.as_bool() is False

def get_cameras():
    out = []

    with NxLib():
        # Reference to the serials subnode of all cameras
        cameras = NxLibItem()[ITM_CAMERAS]

        # Print status information for each camera
        print("SerialNo", " " * 8, "Model", " " * 10, "Status")
        for i in range(cameras.count()):
            if not cameras[i][ITM_STATUS].exists():
                continue
            if check_false(cameras[i][ITM_STATUS][ITM_VALID_IP_ADDRESS]):
                status = "Invalid Ip"
            elif check_true(cameras[i][ITM_STATUS][ITM_OPEN]):
                status = "Open"
            elif check_false(cameras[i][ITM_STATUS][ITM_AVAILABLE]):
                status = "In Use"
            elif check_false(cameras[i][ITM_STATUS][ITM_VALID_CAMERA_FIRMWARE]):
                status = "Invalid Camera Firmware"
            elif check_false(cameras[i][ITM_STATUS][ITM_VALID_PROJECTOR_FIRMWARE]):
                status = "Invalid Projector Firmware"
            elif check_false(cameras[i][ITM_STATUS][ITM_CALIBRATED]):
                status = "Not Calibrated"
            else:
                status = "Available"
            serial = cameras[i].name()
            model = cameras[i][ITM_MODEL_NAME].as_string()
            out.append({"serial": serial, "model": model, "status": status})
            print(f"{serial:<17} {model:<16} {status:<16}")
    return out

@app.route(basePath, methods=['GET'])
def home():
    """Home endpoint that returns a welcome message"""
    return jsonify({
        "message": "Welcome to the Ensenso K8s server!",
        "status": "running",
        "port": 3000
    })

@app.route(basePath + "/health", methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ensenso-k8s"
    })

@app.route(basePath + "/cameras", methods=['GET'])
def info():
    """Info endpoint that returns some sample data"""
    cams = get_cameras()
    return jsonify({
        "cameras": cams,
    })

if __name__ == '__main__':
    print("Starting server on port 3000...")
    app.run(host='0.0.0.0', port=3000, debug=True)
