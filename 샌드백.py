import pygame
import time

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hit the Sandbag")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 설정
FONT = pygame.font.Font(None, 74)
SCORE_FONT = pygame.font.Font(None, 36)
TIME_LIMIT = 10  # 제한 시간 (초)

# 샌드백 클래스
class Sandbag(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 300))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def take_damage(self, damage):
        self.rect.y += damage // 10  # 피해량에 따라 샌드백이 점점 아래로 내려가는 효과

# 게임 초기화
def init_game():
    sandbag = Sandbag()
    all_sprites = pygame.sprite.Group(sandbag)
    score = 0
    start_time = time.time()
    return sandbag, all_sprites, score, start_time

# 게임 루프
def game_loop():
    clock = pygame.time.Clock()
    sandbag, all_sprites, score, start_time = init_game()
    running = True
    game_over = False

    while running:
        SCREEN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    score += 1
                    sandbag.take_damage(5)  # 스페이스바를 누를 때마다 피해 증가

        # 제한 시간 확인
        elapsed_time = time.time() - start_time
        if elapsed_time >= TIME_LIMIT:
            game_over = True

        # 게임 오버 후 메시지 표시
        if game_over:
            game_over_text = FONT.render("Time's Up!", True, BLACK)
            SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))

            score_text = SCORE_FONT.render(f"Total Damage: {score}", True, BLACK)
            SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        # 샌드백 및 스프라이트 그리기
        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# 게임 시작
game_loop()