import numpy as np


class City:


     def __init__(self, x, y, name):
         self.x = x
         self.y = y
         self.name = name


     def distance(self, City2):

         dif_x = self.x - City2.x
         dif_y = self.y - City2.y

         return np.sqrt(np.square(dif_x) - np.square(dif_y))