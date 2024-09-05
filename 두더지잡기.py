import pygame
import random
import time

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("두더지잡기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 두더지 클래스
class Mole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)))

    def reset_position(self):
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))

# 게임 루프
def game_loop():
    mole = Mole()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(mole)

    clock = pygame.time.Clock()
    score = 0
    game_duration = 30  # 게임 시간 30초
    start_time = time.time()

    running = True

    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > game_duration:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mole.rect.collidepoint(event.pos):
                    score += 1
                    mole.reset_position()

        all_sprites.update()

        screen.fill(WHITE)
        all_sprites.draw(screen)

        # 점수 표시
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # 남은 시간 표시
        time_left = max(0, int(game_duration - elapsed_time))
        time_text = font.render(f"Time Left: {time_left}s", True, BLACK)
        screen.blit(time_text, (SCREEN_WIDTH - 200, 10))

        pygame.display.flip()
        clock.tick(60)

    # 게임 오버 화면
    screen.fill(WHITE)
    game_over_text = font.render("Game Over!", True, BLACK)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    pygame.time.wait(3000)  # 3초 동안 게임 오버 화면을 보여줍니다.

    pygame.quit()

# 게임 시작
game_loop()
