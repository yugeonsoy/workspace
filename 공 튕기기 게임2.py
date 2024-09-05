import pygame
import random
import time
import os

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Click the Ball Game")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 공 클래스
class Ball:
    def __init__(self):
        self.size = 50
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = random.randint(0, SCREEN_HEIGHT - self.size)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def draw(self):
        pygame.draw.ellipse(SCREEN, RED, self.rect)
    
    def move(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = random.randint(0, SCREEN_HEIGHT - self.size)
        self.rect.topleft = (self.x, self.y)

# 최고 기록을 읽어오는 함수
def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            return int(file.read().strip())
    return 0

# 최고 기록을 저장하는 함수
def save_high_score(score):
    high_score = load_high_score()
    if score > high_score:
        with open("high_score.txt", "w") as file:
            file.write(str(score))

# 게임 종료 화면
def game_over_screen(score):
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        high_score = score

    SCREEN.fill(WHITE)
    font = pygame.font.SysFont(None, 74)
    message = f"Game Over! Your Score: {score}"
    text = font.render(message, True, (0, 0, 0))
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 50))
    
    font_small = pygame.font.SysFont(None, 36)
    high_score_text = font_small.render(f"High Score: {high_score}", True, (0, 0, 0))
    SCREEN.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    
    pygame.display.flip()
    time.sleep(3)  # 3초 동안 화면을 유지

# 메인 게임 루프
def game_loop():
    clock = pygame.time.Clock()
    ball = Ball()
    score = 0
    start_time = time.time()
    
    running = True
    while running:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 30:
            running = False
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ball.rect.collidepoint(event.pos):
                    score += 1
                    ball.move()

        SCREEN.fill(WHITE)
        ball.draw()
        
        # 점수와 남은 시간 표시
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        time_left = 30 - int(elapsed_time)
        timer_text = font.render(f"Time Left: {time_left}", True, (0, 0, 0))
        
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(timer_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    # 게임 종료 후 점수 및 최고 기록 표시
    game_over_screen(score)
    pygame.quit()

# 게임 시작
if __name__ == "__main__":
    game_loop()
