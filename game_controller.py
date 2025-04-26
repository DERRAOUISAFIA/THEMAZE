# game_controller.py
import time
from maze_3d import Maze3d
from algos import bfs
from monstre_ai import MonstreAI

class GameController:
    def __init__(self):
        # Initialiser les paramètres du jeu
        self.rows, self.cols, self.loopPercent = self.choisir_niveau()
        self.game = Maze3d(self.rows, self.cols, self.loopPercent)

    def choisir_niveau(self):
        """Demande au joueur de choisir un niveau de difficulté."""
        print("Choisissez le niveau de difficulté :")
        print("1. Facile")
        print("2. Moyen")
        print("3. Difficile")
        choix = int(input("Entrez le numéro du niveau choisi: "))
        
        if choix == 1:
            return 5, 5, 10  # Facile
        elif choix == 2:
            return 10, 10, 20  # Moyen
        elif choix == 3:
            return 15, 15, 30  # Difficile
        else:
            print("Choix invalide, niveau facile par défaut.")
            return 5, 5, 10  # Valeur par défaut

    def demarrer_jeu(self):
        """Démarre la logique du jeu."""
        self.game.play_game()

    def mettre_a_jour_jeu(self):
        """Met à jour l'état du jeu à chaque itération."""
        joueur_pos = self.game.joueur_pos
        monstre = self.game.monstre_ai
        
        # Vérifie si le joueur est proche de la sortie
        if self.verifier_sortie(joueur_pos):
            print("Félicitations ! Vous avez atteint la sortie.")
            return True

        # Déplace le joueur et le monstre
        self.game.update_maze()
        path_list = bfs(self.game.maze_map, joueur_pos, self.game.joueur_pos, self.game.murs_dynamiques)
        if path_list:
            self.game.play_game()  # Reprend le jeu
        else:
            print("Aucun chemin trouvé, le joueur reste bloqué.")
            return False

        # Déplace le monstre
        if self.game.monstre_ai.position == self.game.joueur_pos:
            print("Le monstre a attrapé le joueur !")
            return False

        time.sleep(self.game.delay)
        return False

    def verifier_sortie(self, joueur_pos):
        """Vérifie si le joueur a atteint la sortie."""
        # Logique de vérification de la sortie (par exemple, les coordonnées de la sortie)
        return joueur_pos == (self.game.rows - 1, self.game.cols - 1)  # Sortie supposée être en bas à droite
