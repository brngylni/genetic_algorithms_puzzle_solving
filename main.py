from evolution import Evolution
from PIL import Image

'''
Usage:
Evolution(patch_size, image, population_size, generations, mutation_percentage)
Image must be grayscale.
This doesn't work well for the odd patch sizes yet. Tried to do some work but couldn't acquired the necessary actions.
'''

evolution = Evolution(5, Image.open('image2.jpg'), 20, 200, 10)
evolution.coaservate_to_human()


