import pygame
import math
import sys

# Configuration du labyrinthe (1 = mur, 0 = chemin)
maze = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

class RaycastingDemo:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        
        # Position et orientation du joueur
        self.player_x, self.player_y = 1.5, 1.5
        self.player_angle = 0
        self.move_speed = 0.05
        self.rot_speed = 0.05
        
        # Textures simplifiées
        self.wall_color = (200, 100, 50)
        self.floor_color = (50, 50, 50)
        self.sky_color = (100, 100, 255)
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_angle -= self.rot_speed
        if keys[pygame.K_RIGHT]:
            self.player_angle += self.rot_speed
        if keys[pygame.K_UP]:
            move_x = math.cos(self.player_angle) * self.move_speed
            move_y = math.sin(self.player_angle) * self.move_speed
            if maze[int(self.player_y)][int(self.player_x + move_x * 2)] == 0:
                self.player_x += move_x
            if maze[int(self.player_y + move_y * 2)][int(self.player_x)] == 0:
                self.player_y += move_y
        if keys[pygame.K_DOWN]:
            move_x = math.cos(self.player_angle) * self.move_speed
            move_y = math.sin(self.player_angle) * self.move_speed
            if maze[int(self.player_y)][int(self.player_x - move_x * 2)] == 0:
                self.player_x -= move_x
            if maze[int(self.player_y - move_y * 2)][int(self.player_x)] == 0:
                self.player_y -= move_y
    
    def cast_ray(self, angle):
        ray_x, ray_y = self.player_x, self.player_y
        ray_dir_x, ray_dir_y = math.cos(angle), math.sin(angle)
        
        distance = 0
        while distance < 20:
            distance += 0.01
            test_x = int(ray_x + ray_dir_x * distance)
            test_y = int(ray_y + ray_dir_y * distance)
            
            if 0 <= test_x < len(maze[0]) and 0 <= test_y < len(maze):
                if maze[test_y][test_x] == 1:
                    return distance, (test_x, test_y)
            else:
                break
        return 20, None
    
    def render(self):
        self.screen.fill(self.sky_color)
        pygame.draw.rect(self.screen, self.floor_color, 
                        (0, self.height//2, self.width, self.height//2))
        
        for ray in range(self.width):
            ray_angle = (self.player_angle - math.pi/6) + (ray/self.width) * (math.pi/3)
            distance, _ = self.cast_ray(ray_angle)
            
            # Correction de la distorsion
            distance *= math.cos(self.player_angle - ray_angle)
            
            wall_height = min(int(self.height / (distance + 0.0001)), self.height)
            wall_top = (self.height - wall_height) // 2
            
            # Ombre en fonction de la distance
            shade = max(0.2, 1 - distance/15)
            color = tuple(int(c * shade) for c in self.wall_color)
            
            pygame.draw.line(self.screen, color, 
                            (ray, wall_top), (ray, wall_top + wall_height), 2)
        
        # Mini-map
        map_size = 100
        cell_size = map_size // len(maze)
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                   (x * cell_size, y * cell_size, cell_size, cell_size))
        pygame.draw.circle(self.screen, (255, 0, 0),
                          (int(self.player_x * cell_size), int(self.player_y * cell_size)), 3)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.handle_input()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    demo = RaycastingDemo()
    demo.run()