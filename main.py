import pygame
import sys

from Maze import Maze

pygame.init()

# Размеры окна и FPS
width, height = 800, 600
fps = 60

# Размер одной клетки лабиринта в пикселях
maze_cell_size = 15

# Создаём окно
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()

# Загружаем шрифт
font = pygame.font.Font(None, 36)

# Интервал между шагами ходьбы
interval = 0.15
last = 0

# Генерируем лабиринт
maze = Maze(width // maze_cell_size, (height - 50) // maze_cell_size)
maze.generate()

# Время начала и конца прохождения лабиринта
start_time = pygame.time.get_ticks()
solved_time = None

solved = False

while True:
    # Проверяем события окна
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Выходим если пользователь нажал крестик
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                # При нажатии двигаемся сразу, а не ждём интервал.
                last = interval + 1
            elif event.key == pygame.K_SPACE and solved:
                # Перезапуск лабиринта
                maze.reset()
                maze.generate()

                start_time = pygame.time.get_ticks()
                solved_time = None
                solved = False

    if not solved:
        # Логика для не пройденного лабиринта

        pressed_keys = pygame.key.get_pressed()

        if last > interval:
            # Идём в нужную сторону в зависимости от нажатой клавиши

            if maze.is_solved():
                solved = True
                solved_time = pygame.time.get_ticks()
            elif pressed_keys[pygame.K_w]:
                maze.move_player(0, -1)
            elif pressed_keys[pygame.K_a]:
                maze.move_player(-1, 0)
            elif pressed_keys[pygame.K_s]:
                maze.move_player(0, 1)
            elif pressed_keys[pygame.K_d]:
                maze.move_player(1, 0)

            last = 0
    # Очистка экрана
    screen.fill((0, 0, 0))

    if not solved:
        # Рисуем лабиринт, если не он не пройден
        maze.draw(screen, maze_cell_size)

        solving_time = (pygame.time.get_ticks() - start_time) / 1000

        time_text = font.render(f'{solving_time:.2f}', True, (255, 255, 255))
        screen.blit(time_text, (width // 2 - time_text.get_width() // 2, height - 50))
    else:
        # Иначе, рисуем экран победы
        solving_time = (solved_time - start_time) / 1000

        won_text = font.render(f'Победа!', True, (255, 255, 255))
        time_text = font.render(f'{solving_time:.2f}s', True, (255, 255, 255))
        restart_text = font.render(f'Нажмите пробел для перезапуска', True, (255, 255, 255))

        screen.blit(won_text, (width // 2 - won_text.get_width() // 2,
                               height // 2 - won_text.get_height() - time_text.get_height() // 2))
        screen.blit(time_text, (width // 2 - time_text.get_width() // 2,
                                height // 2 - time_text.get_height() // 2))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2,
                                   height // 2 + restart_text.get_height() - time_text.get_height() // 2))

    pygame.display.flip()

    # Запускаем в нужном FPS
    delta = clock.tick(fps)
    last += delta / 1000
