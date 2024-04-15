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

    def __init__(self, next_direction=None, last=None,
                 body_color=None):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
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
        self.head_position_x, self.head_position_y = self.get_head_position()
        self.new_head_position = (
            (self.head_position_x + self.direction[0] * 20),
            (self.head_position_y + self.direction[1] * 20)
        )

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


def defining_boundaries(game_object):
    """Определение границ для змейки"""
    if game_object.new_head_position[0] > SCREEN_WIDTH:
        game_object.new_head_position = (0, game_object.new_head_position[1])
        if len(game_object.positions) > game_object.lenght:
            game_object.positions.pop()

    elif game_object.new_head_position[1] > SCREEN_HEIGHT:
        game_object.new_head_position = (game_object.new_head_position[0], 0)
        if len(game_object.positions) > game_object.lenght:
            game_object.positions.pop()

    elif game_object.new_head_position[0] < 0:
        game_object.new_head_position = (SCREEN_WIDTH,
                                         game_object.new_head_position[1])
        if len(game_object.positions) > game_object.lenght:
            game_object.positions.pop()

    elif game_object.new_head_position[1] < 0:
        game_object.new_head_position = (game_object.new_head_position[0],
                                         SCREEN_HEIGHT)
        if len(game_object.positions) > game_object.lenght:
            game_object.positions.pop()


def main():
    """Основная функция"""
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            if snake.get_head_position() != apple.randomize_position():
                apple.draw()
        if snake.lenght > 5:
            if snake.new_head_position in snake.positions[2:]:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
                apple.randomize_position()
                apple.draw()
        defining_boundaries(snake)
        snake.positions.insert(0, snake.new_head_position)
        if len(snake.positions) > snake.lenght:
            snake.last = snake.positions[-1]
            snake.positions.pop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
