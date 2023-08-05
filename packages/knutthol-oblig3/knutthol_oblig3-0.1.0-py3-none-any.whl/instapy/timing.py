"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
#import instapy
#from . import io
from typing import Callable
import numpy as np
from PIL import Image
import python_filters
import numpy_filters
import numba_filters


def time_one(filter_function: Callable, arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """

    # run the filter function `calls` times
    tid = 0.0
    for call in range(calls): # Calculate the average time of n calls
        start = time.perf_counter()
        filter_function(arguments)
        end = time.perf_counter()
        tid += end - start
    return tid/calls

    # return the _average_ time of one call


def make_reports(filename: str = "../test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    # load the image
    image = np.asarray(Image.open(filename))
    img_tuple = image.shape

    print(f"\nTiming preformed using {filename}: {img_tuple[1]}x{img_tuple[0]}") # print the image name, width, height
    # iterate through the filters
    filter_names = ["color2gray", "color2sepia"]
    for filter_name in filter_names:
        # get the reference filter function
        if filter_name == "color2gray":
            reference_filter = python_filters.python_color2gray
        elif filter_name == "color2seipa":
            reference_filter = python_filters.python_color2sepia
        # time the reference implementation
        reference_time = time_one(reference_filter, image, 3)

        print(
            f"\nReference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )
        # iterate through the implementations
        implementations = ["numpy"]
        for implementation in implementations:

            filter_time = 0.0 
            if implementation == "numpy" and filter_name == "color2gray":
                filter_time = time_one(numpy_filters.numpy_color2gray, image, 3) # time the filter
            elif implementation == "numpy" and filter_name == "color2sepia":
                filter_time = time_one(numpy_filters.numpy_color2sepia, image, 3) # time the filter
            elif implementation == "numba" and filter_name == "color2gray": 
                filter_time = time_one(numba_filters.numba_color2gray, image, 3) # time the filter
            elif implementation == "numba" and filter_name == "color2sepia":
                filter_time = time_one(numba_filters.numba_color2sepia, image, 3) # time the filter
            else:
                pass

            # compare the reference time to the optimized time
            speedup = reference_time / filter_time
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
            )


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()



