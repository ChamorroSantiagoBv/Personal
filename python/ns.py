import pygame
import sys
import time

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Game")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Tiempo de cooldown en segundos
COOLDOWN_TIME = 0.5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Mover jugador y comprobar colisiones
        self.rect.x += dx
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= dx
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y -= dy

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def create_level_1():
    walls = pygame.sprite.Group()
    wall_thickness = 20

    walls.add(Wall(0, 0, SCREEN_WIDTH, wall_thickness))  # Pared superior
    walls.add(Wall(0, 0, wall_thickness, SCREEN_HEIGHT))  # Pared izquierda
    walls.add(Wall(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness))  # Pared inferior

    # Pared derecha con apertura
    walls.add(Wall(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT // 3))  # Pared derecha arriba
    walls.add(Wall(SCREEN_WIDTH - wall_thickness, SCREEN_HEIGHT * 2 // 3, wall_thickness, SCREEN_HEIGHT // 3))  # Pared derecha abajo

    walls.add(Wall(200, 100, wall_thickness, 400))  # Pared vertical
    walls.add(Wall(400, 200, 300, wall_thickness))  # Pared horizontal

    return walls

def create_level_2():
    walls = pygame.sprite.Group()
    wall_thickness = 20

    walls.add(Wall(0, 0, SCREEN_WIDTH // 3, wall_thickness))  # Pared superior izquierda
    walls.add(Wall(SCREEN_WIDTH * 2 // 3, 0, SCREEN_WIDTH // 3, wall_thickness))  # Pared superior derecha
    walls.add(Wall(0, wall_thickness, wall_thickness, SCREEN_HEIGHT // 3))  # Pared izquierda arriba
    walls.add(Wall(0, SCREEN_HEIGHT * 2 // 3, wall_thickness, SCREEN_HEIGHT // 3))  # Pared izquierda abajo
    walls.add(Wall(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness))  # Pared inferior
    walls.add(Wall(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT))  # Pared derecha

    walls.add(Wall(150, 150, 500, wall_thickness))  # Pared horizontal
    walls.add(Wall(150, 150, wall_thickness, 300))  # Pared vertical

    return walls

def create_level_3():
    walls = pygame.sprite.Group()
    wall_thickness = 20

    walls.add(Wall(0, 0, SCREEN_WIDTH, wall_thickness))  # Pared superior
    walls.add(Wall(0, 0, wall_thickness, SCREEN_HEIGHT))  # Pared izquierda
    walls.add(Wall(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH // 3, wall_thickness))  # Pared inferior izquierda
    walls.add(Wall(SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH // 3, wall_thickness))  # Pared inferior derecha
    walls.add(Wall(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT))  # Pared derecha

    walls.add(Wall(300, 100, wall_thickness, 400))  # Pared vertical
    walls.add(Wall(100, 300, 600, wall_thickness))  # Pared horizontal

    return walls

def main():
    player = Player()
    current_level = 1
    walls = create_level_1()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(walls)

    last_level_change_time = time.time()
    wall_thickness = 20  # Definir el grosor de las paredes aquí

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = time.time()

        # Cambiar de nivel cuando el jugador pasa por las aperturas
        if current_level == 1 and player.rect.right >= SCREEN_WIDTH:
            if current_time - last_level_change_time > COOLDOWN_TIME:
                current_level = 2
                walls = create_level_2()
                all_sprites = pygame.sprite.Group()
                all_sprites.add(player)
                all_sprites.add(walls)
                player.rect.left = 0  # Mover el jugador al inicio del nivel 2
                last_level_change_time = current_time

        elif current_level == 2:
            if player.rect.left <= 0:
                if current_time - last_level_change_time > COOLDOWN_TIME:
                    current_level = 1
                    walls = create_level_1()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)
                    all_sprites.add(walls)
                    player.rect.right = SCREEN_WIDTH  # Mover el jugador al final del nivel 1
                    last_level_change_time = current_time
            elif player.rect.top <= 0:
                if current_time - last_level_change_time > COOLDOWN_TIME:
                    current_level = 3
                    walls = create_level_3()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)
                    all_sprites.add(walls)
                    player.rect.bottom = SCREEN_HEIGHT  # Mover el jugador al inicio del nivel 3
                    last_level_change_time = current_time

        elif current_level == 3:
            if player.rect.bottom >= SCREEN_HEIGHT - wall_thickness and SCREEN_WIDTH // 3 < player.rect.x < SCREEN_WIDTH * 2 // 3:
                if current_time - last_level_change_time > COOLDOWN_TIME:
                    current_level = 2
                    walls = create_level_2()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)
                    all_sprites.add(walls)
                    player.rect.top = SCREEN_HEIGHT  # Mover el jugador al final del nivel 2
                    last_level_change_time = current_time

        all_sprites.update(walls)

        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
