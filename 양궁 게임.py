import pygame
import math
import random
import os

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Archery Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# 설정
GRAVITY = 0.5
ARROW_SPEED = 15

# 활 클래스
class Bow:
    def __init__(self):
        self.angle = 0
        self.bow_length = 150

    def draw(self):
        bow_center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        end_x = bow_center[0] + self.bow_length * math.cos(math.radians(self.angle))
        end_y = bow_center[1] - self.bow_length * math.sin(math.radians(self.angle))
        pygame.draw.line(SCREEN, BROWN, bow_center, (end_x, end_y), 8)
        pygame.draw.line(SCREEN, BROWN, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 10), 10)

    def update_angle(self, mouse_y):
        self.angle = min(90, max(0, (SCREEN_HEIGHT // 2 - mouse_y) / 3))

# 화살 클래스
class Arrow:
    def __init__(self, angle, velocity):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.angle = angle
        self.velocity = velocity
        self.dx = velocity * math.cos(math.radians(angle))
        self.dy = -velocity * math.sin(math.radians(angle))

    def update(self):
        self.dx += 0  # 공기 저항은 무시
        self.dy += GRAVITY
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        arrow_length = 40
        arrow_x = self.x + arrow_length * math.cos(math.radians(self.angle))
        arrow_y = self.y - arrow_length * math.sin(math.radians(self.angle))
        pygame.draw.line(SCREEN, BLACK, (self.x, self.y), (arrow_x, arrow_y), 5)

# 과녁 클래스
class Target:
    def __init__(self):
        self.distance = random.randint(300, 600)
        self.x = SCREEN_WIDTH - self.distance
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.radius = 40

    def draw(self):
        pygame.draw.circle(SCREEN, RED, (self.x, self.y), self.radius)
        pygame.draw.circle(SCREEN, WHITE, (self.x, self.y), self.radius - 10)
        pygame.draw.circle(SCREEN, RED, (self.x, self.y), self.radius - 20)
        pygame.draw.circle(SCREEN, WHITE, (self.x, self.y), self.radius - 30)

    def check_hit(self, arrow):
        dist = math.sqrt((self.x - arrow.x) ** 2 + (self.y - arrow.y) ** 2)
        return dist < self.radius

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
    text = font.render(message, True, BLACK)
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 50))
    
    font_small = pygame.font.SysFont(None, 36)
    high_score_text = font_small.render(f"High Score: {high_score}", True, BLACK)
    SCREEN.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    
    pygame.display.flip()
    pygame.time.wait(3000)  # 3초 동안 화면을 유지

# 메인 게임 루프
def game_loop():
    clock = pygame.time.Clock()
    bow = Bow()
    arrow = None
    target = Target()
    score = 0
    is_drawing = False
    
    running = True
    while running:
        SCREEN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 마우스 버튼 눌림
                    is_drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 왼쪽 마우스 버튼 떼어짐
                    is_drawing = False
                    arrow = Arrow(bow.angle, ARROW_SPEED)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bow.update_angle(mouse_y)
        bow.draw()

        if arrow:
            arrow.update()
            arrow.draw()
            if target.check_hit(arrow):
                score += 1
                arrow = None
                target = Target()  # 새 과녁 생성
            elif arrow.x > SCREEN_WIDTH or arrow.y > SCREEN_HEIGHT or arrow.y < 0:
                arrow = None  # 화면을 넘어가면 화살을 제거

        target.draw()
        
        # 점수 표시
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

    # 게임 종료 후 점수 및 최고 기록 표시
    game_over_screen(score)
    pygame.quit()

# 게임 시작
if __name__ == "__main__":
    game_loop()
