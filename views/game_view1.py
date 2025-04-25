import math
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class MazeGame(ShowBase):
    def __init__(self, maze):
        ShowBase.__init__(self)
        
        # Charger le modèle de mur
        self.wall_model = self.loader.loadModel("models/box")
        self.wall_model.setTexture(self.loader.loadTexture("textures/wall.png"))
        
        # Construire le labyrinthe
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 1:  # Mur
                    wall = self.wall_model.copyTo(self.render)
                    wall.setPos(x, y, 0)
                    wall.setScale(1)
        
        # Configurer la caméra
        self.camera.setPos(0.5, 0.5, 2)
        self.camera.lookAt(0.5, 0.5, 0)
        
        # Contrôles
        self.accept("arrow_left", self.rotate, [-10])
        self.accept("arrow_right", self.rotate, [10])
        self.accept("arrow_up", self.move, [1])
        self.accept("arrow_down", self.move, [-1])
    
    def rotate(self, angle):
        self.camera.setH(self.camera.getH() + angle)
    
    def move(self, distance):
        angle = math.radians(self.camera.getH())
        dx = math.sin(angle) * distance
        dy = math.cos(angle) * distance
        self.camera.setPos(
            self.camera.getX() + dx,
            self.camera.getY() + dy,
            self.camera.getZ()
        )

game = MazeGame(maze)
game.run()