import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2인용 대전 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # '맑은 고딕' 폰트 경로
font = pygame.font.Font(font_path, 74)
small_font = pygame.font.Font(font_path, 36)

# 플레이어 설정
PLAYER_WIDTH, PLAYER_HEIGHT = 30, 40  # 플레이어 크기 축소
PLAYER_SPEED = 5
JUMP_HEIGHT = 15  # 점프 높이
GRAVITY = 0.5
BULLET_SPEED = 7

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.color = color
        self.controls = controls
        self.speed = PLAYER_SPEED
        self.jump_power = JUMP_HEIGHT
        self.velocity_y = 0
        self.on_ground = False
        self.jump_count = 0  # 이중 점프를 위한 점프 횟수 추적
        self.health = 100

    def update(self, keys, bullets):
        # 이동
        if keys[self.controls['left']]:
            self.rect.x -= self.speed
        if keys[self.controls['right']]:
            self.rect.x += self.speed

        # 점프 및 이중 점프
        if keys[self.controls['jump']]:
            if self.on_ground or self.jump_count < 2:
                self.velocity_y = -self.jump_power
                self.on_ground = False
                self.jump_count += 1

        # 중력 적용
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # 벽에 닿았을 때 점프 초기화
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.jump_count = 1  # 벽에 닿았을 때 점프 횟수를 1로 초기화

        # 바닥에 도달하면 속도를 0으로 설정
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True
            self.jump_count = 0

        # 총 쏘기
        if keys[self.controls['shoot']]:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.color, self.controls['direction'])
            bullets.add(bullet)

        # 화면 밖으로 나가지 않도록 제한
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # 체력 바
        health_bar_width = self.health
        health_bar = pygame.Surface((health_bar_width, 5))
        health_bar.fill(RED)
        screen.blit(health_bar, (self.rect.x, self.rect.y - 10))

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED
        self.direction = direction

    def update(self):
        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# 게임 루프
def game_loop():
    player1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'shoot': pygame.K_SPACE, 'direction': 'right'}
    player2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'shoot': pygame.K_RETURN, 'direction': 'left'}

    player1 = Player(100, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, BLUE, player1_controls)
    player2 = Player(SCREEN_WIDTH - 150, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, RED, player2_controls)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1, player2)

    bullets = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True

    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 업데이트
        player1.update(keys, bullets)
        player2.update(keys, bullets)
        bullets.update()

        # 총알끼리 충돌 감지
        for bullet1 in bullets:
            for bullet2 in bullets:
                if bullet1 != bullet2 and bullet1.rect.colliderect(bullet2.rect):
                    bullet1.kill()
                    bullet2.kill()

        # 총알과 플레이어 충돌 감지
        for bullet in bullets:
            if bullet.rect.colliderect(player1.rect) and bullet.direction != player1.controls['direction']:
                player1.health -= 10
                bullet.kill()
            if bullet.rect.colliderect(player2.rect) and bullet.direction != player2.controls['direction']:
                player2.health -= 10
                bullet.kill()

        # 게임 종료 조건
        if player1.health <= 0 or player2.health <= 0:
            running = False

        # 그리기
        screen.fill(WHITE)
        all_sprites.draw(screen)
        bullets.draw(screen)
        player1.draw(screen)
        player2.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    # 게임 종료 화면
    screen.fill(WHITE)
    winner_text = "플레이어 1 승리!" if player2.health <= 0 else "플레이어 2 승리!"
    draw_text(winner_text, BLACK, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50)
    pygame.display.flip()
    pygame.time.delay(3000)

    pygame.quit()

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# 게임 시작
game_loop()
