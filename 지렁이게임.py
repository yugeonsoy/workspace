import pygame
import time
import random

# 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# 화면 크기 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# 게임 속도 설정
SNAKE_SPEED = 15

# 지렁이와 먹이의 크기
SNAKE_BLOCK = 10

# 글꼴 설정
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# 점수 표시 함수
def display_score(score):
    value = score_font.render("Score: " + str(score), True, BLACK)
    SCREEN.blit(value, [0, 0])

# 지렁이 그리기 함수
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(SCREEN, RED, [x[0], x[1], snake_block, snake_block])

# 메시지 표시 함수
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    SCREEN.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])

# 게임 루프
def game_loop():
    game_over = False
    game_close = False

    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # 먹이 생성
    foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    while not game_over:
        while game_close:
            SCREEN.fill(BLUE)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # 벽 충돌 확인
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        SCREEN.fill(BLUE)
        pygame.draw.rect(SCREEN, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # 자기 자신과의 충돌 확인
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(SNAKE_BLOCK, snake_list)
        display_score(length_of_snake - 1)

        pygame.display.update()

        # 먹이를 먹었을 때
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            length_of_snake += 1

        pygame.time.Clock().tick(SNAKE_SPEED)

    pygame.quit()
    quit()

# 게임 시작
game_loop()
