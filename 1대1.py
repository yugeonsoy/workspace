import pygame
import random

# 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("1v1 Shooting Game")

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

# 플레이어 클래스
class Player:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 60)
        self.color = color
        self.health = 100
        self.is_jumping = False
        self.jump_count = 10
        self.gravity = 0.5
        self.velocity_y = 0  # 수직 속도 추가

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -15  # 점프 속도 설정 (더 높이 점프)

    def update(self):
        if self.is_jumping:
            self.velocity_y += self.gravity  # 중력 적용
            self.rect.y += self.velocity_y
            
            if self.rect.y >= SCREEN_HEIGHT - 70:  # 바닥에 닿으면
                self.rect.y = SCREEN_HEIGHT - 70
                self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# 총알 클래스
class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 8, 5)  # 총알 길이
        self.direction = direction

    def move(self):
        self.rect.x += self.direction

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

# 충돌 처리 함수
def handle_collision(player, bullets):
    for bullet in bullets:
        if bullet.rect.colliderect(player.rect):
            player.health -= 20  # 체력 감소
            bullets.remove(bullet)  # 맞은 총알 제거
            if player.health <= 0:  # 체력이 0 이하가 되면 True 리턴
                return True
    return False

# 게임 루프
def game_loop():
    player1 = Player(100, SCREEN_HEIGHT - 70, RED)
    player2 = Player(600, SCREEN_HEIGHT - 70, GREEN)  # 거리를 더 멀리 설정

    bullets = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Player 1 controls
        if keys[pygame.K_a]:  # Move left
            player1.move(-5)
        if keys[pygame.K_d]:  # Move right
            player1.move(5)
        if keys[pygame.K_w]:  # Jump
            player1.jump()
        if keys[pygame.K_SPACE]:  # Shoot bullet
            if len(bullets) < 1:  # 최대 총알 개수 제한
                bullets.append(Bullet(player1.rect.right, player1.rect.centery, 10))

        # Player 2 controls
        if keys[pygame.K_LEFT]:  # Move left
            player2.move(-5)
        if keys[pygame.K_RIGHT]:  # Move right
            player2.move(5)
        if keys[pygame.K_UP]:  # Jump
            player2.jump()
        if keys[pygame.K_RETURN]:  # Shoot bullet
            if len(bullets) < 1:  # 최대 총알 개수 제한
                bullets.append(Bullet(player2.rect.left - 8, player2.rect.centery, -10))

        # 총알 이동 및 충돌 처리
        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH:
                bullets.remove(bullet)

        # 충돌 처리
        player1_hit = handle_collision(player1, bullets)
        player2_hit = handle_collision(player2, bullets)

        if player1_hit and player1.health <= 0:
            print("Player 2 wins!")
            running = False
        if player2_hit and player2.health <= 0:
            print("Player 1 wins!")
            running = False

        # 업데이트 플레이어
        player1.update()
        player2.update()

        # 화면 그리기
        SCREEN.fill(WHITE)
        player1.draw(SCREEN)
        player2.draw(SCREEN)

        for bullet in bullets:
            bullet.draw(SCREEN)

        # 건강 상태 표시
        health_font = pygame.font.SysFont(None, 36)
        health_text1 = health_font.render(f"Player 1 Health: {player1.health}", True, BLACK)
        health_text2 = health_font.render(f"Player 2 Health: {player2.health}", True, BLACK)
        SCREEN.blit(health_text1, (10, 10))
        SCREEN.blit(health_text2, (SCREEN_WIDTH - 220, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# 게임 시작
game_loop()
