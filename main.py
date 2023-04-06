from ScreenRecorder import ScreenRecorder

import pygame

NUM_POINTS_X = 192
NUM_POINTS_Y = 108

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def f(x):
    return (2 * (x**3) - 2) / (3 * (x**2) - 10)


def generate_grid():
    z = list()
    for x in range(NUM_POINTS_X):
        x = (x - NUM_POINTS_X / 2) / (NUM_POINTS_X / 2)
        for y in range(NUM_POINTS_Y):
            y = (y - NUM_POINTS_Y / 2) / (NUM_POINTS_Y / 2)
            z.append(x + y*1j)
    return z


if __name__ == '__main__':
    next_grid = generate_grid()
    last_grid = list(next_grid)
    for i in range(len(next_grid)):
        next_grid[i] = f(next_grid[i])
    t = 0
    dt = 1/300
    grey_per_point = 50
    clock = pygame.time.Clock()
    n = 0
    font = pygame.font.SysFont("Arial", 24)
    rec = ScreenRecorder(WINDOW_WIDTH, WINDOW_HEIGHT, 60, out_file="rec.mp4")
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        screen.fill((0, 0, 0))
        for next_z, last_z in zip(next_grid, last_grid):
            z = t * next_z + (1 - t) * last_z
            z_on_screen = (int((z.real + 1) * WINDOW_WIDTH / 2), int((-z.imag + 1) * WINDOW_HEIGHT / 2))
            for x in range(z_on_screen[0] - 1, z_on_screen[0] + 2):
                for y in range(z_on_screen[1] - 1, z_on_screen[1] + 2):
                    pos = (x, y)
                    if 0 <= pos[0] < WINDOW_WIDTH and 0 <= pos[1] < WINDOW_HEIGHT:
                        color = screen.get_at(pos)
                        color.r = min(255, color.r + grey_per_point)
                        color.g = min(255, color.g + grey_per_point)
                        color.b = min(255, color.b + grey_per_point)
                        screen.set_at(pos, color)
        screen.blit(font.render("n = {:.2f}".format(n + t), True, (255, 255, 255)), (10, 10))
        rec.capture_frame(screen)
        pygame.display.flip()
        if t < 1:
            t += dt
        else:
            t = 0
            n += 1
            last_grid = list(next_grid)
            for i in range(len(next_grid)):
                next_grid[i] = f(next_grid[i])
        if n == 3:
            rec.end_recording()
            pygame.quit()
            exit(0)
