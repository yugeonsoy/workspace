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
pygame.display.set_caption("Obstacle Dodge Game")

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

# 설정
player_size = 50
obstacle_size = 60
obstacle_speed = 10  # 장애물 속도 증가
dash_speed = 30  # 대쉬 속도
dash_duration = 10  # 대쉬 지속 시간
score = 0
high_score = 0

# 플레이어 클래스
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_size - 10, player_size, player_size)
        self.is_dashing = False
        self.dash_count = 0

    def move(self, dx):
        if self.is_dashing:
            self.rect.x += dx * dash_speed
            self.dash_count += 1
            if self.dash_count >= dash_duration:
                self.is_dashing = False
                self.dash_count = 0
        else:
            self.rect.x += dx * obstacle_speed

        # 화면 밖으로 나가지 않도록 제한
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - player_size:
            self.rect.x = SCREEN_WIDTH - player_size

    def dash(self):
        if not self.is_dashing:
            self.is_dashing = True
            self.dash_count = 0

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

# 장애물 클래스
class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - obstacle_size), -obstacle_size, obstacle_size, obstacle_size)

    def fall(self):
        self.rect.y += obstacle_speed  # 장애물 속도 적용

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# 게임 루프
def game_loop():
    global score, high_score
    player = Player()
    obstacles = []
    score = 0
    game_over = False
    start_ticks = pygame.time.get_ticks()

    while True:
        SCREEN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1)
        if keys[pygame.K_RIGHT]:
            player.move(1)
        if keys[pygame.K_SPACE]:
            player.dash()

        # 장애물 생성
        if random.randint(1, 10) == 1:  # 약간의 확률로 장애물 생성
            obstacles.append(Obstacle())

        for obstacle in obstacles[:]:
            obstacle.fall()
            if obstacle.rect.y > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
                score += 1  # 장애물을 피하면 점수 증가

            if obstacle.rect.colliderect(player.rect):  # 충돌 검사
                game_over = True

        player.draw(SCREEN)
        for obstacle in obstacles:
            obstacle.draw(SCREEN)

        # 점수 표시
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        if game_over:
            # 게임 오버 처리
            if score > high_score:
                high_score = score
            game_over_text = font.render("Game Over!", True, RED)
            final_score_text = font.render(f"Final Score: {score}", True, BLACK)
            high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
            SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))
            SCREEN.blit(final_score_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            SCREEN.blit(high_score_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50))
            pygame.display.flip()
            pygame.time.delay(2000)  # 2초 대기 후 종료
            break  # 게임 종료

        pygame.display.flip()
        clock.tick(FPS)

# 게임 시작
game_loop()
