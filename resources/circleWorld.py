import pygame
from pygame.locals import *
import numpy as np
import math
import random
from resources.circles import Circle

BACKGROUND_COLOR = (255, 0, 0)
MAX_RADIUS = 50
MUTATION_RATE = 1
IDEAL_RADIUS = 20
IDEAL_COLOR = (255, 255, 0)
random.seed()




class App(object):
    def __init__(self, width=640, height=480):
        self._running = True
        self._display_surface = None
        self.display_size = self.width, self.height = width, height

        self._generate_circle_center_coords()
        self._generation_number = 0

        self._skip10 = False
        self._skip100 = False
        self._skip1000 = False


    def _generate_circle_center_coords(self):
        self.circle_rows = int(int(self.height - self.height*.2) / MAX_RADIUS)
        self.circle_cols = int(self.width / MAX_RADIUS)

        self.circle_center_coords = []
        for row in range(self.circle_rows):
            circle_center_y = int(MAX_RADIUS / 2) + MAX_RADIUS * row
            for col in range(self.circle_cols):
                circle_center_x = int(MAX_RADIUS / 2) + MAX_RADIUS * col
                circle_center = (circle_center_x, circle_center_y)
                self.circle_center_coords.append(circle_center)


    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.display_size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        # Initial parent generation of circles
        # generate cirlces
        self.circles = []
        for circle_center in self.circle_center_coords:
            circle_center_coords = circle_center
            new_circle = Circle(circle_center_coords)
            self.circles.append(new_circle)


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = self._pause = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._pause = False
            elif event.key == pygame.K_UP:
                self._pause = False
                self._skip10 = True
            elif event.key == pygame.K_DOWN:
                self._pause = False
                self._skip100 = True
            elif event.key == pygame.K_g:
                self._pause = False
                self._skip1000 = True
            elif event.key == pygame.K_q:
                self._pause = self._running = False


    def on_loop(self):
        self._generation_number += 1

    def on_render(self):
        # Background
        self._display_surface.fill(BACKGROUND_COLOR)

        # Circles
        for circle in self.circles:
            circle.draw(self._display_surface)

        # Generation number
        text_font = pygame.font.Font(None, 30)
        text = text_font.render("Generation: "+str(self._generation_number), 1, (255, 255, 255))
        self._display_surface.blit(text, (int(self.width * .4), int(self.height * .9)))

        pygame.display.update()
        self._pause = True


    def fitness(self):
        dtype = [('index', int), ('fitness', int)]

        fitness_values = []
        for index, circle in enumerate(self.circles):
            circle_fitness = circle.get_fitness()
            fitness_values.append((index, circle_fitness))

        fitness = np.array(fitness_values, dtype=dtype)
        self.sorted_fitness = np.sort(fitness, order='fitness')


    def selection(self):
        self.top_circles = []

        num_top_cirlces = int(len(self.circles)/2)

        for circle in self.sorted_fitness[:num_top_cirlces]:
            circle_index = circle[0]
            circle_fitness = circle[1]
            circle = self.circles[circle_index]
            circle.set_fitness(circle_fitness)
            self.top_circles.append(circle)


    def replication(self):
        self.circles = []

        coordinate_index = 0
        for index, parent in enumerate(self.top_circles[::2]):
            parent1 = parent
            parent2 = self.top_circles[index+1]
            parents = [parent1, parent2]

            for _ in range(4):
                coordinate = self.circle_center_coords[coordinate_index]
                new_circle = self.circle_sex(coordinate, parents)
                self.circles.append(new_circle)
                coordinate_index += 1


    def circle_sex(self, coordinate, parents):

        parent1_color = parents[0].color
        parent2_color = parents[1].color
        parent1_radius = parents[0].radius
        parent2_radius = parents[1].radius

        chance_for_mutation = np.random.randint(100)
        if chance_for_mutation <= MUTATION_RATE:
            # Color mutation
            color = ()
            for parent1, parent2 in zip(parent1_color, parent2_color):
                color_val = int(np.average([parent1, parent2]))
                mutation = -1*np.random.randint(30) if np.random.randint(2) == 0 else np.random.randint(30)
                mutation += color_val

                if mutation < 0:
                    mutation = 0
                elif mutation > 255:
                    mutation = 255

                color += (mutation,)

            # Radius mutation
            radius_val = int(np.average([parent1_radius, parent2_radius]))
            mutation = -1*np.random.randint(3) if np.random.randint(2) == 0 else np.random.randint(3)
            mutation = max(0, mutation)
            radius = mutation

        else:
            color = parents[np.random.randint(2)].color
            radius = parents[np.random.randint(2)].radius

        new_circle = Circle(coordinate, radius, color)
        return new_circle

    def on_hold(self):
        while self._pause:
            for event in pygame.event.get():
                self.on_event(event)

    def on_cleanup(self):
        pygame.quit()

    def launch(self):
        if self.on_init() == False:
            self._running = False

        skip_counter = 0
        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

            # Evolution
            self.fitness()
            self.selection()
            self.replication()

            # Skips
            if self._skip10:
                if skip_counter == 10:
                    self._skip10 = False
                    skip_counter = 0
                else:
                    skip_counter += 1

            elif self._skip100:
                if skip_counter == 100:
                    self._skip100 = False
                    skip_counter = 0
                else:
                    skip_counter += 1

            elif self._skip1000:
                if skip_counter >= 1000:
                    self._skip1000 = False
                    skip_counter = 0
                else:
                    skip_counter += 1

            # Pause
            else:
                self.on_hold()

        self.on_cleanup()


if __name__ == "__main__":
    circleWorld = App()
    circleWorld.launch()
