import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialisation Pygame + OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Configuration OpenGL
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)  # Recule la caméra

# Données du labyrinthe (1 = mur, 0 = chemin)
maze = np.array([
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
])

def draw_cube(x, y, z):
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.4, 0.2)  # Couleur orange
    # Face avant
    glVertex3f(x-0.5, y-0.5, z+0.5)
    glVertex3f(x+0.5, y-0.5, z+0.5)
    glVertex3f(x+0.5, y+0.5, z+0.5)
    glVertex3f(x-0.5, y+0.5, z+0.5)
    # [...] autres faces (arrière, dessus, dessous, etc.)
    glEnd()

def main():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Gestion des touches (Pygame)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            glRotatef(1, 0, 1, 0)  # Tourne à gauche
        if keys[K_RIGHT]:
            glRotatef(-1, 0, 1, 0) # Tourne à droite

        # Rendu 3D (OpenGL)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
