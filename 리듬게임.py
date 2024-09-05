import pygame
import random

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Friday Night Pygame")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 방향키 맵핑
ARROW_KEYS = {
    pygame.K_LEFT: 'left',
    pygame.K_DOWN: 'down',
    pygame.K_UP: 'up',
    pygame.K_RIGHT: 'right',
}

ARROW_COLORS = {
    'left': RED,
    'down': GREEN,
    'up': BLUE,
    'right': YELLOW,
}

# 노트 클래스
class Note(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
        self.image = pygame.Surface((50, 50))
        self.image.fill(ARROW_COLORS[direction])
        self.rect = self.image.get_rect(midtop=(self.get_start_pos(direction), 0))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # 화면 밖으로 나가면 노트 제거

    def get_start_pos(self, direction):
        return {
            'left': SCREEN_WIDTH * 0.25,
            'down': SCREEN_WIDTH * 0.4,
            'up': SCREEN_WIDTH * 0.6,
            'right': SCREEN_WIDTH * 0.75,
        }[direction]

# 게임 루프
def game_loop():
    all_sprites = pygame.sprite.Group()
    notes = pygame.sprite.Group()
    clock = pygame.time.Clock()
    score = 0
    note_timer = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in ARROW_KEYS:
                    direction = ARROW_KEYS[event.key]
                    for note in notes:
                        if note.direction == direction and SCREEN_HEIGHT - 100 <= note.rect.bottom <= SCREEN_HEIGHT - 50:
                            note.kill()  # 노트 제거
                            score += 1  # 점수 증가
                            break

        # 노트 생성
        note_timer += 1
        if note_timer > 30:  # 노트 생성 주기 조정
            direction = random.choice(list(ARROW_KEYS.values()))
            note = Note(direction)
            all_sprites.add(note)
            notes.add(note)
            note_timer = 0

        # 스프라이트 업데이트
        all_sprites.update()

        # 화면 그리기
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # 점수 표시
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # 판정선 그리기
        pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - 75), (SCREEN_WIDTH, SCREEN_HEIGHT - 75), 5)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# 게임 시작
game_loop()
