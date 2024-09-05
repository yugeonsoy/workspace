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

# 소리 로드
kill_sound = pygame.mixer.Sound("kill_sound.wav")  # 적 처치 사운드 파일
gun_sound = pygame.mixer.Sound("gun_sound.wav")  # 일반 총 소리 파일
shotgun_sound = pygame.mixer.Sound("shotgun_sound.wav")  # 산탄총 소리 파일
sniper_sound = pygame.mixer.Sound("sniper_sound.wav")  # 스나이퍼 소리 파일
kill_banner_image = pygame.image.load("kill_banner.png")  # 킬 배너 PNG 파일
kill_banner_visible = False  # 킬 배너 표시 여부
kill_banner_timer = 0  # 킬 배너 지속 시간

# 총, 산탄총, 스나이퍼 이미지 로드 및 크기 조정
gun_image = pygame.image.load("gun.png")
shotgun_image = pygame.image.load("shotgun.png")
sniper_image = pygame.image.load("sniper.png")  # 스나이퍼 이미지
gun_image = pygame.transform.scale(gun_image, (100, 40))  # 총 크기를 100px로 조정 (높이: 30px)
shotgun_image = pygame.transform.scale(shotgun_image, (170, 50))  # 산탄총 크기를 100px로 조정 (높이: 30px)
sniper_image = pygame.transform.scale(sniper_image, (120, 40))  # 스나이퍼 크기 조정

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5
        self.health = 100
        self.is_dashing = False
        self.dash_speed = 20
        self.dash_cooldown = 0
        self.dash_duration = 10
        self.dash_timer = 0
        self.is_time_stopped = False
        self.time_stop_duration = 180  # 3초간 시간 멈춤
        self.time_stop_timer = 0
        self.e_skill_cooldown = 0  # E 스킬 쿨타임
        self.f_skill_cooldown = 0  # F 스킬 쿨타임
        self.is_shotgun_mode = False  # 산탄총 모드 상태
        self.is_sniper_mode = False  # 스나이퍼 모드 상태

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

        if not self.is_dashing:
            self.rect.x += move_x
            self.rect.y += move_y

            # 대시 스킬
            if keys[pygame.K_LSHIFT] and self.dash_cooldown == 0:
                self.is_dashing = True
                self.dash_timer = self.dash_duration
                self.dash_cooldown = 60  # 대시 쿨다운 시간
        else:
            self.rect.x += move_x * self.dash_speed
            self.rect.y += move_y * self.dash_speed
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False

        # 쿨다운 감소
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.e_skill_cooldown > 0:
            self.e_skill_cooldown -= 1
        if self.f_skill_cooldown > 0:
            self.f_skill_cooldown -= 1

        # E 스킬 사용
        if keys[pygame.K_e] and self.e_skill_cooldown == 0:
            self.health += 30  # E 스킬 사용 시 체력 30 회복
            if self.health > 100:  # 최대 체력 제한
                self.health = 100
            self.e_skill_cooldown = 1200  # E 스킬 쿨타임 10초 (60 FPS 기준)

        # F 스킬: 시간 멈춤
        if keys[pygame.K_f] and self.f_skill_cooldown == 0 and not self.is_time_stopped:
            self.is_time_stopped = True
            self.time_stop_timer = self.time_stop_duration
            self.f_skill_cooldown = 600  # F 스킬 쿨다운 10초 (60 FPS 기준)

        if self.is_time_stopped:
            self.time_stop_timer -= 1
            if self.time_stop_timer <= 0:
                self.is_time_stopped = False

        # 화면 밖으로 나가지 않도록 제한
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # 플레이어 이미지 그리기
        # 총 이미지 그리기
        if self.is_shotgun_mode:
            screen.blit(shotgun_image, (self.rect.centerx - 50, self.rect.centery - 15))  # 산탄총 위치 조정
        elif self.is_sniper_mode:
            screen.blit(sniper_image, (self.rect.centerx - 60, self.rect.centery - 15))  # 스나이퍼 위치 조정
        else:
            screen.blit(gun_image, (self.rect.centerx - 50, self.rect.centery - 15))  # 총 위치 조정

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, color=RED, speed=10):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.angle = angle
        self.velocity_x = math.cos(math.radians(self.angle)) * self.speed
        self.velocity_y = math.sin(math.radians(self.angle)) * self.speed

    def update(self):
        if not player.is_time_stopped:
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
        if not player.is_time_stopped:
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
        bullet = Bullet(self.rect.center, angle, color=BLACK, speed=7)  # 목표물의 총알 속도
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

# 게임 설정
FPS = 60
clock = pygame.time.Clock()

# 그룹 설정
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# 플레이어 및 목표물 생성
player = Player()
all_sprites.add(player)
for _ in range(5):  # 목표물 개수
    target = Target(player)
    all_sprites.add(target)
    targets.add(target)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 마우스 클릭으로 총알 발사
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 마우스 버튼
                if player.is_sniper_mode:
                    # 스나이퍼 발사 (쿨다운 고려)
                    if player.f_skill_cooldown == 0:
                        angle = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - player.rect.centery, pygame.mouse.get_pos()[0] - player.rect.centerx))
                        bullet = Bullet(player.rect.center, angle, speed=20)  # 스나이퍼 총알 속도
                        all_sprites.add(bullet)
                        sniper_sound.play()  # 스나이퍼 발사 소리
                        player.f_skill_cooldown = 120  # 스나이퍼 쿨타임 (예: 2초)
                elif player.is_shotgun_mode:
                    # 산탄총 발사
                    for i in range(-2, 3):  # 산탄총 발사 각도 조정
                        angle = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - player.rect.centery, pygame.mouse.get_pos()[0] - player.rect.centerx)) + i * 10
                        bullet = Bullet(player.rect.center, angle, speed=15)  # 산탄총 총알 속도
                        all_sprites.add(bullet)
                        shotgun_sound.play()  # 산탄총 발사 소리
                else:
                    # 일반 총 발사
                    angle = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - player.rect.centery, pygame.mouse.get_pos()[0] - player.rect.centerx))
                    bullet = Bullet(player.rect.center, angle)
                    all_sprites.add(bullet)
                    gun_sound.play()  # 일반 총 소리

    # 업데이트 및 그리기
    all_sprites.update()
    
    # 쿨다운이 지난 경우 스킬 모드 전환
    if player.e_skill_cooldown == 0 and player.f_skill_cooldown == 0:
        if pygame.key.get_pressed()[pygame.K_1]:
            player.is_shotgun_mode = True
            player.is_sniper_mode = False
        elif pygame.key.get_pressed()[pygame.K_2]:
            player.is_shotgun_mode = False
            player.is_sniper_mode = True
        else:
            player.is_shotgun_mode = False
            player.is_sniper_mode = False

    screen.fill(WHITE)
    all_sprites.draw(screen)

    # 킬 배너 표시
    if kill_banner_visible:
        screen.blit(kill_banner_image, (SCREEN_WIDTH // 2 - kill_banner_image.get_width() // 2, SCREEN_HEIGHT // 2 - kill_banner_image.get_height() // 2))
        kill_banner_timer -= 1
        if kill_banner_timer <= 0:
            kill_banner_visible = False

    pygame.display.flip()
    clock.tick(FPS)

# 게임 종료 화면 표시
screen.fill(BLACK)
font = pygame.font.SysFont(None, 55)
text = font.render("Game Over! Press R to Restart or Q to Quit.", True, WHITE)
text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
screen.blit(text, text_rect)
pygame.display.flip()

# 종료 화면 루프
ending = True
while ending:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ending = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # R 키로 다시 시작
                ending = False
                # 게임 재시작 로직 추가 필요
            if event.key == pygame.K_q:  # Q 키로 종료
                ending = False
                pygame.quit()
    
    # 추가적으로 R이나 Q를 누르라는 메시지를 표시
    pygame.display.flip()

pygame.quit()
