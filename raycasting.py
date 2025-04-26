import pygame
import math

class Raycaster:
    def __init__(self, maze, player_pos=(1.5, 1.5), player_angle=0):
        pygame.init()
        self.maze = maze
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        # Configuration joueur
        self.player_x, self.player_y = player_pos
        self.player_angle = player_angle
        self.move_speed = 0.05
        self.rot_speed = 0.05
        
        # Couleurs
        self.wall_color = (200, 100, 50)
        self.floor_color = (34, 139, 34)
        self.sky_color = (135, 206, 235)
        
        # Personnage
        self.player_img = self._load_player_image()

         # Ajoutez ces paramètres pour la minimap
        self.minimap_size = 120
        self.minimap_margin = 10
        self.minimap_cell_size = self.minimap_size // max(len(maze), len(maze[0]))
        self.minimap_bg_color = (0, 0, 0, 180)  # Noir semi-transparent
        self.minimap_wall_color = (245,255,250,0.9) 
        self.minimap_player_color = (255, 0, 0)  # Rouge
        self.minimap_direction_color = (250, 250, 250)  


    def draw_minimap(self):
        """Dessine la minimap en superposition"""
        # Création d'une surface semi-transparente
        minimap_surface = pygame.Surface((self.minimap_size, self.minimap_size), pygame.SRCALPHA)
        minimap_surface.fill(self.minimap_bg_color)
    
        # Dessin des murs
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x] == 1:
                    pygame.draw.rect(
                        minimap_surface, 
                        self.minimap_wall_color,
                        (x * self.minimap_cell_size, 
                        y * self.minimap_cell_size,
                        self.minimap_cell_size, 
                        self.minimap_cell_size)
                    )
    
        # Dessin du joueur
        pygame.draw.circle(
            minimap_surface,
            self.minimap_player_color,
            (int(self.player_x * self.minimap_cell_size),
            int(self.player_y * self.minimap_cell_size)),
            5
        )
    
        # Dessin de la direction
        end_x = self.player_x * self.minimap_cell_size + math.cos(self.player_angle) * 15
        end_y = self.player_y * self.minimap_cell_size + math.sin(self.player_angle) * 15
        pygame.draw.line(
            minimap_surface,
            self.minimap_direction_color,
            (int(self.player_x * self.minimap_cell_size),
            int(self.player_y * self.minimap_cell_size)),
            (int(end_x), int(end_y)),
            2
        )
    
        # Affichage de la minimap
        self.screen.blit(minimap_surface, (self.minimap_margin, self.minimap_margin))


    def _load_player_image(self):
        try:
            img = pygame.image.load("assets/images/player_back.png").convert_alpha()
            return pygame.transform.scale(img, (100, 150))
        except:
            print("Image joueur non trouvée, utilisation d'un placeholder")
            return None

    def cast_ray(self, angle):
        """Lance un rayon et retourne la distance au mur"""
        ray_x, ray_y = self.player_x, self.player_y
        ray_dir_x, ray_dir_y = math.cos(angle), math.sin(angle)
        
        distance = 0
        while distance < 20:
            distance += 0.01
            test_x = int(ray_x + ray_dir_x * distance)
            test_y = int(ray_y + ray_dir_y * distance)
            
            if 0 <= test_x < len(self.maze[0]) and 0 <= test_y < len(self.maze):
                if self.maze[test_y][test_x] == 1:
                    return distance
            else:
                break
        return 20

    def render(self):
        """Affiche la vue 3D et le personnage"""
        # Fond
        self.screen.fill(self.sky_color)
        pygame.draw.rect(self.screen, self.floor_color, 
                        (0, self.height//2, self.width, self.height//2))
        
        # Raycasting
        for ray in range(self.width):
            ray_angle = (self.player_angle - math.pi/6) + (ray/self.width) * (math.pi/3)
            distance = self.cast_ray(ray_angle)
            
            # Calcul hauteur mur
            wall_height = min(int(self.height / distance), self.height)
            wall_top = (self.height - wall_height) // 2
            
            # Dessin mur
            shade = max(0.2, 1 - distance/15)
            color = tuple(int(c * shade) for c in self.wall_color)
            pygame.draw.line(self.screen, color, (ray, wall_top), (ray, wall_top + wall_height), 2)
        
        # Personnage (vue de dos)
        if self.player_img:
            rect = self.player_img.get_rect(center=(self.width//2, self.height//1.5))
            self.screen.blit(self.player_img, rect)
        else:
            pygame.draw.circle(self.screen, (255, 0, 0), (self.width//2, self.height//1.5), 20)
        self.draw_minimap()

    def update(self, move_forward=False, move_backward=False, turn_left=False, turn_right=False):
        """Met à jour la position du joueur"""
        # Rotation
        if turn_left:
            self.player_angle -= self.rot_speed
        if turn_right:
            self.player_angle += self.rot_speed
        
        # Déplacement
        if move_forward or move_backward:
            move_speed = self.move_speed * (1 if move_forward else -1)
            new_x = self.player_x + math.cos(self.player_angle) * move_speed
            new_y = self.player_y + math.sin(self.player_angle) * move_speed
            
            # Collisions
            if 0 <= int(new_x) < len(self.maze[0]) and 0 <= int(new_y) < len(self.maze):
                if self.maze[int(new_y)][int(new_x)] == 0:
                    self.player_x, self.player_y = new_x, new_y
    def update(self, move_forward=False, move_backward=False, turn_left=False, turn_right=False):
        """Met à jour la position du joueur et vérifie s'il a gagné"""
        # Rotation
        if turn_left:
            self.player_angle -= self.rot_speed
        if turn_right:
            self.player_angle += self.rot_speed
    
        # Déplacement
        if move_forward or move_backward:
            move_speed = self.move_speed * (1 if move_forward else -1)
            new_x = self.player_x + math.cos(self.player_angle) * move_speed
            new_y = self.player_y + math.sin(self.player_angle) * move_speed
        
            # Vérifie si le joueur sort du labyrinthe (condition de victoire)
            if self.is_exit(new_x, new_y):
                return "WIN"
            
            # Collisions normales
            if 0 <= int(new_x) < len(self.maze[0]) and 0 <= int(new_y) < len(self.maze):
                if self.maze[int(new_y)][int(new_x)] == 0:
                    self.player_x, self.player_y = new_x, new_y
    
        return "PLAYING"

    def is_exit(self, x, y):
        """Détecte si le joueur a atteint la sortie"""
        # Coordonnées de la sortie (dernière case vide en bas à droite dans votre maze)
        exit_x = len(self.maze[0]) - 1
        exit_y = len(self.maze) - 1
    
        # Vérifie si le joueur est sur la case de sortie
        return int(x) >= exit_x and int(y) >= exit_y                
