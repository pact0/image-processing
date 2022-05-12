from tkinter import W
from PIL import Image 
import argparse

from openCircle import openCircle
from entropyFilt import entropyFilt
from labeling import connected_component_labelling
from utils import normalize


parser = argparse.ArgumentParser(description='Image processing.')
parser.add_argument('--method', type=str,
                    help='One of the methods: openCircle, entropyFilt, labeling',
                    required=True)
parser.add_argument('--args', type=str, nargs='+',
                    help="""Additional arguments to chosen method:\n
                    openCircle - circle radius (default 2),
                    entropyFilt - distance (default 4),
                    label - connectivity type (default 8)""",
                    required=False)
parser.add_argument('--input', type=str,
                    help='Input image to be processed.',
                    required=True)
parser.add_argument('--output', type=str,
                    help='Path to where a result will be placed.',
                    required=True)
args = parser.parse_args()


try:
    image =Image.open(args.input)

    if args.method == "openCircle":
        result = openCircle(image)

    if args.method == "entropyFilt":
        result = entropyFilt(image)

    if args.method == "labeling":
        result = normalize(connected_component_labelling(image,4))

    image.close()
    result.show()
    result.save(args.output)
except:
    print("Something went wrong...")
    exit()
