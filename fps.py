import pygame
import random
import os

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced Shooting Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 설정
PLAYER_SIZE = (50, 50)
BULLET_SIZE = (10, 5)
ENEMY_SIZE = (50, 50)
ENEMY_COUNT = 5
PLAYER_SPEED = 7  # 속도 증가
BULLET_SPEED = 10  # 속도 증가
ENEMY_SPEED = 8  # 속도 증가
TIME_LIMIT = 30  # 제한 시간

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = PLAYER_SPEED

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # 화면 밖으로 나가지 않게 제한
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PLAYER_SIZE[0]:
            self.rect.x = SCREEN_WIDTH - PLAYER_SIZE[0]
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > SCREEN_HEIGHT - PLAYER_SIZE[1]:
            self.rect.y = SCREEN_HEIGHT - PLAYER_SIZE[1]

# 적 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, ENEMY_SIZE)
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
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, BULLET_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# 폭발 효과 클래스
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.image.load('explosion.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center

# 최고 기록 저장 및 불러오기
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            return int(file.read())
    return 0

def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# 설정 및 초기화
player = Player()
enemies = pygame.sprite.Group()
for _ in range(ENEMY_COUNT):
    enemies.add(Enemy())
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)

score = 0
high_score = load_high_score()
start_ticks = pygame.time.get_ticks()

# 소리 로드
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound('shoot.wav')
hit_sound = pygame.mixer.Sound('hit.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')

# 게임 루프
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)
                all_sprites.add(bullet)
                shoot_sound.play()

    if not game_over:
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
                score += 1
                hit_sound.play()

        # 플레이어와 적의 충돌 감지
        if pygame.sprite.spritecollideany(player, enemies):
            explosion_sound.play()
            explosion = Explosion(player.rect.center)
            all_sprites.add(explosion)
            player.kill()
            game_over = True

        # 시간 계산
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = TIME_LIMIT - elapsed_time

        # 화면 업데이트
        SCREEN.fill(BLACK)
        all_sprites.draw(SCREEN)

        # 점수 표시
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        time_text = font.render(f"Time: {int(remaining_time)}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(time_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(60)

        # 제한 시간 종료 시
        if remaining_time <= 0:
            running = False

    else:
        # 게임 오버 상태에서 잠시 대기 후 종료
        pygame.time.wait(2000)
        running = False

# 최고 점수 업데이트 및 저장
if score > high_score:
    save_high_score(score)
    high_score = score

# 게임 종료 화면
SCREEN.fill(BLACK)
end_text = font.render(f"Game Over! Your Score: {score}", True, WHITE)
high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
SCREEN.blit(end_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
SCREEN.blit(high_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
 