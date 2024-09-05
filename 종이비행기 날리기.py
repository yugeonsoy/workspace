import pygame
import random
import math

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("종이비행기 날리기")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (173, 216, 230)
GREEN = (34, 139, 34)

# 종이비행기 클래스
class PaperPlane:
    def __init__(self, x, y):
        self.image = pygame.image.load("paper_plane.png")
        self.image = pygame.transform.scale(self.image, (60, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.speed = 0
        self.gravity = 0.5
        self.lift = 0.2

    def fly(self):
        # 비행기 각도 및 위치 계산
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(self.angle)) - self.gravity
        self.speed -= self.lift

        # 화면 밖으로 나가지 않도록 조정
        if self.rect.y >= SCREEN_HEIGHT - 50:
            self.rect.y = SCREEN_HEIGHT - 50
            self.speed = 0
        elif self.rect.y <= 0:
            self.rect.y = 0
            self.speed = 0

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        screen.blit(rotated_image, self.rect.topleft)

# 게임 루프
def game_loop():
    plane = PaperPlane(100, SCREEN_HEIGHT // 2)
    running = True
    is_flying = False
    score = 0
    high_score = 0

    while running:
        screen.fill(BLUE)
        pygame.draw.rect(screen, GREEN, pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))  # 땅

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not is_flying:
                # 마우스 클릭 시 비행기 발사
                plane.speed = random.randint(10, 20)
                plane.angle = random.randint(20, 60)
                is_flying = True

        if is_flying:
            plane.fly()
            score = plane.rect.x // 10  # 비행기가 이동한 거리를 점수로 계산

            if plane.rect.x >= SCREEN_WIDTH or plane.speed <= 0:
                is_flying = False
                if score > high_score:
                    high_score = score

                # 비행기 위치 초기화
                plane.rect.x = 100
                plane.rect.y = SCREEN_HEIGHT // 2
                plane.speed = 0
                plane.angle = 0

        plane.draw(screen)

        # 점수 표시
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

# 게임 시작
game_loop()
