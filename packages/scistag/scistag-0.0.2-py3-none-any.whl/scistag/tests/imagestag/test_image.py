"""
Tests the features of the scistag.imagestag.image.Image class
"""
import os

import numpy as np
from scistag.imagestag import Image, ImsFramework
from image_tests_common import stag_image_data
import pytest


def test_load(stag_image_data):
    """
    Tests loading an image from disk
    :param stag_image_data: The stag data fixture
    """
    image = Image(stag_image_data)
    assert image.get_size() == (665, 525)
    assert image.to_pil() is not None
    pixels = image.get_pixels()
    assert pixels.shape == (525, 665, 3)


def test_resize(stag_image_data):
    """
    Tests resizing an image
    :param stag_image_data: The stag data fixture
    """
    image = Image(stag_image_data)
    image.resize((100, 120))
    assert image.get_pixels().shape == (120, 100, 3)


def test_raw(stag_image_data):
    """
    Tests storing an image using numpy array storage
    :param stag_image_data: The stag data fixture
    """
    image_raw = Image(stag_image_data, framework=ImsFramework.RAW)
    data = image_raw.get_handle()
    assert isinstance(data, np.ndarray)


def test_image_color_conversion(stag_image_data):
    """
    Tests the color conversion functions of Image
    :param stag_image_data: The image data in bytes
    """
    image = Image(stag_image_data)
    pixel_data = image.get_pixels()
    bgr_pixel_data = image.get_pixels_bgr()
    gray_pixel_data = image.get_pixels_gray()
    rgb_pixel = (144, 140, 137)
    assert tuple(pixel_data[50, 50, :]) == rgb_pixel
    assert tuple(bgr_pixel_data[50, 50, :]) == (137, 140, 144)
    assert gray_pixel_data[50, 50] == round((np.array(rgb_pixel) * (0.2989, 0.5870, 0.1140)).sum())
    grayscale_image = Image(gray_pixel_data)


def test_resize_ext(stag_image_data):
    """
    Tests Image.resize_ext
    :param stag_image_data: The image data in bytes
    """
    image = Image(stag_image_data)
    # to widescreen
    rescaled = image.resized_ext(target_aspect=16 / 9)  # aspect ratio resizing
    rescaled_pixels = rescaled.get_pixels()
    black_bar_mean = rescaled_pixels[0:, 0:100].mean() + rescaled_pixels[0:, -100:].mean()
    assert black_bar_mean == 0.0
    mean_rescaled = np.mean(rescaled_pixels)
    assert mean_rescaled == pytest.approx(87.5, 0.5)
    # to portrait mode
    rescaled = image.resized_ext(target_aspect=9 / 16)  # aspect ratio resizing
    rescaled_pixels = rescaled.get_pixels()
    black_bar_mean = rescaled_pixels[0:100, 0:].mean() + rescaled_pixels[-100:, 0:].mean()
    assert black_bar_mean == 0.0
    assert rescaled.width < rescaled.height
    # fill widescreen
    filled = image.resized_ext(size=(1920, 1080), fill_area=True, keep_aspect=True)
    filled_pixels = filled.get_pixels()
    mean_filled = np.mean(filled_pixels)
    assert mean_filled == pytest.approx(120.6, 0.05)
    assert filled.width == 1920
    # filled portrait
    filled = image.resized_ext(size=(1080, 1920), fill_area=True, keep_aspect=True)
    filled_pixels = filled.get_pixels()
    mean_filled = np.mean(filled_pixels)
    assert mean_filled == pytest.approx(120.6, 0.05)
    assert filled.width == 1080
    just_scaled = image.resized_ext(size=(600, 600))
    just_scaled_pixels = just_scaled.get_pixels()
    just_scaled_mean = np.mean(just_scaled_pixels)
    assert just_scaled_mean == pytest.approx(120, 0.05)
    scaled_aspect = image.resized_ext(target_aspect=16 / 9, factor=2.0)
    scaled_aspect = scaled_aspect.get_pixels()
    scaled_aspect_mean = np.mean(scaled_aspect)
    assert scaled_aspect_mean == pytest.approx(87.5, 0.05)
    # test exceptions
    try:
        image.resized_ext(size=(1080, 1920), fill_area=True, keep_aspect=False)
        assert False  # shouldn't be reached
    except ValueError:
        pass
    try:
        image.resized_ext(size=(1080, 1920), target_aspect=16 / 9)
        assert False  # shouldn't be reached
    except ValueError:
        pass


def test_encoding(stag_image_data, tmp_path):
    """
    Tests encoding the image in different formats
     :param stag_image_data: The stag data fixture
    """

    # in memory encoding
    image = Image(stag_image_data)
    jpg1_data = image.encode(filetype="jpg", quality=95)
    assert jpg1_data is not None and len(jpg1_data) > 2000
    jpg2_data = image.encode(filetype="jpg", quality=20)
    assert jpg2_data is not None and len(jpg2_data) < len(jpg1_data)
    png_data = image.encode(filetype="png")
    assert png_data is not None and len(png_data) > 0
    test_path = str(tmp_path.joinpath("test_output.png"))
    image.save(target=test_path)
    assert os.path.getsize(test_path) == len(png_data)
    decoded_png = Image(png_data)
    assert np.array_equal(decoded_png.get_pixels_rgb(), image.get_pixels_rgb())
    bmp_data = image.encode(filetype="bmp")
    assert bmp_data is not None and len(bmp_data) > 0
    decoded_bmp = Image(bmp_data)
    assert np.array_equal(decoded_bmp.get_pixels_rgb(), image.get_pixels_rgb())

    # disk encoding
