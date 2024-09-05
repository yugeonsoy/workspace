import pygame
import sys
import time

# 초기화
pygame.init()

# 화면 크기
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("공 튕기기 게임")

# 색상
sky_blue = (135, 206, 235)  # 하늘색
white = (255, 255, 255)

# 공 설정
ball_radius = 20
ball_x = width // 2
ball_y = height // 2
ball_dx = 7  # 공의 속도 증가
ball_dy = 7  # 공의 속도 증가

# 점수 및 시간 설정
score = 0
start_time = time.time()
time_limit = 30  # 제한 시간 (초)

# FPS 설정
clock = pygame.time.Clock()
fps = 60

# 게임 루프
while True:
    # 시간 계산
    elapsed_time = time.time() - start_time
    if elapsed_time > time_limit:
        print(f"게임 종료! 총 점수: {score}")
        pygame.quit()
        sys.exit()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 공이 클릭되었는지 확인
            distance = ((mouse_x - ball_x) ** 2 + (mouse_y - ball_y) ** 2) ** 0.5
            if distance <= ball_radius:
                score += 1

    # 공 위치 업데이트
    ball_x += ball_dx
    ball_y += ball_dy

    # 공이 화면의 가장자리에서 튕기도록 설정
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
        ball_dx = -ball_dx
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
        ball_dy = -ball_dy

    # 화면 색상 채우기 (하늘색)
    screen.fill(sky_blue)

    # 공 그리기
    pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)

    # 점수 표시
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"점수: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # 남은 시간 표시
    remaining_time = max(0, int(time_limit - elapsed_time))
    time_text = font.render(f"남은 시간: {remaining_time}", True, white)
    screen.blit(time_text, (10, 50))

    # 화면 업데이트
    pygame.display.flip()

    # FPS 조절
    clock.tick(fps)
