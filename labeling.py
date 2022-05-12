from union_find import UnionFind
import numpy as np
from PIL import Image 
from utils import image_to_2d_bool_array

CONNECTIVITY_4 = 4
CONNECTIVITY_8 = 8

def connected_component_labelling(input, connectivity_type=CONNECTIVITY_8):
	"""
		2 pass algorithm using disjoint-set data structure with Union-Find algorithms to maintain 
		record of label equivalences.
	"""
	if connectivity_type !=4 and connectivity_type != 8:
		print("Invalid connectivity type (choose 4 or 8)")
		exit()


	print(input)
	width, height = input.size
	bw_image = image_to_2d_bool_array(input)


	result = np.zeros((height, width), dtype=np.int16)
	uf = UnionFind()
	current_label = 1

	# 1st Pass: label image and record label equivalences
	for y, row in enumerate(bw_image):
		for x, pixel in enumerate(row):
			
			if pixel != False:
				# Foreground pixel - work out what its label should be

				# Get set of neighbour's labels
				labels = neighbouring_labels(result, connectivity_type, x, y)

				if not labels:
					# If no neighbouring foreground pixels, new label -> use current_label 
					result[y,x] = current_label
					uf.MakeSet(current_label)
					current_label = current_label + 1			
				
				else:
					# Pixel is definitely part of a connected component: get smallest label of 
					# neighbours
					smallest_label = min(labels)
					result[y,x] = smallest_label

					if len(labels) > 1: # More than one type of label in component -> add 
										# equivalence class
						for label in labels:
							uf.Union(uf.GetNode(smallest_label), uf.GetNode(label))


	# 2nd Pass: replace labels with their root labels
	final_labels = {}
	new_label_number = 1

	for y, row in enumerate(result):
		for x, pixel_value in enumerate(row):
			
			if pixel_value > 0: # Foreground pixel
				# Get element's set's representative value and use as the pixel's new label
				new_label = uf.Find(uf.GetNode(pixel_value)).value 
				result[y,x] = new_label

				# Add label to list of labels used, for 3rd pass (flattening label list)
				if new_label not in final_labels:
					final_labels[new_label] = new_label_number
					new_label_number = new_label_number + 1


	# 3rd Pass: flatten label list so labels are consecutive integers starting from 1 (in order 
	# of top to bottom, left to right)
	# Different implementation of disjoint-set may remove the need for 3rd pass?
	for y, row in enumerate(result):
		for x, pixel_value in enumerate(row):
			
			if pixel_value > 0: # Foreground pixel
				result[y,x] = final_labels[pixel_value]

	return Image.fromarray(result)



def neighbouring_labels(image, connectivity_type, x, y):
	"""
		Gets the set of neighbouring labels of pixel(x,y), depending on the connectivity type.
		Labelling kernel (only includes neighbouring pixels that have already been labelled - 
		row above and column to the left):
			Connectivity 4:
				    n
				 w  x  
			 
			Connectivity 8:
				nw  n  ne
				 w  x   
	"""

	labels = set()

	if (connectivity_type == CONNECTIVITY_4) or (connectivity_type == CONNECTIVITY_8):
		# West neighbour
		if x > 0: # Pixel is not on left edge of image
			west_neighbour = image[y,x-1]
			if west_neighbour > 0: # It's a labelled pixel
				labels.add(west_neighbour)

		# North neighbour
		if y > 0: # Pixel is not on top edge of image
			north_neighbour = image[y-1,x]
			if north_neighbour > 0: # It's a labelled pixel
				labels.add(north_neighbour)


		if connectivity_type == CONNECTIVITY_8:
			# North-West neighbour
			if x > 0 and y > 0:
				northwest_neighbour = image[y-1,x-1]
				if northwest_neighbour > 0:
					labels.add(northwest_neighbour)

			# North-East neighbour
			if y > 0 and x < len(image[y]) - 1:
				northeast_neighbour = image[y-1,x+1]
				if northeast_neighbour > 0:
					labels.add(northeast_neighbour)
	else:
		print("Connectivity type not found.")
	return labels




