
import math
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from pyamaze import maze

class MazeGame(ShowBase):
    def __init__(self, maze):
        ShowBase.__init__(self)
        
        # Charger le modèle de mur
        self.wall_model = self.loader.loadModel("models/box")
        self.wall_model.setTexture(self.loader.loadTexture("assets/images/green_wall.png"))

        # Charger le modèle du personnage
        self.player_model = self.loader.loadModel("models/smiley")
        self.player_model.setTexture(self.loader.loadTexture("assets/images/sprite_baboonMonkJump.png"))
        self.player_model.setScale(0.5)
        self.player_node = self.render.attachNewNode("player")
        self.player_model.reparentTo(self.player_node)
        
        # Construire le labyrinthe
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 1:  # Mur
                    wall = self.wall_model.copyTo(self.render)
                    wall.setPos(x, y, 0)
                    wall.setScale(1)
        
        # Créer un pivot pour la caméra
        self.camera_pivot = self.render.attachNewNode("camera_pivot")
        self.camera.reparentTo(self.camera_pivot)
        self.camera.setPos(0, -self.camera_distance, self.camera_height)
        self.camera.lookAt(self.camera_pivot)
        
        # Mise à jour initiale
        self.update_player()
    
    def update_player(self):
        """Met à jour la position du joueur et de la caméra"""
        self.player_node.setPos(self.player_pos[0], self.player_pos[1], 0)
        self.camera_pivot.setPos(self.player_pos[0], self.player_pos[1], 0)
    
    def rotate(self, angle):
        """Rotation du joueur et de la caméra"""
        self.player_node.setH(self.player_node.getH() + angle)
        self.camera_pivot.setH(self.camera_pivot.getH() + angle)
    
    def move(self, distance):
        """Déplacement du joueur"""
        angle = math.radians(self.player_node.getH())
        dx = math.sin(angle) * distance
        dy = math.cos(angle) * distance
        
        # Vérification des collisions
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Simplification: on suppose que maze est accessible
        if 0 <= int(new_x) < len(maze[0]) and 0 <= int(new_y) < len(maze):
            if maze[int(new_y)][int(new_x)] == 0:
                self.player_pos = [new_x, new_y]
                self.update_player()
game = MazeGame(maze)
game.run()
