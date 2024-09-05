import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basic Shooting Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 설정
PLAYER_SIZE = (50, 50)
BULLET_SIZE = (10, 5)
ENEMY_SIZE = (50, 50)
ENEMY_COUNT = 5
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 3

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = PLAYER_SPEED

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PLAYER_SIZE[0]:
            self.rect.x = SCREEN_WIDTH - PLAYER_SIZE[0]

# 적 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(ENEMY_SIZE)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE[0])
        self.rect.y = random.randint(-200, -50)
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE[0])
            self.rect.y = random.randint(-200, -50)

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(BULLET_SIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# 설정 및 초기화
player = Player()
enemies = pygame.sprite.Group()
for _ in range(ENEMY_COUNT):
    enemies.add(Enemy())
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)

# 게임 루프
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)
                all_sprites.add(bullet)

    keys = pygame.key.get_pressed()
    player.update(keys)
    enemies.update()
    bullets.update()

    # 충돌 처리
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    if hits:
        for hit in hits:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)

    SCREEN.fill(BLACK)
    all_sprites.draw(SCREEN)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
 