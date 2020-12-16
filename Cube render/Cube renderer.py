import math
import sys
import pygame.freetype
from pygame.locals import *
import numpy as np
import time


class Vec3d:
    def __init__(self):
        self.vec = [0, 0, 0, 0]

    @property
    def x(self):
        return self.vec[0]
    @property
    def y(self):
        return self.vec[1]


class Triangle:
    def __init__(self):
        self.triangle = [Vec3d() for i in range(3)]


class Mesh:
    def __init__(self):
        self.halfside = [Triangle() for n in range(12)]


mesh_cube = Mesh()
mesh_cube.halfside[0].triangle[0].vec, mesh_cube.halfside[0].triangle[1].vec, mesh_cube.halfside[0].triangle[2].vec = \
    [0, 0, 0, 1], [0, 1, 0, 1], [1, 1, 0, 1]    # south 1
mesh_cube.halfside[1].triangle[0].vec, mesh_cube.halfside[1].triangle[1].vec, mesh_cube.halfside[1].triangle[2].vec = \
    [0, 0, 0, 1], [1, 1, 0, 1], [1, 0, 0, 1]    # south 2
mesh_cube.halfside[2].triangle[0].vec, mesh_cube.halfside[2].triangle[1].vec, mesh_cube.halfside[2].triangle[2].vec = \
    [1, 0, 0, 1], [1, 1, 0, 1], [1, 1, 1, 1]    # east 1
mesh_cube.halfside[3].triangle[0].vec, mesh_cube.halfside[3].triangle[1].vec, mesh_cube.halfside[3].triangle[2].vec = \
    [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1]   # east 2
mesh_cube.halfside[4].triangle[0].vec, mesh_cube.halfside[4].triangle[1].vec, mesh_cube.halfside[4].triangle[2].vec = \
    [1, 0, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]   # north 1
mesh_cube.halfside[5].triangle[0].vec, mesh_cube.halfside[5].triangle[1].vec, mesh_cube.halfside[5].triangle[2].vec = \
    [1, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1]   # north 2
mesh_cube.halfside[6].triangle[0].vec, mesh_cube.halfside[6].triangle[1].vec, mesh_cube.halfside[6].triangle[2].vec = \
    [0, 0, 1, 1], [0, 1, 1, 1], [0, 1, 0, 1]   # west 1
mesh_cube.halfside[7].triangle[0].vec, mesh_cube.halfside[7].triangle[1].vec, mesh_cube.halfside[7].triangle[2].vec = \
    [0, 0, 1, 1], [0, 1, 0, 1], [0, 0, 0, 1]    # west 2
mesh_cube.halfside[8].triangle[0].vec, mesh_cube.halfside[8].triangle[1].vec, mesh_cube.halfside[8].triangle[2].vec = \
    [0, 1, 0, 1], [0, 1, 1, 1], [1, 1, 1, 1]      # top 1
mesh_cube.halfside[9].triangle[0].vec, mesh_cube.halfside[9].triangle[1].vec, mesh_cube.halfside[9].triangle[2].vec = \
    [0, 1, 0, 1], [1, 1, 1, 1], [1, 1, 0, 1]    # top 2
mesh_cube.halfside[10].triangle[0].vec, mesh_cube.halfside[10].triangle[1].vec, mesh_cube.halfside[10].triangle[2].vec = \
    [1, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]    # bot 1
mesh_cube.halfside[11].triangle[0].vec, mesh_cube.halfside[11].triangle[1].vec, mesh_cube.halfside[11].triangle[2].vec = \
    [1, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]    # bot 2

pygame.init()

resX = 400
resY = 400

teta = 90

asp = resY/resX
F = 1/math.tan(math.radians(teta/2))     # СЕЙЧАС В РАДИАНАХ, возможно нужны градусы я хз

zFar = 1000
zNear = 0.1
q = zFar/(zFar-zNear)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 25

proj_matrix = np.array([[asp*F, 0, 0, 0], [0, F, 0, 0], [0, 0, q, 1], [0, 0, q*zNear, 0]])

cube_projected = Mesh()
trans_cube = Mesh()
cube_rotX = Mesh()
cube_rotZ = Mesh()


screen = pygame.display.set_mode((resX, resY), 0, 32)  # отрисовка окна
pygame.display.set_caption('3d cube')
fpsClock = pygame.time.Clock()
screen.fill(WHITE)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    fTeta = 1*time.clock()

    rotX = np.array([[1, 0, 0, 0], [0, math.cos(fTeta), math.sin(fTeta), 0], [0, -math.sin(fTeta), math.cos(fTeta), 0],
                     [0, 0, 0, 1]])

    rotZ = np.array([[math.cos(fTeta), math.sin(fTeta), 0, 0], [-math.sin(fTeta), math.cos(fTeta), 0, 0], [0, 0, 1, 0],
                     [0, 0, 0, 1]])

    for i in range(len(trans_cube.halfside)):  # вращение
        for n in range(3):
            cube_rotX.halfside[i].triangle[n].vec = mesh_cube.halfside[i].triangle[n].vec @ rotZ

    for i in range(len(trans_cube.halfside)):  # вращение
        for n in range(3):
            cube_rotZ.halfside[i].triangle[n].vec = cube_rotX.halfside[i].triangle[n].vec @ rotX

    trans_cube = cube_rotZ

    for i in range(len(trans_cube.halfside)):  # смещение по z
        for n in range(3):
            trans_cube.halfside[i].triangle[n].vec[2] += 3

    for i in range(len(trans_cube.halfside)):  # проецируем
        for n in range(3):
            cube_projected.halfside[i].triangle[n].vec = trans_cube.halfside[i].triangle[n].vec @ proj_matrix
            if cube_projected.halfside[i].triangle[n].vec[3] != 0:
                cube_projected.halfside[i].triangle[n].vec[0] /= cube_projected.halfside[i].triangle[n].vec[3]
                cube_projected.halfside[i].triangle[n].vec[1] /= cube_projected.halfside[i].triangle[n].vec[3]

            cube_projected.halfside[i].triangle[n].vec[0] += 1  # scale into view
            cube_projected.halfside[i].triangle[n].vec[1] += 1

            cube_projected.halfside[i].triangle[n].vec[0] *= 0.5 * resX
            cube_projected.halfside[i].triangle[n].vec[1] *= 0.5 * resY

    for i in range(len(mesh_cube.halfside)):
        pygame.draw.aalines(screen, BLACK, True, [cube_projected.halfside[i].triangle[0].vec[:2],
                                                 cube_projected.halfside[i].triangle[1].vec[:2],
                                                 cube_projected.halfside[i].triangle[2].vec[:2]], 3)

    pygame.display.update()
    fpsClock.tick(FPS)