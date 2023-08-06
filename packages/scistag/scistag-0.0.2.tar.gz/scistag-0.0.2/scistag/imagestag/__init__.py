"""
The ImageStag module provides a large set of image creation, manipulation and analysis methods by combining the
strengths of the well known libraries PILLOW, OpenCV and scikit-image.
"""

from .definitions import ImsFramework, PIL, PIL_AVAILABLE, cv, OPENCV_AVAILABLE
from .bounding import Bounding2D, Pos2D, Size2D
from .image import Image, PixelFormat, InterpolationMethod
from .image_filter import ImageFilter
from .color import Color, ColorTypes
from .canvas import Canvas

__all__ = ["Bounding2D", "Pos2D", "Size2D", "Color", "ColorTypes", "ImsFramework", "Image", "ImageFilter",
           "PixelFormat", "InterpolationMethod", "cv", "OPENCV_AVAILABLE", "PIL", "PIL_AVAILABLE",
           "Canvas"]
