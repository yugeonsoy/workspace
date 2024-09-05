import pygame
import random
import math

# 초기화
pygame.init()

# 전체화면 모드로 설정
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Shooting Game with Skills")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 사운드 및 이미지 로드
try:
    kill_sound = pygame.mixer.Sound("kill_sound.wav")  # 적 처치 사운드 파일
    bullet_hit_sound = pygame.mixer.Sound("bullet_hit.wav")  # 총알 맞았을 때 소리 파일
    shotgun_sound = pygame.mixer.Sound("shotgun_fire.wav")  # 샷건 발사 소리 파일
    rifle_sound = pygame.mixer.Sound("rifle_fire.wav")  # 라이플 발사 소리 파일
    sniper_sound = pygame.mixer.Sound("sniper_fire.wav")  # 스나이퍼 총 발사 소리 파일
    
    kill_banner_image = pygame.image.load("kill_banner.png")  # 킬 배너 PNG 파일
    shotgun_image = pygame.image.load("shotgun.png")  # 샷건 이미지 파일
    rifle_image = pygame.image.load("rifle.png")  # 라이플 이미지 파일
    sniper_rifle_image = pygame.image.load("sniper_rifle.png")  # 스나이퍼 총 이미지 파일
except FileNotFoundError as e:
    print(f"파일을 찾을 수 없습니다: {e}")

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5
        self.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0

        if keys[pygame.K_a]:
            move_x = -self.speed
        if keys[pygame.K_d]:
            move_x = self.speed
        if keys[pygame.K_w]:
            move_y = -self.speed
        if keys[pygame.K_s]:
            move_y = self.speed

        self.rect.x += move_x
        self.rect.y += move_y

        # 화면 밖으로 나가지 않도록 제한
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, speed=10):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.angle = angle
        self.velocity_x = math.cos(math.radians(self.angle)) * self.speed
        self.velocity_y = math.sin(math.radians(self.angle)) * self.speed

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()  # 화면 밖으로 나가면 삭제

# 목표물 클래스
class Target(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20)))
        self.speed = random.randint(2, 5)
        self.player = player
        self.shoot_delay = random.randint(60, 120)  # 목표물의 발사 간격 조정 (프레임 단위)
        self.shoot_timer = 0

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0

        # 플레이어를 향해 일정 간격으로 총알 발사
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.shoot()

    def shoot(self):
        angle = math.degrees(math.atan2(self.player.rect.centery - self.rect.centery, self.player.rect.centerx - self.rect.centerx))
        bullet = Bullet(self.rect.center, angle, speed=7)  # 목표물의 총알 속도
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

# 게임 루프
def game_loop():
    global all_sprites, enemy_bullets, targets, player

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    targets = pygame.sprite.Group()

    for _ in range(5):  # 5개의 목표물 생성
        target = Target(player)
        all_sprites.add(target)
        targets.add(target)

    clock = pygame.time.Clock()
    running = True
    score = 0

    # 총 상태
    current_gun = None
    shotgun_cooldown = 0
    rifle_cooldown = 0
    sniper_cooldown = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 마우스 버튼 클릭 시
                    mx, my = pygame.mouse.get_pos()
                    angle = math.degrees(math.atan2(my - player.rect.centery, mx - player.rect.centerx))

                    # 현재 총에 따라 총알 발사
                    if current_gun == "sniper":
                        if sniper_cooldown <= 0:
                            bullet = Bullet(player.rect.center, angle, speed=25)  # 스나이퍼 속도
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            sniper_cooldown = 120  # 2초 쿨다운
                            sniper_sound.play()
                    elif current_gun == "rifle":
                        if rifle_cooldown <= 0:
                            bullet = Bullet(player.rect.center, angle, speed=15)  # 라이플 속도
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            rifle_cooldown = 60  # 1초 쿨다운
                            rifle_sound.play()
                    elif current_gun == "shotgun":
                        if shotgun_cooldown <= 0:
                            bullet_count = 5  # 발사할 총알 수
                            spread_angle = 10  # 각도 차이
                            for i in range(bullet_count):
                                bullet_angle = angle + (spread_angle * (i - bullet_count // 2))
                                bullet = Bullet(player.rect.center, bullet_angle, speed=10)  # 산탄총 속도
                                all_sprites.add(bullet)
                                bullets.add(bullet)
                            shotgun_cooldown = 180  # 3초 쿨다운
                            shotgun_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            current_gun = "pistol"  # 권총 모드
        elif keys[pygame.K_2]:
            current_gun = "shotgun"  # 산탄총 모드
        elif keys[pygame.K_3]:
            current_gun = "rifle"  # 라이플 모드
        elif keys[pygame.K_4]:
            current_gun = "sniper"  # 스나이퍼 모드

        # 총알 업데이트
        all_sprites.update()

        # 쿨다운 감소
        if shotgun_cooldown > 0:
            shotgun_cooldown -= 1
        if rifle_cooldown > 0:
            rifle_cooldown -= 1
        if sniper_cooldown > 0:
            sniper_cooldown -= 1

        # 플레이어가 적의 총알에 맞았는지 확인
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            player.health -= 10  # 맞을 때마다 체력 10 감소
            bullet_hit_sound.play()  # 맞았을 때 소리 재생
            if player.health <= 0:
                print("Game Over")
                running = False

        # 목표물과 플레이어의 총알 충돌 처리
        for bullet in bullets:
            if pygame.sprite.spritecollide(bullet, targets, True):
                score += 1
                kill_sound.play()
                bullet.kill()  # 총알 삭제

        # 화면 그리기
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(60)  # FPS 설정

    pygame.quit()

# 게임 시작
game_loop()
