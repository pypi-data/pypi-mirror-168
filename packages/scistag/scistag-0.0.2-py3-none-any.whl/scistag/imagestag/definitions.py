"""
Defines the common definitions required by all major components of the ImageStag module.
"""

import enum

try:
    import PIL

    PIL_AVAILABLE = True
except ModuleNotFoundError:
    PIL_AVAILABLE = False
    PIL = None

try:
    import cv2 as cv

    OPENCV_AVAILABLE = True
except ModuleNotFoundError:
    cv = None
    OPENCV_AVAILABLE = False


class ImsFramework(enum.Enum):
    """
    Definition of available frameworks for storing and modifying pixel data in ImageStag
    """

    PIL = "PIL"
    "Prefer using a Pillow image handle to store the pixel data"
    RAW = "NP"
    "Prefer using numpy to store the image data. RGB and RGBA images are represented in RGB/RGBA order"
    CV = "CV"
    "Prefer using OpenCV to store the pixel data. RGB and RGBA images are represented in BGR/BGRA order"


__all__ = ["ImsFramework", "OPENCV_AVAILABLE", "PIL_AVAILABLE", "cv", "PIL"]
