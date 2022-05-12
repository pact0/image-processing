import numpy as np
import math

def entropyFilt(input, distance = 4):
    N = 3 * (2 * distance + 1) * (2 * distance + 1)
    rgb_im = input.convert('RGB')

    width, height = rgb_im.size
    result = rgb_im.copy()
    results = np.zeros(width * height)

    for x in range(width):
        for y in range(height):

            #hist = [[0] * width] * height
            hist = np.zeros(width * height)
            # iterate over neighbours
            for i in range(-distance,distance):
                for j in range(-distance,distance):
                        adjX = x + i; 
                        if (adjX < 0 or adjX >= width):
                             adjX = x - i
                        adjY = y + j
                        if (adjY < 0 or adjY >= height):
                            adjY = y - j
                        r,g,b = rgb_im.getpixel((adjX,adjY))
                        hist[r] = hist[r] + 1
                        hist[g] = hist[g] + 1
                        hist[b] = hist[b] + 1

            E = 0
            for i in range(256):
                prob = hist[i] / N
                if prob != 0:
                    tempE = -1 * (math.log2(prob) * prob)
                    E = E+tempE
            results[y*width+x] = E
    
    pMin = min(results)
    pMax = max(results)
    
    if pMin == pMax:
        return input;

    for x in range(width):
        for y in range(height):
            normalized = int((results[y*width + x] - pMin) * 255 / (pMax - pMin))

            result.putpixel((x,y), (normalized,normalized,normalized))
    return result