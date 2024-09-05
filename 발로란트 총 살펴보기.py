from PIL import Image, ImageSequence
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import pygame
import random
from matplotlib import font_manager, rc
from matplotlib.animation import FuncAnimation
import imageio

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 경우 '맑은 고딕' 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 이미지 및 오디오 파일 경로 설정
image_paths_page1 = ["your_image_1.png", "your_image_2.png", "your_image_3.png", "your_image_4.png"]
audio_paths_page1 = ["your_audio_1.mp3", "your_audio_2.mp3", "your_audio_3.mp3", "your_audio_4.mp3"]
labels_page1 = [
    "스펙트럼 팬텀",
    "2023챔피언스 밴달",
    "2021챔피언스 밴달",
    "2022챔피언스 밴달"
]

image_paths_page2 = ["your_image_5.png", "your_image_6.png", "your_image_7.png", "your_image_8.png"]  # 8번째 이미지 추가
audio_paths_page2 = [
    ["your_audio_5.mp3"], 
    ["your_audio_6.mp3"], 
    ["your_audio_7.mp3"],
    ["your_audio_8_1.mp3", "your_audio_8_2.mp3", "your_audio_8_3.mp3", "your_audio_8_4.mp3", "your_audio_8_5.mp3"]  # 8번째 이미지에 대해 5개의 오디오 파일 추가
]
labels_page2 = [
    "2021 자세히보기",
    "2022 자세히보기",
    "추가된 이미지",
    "5개의 노래 재생 이미지"  # 8번째 이미지에 대한 라벨
]

pages = [
    (image_paths_page1, audio_paths_page1, labels_page1),
    (image_paths_page2, audio_paths_page2, labels_page2)
]

current_page = 0
background_colors = ['#ffcccc', '#ccffcc', '#ccccff', '#ffffcc']
border_color = '#FFD700'
current_background_color = random.choice(background_colors)

for page in pages:
    for path_group in page[0] + [item for sublist in page[1] for item in sublist]:
        if not os.path.exists(path_group):
            print(f"파일을 찾을 수 없습니다: {path_group}")
            exit()

pygame.mixer.init()

def load_page(page_index):
    global images, audio_paths, labels
    image_paths, audio_paths, labels = pages[page_index]
    images = [Image.open(path) for path in image_paths]

load_page(current_page)

is_playing = [False] * len(image_paths_page2)
patches_list = [None] * len(image_paths_page2)
audio_index = [0] * len(image_paths_page2)  # 각 이미지에 대해 현재 재생 중인 오디오 인덱스 추적

def on_click(event):
    global is_playing, patches_list, audio_index
    if event.inaxes in axes:
        index = list(axes).index(event.inaxes)
        if is_playing[index]:
            pygame.mixer.music.stop()
            is_playing[index] = False
            audio_index[index] = 0  # 오디오 인덱스 초기화
            if patches_list[index] is not None:
                patches_list[index].remove()
                patches_list[index] = None
            fig.patch.set_facecolor(current_background_color)
            fig.canvas.draw()
        else:
            play_audio_sequence(index)
            is_playing[index] = True
            patches_list[index] = patches.Rectangle((-2, -2), images[index].size[0]+4, images[index].size[1]+4, linewidth=3, edgecolor=border_color, facecolor='none')
            axes[index].add_patch(patches_list[index])
            fig.patch.set_facecolor(current_background_color)
            fig.canvas.draw()
            play_animation(event.inaxes, index)

def play_audio_sequence(index):
    global audio_index, is_playing
    if audio_index[index] < len(audio_paths[index]):
        pygame.mixer.music.load(audio_paths[index][audio_index[index]])
        pygame.mixer.music.play()
        audio_index[index] += 1
        pygame.mixer.music.set_endevent(pygame.USEREVENT + index)  # 오디오 끝 이벤트 설정
    else:
        is_playing[index] = False
        audio_index[index] = 0

def next_page(event):
    global current_page, current_background_color
    if event.inaxes == next_button.ax:
        current_page = (current_page + 1) % len(pages)
        load_page(current_page)
        current_background_color = random.choice(background_colors)
        update_page()

def prev_page(event):
    global current_page, current_background_color
    if event.inaxes == prev_button.ax:
        current_page = (current_page - 1) % len(pages)
        load_page(current_page)
        current_background_color = random.choice(background_colors)
        update_page()

def update_page():
    global patches_list, audio_index
    for ax in axes:
        ax.clear()
    
    for ax in axes:
        ax.set_visible(False)

    for i, (ax, img, label) in enumerate(zip(axes, images, labels)):
        ax.imshow(img)
        ax.axis('off')
        ax.text(0.5, -0.1, label, transform=ax.transAxes, ha='center', va='top', fontsize=16, color='black')
        ax.set_visible(True)
        patches_list[i] = None
        audio_index[i] = 0

    fig.patch.set_facecolor(current_background_color)
    fig.canvas.draw()

def play_animation(ax, index):
    # 애니메이션 GIF 파일을 열어 이미지 위에 오버레이
    gif_path = 'path_to_your_animation.gif'  # 애니메이션 GIF 파일 경로
    gif = Image.open(gif_path)
    
    def update(frame):
        ax.clear()  # 기존 내용 지우기
        img = ImageSequence.Iterator(gif).__next__()  # 다음 프레임 얻기
        ax.imshow(img)
        ax.axis('off')
        return ax,

    ani = FuncAnimation(fig, update, frames=range(len(list(ImageSequence.Iterator(gif)))), interval=100, blit=False, repeat=True)
    plt.draw()

fig, axs = plt.subplots(2, 2, figsize=(20, 20), dpi=300)
axes = axs.flatten()

button_ax_prev = plt.axes([0.1, 0.02, 0.1, 0.05])
button_ax_next = plt.axes([0.8, 0.02, 0.1, 0.05])
prev_button = plt.Button(button_ax_prev, 'Previous Page')
next_button = plt.Button(button_ax_next, 'Next Page')

prev_button.on_clicked(prev_page)
next_button.on_clicked(next_page)

fig.canvas.mpl_connect('button_press_event', on_click)

pygame.mixer.music.set_endevent(pygame.USEREVENT)

# pygame 이벤트 루프에서 재생 끝 처리
def event_handler():
    for event in pygame.event.get():
        if event.type >= pygame.USEREVENT:
            index = event.type - pygame.USEREVENT
            play_audio_sequence(index)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

update_page()

while True:
    event_handler()
    plt.pause(0.01)
