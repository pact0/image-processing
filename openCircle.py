import numpy as np

def create_circular_mask(h, w, center=None, radius=None):
    """
        Creates a circular mask with specified height, widtth, center and radius.
    """

    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask


def erode(input, radius=2):
    """
        Erodes the grayscale, binary, or packed binary image input
        using the circular structuring element witth specified radius.
        Returns processed image.
    """
    rgb_im = input.convert('RGB')

    width, height = rgb_im.size
    result = rgb_im.copy()
    mask = create_circular_mask(2*radius+1,2*radius+1)
    maskWidth, maskHeight = mask.shape

    for x in range(width):
        for y in range(height):
            R = []
            G = []
            B = []

            for i in range(maskWidth):
                for j in range(maskHeight):
                    if mask[i][j] == False:
                        continue

                    adjX = x+i - radius
                    adjY = y+j - radius

                    if adjX < 0 or adjX >= width or adjY < 0 or adjY >= height:
                        R.append(0)
                        G.append(0)
                        B.append(0)
                    else:
                        r,g,b = rgb_im.getpixel((adjX,adjY))
                        R.append(r)
                        G.append(g)
                        B.append(b)

            result.putpixel((x,y),(min(R),min(G),min(B)))
    return result


def dilate(input, radius=2):
    """
        Dilates the grayscale, binary, or packed binary image input
        using the circular structuring element witth specified radius.
        Returns processed image.
    """
    rgb_im = input.convert('RGB')

    width, height = rgb_im.size
    result = rgb_im.copy()
    mask = create_circular_mask(2*radius+1,2*radius+1)
    maskWidth, maskHeight = mask.shape

    for x in range(width):
        for y in range(height):
            R = []
            G = []
            B = []

            for i in range(maskWidth):
                for j in range(maskHeight):
                    if mask[i][j] == False:
                        continue

                    adjX = x+i - radius
                    adjY = y+j - radius

                    if adjX < 0 or adjX >= width or adjY < 0 or adjY >= height:
                        R.append(0)
                        G.append(0)
                        B.append(0)
                    else:
                        r,g,b = rgb_im.getpixel((adjX,adjY))
                        R.append(r)
                        G.append(g)
                        B.append(b)

            result.putpixel((x,y),(max(R),max(G),max(B)))
    return result


def openCircle(input, radius=2):
    """
        Performs morphological opening on the grayscale or binary image input using the 
        structuring element which in this case is circular with specified radius.
        The morphological opening operation is an erosion followed by a dilation, 
        using the same structuring element for both operations. Returns processed image.
    """
    return erode(dilate(input,radius), radius)