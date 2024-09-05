import pygame
import random
import math
import os

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

# 배경 이미지 로드 및 크기 조정 (10개의 배경 이미지)
background_images = [
    pygame.transform.scale(pygame.image.load(f"background_{i}.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)) 
    for i in range(1, 11)
]

# 소리 로드
kill_sound = pygame.mixer.Sound("kill_sound.wav")
gun_sound = pygame.mixer.Sound("gun_sound.wav")
shotgun_sound = pygame.mixer.Sound("shotgun_sound.wav")
sniper_sound = pygame.mixer.Sound("sniper_sound.wav")
hit_sound = pygame.mixer.Sound("hit_sound.wav")
kill_banner_image = pygame.image.load("kill_banner.png")
kill_banner_visible = False
kill_banner_timer = 0

# 배경 음악 로드 및 재생
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# 최고 기록 파일 경로
HIGHLIGHT_FILE = "highlight7.txt"

# 최고 기록 불러오기
def load_high_score():
    if os.path.exists(HIGHLIGHT_FILE):
        with open(HIGHLIGHT_FILE, "r") as file:
            return int(file.read().strip())
    else:
        return 0

# 최고 기록 저장
def save_high_score(high_score):
    with open(HIGHLIGHT_FILE, "w") as file:
        file.write(str(high_score))

# 총과 산탄총, 스나이퍼 이미지 로드 및 크기 조정
gun_image = pygame.image.load("toe.png")
shotgun_image = pygame.image.load("shotgun.png")
sniper_image = pygame.image.load("sniper.png")
gun_image = pygame.transform.scale(gun_image, (200, 80))
shotgun_image = pygame.transform.scale(shotgun_image, (170, 50))
sniper_image = pygame.transform.scale(sniper_image, (200, 50))

# 마우스 포인터 이미지 로드 및 크기 조정
mouse_image = pygame.image.load("mouse_cursor.png")
mouse_image = pygame.transform.scale(mouse_image, (80, 80))

# 마우스 포인터를 숨김
pygame.mouse.set_visible(False)

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 10
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
        self.hit_timer = 0  # 플레이어가 맞았을 때 색을 변경할 타이머
        self.is_invincible = False  # 무적 상태
        self.invincibility_timer = 0  # 무적 지속 시간
        self.q_skill_cooldown = 0  # Q 스킬 쿨타임

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

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.e_skill_cooldown > 0:
            self.e_skill_cooldown -= 1
        if self.f_skill_cooldown > 0:
            self.f_skill_cooldown -= 1
        if self.q_skill_cooldown > 0:
            self.q_skill_cooldown -= 1

        if keys[pygame.K_e] and self.e_skill_cooldown == 0:
            self.health += 30
            if self.health > 100:  # 최대 체력 제한
                self.health = 100
            self.e_skill_cooldown = 800  # E 스킬 쿨타임 10초 (60 FPS 기준)

        if keys[pygame.K_f] and self.f_skill_cooldown == 0 and not self.is_time_stopped:
            self.is_time_stopped = True
            self.time_stop_timer = self.time_stop_duration
            self.f_skill_cooldown = 500  # F 스킬 쿨다운 10초 (60 FPS 기준)

        if self.is_time_stopped:
            self.time_stop_timer -= 1
            if self.time_stop_timer <= 0:
                self.is_time_stopped = False

        if keys[pygame.K_q] and self.q_skill_cooldown == 0:
            self.is_invincible = True
            self.invincibility_timer = 120  # 무적 지속 시간 2초 (120 프레임)
            self.q_skill_cooldown = 300  # Q 스킬 쿨다운 8초 (480 프레임)

        if self.is_invincible:
            self.invincibility_timer -= 1
            self.image.fill(GREEN)  # 무적일 때 색상을 변경
            if self.invincibility_timer <= 0:
                self.is_invincible = False
                self.image = self.original_image.copy()

        if self.hit_timer > 0:
            self.hit_timer -= 1
            if not self.is_invincible:  # 무적 상태가 아닐 때만 색상을 빨간색으로 변경
                self.image.fill(RED)
        elif not self.is_invincible:
            self.image = self.original_image.copy()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        mx, my = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(my - self.rect.centery, mx - self.rect.centerx))

        if self.is_sniper_mode:
            rotated_gun = pygame.transform.rotate(sniper_image, -angle)
        elif self.is_shotgun_mode:
            rotated_gun = pygame.transform.rotate(shotgun_image, -angle)
        else:
            rotated_gun = pygame.transform.rotate(gun_image, -angle)

        gun_rect = rotated_gun.get_rect(center=self.rect.center)
        screen.blit(rotated_gun, gun_rect.topleft)

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
    def __init__(self, player, speed_multiplier=1, bullet_speed=7):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20)))
        self.speed = random.randint(2, 5) * speed_multiplier
        self.player = player
        self.shoot_delay = random.randint(60, 120)
        self.shoot_timer = 0
        self.bullet_speed = bullet_speed

    def update(self):
        if not player.is_time_stopped:
            self.rect.x += self.speed
            if self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0

            self.shoot_timer += 0.5
            if self.shoot_timer >= self.shoot_delay:
                self.shoot_timer = 0
                self.shoot()

    def shoot(self):
        angle = math.degrees(math.atan2(self.player.rect.centery - self.rect.centery, self.player.rect.centerx - self.rect.centerx))
        bullet = Bullet(self.rect.center, angle, color=GREEN, speed=self.bullet_speed)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

# 체력 회복 아이템 클래스
class HealthItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 255))  # 보라색으로 색상 설정
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20)))

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            player.health += 20
            if player.health > 100:
                player.health = 100
            self.kill()

# 게임 루프
def game_loop():
    global all_sprites, enemy_bullets, targets, player, kill_banner_visible, kill_banner_timer

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    health_items = pygame.sprite.Group()

    level = 1
    level_duration = 2400  # 30초마다 레벨업 (60 FPS 기준)
    level_timer = 0
    health_item_timer = 300
    bullet_speed = 6
    high_score = load_high_score()

    for _ in range(5):
        target = Target(player)
        all_sprites.add(target)
        targets.add(target)

    clock = pygame.time.Clock()
    running = True
    score = 0

    shotgun_cooldown = 0
    normal_cooldown = 0  # 일반 총의 쿨타임 변수
    sniper_cooldown = 0  # 스나이퍼 쿨다운 변수

    shotgun_speed = 15
    normal_speed = 30
    sniper_speed = 55

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    angle = math.degrees(math.atan2(my - player.rect.centery, mx - player.rect.centerx))

                    if player.is_sniper_mode:
                        if sniper_cooldown <= 0:
                            bullet = Bullet(player.rect.center, angle, speed=sniper_speed)
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            sniper_sound.play()
                            sniper_cooldown = 120  # 스나이퍼 쿨다운 2초 (120 프레임)

                    elif player.is_shotgun_mode:
                        if shotgun_cooldown <= 0:
                            bullet_count = 5
                            spread_angle = 10

                            for i in range(bullet_count):
                                bullet_angle = angle + (spread_angle * (i - bullet_count // 2))
                                bullet = Bullet(player.rect.center, bullet_angle, speed=shotgun_speed)
                                all_sprites.add(bullet)
                                bullets.add(bullet)
                            shotgun_sound.play()
                            shotgun_cooldown = 180  # 산탄총 쿨다운 3초

                    else:
                        if normal_cooldown <= 0:
                            bullet = Bullet(player.rect.center, angle, speed=normal_speed)
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            gun_sound.play()
                            normal_cooldown = 60  # 일반 총 쿨다운

        keys = pygame.key.get_pressed()
        if keys[pygame.K_2]:
            player.is_shotgun_mode = not player.is_shotgun_mode
            if player.is_shotgun_mode:
                player.is_sniper_mode = False
        if keys[pygame.K_3]:
            player.is_sniper_mode = not player.is_sniper_mode
            if player.is_sniper_mode:
                player.is_shotgun_mode = False

        all_sprites.update()

        if shotgun_cooldown > 0:
            shotgun_cooldown -= 1
        if normal_cooldown > 0:
            normal_cooldown -= 1
        if sniper_cooldown > 0:
            sniper_cooldown -= 1

        level_timer += 1
        if level_timer >= level_duration:
            level_timer = 0
            level += 1
            if level > 10:
                level = 10
            for target in targets:
                target.speed += 1
                target.bullet_speed += 0.5

            for _ in range(level):
                new_target = Target(player, speed_multiplier=1 + (level - 1) * 0.1, bullet_speed=bullet_speed + (level - 1) * 0.5)
                all_sprites.add(new_target)
                targets.add(new_target)

        health_item_timer -= 1
        if health_item_timer <= 0:
            health_item_timer = random.randint(300, 600)
            health_item = HealthItem()
            all_sprites.add(health_item)
            health_items.add(health_item)

        if pygame.sprite.spritecollide(player, enemy_bullets, True) and not player.is_invincible:
            player.health -= 10
            player.hit_timer = 10
            hit_sound.play()
            if player.health <= 0:
                running = False

        for bullet in bullets:
            hit_targets = pygame.sprite.spritecollide(bullet, targets, True)
            for target in hit_targets:
                bullet.kill()
                score += 10

                kill_sound.play()

                kill_banner_visible = True
                kill_banner_timer = 170  # 2초 동안 표시

                new_target = Target(player, speed_multiplier=1 + (level - 1) * 0.1, bullet_speed=bullet_speed + (level - 1) * 0.5)
                all_sprites.add(new_target)
                targets.add(new_target)

        if kill_banner_visible:
            kill_banner_timer -= 1
            if kill_banner_timer <= 0:
                kill_banner_visible = False

        # 레벨에 따라 배경 이미지 변경
        screen.blit(background_images[level - 1], (0, 0))

        all_sprites.draw(screen)
        player.draw(screen)

        # 마우스 커서 그리기
        mx, my = pygame.mouse.get_pos()
        screen.blit(mouse_image, (mx - mouse_image.get_width() // 2, my - mouse_image.get_height() // 2))

        if kill_banner_visible:
            banner_rect = kill_banner_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(kill_banner_image, banner_rect)

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        health_text = font.render(f"Health: {player.health}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        mode_text = font.render(
            "Sniper Mode: ON" if player.is_sniper_mode else (
                "Shotgun Mode: ON" if player.is_shotgun_mode else "Shotgun Mode: OFF, Sniper Mode: OFF"),
            True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (SCREEN_WIDTH - 150, 10))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 50, 50))
        screen.blit(mode_text, (SCREEN_WIDTH // 2 - 150, 90))

        pygame.display.flip()
        clock.tick(60)

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    game_over_screen(score, high_score)

def game_over_screen(final_score, high_score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 36)
    game_over_text = font.render("Game Over", True, RED)
    final_score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, GREEN)
    restart_text = font.render("Press 'R' to Restart", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 100))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_restart = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                    waiting_for_restart = False

# 게임 시작
game_loop()
