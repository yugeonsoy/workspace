import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 400  # 화면 크기 조정
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 타일 크기
TILE_SIZE = 20

# 미로 크기
MAZE_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAZE_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# 미로 생성 (1은 벽, 0은 길)
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]

    def carve_passages_from(x, y):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # 우, 하, 좌, 상
        random.shuffle(directions)  # 랜덤 방향 설정
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0  # 벽 제거
                maze[ny][nx] = 0  # 길 생성
                carve_passages_from(nx, ny)  # 재귀 호출

    # 시작 지점에서 미로 생성
    carve_passages_from(1, 1)
    return maze

# 미로 생성
MAZE = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, dx, dy):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        if 0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT:
            if MAZE[new_y // TILE_SIZE][new_x // TILE_SIZE] == 0:
                self.rect.x = new_x
                self.rect.y = new_y

# 목표 클래스
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 게임 초기화
def init_game():
    player_start_x, player_start_y = TILE_SIZE, TILE_SIZE  # 플레이어 시작 위치

    # 랜덤 목표 위치
    while True:
        goal_x = random.randint(0, MAZE_WIDTH - 1) * TILE_SIZE
        goal_y = random.randint(0, MAZE_HEIGHT - 1) * TILE_SIZE
        if MAZE[goal_y // TILE_SIZE][goal_x // TILE_SIZE] == 0:  # 목표가 길인 경우
            break

    player = Player(player_start_x, player_start_y)
    goal = Goal(goal_x, goal_y)
    all_sprites = pygame.sprite.Group(player, goal)
    return player, goal, all_sprites

# 게임 루프
def game_loop():
    player, goal, all_sprites = init_game()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-TILE_SIZE, 0)
        if keys[pygame.K_RIGHT]:
            player.move(TILE_SIZE, 0)
        if keys[pygame.K_UP]:
            player.move(0, -TILE_SIZE)
        if keys[pygame.K_DOWN]:
            player.move(0, TILE_SIZE)

        # 플레이어가 목표에 도달했는지 확인
        if pygame.sprite.collide_rect(player, goal):
            print("You reached the goal!")
            running = False

        # 화면 그리기
        SCREEN.fill(WHITE)
        for row in range(len(MAZE)):
            for col in range(len(MAZE[row])):
                if MAZE[row][col] == 1:
                    pygame.draw.rect(SCREEN, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(15)  # 게임 속도 조절

    pygame.quit()

# 게임 시작
game_loop()
