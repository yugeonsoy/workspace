import random
import pygame
import sys

# Pygame 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("검 강화 시스템")

# 폰트 설정
font = pygame.font.SysFont(None, 48)

# 입력된 텍스트 저장
input_box = pygame.Rect(300, 250, 200, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive  # 초기화
active = False
text = ''  # 초기화

def 강화_확률(단계):
    확률_목록 = [0.8, 0.65, 0.45, 0.3, 0.2]
    return 확률_목록[단계]

def 강화_검(검이름, 현재단계):
    if 현재단계 >= 5:
        return f"{검이름}의 강화 단계는 이미 최대입니다.", True
    
    성공확률 = 강화_확률(현재단계)
    if random.random() <= 성공확률:
        새로운단계 = 현재단계 + 1
        return f"검 강화 성공! (현재 검 등급: {검이름} {새로운단계}단계)", False
    else:
        return "검이 깨졌다 (강화 실패)", True

def main():
    global text, color  # 전역 변수로 사용
    현재단계 = 0
    강화종료 = False
    검이름 = ""  # 초기화

    # 게임 루프
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text:
                            검이름 = text  # 이름을 입력받은 후 변수에 저장
                            text = ''
                        else:
                            검이름 = "기본 검"  # 기본 이름 설정
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)

        if 강화종료:
            종료메시지 = font.render(f"{검이름} 강화 종료", True, RED)
            screen.blit(종료메시지, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
        else:
            현재단계_메시지 = font.render(f"현재 단계: {현재단계}단계", True, BLACK)

            if 검이름:  # 검이름이 비어있지 않을 때만 강화 결과 계산
                강화결과 = 강화_검(검이름, 현재단계)
                강화결과_메시지 = font.render(강화결과[0], True, GREEN if not 강화결과[1] else RED)
                screen.blit(강화결과_메시지, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 20))

                if 강화결과[1]:  # 강화 종료
                    강화종료 = True
                else:
                    현재단계 += 1  # 성공 시 단계 증가

            screen.blit(현재단계_메시지, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))

            # 텍스트 박스 표시
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

if __name__ == "__main__":
    main()
