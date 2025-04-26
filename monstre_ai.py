# ======= monstre_ai.py =======

from algos import a_star_path

class MonstreAI:
    def __init__(self, start_pos):
        self.position = start_pos

    def trouver_chemin(self, joueur_pos, maze_map, murs_dynamiques):
        """Trouve le chemin optimal vers le joueur."""
        path = a_star_path(self.position, joueur_pos, maze_map, murs_dynamiques)
        return path

    def bouger(self, joueur_pos, maze_map, murs_dynamiques):
        """Met à jour la position du monstre vers le joueur."""
        path = self.trouver_chemin(joueur_pos, maze_map, murs_dynamiques)
        if path and len(path) > 1:
            self.position = path[1]
