"""numpy implementation of image filters"""

from typing import Optional
import numpy as np
from PIL import Image

def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
   
    # Hint: use numpy slicing in order to have fast vectorized code
    image_copy = gray_image.copy()
    
    gray_image[:,:,0] = (gray_image[:,:,0] * 0.21 + gray_image[:,:,1] * 0.72 + gray_image[:,:,2] * 0.07) / 3
    gray_image[:,:,1] = (image_copy[:,:,0] * 0.21 + image_copy[:,:,1] * 0.72 + image_copy[:,:,2] * 0.07) / 3
    gray_image[:,:,2] = (image_copy[:,:,0] * 0.21 + image_copy[:,:,1] * 0.72 + image_copy[:,:,2] * 0.07) / 3
    
    

    #gray_image = np.dot(gray_image[:,:,:3], [0.21, 0.72, 0.07])
    #gray_image = gray_image/3
 
    gray_image = gray_image.astype("uint8") # Converting float
 
    return gray_image

def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """


    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")


    ####
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix

    sepia_matrix = [
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131]]
    
    sepia_image = np.dot(sepia_image[:,:,0], [0.393, 0.769, 0.189])
    sepia_image = np.dot(sepia_image[:,:,1], [0.349, 0.686, 0.168])
    sepia_image = np.dot(sepia_image[:,:,2], [0.272, 0.534, 0.131])
    #sepia_matrix = np.array(sepia_matrix)
    """ image_copy = sepia_image.copy()
    sepia_image[:,:,0] = (image_copy[:,:,0] * 0.393 + image_copy[:,:,1] * 0.769 + image_copy[:,:,2] * 0.189) / 3
    sepia_image[:,:,1] = (image_copy[:,:,0] * 0.349 + image_copy[:,:,1] * 0.686 + image_copy[:,:,2] * 0.168) / 3
    sepia_image[:,:,2] = (image_copy[:,:,0] * 0.272 + image_copy[:,:,1] * 0.534 + image_copy[:,:,2] * 0.131) / 3
    """
    

   #####

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix
    # Apply the matrix filter


    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    vfunc = np.vectorize(min_val)
    vfunc(sepia_image)
    # Return image (make sure it's the right type!)
    sepia_image = sepia_image.astype("uint8") # Converting float
    return sepia_image

def min_val(a):
    if a > 255:
        return 255
    return a


filename = "../test/rain.jpg"
pixels = np.asarray(Image.open(filename))

#image = Image.fromarray(pixels)
#image.display(pixels)

grayscale_image = numpy_color2gray(pixels)

#image = Image.fromarray(grayscale_image)
#image.save("../test/test.jpg")

Image.fromarray(grayscale_image).show()



