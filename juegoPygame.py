import pygame
import sys

# Dimensiones de la ventana y tamaño de cada celda del laberinto
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 40

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Matriz que representa el laberinto
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 4, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# Posición del jugador
player_pos = (1, 1)


def draw_maze(screen):
    screen.fill(BLACK)

    for y in range(len(laberinto)):
        for x in range(len(laberinto[y])):
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if laberinto[y][x] == 1:
                pygame.draw.rect(screen, WHITE, cell_rect)
            elif laberinto[y][x] == 2:
                pygame.draw.rect(screen, RED, cell_rect)
            elif laberinto[y][x] == 4:
                pygame.draw.rect(screen, WHITE, cell_rect)
                pygame.draw.circle(screen, RED, (cell_rect.centerx, cell_rect.centery), CELL_SIZE // 2)

    pygame.display.flip()


def move_player(dx, dy):
    global player_pos

    x, y = player_pos
    new_x = x + dx
    new_y = y + dy

    # Verificar si el movimiento es válido dentro de los límites del laberinto
    if 0 <= new_x < len(laberinto[0]) and 0 <= new_y < len(laberinto):
        # Verificar si la posición a la que se desea mover no es una pared
        if laberinto[new_y][new_x] != 1:
            player_pos = (new_x, new_y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Laberinto')
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_player(1, 0)

        draw_maze(screen)
        clock.tick(60)


if __name__ == '__main__':
    main()
