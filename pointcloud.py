import numpy as np

from nxlib import NxLib, NxLibItem
from nxlib import Camera
from nxlib.constants import *

def check_true(item):
    return item.exists() and item.as_bool() is True


def check_false(item):
    return item.exists() and item.as_bool() is False

def filter_nans(point_map):
    """ Filter NaN values. """
    return point_map[~np.isnan(point_map).any(axis=1)]


def reshape_point_map(point_map):
    """ Reshape the point map array from (m x n x 3) to ((m*n) x 3). """
    return point_map.reshape(
        (point_map.shape[0] * point_map.shape[1]), point_map.shape[2])


with NxLib():
    # todo do we need this? 
    # If camera would use this, for communication, this would make things easier.
    # nxlib.api.open_tcp_port()
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
        print(f"{serial:<17} {model:<16} {status:<16}")


with NxLib(), Camera.from_serial(serial,
                                 [VAL_STRUCTURED_LIGHT, VAL_STEREO]) as camera:
    camera.capture()
    camera.compute_disparity_map()
    camera.compute_point_map()
    camera.get_point_map()