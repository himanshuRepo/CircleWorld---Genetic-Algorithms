import numpy as np
import math
import pygame

MAX_RADIUS = 50
IDEAL_RADIUS = 20
IDEAL_COLOR = (255, 255, 0)

class Circle(object):
    def __init__(self, center=None, radius=None, color=None):
        if radius != None:
            self.center = center
            self.radius = radius
            self.color = color
        else:
            self.center = center
            self.gen_color()
            self.gen_radius()


    def gen_color(self):
        self.color = tuple([self.random_index_generator(256) for _ in range(3)])

    def gen_radius(self):
        self.radius = min(self.random_index_generator(MAX_RADIUS), int(MAX_RADIUS/2))

    def random_index_generator(self, size):
        return np.random.randint(size)

    def draw(self, display_surface):
        pygame.draw.circle(display_surface, self.color, self.center, self.radius, 0)

    def transfer_genes(self):
        return self.color, self.radius

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_fitness(self):
        # Color
        diff1 = math.fabs(IDEAL_COLOR[0] - self.color[0])
        diff2 = math.fabs(IDEAL_COLOR[1] - self.color[1])
        diff3 = math.fabs(IDEAL_COLOR[2] - self.color[2])
        fitness = (diff1 + diff2 + diff3)**2

        # Radius
        diff4 = IDEAL_RADIUS - self.radius
        fitness += diff4**2

        return fitness
