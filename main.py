from maze_3d import Maze3d

# Fonction pour choisir le niveau
def choisir_niveau():
    print("Choisissez le niveau de difficulté :")
    print("1. Facile")
    print("2. Moyen")
    print("3. Difficile")

    choix = int(input("Entrez le numéro du niveau choisi: "))

    if choix == 1:
        rows, cols, loopPercent = 5, 5, 10  # Facile : petite taille de labyrinthe, peu de boucles
    elif choix == 2:
        rows, cols, loopPercent = 10, 10, 20  # Moyen : taille moyenne, plus de boucles
    elif choix == 3:
        rows, cols, loopPercent = 15, 15, 30  # Difficile : grande taille de labyrinthe, beaucoup de boucles
    else:
        print("Choix invalide, niveau facile par défaut.")
        rows, cols, loopPercent = 5, 5, 10  # Valeur par défaut en cas de mauvaise entrée

    return rows, cols, loopPercent

# Demander au joueur de choisir
rows, cols, loopPercent = choisir_niveau()

# Créer le jeu avec les paramètres choisis
game = Maze3d(rows, cols, loopPercent)

# Jouer !
game.play_game()
