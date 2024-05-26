import os
import pygame

ASSETS_IMAGE = "assets/images/"


def load_image(path):
    """Load an image.
    Load an image from the assets/images folder
    And return it with the colorkey set to black (for transparency).

    Args:
        path (str): The path to the image file.

    Returns:
        pygame.Surface: The image loaded.
    """
    image = pygame.image.load(ASSETS_IMAGE + path).convert()
    image.set_colorkey((0, 0, 0))

    return image


def load_images(path):
    """Load multiple images.
    Load multiple images from the assets/images folder
    And return them with the colorkey set to black (for transparency).

    Args:
        path (str): The path to the images folder.

    Returns:
        list: A list of images loaded.
    """
    images = []
    for image in sorted(os.listdir(ASSETS_IMAGE + path)):
        images.append(load_image(path + '/' + image))

    return images
