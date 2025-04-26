import pygame
from raycasting import Raycaster

# Configuration du labyrinthe
MAZE = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0]
]

def main():
    # Initialisation
    raycaster = Raycaster(MAZE)
    clock = pygame.time.Clock()
    running = True
    
    # États de contrôle
    controls = {
        'forward': False,
        'backward': False,
        'left': False,
        'right': False
    }
    
    # Message de victoire
    font = pygame.font.Font(None, 74)
    win_text = font.render('VOUS AVEZ GAGNE!', True, (0, 255, 0))
    text_rect = win_text.get_rect(center=(raycaster.width//2, raycaster.height//2))
    
    game_state = "PLAYING"  # "PLAYING" ou "WIN"

    # Boucle principale
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pressions des touches
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    controls['forward'] = True
                elif event.key == pygame.K_DOWN:
                    controls['backward'] = True
                elif event.key == pygame.K_LEFT:
                    controls['left'] = True
                elif event.key == pygame.K_RIGHT:
                    controls['right'] = True
            
            # Relâchement des touches
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    controls['forward'] = False
                elif event.key == pygame.K_DOWN:
                    controls['backward'] = False
                elif event.key == pygame.K_LEFT:
                    controls['left'] = False
                elif event.key == pygame.K_RIGHT:
                    controls['right'] = False
        
        # Mise à jour du raycaster
        if game_state == "PLAYING":
            # Mise à jour du jeu
            game_state = raycaster.update(
                move_forward=controls['forward'],
                move_backward=controls['backward'],
                turn_left=controls['left'],
                turn_right=controls['right']
            )
        
        # Rendu
        raycaster.render()
        # Afficher message de victoire
        if game_state == "WIN":
            # Fond semi-transparent
            s = pygame.Surface((raycaster.width, raycaster.height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            raycaster.screen.blit(s, (0, 0))
            # Message
            raycaster.screen.blit(win_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)  # Affiche pendant 3 secondes
            running = False  # Quitte le jeu
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()