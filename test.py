import pygame
import random
import math
import os

# 초기화
pygame.init()

# 전체화면 모드로 설정
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Shooting Game with Revival")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 소리 로드
kill_sound = pygame.mixer.Sound("kill_sound.wav")  # 적 처치 사운드 파일
gun_sound = pygame.mixer.Sound("gun_sound.wav")  # 일반 총 소리 파일
shotgun_sound = pygame.mixer.Sound("shotgun_sound.wav")  # 샷건 소리 파일
sniper_sound = pygame.mixer.Sound("sniper_sound.wav")  # 스나이퍼 소리 파일
hit_sound = pygame.mixer.Sound("hit_sound.wav")  # 플레이어가 맞았을 때의 효과음
revive_sound = pygame.mixer.Sound("revive_sound.wav")  # 부활 사운드 파일
kill_banner_image = pygame.image.load("kill_banner.png")  # 킬 배너 PNG 파일
kill_banner_visible = False  # 킬 배너 표시 여부
kill_banner_timer = 0  # 킬 배너 지속 시간
kill_banner_player = None  # 어느 플레이어가 킬 배너를 띄웠는지

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
gun_image = pygame.image.load("gun.png")
shotgun_image = pygame.image.load("shotgun.png")
sniper_image = pygame.image.load("sniper.png")
knife_image = pygame.image.load("knife.png")  # 플레이어 2의 칼 이미지
gun_image = pygame.transform.scale(gun_image, (100, 40))  # 총 크기를 100px로 조정 (높이: 30px)
shotgun_image = pygame.transform.scale(shotgun_image, (170, 50))  # 산탄총 크기를 170px로 조정 (높이: 50px)
sniper_image = pygame.transform.scale(sniper_image, (200, 50))  # 스나이퍼 크기를 200px로 조정 (높이: 50px)
knife_image = pygame.transform.scale(knife_image, (60, 20))  # 칼 크기 조정

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, color, controls, start_position):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=start_position)
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
        self.hit_timer = 0  # 플레이어가 맞았을 때 색을 변경할 타이머
        self.is_invincible = False  # 무적 상태
        self.invincibility_timer = 0  # 무적 지속 시간
        self.q_skill_cooldown = 0  # Q 스킬 쿨타임
        self.controls = controls  # 조작 키를 저장
        self.is_dead = False  # 플레이어 사망 여부
        self.revive_timer = 0  # 부활 타이머

    def update(self):
        if self.is_dead:
            return

        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0

        if keys[self.controls["left"]]:
            move_x = -self.speed
        if keys[self.controls["right"]]:
            move_x = self.speed
        if keys[self.controls["up"]]:
            move_y = -self.speed
        if keys[self.controls["down"]]:
            move_y = self.speed

        if not self.is_dashing:
            self.rect.x += move_x
            self.rect.y += move_y

            # 대시 스킬
            if keys[self.controls["dash"]] and self.dash_cooldown == 0:
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
        if self.q_skill_cooldown > 0:
            self.q_skill_cooldown -= 1

        # E 스킬 사용
        if "skill_e" in self.controls and keys[self.controls["skill_e"]] and self.e_skill_cooldown == 0:
            self.health += 30  # E 스킬 사용 시 체력 30 회복
            if self.health > 100:  # 최대 체력 제한
                self.health = 100
            self.e_skill_cooldown = 1200  # E 스킬 쿨타임 10초 (60 FPS 기준)

        # F 스킬: 시간 멈춤
        if "skill_f" in self.controls and keys[self.controls["skill_f"]] and self.f_skill_cooldown == 0 and not self.is_time_stopped:
            self.is_time_stopped = True
            self.time_stop_timer = self.time_stop_duration
            self.f_skill_cooldown = 600  # F 스킬 쿨다운 10초 (60 FPS 기준)

        if self.is_time_stopped:
            self.time_stop_timer -= 1
            if self.time_stop_timer <= 0:
                self.is_time_stopped = False

        # Q 스킬: 무적
        if "skill_q" in self.controls and keys[self.controls["skill_q"]] and self.q_skill_cooldown == 0:
            self.is_invincible = True
            self.invincibility_timer = 120  # 무적 지속 시간 2초 (120 프레임)
            self.q_skill_cooldown = 480  # Q 스킬 쿨다운 8초 (480 프레임)

        if self.is_invincible:
            self.invincibility_timer -= 1
            self.image.fill(GREEN)  # 무적일 때 색상을 변경
            if self.invincibility_timer <= 0:
                self.is_invincible = False
                self.image = self.original_image.copy()

        # 맞았을 때의 색상 변경 처리
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if not self.is_invincible:  # 무적 상태가 아닐 때만 색상을 빨간색으로 변경
                self.image.fill(RED)
        elif not self.is_invincible:
            self.image = self.original_image.copy()

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

        # 마우스 위치에 따라 총을 회전 (플레이어 1만)
        if "skill_f" in self.controls or "skill_e" in self.controls:
            mx, my = pygame.mouse.get_pos()
            angle = math.degrees(math.atan2(my - self.rect.centery, mx - self.rect.centerx))  # 마우스와의 각도 계산

            if self.is_sniper_mode:
                rotated_gun = pygame.transform.rotate(sniper_image, -angle)  # 각도에 따라 총 이미지 회전
            elif self.is_shotgun_mode:
                rotated_gun = pygame.transform.rotate(shotgun_image, -angle)  # 각도에 따라 총 이미지 회전
            else:
                rotated_gun = pygame.transform.rotate(gun_image, -angle)  # 각도에 따라 총 이미지 회전

            gun_rect = rotated_gun.get_rect(center=self.rect.center)
            screen.blit(rotated_gun, gun_rect.topleft)

# 칼 공격 클래스 (플레이어 2 전용)
class KnifeAttack(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = knife_image
        self.rect = self.image.get_rect(center=player.rect.center)
        self.player = player

    def update(self):
        # 칼의 방향 설정 및 플레이어 위치에 따라 이동
        self.rect.center = self.player.rect.center
        if pygame.sprite.spritecollide(self, targets, True):  # 적과 충돌하면 제거
            global kill_banner_visible, kill_banner_timer, kill_banner_player
            kill_sound.play()
            self.kill()
            kill_banner_visible = True
            kill_banner_timer = 170  # 2초 동안 표시
            kill_banner_player = self.player  # 어느 플레이어가 킬 배너를 띄웠는지

    def draw(self, screen):
        # 플레이어 위에 칼을 그리기 위해 draw 메서드 추가
        screen.blit(self.image, self.rect.topleft)

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
        if not player1.is_time_stopped:
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
        self.shoot_delay = random.randint(60, 120)  # 목표물의 발사 간격 조정 (프레임 단위)
        self.shoot_timer = 0
        self.bullet_speed = bullet_speed

    def update(self):
        if not player1.is_time_stopped:
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
        bullet = Bullet(self.rect.center, angle, color=BLACK, speed=self.bullet_speed)  # 목표물의 총알 속도
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
        # 플레이어와 충돌하면 체력 회복 및 아이템 제거
        if pygame.sprite.collide_rect(self, player1):
            player1.health += 10
            if player1.health > 100:  # 체력 최대치 100으로 제한
                player1.health = 100
            self.kill()
        elif pygame.sprite.collide_rect(self, player2):
            player2.health += 10
            if player2.health > 100:  # 체력 최대치 100으로 제한
                player2.health = 100
            self.kill()

# 게임 루프
def game_loop():
    global all_sprites, enemy_bullets, targets, player1, player2, kill_banner_visible, kill_banner_timer, kill_banner_player

    player1_controls = {
        "up": pygame.K_i,
        "down": pygame.K_k,
        "left": pygame.K_j,
        "right": pygame.K_l,
        "dash": pygame.K_b,
        "skill_e": pygame.K_o,
        "skill_f": pygame.K_p,
        "skill_q": pygame.K_u,
    }

    player2_controls = {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "dash": pygame.K_LSHIFT,
    }

    player1 = Player(BLUE, player1_controls, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    player2 = Player(YELLOW, player2_controls, (2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1, player2)

    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    health_items = pygame.sprite.Group()  # 체력 아이템 그룹 추가
    knives = pygame.sprite.Group()  # 플레이어 2의 칼 공격 그룹 추가

    level = 1
    level_duration = 1800  # 30초마다 레벨업 (60 FPS 기준)
    level_timer = 0
    health_item_timer = 300  # 체력 회복 아이템 생성 간격 타이머
    bullet_speed = 7  # 기본 적 총알 속도
    high_score = load_high_score()

    for _ in range(5):  # 5개의 목표물 생성
        target = Target(player1)
        all_sprites.add(target)
        targets.add(target)

    clock = pygame.time.Clock()
    running = True
    score = 0

    # 쿨다운 변수를 추가합니다.
    shotgun_cooldown = 0
    normal_cooldown = 0  # 일반 총의 쿨타임 변수
    sniper_cooldown = 0  # 스나이퍼 쿨다운 변수
    knife_cooldown = 0  # 칼 공격 쿨다운 변수
    revive_timer = 0  # 부활 타이머

    # 산탄총, 일반 총, 스나이퍼 속도
    shotgun_speed = 10  # 산탄총의 속도
    normal_speed = 20  # 일반 총의 속도
    sniper_speed = 50  # 스나이퍼의 속도

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC 키로 종료
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 마우스 버튼 클릭 시
                    mx, my = pygame.mouse.get_pos()
                    angle = math.degrees(math.atan2(my - player1.rect.centery, mx - player1.rect.centerx))

                    # 쿨다운이 끝나면 총알 발사
                    if player1.is_sniper_mode:  # 스나이퍼 모드일 때
                        if sniper_cooldown <= 0:
                            bullet = Bullet(player1.rect.center, angle, speed=sniper_speed)  # 스나이퍼 속도
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            sniper_sound.play()  # 스나이퍼 소리 재생
                            sniper_cooldown = 120  # 스나이퍼 쿨다운 2초 (120 프레임)

                    elif player1.is_shotgun_mode:  # 산탄총 모드일 때
                        if shotgun_cooldown <= 0:
                            # 산탄총 발사
                            bullet_count = 5  # 발사할 총알 수
                            spread_angle = 10  # 각도 차이

                            for i in range(bullet_count):
                                bullet_angle = angle + (spread_angle * (i - bullet_count // 2))
                                bullet = Bullet(player1.rect.center, bullet_angle, speed=shotgun_speed)  # 산탄총 속도
                                all_sprites.add(bullet)
                                bullets.add(bullet)
                            shotgun_sound.play()  # 샷건 소리 재생
                            shotgun_cooldown = 180  # 산탄총 쿨다운 3초

                    else:  # 일반 총 발사
                        if normal_cooldown <= 0:
                            bullet = Bullet(player1.rect.center, angle, speed=normal_speed)  # 일반 총 속도
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            gun_sound.play()  # 일반 총 소리 재생
                            normal_cooldown = 60  # 일반 총 쿨다운

        keys = pygame.key.get_pressed()

        # 플레이어 2 칼 공격 처리
        if keys[pygame.K_SPACE] and knife_cooldown <= 0 and not player2.is_dead:
            knife = KnifeAttack(player2)
            knives.add(knife)
            all_sprites.add(knife)
            knife_cooldown = 60  # 칼 공격 쿨다운 1초

        # 쿨다운 감소
        if shotgun_cooldown > 0:
            shotgun_cooldown -= 1
        if normal_cooldown > 0:
            normal_cooldown -= 1
        if sniper_cooldown > 0:
            sniper_cooldown -= 1
        if knife_cooldown > 0:
            knife_cooldown -= 1

        # 부활 처리
        if player2.is_dead and not player1.is_dead:
            if keys[pygame.K_e] and pygame.sprite.collide_rect(player1, player2):
                revive_timer += 1
                if revive_timer >= 180:  # 3초 동안 E 키를 눌러야 부활
                    player2.revive()
                    revive_sound.play()
                    revive_timer = 0
            else:
                revive_timer = 0

        # 총알 및 칼 공격 업데이트
        all_sprites.update()

        # 레벨업 처리
        level_timer += 1
        if level_timer >= level_duration:
            level_timer = 0
            level += 1
            if level > 10:
                level = 10  # 최대 레벨 10으로 고정
            for target in targets:
                target.speed += 1  # 레벨이 오를 때마다 목표물 속도 증가
                target.bullet_speed += 0.5  # 레벨이 오를 때마다 총알 속도 증가

            # 새로운 목표물 추가
            for _ in range(level):  # 레벨에 비례하여 새로운 목표물 생성
                new_target = Target(player1, speed_multiplier=1 + (level - 1) * 0.1, bullet_speed=bullet_speed + (level - 1) * 0.5)
                all_sprites.add(new_target)
                targets.add(new_target)

        # 체력 회복 아이템 생성
        health_item_timer -= 1
        if health_item_timer <= 0:
            health_item_timer = random.randint(300, 600)  # 무작위 간격으로 생성
            health_item = HealthItem()
            all_sprites.add(health_item)
            health_items.add(health_item)

        # 플레이어 1이 적의 총알에 맞았는지 확인
        if pygame.sprite.spritecollide(player1, enemy_bullets, True) and not player1.is_invincible:
            player1.health -= 10  # 맞을 때마다 체력 10 감소
            player1.hit_timer = 10  # 맞았을 때 색을 변경할 타이머 설정
            hit_sound.play()  # 맞을 때 효과음 재생
            if player1.health <= 0:
                running = False

        # 플레이어 2가 적의 총알에 맞았는지 확인
        if pygame.sprite.spritecollide(player2, enemy_bullets, True) and not player2.is_invincible and not player2.is_dead:
            player2.health -= 10  # 맞을 때마다 체력 10 감소
            player2.hit_timer = 10  # 맞았을 때 색을 변경할 타이머 설정
            hit_sound.play()  # 맞을 때 효과음 재생
            if player2.health <= 0:
                player2.die()

        # 목표물과 플레이어 1의 총알 충돌 감지
        for bullet in bullets:
            hit_targets = pygame.sprite.spritecollide(bullet, targets, True)
            for target in hit_targets:
                bullet.kill()
                score += 10

                # 킬 사운드 재생
                kill_sound.play()

                # 킬 배너 표시
                kill_banner_visible = True
                kill_banner_timer = 170  # 2초 동안 표시
                kill_banner_player = player1  # 플레이어 1이 킬 배너를 띄움

                # 새로운 목표물 생성
                new_target = Target(player1, speed_multiplier=1 + (level - 1) * 0.1, bullet_speed=bullet_speed + (level - 1) * 0.5)
                all_sprites.add(new_target)
                targets.add(new_target)

        # 킬 배너 타이머 감소
        if kill_banner_visible:
            kill_banner_timer -= 1
            if kill_banner_timer <= 0:
                kill_banner_visible = False

        screen.fill(WHITE)
        all_sprites.draw(screen)
        player1.draw(screen)  # 플레이어 1 그리기
        player2.draw(screen)  # 플레이어 2 그리기

        # 플레이어 2의 칼이 가려지지 않도록 draw 호출
        for knife in knives:
            knife.draw(screen)

        # 킬 배너 표시
        if kill_banner_visible:
            banner_rect = kill_banner_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(kill_banner_image, banner_rect)
            player_text = f"Player 1" if kill_banner_player == player1 else f"Player 2"
            font = pygame.font.SysFont(None, 36)
            player_name_text = font.render(player_text, True, BLACK)
            screen.blit(player_name_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 150))

        # 점수와 체력, 레벨, 최고 기록 표시
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        health_text1 = font.render(f"Player 1 Health: {player1.health}", True, BLACK)
        health_text2 = font.render(f"Player 2 Health: {player2.health}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text1, (SCREEN_WIDTH - 300, 10))
        screen.blit(health_text2, (SCREEN_WIDTH - 300, 40))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 50, 50))

        pygame.display.flip()
        clock.tick(60)

    # 게임 오버 시 최고 기록 갱신 여부 확인
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    game_over_screen(score, high_score)

# 종료 화면 및 다시 시작 기능
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
                    game_loop()  # 다시 시작
                    waiting_for_restart = False

# 게임 시작
game_loop()
