import pygame
import csv
from settings import *
def import_map_data(path):

    temp_list = []
    with open(path) as file:
        rows = csv.reader(file)
        for row in rows:
            temp_list.append(row)

    return temp_list


def import_images(path):
    
    temp_list = []
    image = pygame.image.load(path).convert_alpha()
    image_width = image.get_width()
    number_tiles = image_width//tile_size

    for i in range(number_tiles):
        new_image = image.subsurface(pygame.Rect(i*tile_size, 0, tile_size, tile_size))
        transformed_image = pygame.transform.scale(new_image, (tile_size*scaling_factor, tile_size*scaling_factor))
        temp_list.append(transformed_image)

    return temp_list
