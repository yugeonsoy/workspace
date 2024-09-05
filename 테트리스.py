import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (128, 0, 128),  # Purple
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
]

# 테트리미노 모양 정의
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]]
]

# 블록 크기 및 게임 보드 크기 설정
BLOCK_SIZE = 30
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# 테트리미노 클래스
class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, screen):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, pygame.Rect((self.x + j) * BLOCK_SIZE, (self.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# 게임 보드 클래스
class Board:
    def __init__(self):
        self.grid = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_tetromino = Tetromino()

    def collide(self):
        for i, row in enumerate(self.current_tetromino.shape):
            for j, cell in enumerate(row):
                if cell:
                    if (self.current_tetromino.x + j < 0 or
                        self.current_tetromino.x + j >= BOARD_WIDTH or
                        self.current_tetromino.y + i >= BOARD_HEIGHT or
                        self.grid[self.current_tetromino.y + i][self.current_tetromino.x + j] != BLACK):
                        return True
        return False

    def freeze(self):
        for i, row in enumerate(self.current_tetromino.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_tetromino.y + i][self.current_tetromino.x + j] = self.current_tetromino.color
        self.clear_lines()
        self.current_tetromino = Tetromino()
        if self.collide():
            self.__init__()  # 게임 리셋

    def clear_lines(self):
        self.grid = [row for row in self.grid if BLACK in row]
        while len(self.grid) < BOARD_HEIGHT:
            self.grid.insert(0, [BLACK for _ in range(BOARD_WIDTH)])

    def move_down(self):
        self.current_tetromino.y += 1
        if self.collide():
            self.current_tetromino.y -= 1
            self.freeze()

    def move_side(self, dx):
        self.current_tetromino.x += dx
        if self.collide():
            self.current_tetromino.x -= dx

    def rotate(self):
        original_shape = self.current_tetromino.shape
        self.current_tetromino.rotate()
        if self.collide():
            self.current_tetromino.shape = original_shape

    def draw(self, screen):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                pygame.draw.rect(screen, GRAY, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
                if self.grid[y][x] != BLACK:
                    pygame.draw.rect(screen, self.grid[y][x], pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        self.current_tetromino.draw(screen)

# 게임 루프
def game_loop():
    board = Board()
    clock = pygame.time.Clock()
    fall_time = 0

    running = True
    while running:
        screen.fill(BLACK)
        fall_speed = 500  # 500 milliseconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.move_side(-1)
                if event.key == pygame.K_RIGHT:
                    board.move_side(1)
                if event.key == pygame.K_DOWN:
                    board.move_down()
                if event.key == pygame.K_UP:
                    board.rotate()

        fall_time += clock.get_rawtime()
        if fall_time >= fall_speed:
            board.move_down()
            fall_time = 0

        board.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# 게임 시작
game_loop()
