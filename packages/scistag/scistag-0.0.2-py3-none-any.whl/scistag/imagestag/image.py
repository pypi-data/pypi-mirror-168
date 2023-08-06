"""
Implements the class :class:`.Image` which is SciStag's main class for loading, storing and keeping image data in
memory.
"""

import io
import os
from enum import Enum
from typing import Union, Tuple, Optional

import PIL.Image
import numpy as np

from .color import Color
from .bounding import Size2D
from .definitions import ImsFramework, OPENCV_AVAILABLE, cv

SUPPORTED_IMAGE_FILETYPES = ["png", "bmp", "jpg", "jpeg", "gif"]
"List of image file types which can be read and written"

SUPPORTED_IMAGE_FILETYPE_SET = set(SUPPORTED_IMAGE_FILETYPES)
"Set of image file types which can be read and written"


class InterpolationMethod(Enum):
    """
    Enumeration of image interpolation methods
    """

    NEAREST = 0
    "The pixel will be kept intact, the upscaled image has quite hard pixel edges and the downscaled image is noisy"
    LINEAR = 1
    "Linear interpolation. Mixes up to four colors based upon subpixel position."
    CUBIC = 2
    "Cubic interpolation. Matches the pixels of the source region to the image region and tries to preserve contours"
    LANCZOS = 3
    "The highest image rescaling quality available in cv2/PIL. Use this if performance is not the most important"

    def to_cv(self):
        """
        Maps the enum to the corresponding OpenCV type

        :return: The OpenCV constant
        """
        cv2_mapping = {
            self.NEAREST: 6,  # INTER_NEAREST_EXACT,
            self.LINEAR: 1,  # INTER_LINEAR,
            self.CUBIC: 2,  # INTER_CUBIC
            self.LANCZOS: 4  # INTER_LANCZOS4
        }
        "Definition of mappings from SciStag.Image to OpenCV"
        return cv2_mapping[self]

    def to_pil(self):
        """
        Maps the enum to the corresponding PIL type

        :return: The PIL constant
        """
        pil_mapping = {
            self.NEAREST: PIL.Image.Resampling.NEAREST,
            self.LINEAR: PIL.Image.Resampling.BILINEAR,
            self.CUBIC: PIL.Image.Resampling.BICUBIC,
            self.LANCZOS: PIL.Image.Resampling.LANCZOS
        }
        "Definition of mappings from SciStag.Image to PIL"
        return pil_mapping[self]


class PixelFormat(Enum):
    """
    Enumeration of different pixel formats
    """
    RGB = 0
    "Red Green Blue"
    RGBA = 1
    "Red Green Blue Alpha"
    BGR = 5
    "Blue Green Red"
    BGRA = 6
    "Blue Green Red Alpha"
    GRAY = 10
    "Grayscale"


IMAGE_SOURCE_TYPES = Union[str, np.ndarray, bytes, PIL.Image.Image, "Image"]
"The valid source type for loading an image"


class Image:
    """
    SciStag's default class for storing image data in all common pixel formats.


    The data is internally either stored using the PILLOW image library's Image class or as a classical numpy
    array, depending on how it was initialized. If not specified otherwise it will always the PILLOW representation
    as this is very well suited to visualize the data or modify it using the Canvas class.

    If you want to access the data directly you can at all times call the to_pil or get_pixels function.
    """

    def __init__(self, source: IMAGE_SOURCE_TYPES, framework: ImsFramework = None,
                 source_pixel_format: Optional[PixelFormat] = None):
        """
        Creates an image from a set of various sources

        :param source: The image source. Either a file name, a http URL, numpy array or one of the supported low level
            types
        :param framework: The framework to be used if the file is loaded from disk
        :param source_pixel_format: The pixel format - if the data was passed as np.array

        Raises a ValueError if the image could not be loaded
        """
        if source_pixel_format is None:
            source_pixel_format = PixelFormat.RGB
        self.width = 1
        "The image's width in pixels"
        self.height = 1
        "The image's height in pixels"
        self.framework = framework if framework is not None else ImsFramework.PIL
        "The framework being used. ImsFramework.PIL by default."
        self._pil_handle: Optional[PIL.Image.Image] = None
        "The PILLOW handle (if available)"
        self._pixel_data: Optional[np.ndarray] = None
        "The pixel data (if available) as numpy array"
        self.pixel_format = source_pixel_format
        "The base format (rgb, rbga, bgr etc.)"
        # ------- preparation of source data -------
        source = self._prepare_data_source(framework, source)
        # ------------------------------------------
        if framework is None:
            framework = ImsFramework.PIL
        if framework == ImsFramework.PIL:
            self.init_as_pil(source)
        elif framework == ImsFramework.RAW:
            self._pixel_data = self._pixel_data_from_source(source)
            self.height, self.width = self._pixel_data.shape[0:2]
            self.pixel_format = self.detect_format(self._pixel_data)
        elif framework == ImsFramework.CV:
            self.init_as_cv2(source)
        else:
            raise NotImplemented

    def _prepare_data_source(self, framework, source):
        """
        Prepares and if necessary converts the data source to a supported format

        :param framework: The framework being used
        :param source: The source, a byte steam, a filename or a http URL
        :return: The prepared source data
        """
        if isinstance(source, type(self)):
            source = source.to_pil()
        if isinstance(source, np.ndarray) and self.pixel_format == PixelFormat.BGR and framework != ImsFramework.CV:
            source = self.normalize_to_rgb(source, keep_gray=True, input_format=self.pixel_format)
            self.pixel_format = self.detect_format(source)
        # fetch from web if desired
        if isinstance(source, str) and (source.startswith("http:") or source.startswith("https:")):
            from scistag.webstag import web_fetch
            source = web_fetch(source)
            if source is None:
                raise ValueError("Image data could not be received")
        return source

    def init_as_cv2(self, source: np.ndarray):
        """
        Initializes the image from a numpy array and assuming OpenCV's BGR / BGRA color channel order

        :param source: The data source
        """
        if isinstance(source, np.ndarray):
            self._pixel_data = self.normalize_to_bgr(source, input_format=self.pixel_format, keep_gray=True)
            self.pixel_format = self.detect_format(self._pixel_data, is_cv2=True)
        else:
            self._pixel_data = Image(source).get_pixels(desired_format=self.pixel_format)
            self.pixel_format = self.detect_format(self._pixel_data, is_cv2=True)
        self.height, self.width = self._pixel_data.shape[0:2]

    def init_as_pil(self, source):
        """
        Initializes the image as PIL image

        :param source: The data source
        """
        if isinstance(source, str):
            self._pil_handle = PIL.Image.open(source)
        elif isinstance(source, bytes):
            data = io.BytesIO(source)
            self._pil_handle = PIL.Image.open(data)
        elif isinstance(source, np.ndarray):
            self._pil_handle = PIL.Image.fromarray(source)
        elif isinstance(source, PIL.Image.Image):
            self._pil_handle = source
        else:
            raise NotImplemented
        if self._pil_handle.mode == "P":
            palette = self._pil_handle.palette.colors
            if 'transparency' in self._pil_handle.info:
                self._pil_handle = self._pil_handle.convert("RGBA")
            else:
                self._pil_handle = self._pil_handle.convert("RGB")
        self.width = self._pil_handle.width
        self.height = self._pil_handle.height
        self.pixel_format = self._pil_handle.mode.lower()

    def is_bgr(self) -> bool:
        """
        Returns if the current format is bgr or bgra

        :return: True if the image currently in bgr or bgra format
        """
        return self.pixel_format == PixelFormat.BGR or self.pixel_format == PixelFormat.BGRA

    @classmethod
    def detect_format(cls, pixels: np.ndarray, is_cv2=False):
        """
        Detects the format

        :param pixels: The pixels
        :param is_cv2: Defines if the source was OpenCV
        :return: The pixel format. See PixelFormat
        """
        if len(pixels.shape) == 2:
            return PixelFormat.GRAY
        if is_cv2:
            return PixelFormat.BGR if pixels.shape[2] == 3 else PixelFormat.BGRA
        return PixelFormat.RGB if pixels.shape[2] == 3 else PixelFormat.RGBA

    @classmethod
    def _pixel_data_from_source(cls, source: Union[str, np.ndarray, bytes, PIL.Image.Image]) -> np.ndarray:
        """
        Loads an arbitrary source and returns it as pixel data

        :param source: The data source. A filename, a http url, numpy array or a PIL image
        :return: The pixel data
        """
        if isinstance(source, np.ndarray):
            return source
        elif isinstance(source, PIL.Image.Image):
            # noinspection PyTypeChecker
            return np.array(source)
        elif isinstance(source, str) or isinstance(source, bytes):
            return Image(source, framework=ImsFramework.PIL).get_pixels()
        else:
            raise NotImplemented

    def get_size(self) -> Tuple[int, int]:
        """
        Returns the image's size in pixels

        :return: The size as tuple (width, height)
        """
        if self.framework == ImsFramework.PIL:
            return self._pil_handle.size
        if self._pixel_data is not None:
            return self._pixel_data.shape[0:2][::-1]
        raise NotImplemented

    def get_size_as_size(self) -> Size2D:
        """
        Returns the image's size

        :return: The size
        """
        if self.framework == ImsFramework.PIL:
            return Size2D(self.get_size())
        else:
            raise NotImplemented

    def crop(self, box: Tuple[int, int, int, int]) -> "Image":
        """
        Crops a region of the image and returns it

        :param box: The box in the form x, y, x2, y2
        :return: The image of the defined sub region
        """
        if box[2] < box[0] or box[3] < box[1]:
            raise ValueError("X2 or Y2 are not allowed to be smaller than X or Y")
        if box[0] < 0 or box[1] < 0 or box[2] >= self.width or box[3] >= self.height:
            raise ValueError("Box region out of image bounds")
        if self._pil_handle:
            return Image(self._pil_handle.crop(box=box))
        elif self._pixel_data:
            cropped = self._pixel_data[box[1]:box[3] + 1, box[0]:box[2] + 1, :] if len(self._pixel_data.shape) == 3 \
                else self._pixel_data[box[1]:box[3] + 1, box[0]:box[2] + 1]
            return Image(cropped, framework=self.framework, source_pixel_format=self.pixel_format)
        else:
            raise NotImplementedError("Crop not implemented for the sdk type")

    def resize(self, size: tuple):
        """
        Resizes the image to given resolution (modifying this image directly)

        :param size: The new size
        """
        if self.framework == ImsFramework.PIL:
            self._pil_handle = self._pil_handle.resize(size, PIL.Image.Resampling.LANCZOS)
        elif self._pixel_data is not None:
            if OPENCV_AVAILABLE:
                self._pixel_data = cv.resize(self._pixel_data, dsize=size, interpolation=cv.INTER_LANCZOS4)
            else:
                image = Image(self._pixel_data, framework=ImsFramework.PIL)
                image.resize(size)
                self._pixel_data = image.get_pixels(desired_format=self.pixel_format)
        else:
            raise NotImplemented
        self.width, self.height = size

    def resized(self, size: tuple) -> "Image":
        """
        Returns an image resized to to given resolution

        :param size: The new size
        """
        if self.framework == ImsFramework.PIL:
            return Image(self._pil_handle.resize(size, PIL.Image.LANCZOS), framework=ImsFramework.PIL)
        elif self._pixel_data is not None:
            return Image(self.to_pil().resize(size, PIL.Image.LANCZOS))
        else:
            raise NotImplemented

    def resized_ext(self, size: Optional[Tuple[int, int]] = None, keep_aspect: bool = False,
                    target_aspect: Optional[float] = None,
                    fill_area: bool = False, factor: Optional[float] = None,
                    interpolation: InterpolationMethod = InterpolationMethod.LANCZOS,
                    background_color=Color(0.0, 0.0, 0.0, 1.0)) -> "Image":
        """
        Returns a resized variant of the image with several different configuration possibilities.

        :param size: The target size as tuple (in pixels) (optional)
        :param keep_aspect: Defines if the aspect ratio shall be kept. if set to true the image
            will be zoomed or shrinked equally on both axis so it fits the target size. False by default.
        :param target_aspect: If defined the image will be forced into given aspect ratio by adding "black bars"
            (or the color you defined in "background_color"). Common values are for example 4/3, 16/9 or 21/9.
            Note that this does NOT change the aspect ratio of the real image itself. If you want to change this just
            call this function with the desired "size" parameter.
            It will always preserve the size of the axis to which no black bares are added, so e.g. converting an image
            from 4:3 to 16:9 resulting in black bars on left and right side the original height will be kept. Converting
            an image from 16:9 to 4:3 on the other hand where black bars are added on top and bottom the width will be
            kept. Overrides "size".
        :param fill_area: Defines if the whole area shall be filled with the original image. False by default. Only
            evaluated if keep_aspect is True as well as otherwise a simple definition of "size" would anyway do the job.
        :param factor: Scales the image by given factor. Overwrites size. Can be combined with target_aspect.
            None by default. Overrides "size".
        :param interpolation: The interpolation method.
        :param background_color: The color which shall be used to fill the empty area, e.g. when a certain aspect ratio
            is enforced.
        """
        handle = self.to_pil()
        resample_method = interpolation.to_pil()
        int_color = background_color.int_rgba()
        bordered_image_size = None  # target image size (including black borders)
        if keep_aspect and size is not None:
            if fill_area:
                factor = max([size[0] / self.width, size[1] / self.height])
                virtual_size = int(round(factor * self.width)), int(round(factor * self.height))
                ratio = size[0] / virtual_size[0], size[1] / virtual_size[1]
                used_pixels = int(round(self.width * ratio[0])), int(round(self.height * ratio[1]))
                offset = self.width // 2 - used_pixels[0] // 2, self.height // 2 - used_pixels[1] // 2
                return Image(handle.resize(size, resample=resample_method,
                                           box=[offset[0], offset[1], offset[0] + used_pixels[0] - 1,
                                                offset[1] + used_pixels[1] - 1]))
            else:
                bordered_image_size = size
                factor = min([size[0] / self.width, size[1] / self.height])
        if fill_area:
            raise ValueError('fill_area==True without keep_aspect==True has no effect. If you anyway just want to ' +
                             'fill the whole area with the image just provide "size" and set "fill_area" to False')
        if target_aspect is not None:
            if size is not None:
                raise ValueError('"target_aspect" can not be combined with "size" but just with factor. ' +
                                 'Use "size" + "keep_aspect" instead if you know the desired target size already.')
            factor = 1.0 if factor is None else factor
            if factor != 1.0:  # if the image shall also be resized
                size = int(round(self.width * factor)), int(round(self.height * factor))
            else:
                size = self.width, self.height
        if factor is not None:
            size = int(round(self.width * factor)), int(round(self.height * factor))
        assert size is not None and size[0] > 0 and size[1] > 0
        if size != (self.width, self.height):
            handle = handle.resize(size, resample=resample_method)
        if target_aspect is not None:
            rs = 1.0 / target_aspect
            cur_aspect = self.width / self.height
            if cur_aspect < target_aspect:  # if cur_aspect is smaller we need to add black bars to the sides
                bordered_image_size = (
                    int(round(self.height * target_aspect * factor)), int(round(self.height * factor)))
            else:  # otherwise to top and bottom
                bordered_image_size = (int(round(self.width * factor)), int(round(self.width * rs ** factor)))
        if bordered_image_size is not None:
            new_image = PIL.Image.new(handle.mode, bordered_image_size, int_color)
            position = (new_image.width // 2 - handle.width // 2, new_image.height // 2 - handle.height // 2)
            new_image.paste(handle, position)
            return Image(new_image)
        return Image(handle)

    def get_handle(self) -> Union[np.ndarray, PIL.Image.Image]:
        """
        Returns the low level data handle, for example a numpy array or a PIL handle.

        Do not use this to modify the data and be aware of the the type could change dynamically. Use
        :method:`~get_pixels` or :method:`~to_pil` if you need a guaranteed type.

        :return: The handle
        """
        return self._pil_handle if self.framework == ImsFramework.PIL else self._pixel_data

    @staticmethod
    def bgr_to_rgb(pixel_data: np.ndarray) -> np.ndarray:
        """
        Converts BGR to RGB or the otherwise round

        :param pixel_data: The input pixel data
        :return: The output pixel data
        """
        if len(pixel_data.shape) == 3 and pixel_data.shape[2] == 3:
            return pixel_data[..., ::-1].copy()
        elif len(pixel_data.shape) == 3 and pixel_data.shape[2] == 4:
            return pixel_data[..., [2, 1, 0, 3]].copy()

    @classmethod
    def normalize_to_rgb(cls, pixels: np.ndarray, input_format: PixelFormat = PixelFormat,
                         keep_gray=False) -> np.ndarray:
        """
        Guarantees that the output will be in the RGB or RGBA format

        :param pixels: The pixel data as :class:`np.ndarray`
        :param input_format: The input format representation, e.g. see :class:`.PixelFormat`
        :param keep_gray: Defines if single channel formats shall be kept intact. False by default.
        :return: The RGB image as numpy array. If keep_gray was set and the input was single channeled the original.
        """
        if len(pixels.shape) == 2:  # grayscale?
            if keep_gray:
                return pixels
            return np.stack((pixels,) * 3, axis=-1)
        if input_format == PixelFormat.BGR or input_format == PixelFormat.BGRA:
            return cls.bgr_to_rgb(pixels)
        else:
            return pixels

    @classmethod
    def normalize_to_bgr(cls, pixels: np.ndarray, input_format: PixelFormat = PixelFormat.RGB,
                         keep_gray=False) -> np.ndarray:
        """
        Guarantees that the output will be in the BGR or BGRA format

        :param pixels: The pixel data
        :param input_format: The input format representation, e.g. see :class:`.PixelFormat`
        :param keep_gray: Defines if single channel formats shall be kept intact. False by default.
        :return: The BGR image as numpy array. If keep_gray was set and the input was single channeled the original.
        """
        if len(pixels.shape) == 2:  # grayscale?
            if keep_gray:
                return pixels
            return np.stack((pixels,) * 3, axis=-1)
        if input_format == PixelFormat.BGR or input_format == PixelFormat.BGRA:
            return pixels
        else:
            return cls.bgr_to_rgb(pixels)

    @classmethod
    def normalize_to_gray(cls, pixels: np.ndarray, input_format: PixelFormat = PixelFormat.RGB) -> np.ndarray:
        """
        Guarantees that the output will be grayscale

        :param pixels: The pixel data :class:`np.ndarray`
        :param input_format: The input format representation, e.g. see :class:`.PixelFormat`
        :return: The grayscale image as :class:`np.ndarray`
        """
        if len(pixels.shape) == 2:  # grayscale?
            return pixels
        if input_format == PixelFormat.BGR or input_format == PixelFormat.BGRA:
            blue, green, red = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        else:
            red, green, blue = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        return (0.2989 * red + 0.5870 * green + 0.1140 * blue).round().astype(np.uint8)

    def get_pixels(self, desired_format: PixelFormat = PixelFormat.RGB) -> np.ndarray:
        """
        Returns the image's pixel data as :class:`np.ndarray`.

        Note that manipulating the data will has no effect to the image if the internal representation is not a numpy
        array.

        :param desired_format: The desired output pixel format, e.g. see :class:`.PixelFormat`
        :return: The numpy array containing the pixels
        """
        if self.framework != ImsFramework.PIL:  # not PIL
            pixel_data = self._pixel_data
        else:
            image: PIL.Image.Image = self._pil_handle
            # noinspection PyTypeChecker
            pixel_data = np.array(image)
        if self.pixel_format == desired_format:
            return pixel_data
        to_bgr = desired_format == PixelFormat.BGR or desired_format == PixelFormat.BGRA
        to_gray = desired_format == PixelFormat.GRAY
        to_rgb = desired_format == PixelFormat.RGB or desired_format == PixelFormat.RGBA
        if self.pixel_format not in {PixelFormat.RGB, PixelFormat.RGBA} and to_rgb:
            return self.normalize_to_rgb(pixel_data, input_format=self.pixel_format)
        elif to_gray:
            return self.normalize_to_gray(pixel_data, input_format=self.pixel_format)
        elif to_bgr:
            pixel_data = self.normalize_to_bgr(pixel_data, input_format=self.pixel_format)
        return pixel_data

    def get_pixels_rgb(self) -> np.ndarray:
        """
        Returns the pixels and ensures they are either rgb or rgba
        """
        return self.get_pixels(desired_format=PixelFormat.RGB)

    def get_pixels_bgr(self) -> np.ndarray:
        """
        Returns the pixels and ensures they are either bgr or bgra
        """
        return self.get_pixels(desired_format=PixelFormat.BGR)

    def get_pixels_gray(self) -> np.ndarray:
        """
        Returns the pixels and ensures they are gray scale
        """
        return self.get_pixels(desired_format=PixelFormat.GRAY)

    def to_pil(self) -> PIL.Image.Image:
        """
        Converts the image to a PIL image object

        :return: The PIL image
        """
        if self._pil_handle is not None:
            return self._pil_handle
        else:
            pixel_data = self.get_pixels()  # guarantee RGB
            return PIL.Image.fromarray(pixel_data)

    def encode(self, filetype: str = "png", quality: int = 90) -> Optional[bytes]:
        """
        Compresses the image and returns the compressed file's data as bytes object.

        :param filetype: The output file type. Valid types are "png", "jpg"/"jpeg", "bmp" and "gif"
        :param quality: The image quality between (0 = worst quality) and (95 = best quality). >95 = minimal loss
        :return: The bytes object if no error occurred, otherwise None
        """
        filetype = filetype.lstrip(".").lower()
        assert filetype in SUPPORTED_IMAGE_FILETYPE_SET
        if filetype == "jpg":
            filetype = "jpeg"
        parameters = {}
        if filetype.lower() in {"jpg", "jpeg"}:
            assert 0 <= quality <= 100
            parameters["quality"] = quality
        output_stream = io.BytesIO()
        self.to_pil().save(output_stream, format=filetype, **parameters)
        data = output_stream.getvalue()
        return data if len(data) > 0 else None

    def save(self, target: Union[str], **params):
        """
        Saves the image to disk

        :param target: The storage target such as a filename
        :param params: See :meth:`~encode`
        :return: True on success
        """
        with open(target, "wb") as output_file:
            extension = os.path.splitext(target)[1]
            data = self.encode(filetype=extension, **params)
            output_file.write(data)
            return data is not None


__all__ = ["Image", "IMAGE_SOURCE_TYPES", "PixelFormat", "InterpolationMethod"]
