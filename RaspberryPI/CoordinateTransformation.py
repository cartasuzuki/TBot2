import numpy as np
from scipy.spatial.transform import Rotation

def convert_to_frame1(p, frame1_origin, frame1_orientation):
    """
    Convert the coordinates of a point `p` from the original frame `frame0` to coordinates based on a second frame `frame1`.

    Args:
    p (list): List of three numbers representing the (x, y, z) coordinates in `frame0`.
    frame1_origin (list): List of three numbers representing the (x, y, z) coordinates of the origin of `frame1` in `frame0`.
    frame1_orientation (list): List of three numbers representing the orientation of `frame1` relative to `frame0`, in the format of Euler angles (in degrees) in the order of `zyx`.

    Returns:
    A list of three numbers representing the converted (x, y, z) coordinates of `p` in `frame1`.
    """
    # Define the rotation matrix for the orientation of `frame1` relative to `frame0`
    R = Rotation.from_euler("zyx", frame1_orientation, degrees=True).as_matrix()

    # Define the translation vector from `frame0` to `frame1`
    t = np.array(frame1_origin)

    # Transform `p` to `frame1` coordinates
    p_frame1 = R @ (np.array(p) - t)

    return p_frame1.tolist()