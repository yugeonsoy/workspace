import pygame
import random
import math

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # 전체화면 모드
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("2D Shooter Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 이미지 및 소리 로드
gun_image = pygame.image.load("gun.png").convert_alpha()  # 총 이미지 로드 (PNG 파일)
gun_sound = pygame.mixer.Sound("gun_sound.wav")  # 총 소리 파일 로드

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.original_image = gun_image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5
        self.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # 마우스 커서의 위치에 따라 총의 각도를 회전시킴
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx))
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # 화면 밖으로 나가지 않도록 제한
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self, all_sprites, bullets):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bullet = Bullet(self.rect.centerx, self.rect.centery, mouse_x, mouse_y)
        all_sprites.add(bullet)
        bullets.add(bullet)
        gun_sound.play()  # 총 발사 소리 재생

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=(x, y))
        angle = math.atan2(target_y - y, target_x - x)
        self.speed_x = math.cos(angle) * 10
        self.speed_y = math.sin(angle) * 10

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()  # 화면 밖으로 나가면 총알 삭제

# 적 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)))
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.x += random.choice([-1, 1]) * self.speed
        self.rect.y += random.choice([-1, 1]) * self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# 게임 루프
def game_loop():
    player = Player()
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    all_sprites.add(player)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(all_sprites, bullets)

        all_sprites.update()

        # 적 생성 (간단히 구현하기 위해 일정 시간마다 적이 나타나도록 설정)
        if random.random() < 0.02:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # 총알과 적의 충돌 처리
        for bullet in bullets:
            enemy_hit = pygame.sprite.spritecollideany(bullet, enemies)
            if enemy_hit:
                bullet.kill()
                enemy_hit.kill()

        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# 게임 시작
game_loop()
