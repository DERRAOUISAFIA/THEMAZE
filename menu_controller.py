# menu_controller.py
import sys
from game_controller import GameController

class MenuController:
    def __init__(self):
        self.menu_options = {
            1: self.jouer,
            2: self.quitter
        }

    def afficher_menu(self):
        print("=== Menu ===")
        print("1. Jouer")
        print("2. Quitter")
        choix = int(input("Choisissez une option: "))
        self.menu_options.get(choix, self.option_invalide)()

    def jouer(self):
        print("Lancement du jeu...")
        game_controller = GameController()  # Création de l'objet GameController
        game_controller.demarrer_jeu()  # Lancer le jeu

    def quitter(self):
        print("Merci d'avoir joué ! À bientôt.")
        sys.exit(0)

    def option_invalide(self):
        print("Option invalide, veuillez réessayer.")
        self.afficher_menu()
