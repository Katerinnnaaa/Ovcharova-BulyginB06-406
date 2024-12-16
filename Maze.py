import random
from collections import deque

import pygame


class Maze:
    def __init__(self, width, height):
        """
        Класс лабиринта
        :param width: Ширина поля в клетках
        :param height: Высота поля в клетках
        """
        self.width = width
        self.height = height

        # Положение игрока
        self.p_pos_x = 0
        self.p_pos_y = 0

        # Путь за игроком
        self.p_path = [[0 for _ in range(width)] for _ in range(height)]

        # Положение выхода
        self.g_pos_x, self.g_pos_y = 1, 1

        # Клетки лабиринта
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        # Посещённые клетки во время генерации
        self.visited = [[False for _ in range(width)] for _ in range(height)]

        self.directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Вниз, Вправо, Вверх, Влево

    def reset(self):
        """
        Установить все переменные в начальное состояние
        :return:
        """

        self.p_pos_x = 0
        self.p_pos_y = 0
        self.p_path = [[0 for _ in range(self.width)] for _ in range(self.height)]

        self.g_pos_x, self.g_pos_y = 1, 1

        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

    def generate(self):
        """
        Сгенерировать лабиринт с помощью алгоритма Prim
        :return:
        """
        # Начинаем с сетки полностью заполненной стенами
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # Никакая клетка не посещена
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        # Начальная клетка
        start_x, start_y = self.p_pos_x, self.p_pos_y

        # Выбираем клетку как начало лабиринта и посещаем её
        self.maze[start_y][start_x] = 0
        self.visited[start_y][start_x] = True

        walls = []  # Список стен

        # Добавляем стены для начальной клетки
        self._add_walls(start_x, start_y, walls)

        while walls:
            # Выбираем случайную стену
            wall = random.choice(walls)
            walls.remove(wall)

            x, y, direction = wall
            nx, ny = x + direction[0], y + direction[1]

            # Проверяем что клетка в пределах лабиринта и не была уже посещена
            if 0 <= nx < self.width and 0 <= ny < self.height and not self.visited[ny][nx]:
                # Делаем проход в стене
                self.maze[y + direction[1] // 2][x + direction[0] // 2] = 0

                self.maze[ny][nx] = 0  # Создаём путь
                self.visited[ny][nx] = True

                # Добавляем стены новой клетки
                self._add_walls(nx, ny, walls)

        # Находим самую дальнюю точку после генерации
        self.find_farthest_point(start_x, start_y)

    def _add_walls(self, x, y, walls):
        """
        Добавить стены клетки в список стен
        :param x: X координата клетки
        :param y: Y координата клетки
        :param walls: Список для добавления
        :return:
        """
        # Идём по направлениям
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy

            # Если клетка в которую стена ведёт не была посещена
            if 0 <= nx < self.width and 0 <= ny < self.height and not self.visited[ny][nx]:
                # Добавляем стену
                walls.append((x, y, (dx, dy)))

    def find_farthest_point(self, start_x, start_y):
        """
        Найти самую далёкую точку от начала
        :param start_x: X координата начала
        :param start_y: Y координата начала
        :return:
        """
        # Очередь хранящая X координату, Y координату, расстояние
        queue = deque([(start_x, start_y, 0)])

        max_distance = -1  # Максимальное найденное расстояние
        farthest_point = (start_x, start_y)  # Точка с таким расстоянием

        # Мы еще не посещали ни одну клетку
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        while queue:
            # Получаем точку из очереди
            x, y, distance = queue.popleft()

            # Если дальше чем max_distance, то обновляем максимальное расстояние
            if distance > max_distance:
                max_distance = distance
                farthest_point = (x, y)

            # Идём по соседям клетки
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy

                # Если есть проход
                if 0 <= nx < self.width and 0 <= ny < self.height and (self.maze[ny][nx] == 0):
                    if self.visited[ny][nx]:
                        continue
                    # Если не посещена
                    self.visited[ny][nx] = True
                    # Добавляем в очередь
                    queue.append((nx, ny, distance + 1))

        self.g_pos_x, self.g_pos_y = farthest_point

    def is_solved(self):
        """
        Проверка пройден ли лабиринт
        :return: True - да, False - нет
        """
        return (self.p_pos_x == self.g_pos_x) and (self.p_pos_y == self.g_pos_y)

    def move_player(self, dx, dy):
        """
        Переместить игрока
        :param dx: Относительная координата X
        :param dy: Относительная координата Y
        :return:
        """
        # Если никуда не двигаемся, то не выполняем функцию
        if dx == 0 and dy == 0:
            return

        # Перемещаем игрока
        self.p_pos_y += dy
        self.p_pos_x += dx

        # Если переместили в стену или за пределы возвращаем игрока назад
        if (not (0 <= self.p_pos_y < self.height) or
                not (0 <= self.p_pos_x < self.width) or
                (self.maze[self.p_pos_y][self.p_pos_x] != 0)):
            self.p_pos_y -= dy
            self.p_pos_x -= dx
            return

        if self.p_path[self.p_pos_y][self.p_pos_x] == 0:
            # Если перешли на клетку на которой нет пути игрока, то прошлая клетка путь игрока
            self.p_path[self.p_pos_y - dy][self.p_pos_x - dx] = 1
        elif self.p_path[self.p_pos_y][self.p_pos_x] == 1:
            # Если перешли на клетку на которой есть путь игрока, то игрок идёт назад, удаляем путь
            self.p_path[self.p_pos_y - dy][self.p_pos_x - dx] = 0

    def draw(self, screen, cell_size):
        """
        Отображение лабиринта
        :param screen: Окно на котором рисовать
        :param cell_size: Размер клетки в пикселях
        :return:
        """

        # Для каждой клетки
        for y in range(self.height):
            for x in range(self.width):
                # Если стена рисуем белым иначе чёрным
                color = (255, 255, 255) if self.maze[y][x] == 1 else (0, 0, 0)

                if x == self.p_pos_x and y == self.p_pos_y:
                    # Если игрок рисуем красным
                    color = (255, 0, 0)
                elif x == self.g_pos_x and y == self.g_pos_y:
                    # Если выход, то оранжевым
                    color = (255, 127, 0)
                elif self.p_path[y][x] == 1:
                    # Если путь, то тёмно-зелёным
                    color = (0, 127, 0)

                # Рисуем клетку
                pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
