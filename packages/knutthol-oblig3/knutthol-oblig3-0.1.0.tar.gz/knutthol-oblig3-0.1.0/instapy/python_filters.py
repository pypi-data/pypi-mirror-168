"""pure Python implementation of image filters"""

import numpy as np
import math
from PIL import Image


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform

    image_list = gray_image.tolist() # Converted to python list for pure python code
    for x in range(len(image_list)): # Looping through the x dimention of the image 
        for y in range(len(image_list[x])): # Looping through the y dimention of the image
            red = image_list[x][y][0] * 0.21
            green = image_list[x][y][1] * 0.72
            blue = image_list[x][y][2] * 0.07
            weighted_rgb = (red + green + blue)/3 # Calculating weighted rgb value
            for c in range(len(image_list[x][y])): # Updating pixels rgb values
                image_list[x][y][c] = weighted_rgb

    gray_image = np.array(image_list) # Converting from python list to numpy array
    gray_image = gray_image.astype("uint8") # Converting float values to int values
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    # Iterate through the pixels
    # applying the sepia matrix

    sepia_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform

    image_list = sepia_image.tolist() # Converted to python list for pure python code
    for x in range(len(image_list)): # Looping through the x dimention of the image 
        for y in range(len(image_list[x])): # Looping through the y dimention of the image
            image_list[x][y][0] = min(255,(image_list[x][y][0] * 0.393 + image_list[x][y][1] * 0.769 + image_list[x][y][2] * 0.189) / 3)
            image_list[x][y][1] = min(255,(image_list[x][y][0] * 0.349 + image_list[x][y][1] * 0.686 + image_list[x][y][2] * 0.168) / 3)
            image_list[x][y][2] = min(255,(image_list[x][y][0] * 0.272 + image_list[x][y][1] * 0.534 + image_list[x][y][2] * 0.131) / 3)


    sepia_image = np.array(image_list) # Converting from python list to numpy array
    sepia_image = sepia_image.astype("uint8") # Converting float values to int values

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image


filename = "../test/rain.jpg"
pixels = np.asarray(Image.open(filename))

#image = Image.fromarray(pixels)
#image.display(pixels)

#grayscale_image = python_color2gray(pixels)
grayscale_image = python_color2sepia(pixels)
#image = Image.fromarray(grayscale_image)
#image.save("../test/test.jpg")

Image.fromarray(grayscale_image).show()

#filename = "rain.jpg"
#pixels = np.asarray(Image.open(filename))
#pixels = np.asarray(image)
#image = Image.fromarray(pixels)