import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini LoL Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 플레이어 클래스
class Champion:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = BLUE
        self.health = 100
        self.speed = 5
        self.bullets = []
        self.cooldown = 0

    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

    def shoot(self):
        if self.cooldown == 0:
            bullet = pygame.Rect(self.rect.centerx, self.rect.centery, 10, 10)
            self.bullets.append(bullet)
            self.cooldown = 20

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        for bullet in self.bullets[:]:
            bullet.y -= 10
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(screen, BLACK, bullet)

    def draw_health(self, screen):
        health_text = font.render(f"Health: {self.health}", True, BLACK)
        screen.blit(health_text, (10, 10))

# 미니언 클래스
class Minion:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 40), random.randint(-100, -40), 40, 40)
        self.color = RED
        self.health = 10  # 체력을 낮게 설정하여 한 방에 죽도록
        self.speed = 3

    def move(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, SCREEN_WIDTH - 40)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# 충돌 처리 함수
def handle_collision(champion, minions):
    for minion in minions:
        for bullet in champion.bullets:
            if minion.rect.colliderect(bullet):
                minion.health -= 10
                champion.bullets.remove(bullet)
                if minion.health <= 0:
                    minions.remove(minion)
                    break

# 게임 루프
def game_loop():
    player = Champion(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    minions = [Minion() for _ in range(5)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.move(keys)

        if keys[pygame.K_SPACE]:
            player.shoot()

        player.update()

        for minion in minions:
            minion.move()

        handle_collision(player, minions)

        # 화면 그리기
        SCREEN.fill(WHITE)
        player.draw(SCREEN)
        player.draw_health(SCREEN)
        for minion in minions:
            minion.draw(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# 게임 시작
game_loop()
