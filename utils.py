import numpy as np

def image_to_2d_bool_array(image):
	im2 = image.convert('L')
	arr = np.asarray(im2)
	arr = arr != 0

	return arr
	
def normalize(image):
    result = image.copy()
    width, height = image.size
    min,max = image.getextrema()

    
    if min == max:
        return image;

    for x in range(width):
        for y in range(height):
            normalized = int((image.getpixel((x,y)) - min) * 255 / (max - min))

            result.putpixel((x,y), (normalized))
    return result