import pygame
import sys
import json

# 초기화
pygame.init()

# 색상 정의
LIGHT_BLUE = (135, 206, 235)  # 하늘색

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("마인크래프트 스타일 2D 게임")

# 블록 클래스
class Block:
    def __init__(self, x, y, image):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.image = pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))  # 이미지 크기 조정

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)  # 이미지 그리기

# 이미지 로드 함수
def load_images():
    images = {
        'wood': pygame.image.load('wood.png'),
        'grass': pygame.image.load('grass.png'),
        'stone': pygame.image.load('stone.png'),
        'sand': pygame.image.load('sand.png'),
        'terracotta': pygame.image.load('terracotta.png'),
        'brick': pygame.image.load('brick.png'),
    }
    return images

# 게임 상황을 저장하는 함수
def save_game(blocks, filename='save.json'):
    with open(filename, 'w') as f:
        json.dump([{'x': block.rect.x, 'y': block.rect.y, 'type': block.image_name} for block in blocks], f)

# 게임 상황을 불러오는 함수
def load_game(images, filename='save.json'):
    blocks = []
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            for block_data in data:
                if 'type' in block_data:  # 'type' 키가 있는지 확인
                    block_type = block_data['type']
                    blocks.append(Block(block_data['x'], block_data['y'], images[block_type]))
                    blocks[-1].image_name = block_type  # 블록의 타입을 저장
                else:
                    print("블록 데이터에 'type' 키가 없습니다:", block_data)
    except FileNotFoundError:
        print("저장된 게임이 없습니다.")
    except json.JSONDecodeError:
        print("저장된 파일을 읽는 중 오류가 발생했습니다.")
    return blocks

# 게임 루프
def game_loop():
    images = load_images()  # 이미지 로드
    blocks = load_game(images)  # 저장된 게임을 불러옴
    current_block_image = images['wood']  # 현재 선택된 블록 이미지
    current_block_type = 'wood'  # 현재 선택된 블록 타입
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트
                x, y = event.pos
                grid_x = x // BLOCK_SIZE * BLOCK_SIZE
                grid_y = y // BLOCK_SIZE * BLOCK_SIZE

                if event.button == 1:  # 왼쪽 클릭: 블록 추가
                    blocks.append(Block(grid_x, grid_y, current_block_image))
                    blocks[-1].image_name = current_block_type  # 블록 타입 저장
                elif event.button == 3:  # 오른쪽 클릭: 블록 삭제
                    blocks = [block for block in blocks if block.rect.topleft != (grid_x, grid_y)]

            # 블록 선택
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # 나무
                    current_block_image = images['wood']
                    current_block_type = 'wood'
                elif event.key == pygame.K_2:  # 풀
                    current_block_image = images['grass']
                    current_block_type = 'grass'
                elif event.key == pygame.K_3:  # 돌
                    current_block_image = images['stone']
                    current_block_type = 'stone'
                elif event.key == pygame.K_4:  # 모래
                    current_block_image = images['sand']
                    current_block_type = 'sand'
                elif event.key == pygame.K_5:  # 테라코타
                    current_block_image = images['terracotta']
                    current_block_type = 'terracotta'
                elif event.key == pygame.K_6:  # 벽돌
                    current_block_image = images['brick']
                    current_block_type = 'brick'
                elif event.key == pygame.K_s:  # 게임 저장
                    save_game(blocks)
                elif event.key == pygame.K_l:  # 게임 불러오기
                    blocks = load_game(images)

        # 화면 그리기
        screen.fill(LIGHT_BLUE)  # 배경색
        for block in blocks:
            block.draw(screen)

        # UI 그리기
        font = pygame.font.Font(None, 36)
        text = font.render(f"현재 블록: {current_block_type}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        instructions = font.render("블록 추가: 왼쪽 클릭 | 블록 삭제: 오른쪽 클릭", True, (255, 255, 255))
        screen.blit(instructions, (10, 40))
        instructions2 = font.render("1: 나무 | 2: 풀 | 3: 돌 | 4: 모래 | 5: 테라코타 | 6: 벽돌", True, (255, 255, 255))
        screen.blit(instructions2, (10, 70))
        instructions3 = font.render("S: 게임 저장 | L: 게임 불러오기", True, (255, 255, 255))
        screen.blit(instructions3, (10, 100))

        pygame.display.flip()

# 게임 시작
game_loop()
