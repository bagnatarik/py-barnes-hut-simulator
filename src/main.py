from classes.two_dimensions.window import Window
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

Window.initializefont()

pygame.init()

width, height = 800, 800

# Créer la fenêtre
screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Window.killfont()
            pygame.quit()
            quit()

    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Window.text_out("Hello, OpenGL!")
    # Window.text_out_at(100, 100, "Positioned Text")
    # pygame.display.flip()
    # pygame.time.wait(10)