import sys
import pygame
import time
import os

# Initialize pygame
pygame.init()


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_BLUE= (0,0,139)
GREEN = (0, 255, 0)
ORANGE = (255, 128, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)
BACKGROUND_COLOR = (240, 240, 255)
WALL_COLOR = (60, 60, 90)
PLAYER_COLOR = (255, 99, 130)
EXIT_COLOR = (120, 200, 120)
BUTTON_COLOR = (200, 200, 230)
HOVER_COLOR = (170, 170, 210)
TEXT_COLOR = (30, 30, 30)
YELLOW =(139, 128,0)

# Fonts
font_very_large = pygame.font.Font(None, 72)
font_large = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Window size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The maze")

# Load sound effects/chemin a verifier
son_click = pygame.mixer.Sound("interface-graphique/assets/songs/678248__pixeliota__mouse-click-sound.mp3")
son_menu = pygame.mixer.Sound("interface-graphique/assets/songs/menu.wav")

# Load and scale background
try:
    background = pygame.image.load("interface-graphique/assets/images/maze.jpg")
    background = pygame.transform.scale(background, (800, 600))
except:
    background = pygame.Surface((800, 600))
    background.fill(LIGHT_BLUE)

def show_main_menu():
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))
    
    # Titre principal avec ombre
    title = font_very_large.render("The Maze", True, (0, 0, 0))  # Ombre
    title_shadow = font_very_large.render("The Maze", True, RED)  # Texte principal
    title_x = WIDTH // 2 - title.get_width() // 2
    title_y = HEIGHT // 4 - 30
    
    screen.blit(title, (title_x + 3, title_y + 3))  # Ombre décalée
    screen.blit(title_shadow, (title_x, title_y))   # Texte principal
    
    # Ligne décorative sous le titre
    pygame.draw.line(screen, GOLD, 
                   (WIDTH//2 - title.get_width()//2, title_y + title.get_height() + 5),
                   (WIDTH//2 + title.get_width()//2, title_y + title.get_height() + 5), 3)
    
    # Boutons des niveaux avec effets améliorés
    niveaux = ["Simple", "Moyen", "Avancé"]
    buttons = []
    
    for i, niveau in enumerate(niveaux):
        rect = pygame.Rect(WIDTH//2 - 125, HEIGHT//2 - 50 + i*90, 250, 60)
        buttons.append((rect, niveau))
        
        # Couleur différente pour chaque niveau
        if niveau == "Simple":
            color, hover_color = GREEN, DARK_GREEN
        elif niveau == "Moyen":
            color, hover_color = BLUE, DARK_BLUE
        else:
            color, hover_color = ORANGE, DARK_RED
        
        # Dessin du bouton avec ombre et effet de survol
        btn_color = hover_color if rect.collidepoint(pygame.mouse.get_pos()) else color
        
        # Ombre du bouton
        shadow_rect = rect.copy()
        shadow_rect.y += 5
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=10)
        
        # Bouton principal
        pygame.draw.rect(screen, btn_color, rect, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, rect, 2, border_radius=10)
        
        # Texte avec ombre légère
        text = font_large.render(niveau, True, (0, 0, 0))
        screen.blit(text, (rect.centerx - text.get_width()//2 + 2, rect.centery - text.get_height()//2 + 2))
        
        text = font_large.render(niveau, True, WHITE)
        screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))
        
        # Indicateurs de difficulté (points)
        for j in range(i+1):
            pygame.draw.circle(screen, GOLD, (rect.x + 30 + j*20, rect.centery), 5)

    # Bouton Quitter amélioré
    quit_rect = pygame.Rect(WIDTH//2 - 125, HEIGHT//2+ 215, 250, 70)
    quit_color = HOVER_COLOR if quit_rect.collidepoint(pygame.mouse.get_pos()) else DARK_RED
    
    # Ombre du bouton quitter
    shadow_rect = quit_rect.copy()
    shadow_rect.y += 5
    pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=10)
    
    # Bouton quitter principal
    pygame.draw.rect(screen, quit_color, quit_rect, border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, quit_rect, 2, border_radius=10)
    
    # Texte avec ombre
    quit_text = font_large.render("Quitter", True, (0, 0, 0))
    screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width()//2 + 2, 
                          quit_rect.centery - quit_text.get_height()//2 + 2))
    
    quit_text = font_large.render("Quitter", True, WHITE)
    screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width()//2, 
                          quit_rect.centery - quit_text.get_height()//2))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, niveau in buttons:
                    if rect.collidepoint(event.pos):
                        son_click.play()
                        return {"Simple": (10, 10,200), 
                                "Moyen": (15, 12,300), 
                                "Avancé": (20, 15,100)}[niveau]
                
                if quit_rect.collidepoint(event.pos):
                    son_click.play()
                    pygame.time.delay(300)
                    pygame.quit()
                    exit()


def show_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # menu principal 
    menu_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 150, 300, 350)  
    pygame.draw.rect(screen, GRAY, menu_rect, border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, menu_rect, 2, border_radius=10)
    
    # titre menu
    title = font_large.render("Menu Pause", True, WHITE)
    screen.blit(title, (menu_rect.x + menu_rect.width//2 - title.get_width()//2, 
                        menu_rect.y + 20))

    # bouton Reprendre
    resume_rect = pygame.Rect(menu_rect.x + 50, menu_rect.y + 70, 200, 40)
    pygame.draw.rect(screen, GREEN, resume_rect, border_radius=5)
    pygame.draw.rect(screen, DARK_GRAY, resume_rect, 2, border_radius=5)
    resume_text = font_small.render("Reprendre", True, BLACK)
    screen.blit(resume_text, (resume_rect.x + resume_rect.width//2 - resume_text.get_width()//2, 
                             resume_rect.y + 10))

    # bouton Recommencer 
    restart_rect = pygame.Rect(menu_rect.x + 50, menu_rect.y + 130, 200, 40)
    pygame.draw.rect(screen, (255, 204, 0), restart_rect, border_radius=5)
    pygame.draw.rect(screen, DARK_GRAY, restart_rect, 2, border_radius=5)
    restart_text = font_small.render("Recommencer", True, BLACK)
    screen.blit(restart_text, (restart_rect.x + restart_rect.width//2 - restart_text.get_width()//2, 
                              restart_rect.y + 10))

    # bouton Retour à l'accueil
    home_rect = pygame.Rect(menu_rect.x + 50, menu_rect.y + 190, 200, 40) 
    pygame.draw.rect(screen, BLUE, home_rect, border_radius=5)
    pygame.draw.rect(screen, DARK_GRAY, home_rect, 2, border_radius=5)
    home_text = font_small.render("Retour à l'accueil", True, BLACK)
    screen.blit(home_text, (home_rect.x + home_rect.width//2 - home_text.get_width()//2, 
                           home_rect.y + 10))
    
    # bouton Quitter
    quit_rect = pygame.Rect(menu_rect.x + 50, menu_rect.y + 250, 200, 40)
    pygame.draw.rect(screen, RED, quit_rect, border_radius=5)
    pygame.draw.rect(screen, DARK_GRAY, quit_rect, 2, border_radius=5)
    quit_text = font_small.render("Quitter le jeu", True, BLACK)
    screen.blit(quit_text, (quit_rect.x + quit_rect.width//2 - quit_text.get_width()//2, 
                           quit_rect.y + 10))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    son_click.play()
                    return "resume"
                elif restart_rect.collidepoint(event.pos):
                    son_click.play()
                    return "restart"
                elif home_rect.collidepoint(event.pos):
                    son_click.play()
                    return "menu"
                elif quit_rect.collidepoint(event.pos):
                    son_click.play()
                    pygame.quit()
                    sys.exit()


def menu_choix_joueur():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # menu principal 
    menu_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 150, 300, 350)  
    pygame.draw.rect(screen, GRAY, menu_rect, border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, menu_rect, 2, border_radius=10)
    
    # titre menu
    title = font_large.render("choisir un joueur", True, WHITE)
    screen.blit(title, (menu_rect.x + menu_rect.width//2 - title.get_width()//2, 
                        menu_rect.y + 20))

    # bouton homme
    homme_rect = pygame.Rect(menu_rect.x + 50, menu_rect.y + 70, 200, 40)
    pygame.draw.rect(screen, GREEN, homme_rect, border_radius=5)
    pygame.draw.rect(screen, DARK_GRAY, homme_rect, 2, border_radius=5)
    homme_text = font_small.render("homme", True, BLACK)
    screen.blit(homme_text, (homme_rect.x + homme_rect.width//2 - homme_text.get_width()//2, 
                             homme_rect.y + 10))

    # bouton femme
    femme_rect = pygame.Rect(menu_rect.x + 50, menu_rect.y + 130, 200, 40)
    pygame.draw.rect(screen, (255, 204, 0), femme_rect, border_radius=5)
    pygame.draw.rect(screen, DARK_GRAY, femme_rect, 2, border_radius=5)
    femme_text = font_small.render("femme", True, BLACK)
    screen.blit(femme_text, (femme_rect.x + femme_rect.width//2 - femme_text.get_width()//2, 
                              femme_rect.y + 10))
    pygame.display.flip()
     
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if homme_rect.collidepoint(event.pos):
                    son_click.play()
                    return "homme"
                elif femme_rect.collidepoint(event.pos):
                    son_click.play()
                    return "femme"
#def main():
   # while True:
        # show_main menus return 3 argument 
        #rows, cols ,loop= show_main_menu()
        

#if __name__ == "__main__":
   # main()

