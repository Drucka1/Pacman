import os
from PIL.ImageTk import PhotoImage

class GameImage():

    def __init__(self):
        ''' Initializes a game image object that holds all of the images for the game. 
            The os library is used to get the current directory, and then iterates 
            through all of the images inside the 'images' directory. '''
        self.start_directory = os.getcwd()

        # Ran from src directory
        if self.start_directory.split(os.sep)[-1] == "src":
            self.image_directory = os.path.join('..', 'static', 'images')
        # Ran from Pacman directory
        else:
            self.image_directory = os.path.join(self.start_directory, 'static', 'images')

        self.game_images = dict()

        for image in os.listdir(self.image_directory):
            self.game_images[image[:-4]] = PhotoImage(file=os.path.join(self.image_directory, image))

    def return_image(self, image) -> PhotoImage:
        ''' Returns the image from the image_directory given the image argument. '''
        return self.game_images[image]
