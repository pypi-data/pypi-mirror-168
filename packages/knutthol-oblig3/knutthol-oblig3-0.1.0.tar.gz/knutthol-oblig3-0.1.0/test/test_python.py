#from instapy.python_filters import python_color2gray, python_color2sepia
from python_filters import *
import numpy as np
from PIL import Image
import pytest


def test_color2gray(image):
    """ Method tests if the color2gray function returns correct results"""
    # run color2gray
    filename = "test/rain.jpg"
    pixels = np.asarray(Image.open(filename))
    grayscale_image = python_color2gray(pixels)
    # check that the result has the right shape, type
    print(grayscale_image.shape)
    assert isinstance(grayscale_image, np.array) == True # Test if filter function returns numpyarray
    assert grayscale_image.shape == (600,400,3) # Test if image shape is corect
    assert grayscale_image[0][0][:3] == [23, 23, 342] # Test if pixle is corectly filtered
    assert grayscale_image[0][1][:3] == [23, 23, 342] # Test if pixle is corectly filtered
    assert grayscale_image[0][2][:3] == [23, 23, 342] # Test if pixle is corectly filtered
    # assert uniform r,g,b values


def test_color2sepia(image):
    # run color2sepia
    # check that the result has the right shape, type
    filename = "test/rain.jpg"
    pixels = np.asarray(Image.open(filename))
    grayscale_image = python_color2sepia(pixels)
    # check that the result has the right shape, type
    print(grayscale_image.shape)
    assert isinstance(grayscale_image, np.array) == True # Test if filter function returns numpyarray
    assert grayscale_image.shape == (600,400,3) # Test if image shape is corect

    # verify some individual pixel samples
    # according to the sepia matrix
    assert grayscale_image[0][0][:3] == [23, 23, 342] # Test if pixle is corectly filtered
    assert grayscale_image[0][1][:3] == [23, 23, 342] # Test if pixle is corectly filtered
    assert grayscale_image[0][2][:3] == [23, 23, 342] # Test if pixle is corectly filtered
