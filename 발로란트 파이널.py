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
shotgun_sound = pygame.mixer.Sound("shotgun_sound.wav")  # 샷건 소리 파일
kill_banner_image = pygame.image.load("kill_banner.png")  # 킬 배너 PNG 파일
kill_banner_visible = False  # 킬 배너 표시 여부
kill_banner_timer = 0  # 킬 배너 지속 시간

# 총과 산탄총 이미지 로드 및 크기 조정
gun_image = pygame.image.load("gun.png")
shotgun_image = pygame.image.load("shotgun.png")
gun_image = pygame.transform.scale(gun_image, (100, 40))  # 총 크기를 100px로 조정 (높이: 30px)
shotgun_image = pygame.transform.scale(shotgun_image, (170, 50))  # 산탄총 크기를 100px로 조정 (높이: 30px)

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

# 게임 루프
def game_loop():
    global all_sprites, enemy_bullets, targets, player, kill_banner_visible, kill_banner_timer

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

    # 쿨다운 변수를 추가합니다.
    shotgun_cooldown = 0
    normal_cooldown = 0  # 일반 총의 쿨타임 변수

    # 산탄총 속도
    shotgun_speed = 10  # 산탄총의 속도
    normal_speed = 30  # 일반 총의 속도

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
                    angle = math.degrees(math.atan2(my - player.rect.centery, mx - player.rect.centerx))

                    # 쿨다운이 끝나면 총알 발사
                    if player.is_shotgun_mode:  # 산탄총 모드일 때
                        if shotgun_cooldown <= 0:
                            # 산탄총 발사
                            bullet_count = 5  # 발사할 총알 수
                            spread_angle = 10  # 각도 차이

                            for i in range(bullet_count):
                                bullet_angle = angle + (spread_angle * (i - bullet_count // 2))
                                bullet = Bullet(player.rect.center, bullet_angle, speed=shotgun_speed)  # 산탄총 속도
                                all_sprites.add(bullet)
                                bullets.add(bullet)
                            shotgun_sound.play()  # 샷건 소리 재생
                            shotgun_cooldown = 180  # 산탄총 쿨다운 3초

                    else:  # 일반 총 발사
                        if normal_cooldown <= 0:
                            bullet = Bullet(player.rect.center, angle, speed=normal_speed)  # 일반 총 속도
                            all_sprites.add(bullet)
                            bullets.add(bullet)
                            gun_sound.play()  # 일반 총 소리 재생
                            normal_cooldown = 60  # 일반 총 쿨다운

        keys = pygame.key.get_pressed()
        if keys[pygame.K_2]:
            player.is_shotgun_mode = not player.is_shotgun_mode  # 산탄총 모드 토글

        # 총알 업데이트
        all_sprites.update()

        # 쿨다운 감소
        if shotgun_cooldown > 0:
            shotgun_cooldown -= 1
        if normal_cooldown > 0:
            normal_cooldown -= 1

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

                # 킬 사운드 재생
                kill_sound.play()

                # 킬 배너 표시
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
        all_sprites.draw(screen)
        player.draw(screen)  # 플레이어 그리기

        # 점수와 체력 표시
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        health_text = font.render(f"Health: {player.health}", True, BLACK)
        mode_text = font.render("Shotgun Mode: ON" if player.is_shotgun_mode else "Shotgun Mode: OFF", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (SCREEN_WIDTH - 150, 10))
        screen.blit(mode_text, (SCREEN_WIDTH // 2 - 100, 10))

        # 킬 배너 표시
        if kill_banner_visible:
            banner_rect = kill_banner_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(kill_banner_image, banner_rect)

        pygame.display.flip()
        clock.tick(60)

    # 종료 화면 표시
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 36)
    game_over_text = font.render("Game Over", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)  # 3초간 종료 화면 유지

    pygame.quit()

# 게임 시작
game_loop()
