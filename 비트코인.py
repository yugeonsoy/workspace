import pygame
import random
import time
import os

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bitcoin Trading Simulation")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 초기 비트코인 가격 및 소지금 설정
bitcoin_price = 50000  # 시작 가격
cash = 100000  # 시작 소지금
btc_owned = 0  # 보유 비트코인 수
total_assets = cash  # 전체 자산 (소지금 + 비트코인 가격)
price_change_interval = 5  # 5초 간격
last_update_time = time.time()

# 소지금 저장 파일
cash_file = "cash.txt"

# 소지금 불러오기
def load_cash():
    global cash
    if os.path.exists(cash_file):
        with open(cash_file, 'r') as file:
            cash = int(file.read())
    else:
        cash = 100000  # 기본 소지금

# 소지금 저장
def save_cash():
    with open(cash_file, 'w') as file:
        file.write(str(cash))

# 게임 루프
def game_loop():
    global bitcoin_price, cash, btc_owned, total_assets, last_update_time

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # 'B' 키를 누르면 비트코인 구매
                if event.key == pygame.K_b:
                    if cash >= bitcoin_price:  # 소지금이 가격 이상일 때
                        cash -= bitcoin_price
                        btc_owned += 1
                # 'S' 키를 누르면 비트코인 판매
                if event.key == pygame.K_s:
                    if btc_owned > 0:  # 비트코인이 있을 때
                        cash += bitcoin_price
                        btc_owned -= 1

        # 가격 변경 (5초마다)
        current_time = time.time()
        if current_time - last_update_time >= price_change_interval:
            price_change = random.randint(-10000, 10000)  # -10000 ~ +3000 달러 범위에서 랜덤 변화
            
            # 비트코인 가격이 최소 3000 상승 또는 하락하도록 조정
            if price_change < -10000:  # 하락폭이 3000 이하일 경우
                price_change = -10000
            elif price_change > 10000:  # 상승폭이 10000 초과일 경우
                price_change = 10000

            bitcoin_price += price_change
            last_update_time = current_time

        # 전체 자산 계산
        total_assets = cash + (btc_owned * bitcoin_price)

        # 화면 그리기
        SCREEN.fill(WHITE)

        # 비트코인 가격 및 소지금, 보유 비트코인 수, 전체 자산 표시
        price_text = font.render(f"BTC Price: ${bitcoin_price}", True, BLACK)
        cash_text = font.render(f"Cash: ${cash}", True, BLACK)
        btc_text = font.render(f"BTC Owned: {btc_owned}", True, BLACK)
        assets_text = font.render(f"Total Assets: ${total_assets}", True, GREEN)

        SCREEN.blit(price_text, (SCREEN_WIDTH // 2 - price_text.get_width() // 2, 50))
        SCREEN.blit(cash_text, (SCREEN_WIDTH // 2 - cash_text.get_width() // 2, 100))
        SCREEN.blit(btc_text, (SCREEN_WIDTH // 2 - btc_text.get_width() // 2, 150))
        SCREEN.blit(assets_text, (SCREEN_WIDTH // 2 - assets_text.get_width() // 2, 200))

        # 조작 안내 텍스트
        instructions_text = font.render("Press 'B' to Buy, 'S' to Sell", True, BLACK)
        SCREEN.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, 250))

        pygame.display.flip()

        # 화면 업데이트 속도 조절
        pygame.time.Clock().tick(30)

    save_cash()  # 게임 종료 시 소지금을 저장
    pygame.quit()

# 초기 소지금 불러오기
load_cash()

# 게임 시작
game_loop()
