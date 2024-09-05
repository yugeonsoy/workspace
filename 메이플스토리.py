import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("메이플스토리 스타일 게임")

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

# 캐릭터 클래스
class Character:
    def __init__(self):
        self.rect = pygame.Rect(100, SCREEN_HEIGHT - 70, 50, 50)
        self.color = GREEN
        self.gravity = 0.5
        self.velocity_y = 0
        self.is_jumping = False
        self.health = 100

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -10

    def update(self):
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            
            if self.rect.y >= SCREEN_HEIGHT - 70:
                self.rect.y = SCREEN_HEIGHT - 70
                self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# 적 클래스
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 100), 50, 50)
        self.color = RED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# 게임 루프
def game_loop():
    character = Character()
    enemies = [Enemy() for _ in range(5)]  # 적 5마리 생성

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # 왼쪽 이동
            character.move(-5)
        if keys[pygame.K_d]:  # 오른쪽 이동
            character.move(5)
        if keys[pygame.K_w]:  # 점프
            character.jump()

        # 캐릭터 업데이트
        character.update()

        # 화면 그리기
        screen.fill(WHITE)
        character.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        # 건강 상태 표시
        health_font = pygame.font.SysFont(None, 36)
        health_text = health_font.render(f"Health: {character.health}", True, BLACK)
        screen.blit(health_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

# 게임 시작
game_loop()
