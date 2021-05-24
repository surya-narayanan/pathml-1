"""
Copyright 2021, Dana-Farber Cancer Institute and Weill Cornell Medicine
License: GNU GPL 2.0
"""

import pytest
import numpy as np
import cv2
import openslide
import javabridge

from pathml.core import HESlide, Tile, Masks, types


def pytest_sessionfinish(session, exitstatus):
    """
    Pytest will not terminate if javabridge is not killed.
    But if we terminate javabridge in BioFormatsBackend, we can not spawn another javabridge in the same thread.

    This Pytest sessionfinish hook runs automatically at the end of testing.
    """
    javabridge.kill_vm()


def create_HE_tile():
    s = openslide.open_slide("tests/testdata/small_HE.svs")
    im_image = s.read_region(level = 0, location = (900, 800), size = (500, 500))
    im_np = np.asarray(im_image)
    im_np_rgb = cv2.cvtColor(im_np, cv2.COLOR_RGBA2RGB)
    # make mask object
    masks = np.random.randint(low = 1, high = 255, size = (im_np_rgb.shape[0], im_np_rgb.shape[1]), dtype = np.uint8)
    masks = Masks(masks = {"testmask": masks})
    # labels dict
    labs = {"test_string_label": "testlabel", "test_array_label": np.array([2, 3, 4]),
            "test_int_label": 3,  "test_float_label": 3.0}
    tile = Tile(image = im_np_rgb, coords = (1, 3), masks = masks, labels = labs)
    return tile




@pytest.fixture
def tileHE():
    """
    Example of pathml.core.Tile object
    """
    tile = create_HE_tile()
    tile.slide_type = types.HE
    return tile
