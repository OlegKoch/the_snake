from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс"""

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Метод родительского класса для отрисоки объектов"""
        pass


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self, body_color=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Метод, обеспечивающий рандомное положение яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод, отрисовывающий яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self, lenght=1, next_direction=None, last=None,
                 body_color=None):
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.lenght = lenght
        self.direction = RIGHT
        self.next_direction = next_direction
        self.last = last

    def update_direction(self):
        """Обновление направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод, получающий текущую голову змейки"""
        return self.positions[0]

    def move(self):
        """Метод, ответственный за движение змейки"""
        self.head_position = self.get_head_position()
        self.new_head_position = (
            (self.head_position[0] + self.direction[0] * 20),
            (self.head_position[1] + self.direction[1] * 20)
        )
        if self.new_head_position[0] > SCREEN_WIDTH:
            self.new_head_position = (0, self.new_head_position[1])
            if len(self.positions) > self.lenght:
                self.positions.pop()

        if self.new_head_position[1] > SCREEN_HEIGHT:
            self.new_head_position = (self.new_head_position[0], 0)
            if len(self.positions) > self.lenght:
                self.positions.pop()

        if self.new_head_position[0] < 0:
            self.new_head_position = (SCREEN_WIDTH, self.new_head_position[1])
            if len(self.positions) > self.lenght:
                self.positions.pop()

        if self.new_head_position[1] < 0:
            self.new_head_position = (self.new_head_position[0], SCREEN_HEIGHT)
            if len(self.positions) > self.lenght:
                self.positions.pop()
        self.positions.insert(0, self.new_head_position)
        if len(self.positions) > self.lenght:
            self.last = self.positions[-1]
            self.positions.pop()

    def reset(self):
        """Сброс змейки"""
        self.lenght = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    # Метод draw класса Snake
    def draw(self):
        """Отрисовка"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция"""
    apple = Apple()
    snake = Snake()
    apple.draw()
    # Тут нужно создать экземпляры классов.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        if snake.positions[0] == apple.position:
            snake.lenght += 1
            apple.randomize_position()
            apple.draw()

        for pos in snake.positions[2:]:
            if pos == snake.new_head_position:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
                apple.randomize_position()
                apple.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        pygame.display.update()

    # Тут опишите основную логику игры.


if __name__ == '__main__':
    main()
