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

# 킬 사운드 로드
kill_sound = pygame.mixer.Sound("kill_sound.wav")  # 적 처치 사운드 파일
kill_banner_image = pygame.image.load("kill_banner.png")  # 킬 배너 PNG 파일
kill_banner_visible = False  # 킬 배너 표시 여부
kill_banner_timer = 0  # 킬 배너 지속 시간

# 총 클래스
class Gun:
    def __init__(self, bullet_color, bullet_speed, bullet_size, fire_rate):
        self.bullet_color = bullet_color
        self.bullet_speed = bullet_speed
        self.bullet_size = bullet_size
        self.fire_rate = fire_rate  # 연사 속도 (프레임)

# 총 객체 생성
gun1 = Gun(RED, 10, (10, 5), 15)  # 총 1: 일반 총
gun2 = Gun(GREEN, 8, (20, 10), 30)  # 총 2: 산탄총

guns = [gun1, gun2]
current_gun_index = 0  # 현재 선택된 총의 인덱스

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
            self.f_skill_cooldown = 600  # F 스킬 쿨타임 10초 (60 FPS 기준)

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

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, gun):
        super().__init__()
        self.image = pygame.Surface(gun.bullet_size)
        self.image.fill(gun.bullet_color)
        self.rect = self.image.get_rect(center=pos)
        self.speed = gun.bullet_speed
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
        bullet = Bullet(self.rect.center, angle, gun1)  # 기본 총으로 발사
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

# 게임 루프
def game_loop():
    global all_sprites, enemy_bullets, targets, player, kill_banner_visible, kill_banner_timer, current_gun_index

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
    fire_cooldown = 0  # 발사 쿨다운

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 마우스 클릭 시 총알 발사
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 마우스 버튼 클릭 시
                    mx, my = pygame.mouse.get_pos()
                    angle = math.degrees(math.atan2(my - player.rect.centery, mx - player.rect.centerx))

                    # 발사 쿨다운 체크
                    if fire_cooldown == 0:
                        bullet = Bullet(player.rect.center, angle, guns[current_gun_index])
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        fire_cooldown = guns[current_gun_index].fire_rate  # 발사 쿨다운 설정

            # 총 선택
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_gun_index = 0  # 총 1 선택
                elif event.key == pygame.K_2:
                    current_gun_index = 1  # 총 2 선택

        # 쿨다운 감소
        if fire_cooldown > 0:
            fire_cooldown -= 1

        all_sprites.update()

        # 플레이어가 적의 총알에 맞았는지 확인
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            player.health -= 10  # 맞을 때마다 체력 10 감소
            if player.health <= 0:
                print("Game Over")
                running = False

        # 목표물과 플레이어의 총알 충돌 감지
        for bullet in bullets:
            hit_targets = pygame.sprite.spritecollide(bullet, targets, True)
            for target in hit_targets:
                bullet.kill()
                score += 10
                kill_sound.play()  # 킬 사운드 재생
                kill_banner_visible = True
                kill_banner_timer = 170  # 2초 동안 표시

                # 새로운 목표물 생성
                new_target = Target(player)
                all_sprites.add(new_target)
                targets.add(new_target)

        # 킬 배너 타이머 감소
        if kill_banner_visible:
            kill_banner_timer -= 1
            if kill_banner_timer <= 0:
                kill_banner_visible = False

        screen.fill(WHITE)

        # 모든 스프라이트 그리기
        all_sprites.draw(screen)

        # 킬 배너 표시
        if kill_banner_visible:
            screen.blit(kill_banner_image, (SCREEN_WIDTH // 2 - kill_banner_image.get_width() // 2, 50))

        # 체력 표시
        health_text = f"Health: {player.health}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(health_text, True, BLACK)
        screen.blit(text_surface, (10, 10))

        # 점수 표시
        score_text = f"Score: {score}"
        score_surface = font.render(score_text, True, BLACK)
        screen.blit(score_surface, (SCREEN_WIDTH - 150, 10))

        # 화면 업데이트
        pygame.display.flip()
        clock.tick(60)  # FPS 제한

    pygame.quit()

# 게임 실행
game_loop()
