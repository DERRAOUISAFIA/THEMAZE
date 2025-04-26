import random
import time
from random import sample
from pyamaze import maze, agent, COLOR
from algos import bfs
from monstre_ai import MonstreAI

class Maze3d:
    def __init__(self, rows, cols, loopPercent, delay=0.05):  # Plus rapide !
        self.m = maze(rows, cols)
        self.m.CreateMaze(loopPercent=loopPercent)
        self.rows = rows
        self.cols = cols
        self.maze_map = self.m.maze_map
        self.joueur_pos = (1, 1)
        self.monstre_ai = MonstreAI((self.rows, self.cols))
        self.delay = delay

        self.murs_dynamiques = set()
        self.pieges_dynamiques = set()
        self.pieges_agents = []  # On va stocker les agents "pièges"
    
    def update_maze(self):
        """Met à jour dynamiquement murs et pièges."""
        if random.random() < 0.1:
            x, y = sample(list(self.maze_map.keys()), 1)[0]
            self.murs_dynamiques.add((x, y))
            print(f"Mur dynamique ajouté à {(x, y)}")

        if random.random() < 0.1:
            x, y = sample(list(self.maze_map.keys()), 1)[0]
            self.pieges_dynamiques.add((x, y))
            print(f"Piège ajouté à {(x, y)}")
            piege = agent(self.m, x, y, color=COLOR.yellow, shape='square')  # Piège visible
            self.pieges_agents.append(piege)

    def play_game(self):
        """Lance le jeu."""
        path_list = bfs(self.maze_map, (self.rows, self.cols), (1, 1), self.murs_dynamiques)

        if not path_list:
            print("Aucun chemin trouvé entre le joueur et la sortie.")
            return

        print("Path trouvé:", path_list)

        joueur = agent(self.m, color=COLOR.red, shape='circle')
        monstre = agent(self.m, color=COLOR.green, shape='square')

        self.m.tracePath({joueur: [self.joueur_pos]}, delay=100)

        for next_pos in path_list[1:]:
            # Déplacer le joueur doucement
            self.m.tracePath({joueur: [self.joueur_pos, next_pos]}, delay=20)
            self.joueur_pos = next_pos

            # Mise à jour dynamique du labyrinthe
            self.update_maze()

            # Déplacer le monstre doucement
            ancienne_pos_monstre = self.monstre_ai.position
            self.monstre_ai.bouger(self.joueur_pos, self.maze_map, self.murs_dynamiques)
            self.m.tracePath({monstre: [ancienne_pos_monstre, self.monstre_ai.position]}, delay=20)

            # Vérifier si le monstre a attrapé le joueur
            if self.monstre_ai.position == self.joueur_pos:
                print("💀 Le monstre a attrapé le joueur !")
                break

            time.sleep(self.delay)  # petit temps entre chaque étape pour plus de fluidité
    
        self.m.run()
