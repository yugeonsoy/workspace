import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slot Machine Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 폰트 설정 (작게 조정)
font = pygame.font.SysFont(None, 36)  # 폰트 크기를 36으로 조정

# 슬롯 심볼 설정
symbols = ['CHERRY', 'LEMON', 'BELL', 'DIAMOND', 'SEVEN']

# 슬롯머신 릴 클래스
class Reel:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.symbol = random.choice(symbols)

    def spin(self):
        self.symbol = random.choice(symbols)

    def draw(self, screen):
        text = font.render(self.symbol, True, BLACK)
        screen.blit(text, (self.rect.x + self.rect.width // 2 - text.get_width() // 2, self.rect.y + self.rect.height // 2 - text.get_height() // 2))

# 게임 루프
def game_loop():
    reels = [Reel(150, 150), Reel(250, 150), Reel(350, 150)]
    result = ""
    rolling = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 슬롯머신 버튼 클릭 감지
                if 250 < mouse_pos[0] < 350 and 320 < mouse_pos[1] < 370:
                    for reel in reels:
                        reel.spin()
                    rolling = True
                    # 슬롯 결과 확인
                    if reels[0].symbol == reels[1].symbol == reels[2].symbol:
                        result = "WIN!"
                    else:
                        result = "TRY AGAIN"

        # 화면 그리기
        SCREEN.fill(WHITE)

        # 슬롯 릴 그리기
        for reel in reels:
            reel.draw(SCREEN)

        # 결과 표시
        if rolling:
            result_text = font.render(result, True, RED if result == "WIN!" else BLACK)
            SCREEN.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, 300))

        # 슬롯머신 버튼
        pygame.draw.rect(SCREEN, GREEN, (250, 320, 100, 50))
        button_text = font.render("SPIN", True, WHITE)
        SCREEN.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2, 325))

        pygame.display.flip()

    pygame.quit()

# 게임 시작
game_loop()
