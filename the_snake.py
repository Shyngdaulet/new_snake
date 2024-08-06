from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_POSITION = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех иогровых объектов."""

    def __init__(self, position=CENTER_POSITION, color=None):
        self.position = position
        self.body_color = color

    def draw(self):
        """Метод для отрисовки игрового объекта."""
        raise NotImplementedError(
            'This method should be implemented in subclasses'
        )


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, occupied_positions):
        super().__init__(color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Метод для случайного выбора новой позиции яблока."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self):
        """Метод для отрисовки яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self, position=CENTER_POSITION, color=SNAKE_COLOR):
        super().__init__(position=position, color=color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод для обновления направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для перемещения змейки."""
        self.update_direction()
        head_x, head_y = self.get_head_position()
        x, y = self.direction
        new = ((head_x + (x * GRID_SIZE)) % SCREEN_WIDTH,
               (head_y + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Метод для сброса змейки в начальное состояние."""
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)
        pygame.display.update()

    def grow(self):
        """Метод для увеличения длины змейки."""
        self.length += 1

    def draw(self):
        """Метод для отрисовки змейки на экране."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Метод для получения текущей позиции головы змейки."""
        return self.positions[0]


def handle_keys(snake):
    """Функция для обработки событий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция для запуска игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        if (
            len(snake.positions) > 2
            and snake.get_head_position() in snake.positions[2:]
        ):
            snake.reset()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()