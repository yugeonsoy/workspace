import os
import pygame
import random
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager, rc

# Pygame 초기화
pygame.init()

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 이미지 및 오디오 파일 경로 설정
image_paths_page1 = [
    r"C:\workspace\your_image_1.png",
    r"C:\workspace\your_image_2.png",
    r"C:\workspace\your_image_3.png",
    r"C:\workspace\your_image_4.png"
]
audio_paths_page1 = [
    [r"C:\workspace\your_audio_1.mp3"],
    [r"C:\workspace\your_audio_2.mp3"],
    [r"C:\workspace\your_audio_3.mp3"],
    [r"C:\workspace\your_audio_4.mp3"]
]

image_paths_page2 = [
    r"C:\workspace\your_image_5.png",
    r"C:\workspace\your_image_6.png",
    r"C:\workspace\your_image_7.png",
    r"C:\workspace\your_image_8.png"
]
audio_paths_page2 = [
    [r"C:\workspace\your_audio_5.mp3"],
    [r"C:\workspace\your_audio_6.mp3"],
    [r"C:\workspace\your_audio_7.mp3"],
    [
        r"C:\workspace\your_audio_8_1.mp3", 
        r"C:\workspace\your_audio_8_2.mp3", 
        r"C:\workspace\your_audio_8_3.mp3", 
        r"C:\workspace\your_audio_8_4.mp3", 
        r"C:\workspace\your_audio_8_5.mp3"
    ]
]
labels_page1 = [
    "스펙트럼 팬텀",
    "2023챔피언스 밴달",
    "2021챔피언스 밴달",
    "2022챔피언스 밴달"
]
labels_page2 = [
    "2021 자세히보기",
    "2022 자세히보기",
    "스펙트럼 마무리",
    "약탈자 밴달"
]

pages = [
    (image_paths_page1, audio_paths_page1, labels_page1),
    (image_paths_page2, audio_paths_page2, labels_page2)
]

current_page = 0
background_colors = ['#ffcccc', '#ccffcc', '#ccccff', '#ffffcc']
border_color = '#FFD700'
current_background_color = random.choice(background_colors)

# 파일 경로 확인 및 디버깅
for page in pages:
    for image_path in page[0]:
        if not os.path.exists(image_path):
            print(f"파일을 찾을 수 없습니다: {image_path}")
            exit()
        else:
            print(f"파일을 찾았습니다: {image_path}")
    for audio_group in page[1]:
        for audio_path in audio_group:
            if not os.path.exists(audio_path):
                print(f"파일을 찾을 수 없습니다: {audio_path}")
                exit()
            else:
                print(f"파일을 찾았습니다: {audio_path}")

pygame.mixer.init()

def load_page(page_index):
    global images, audio_paths, labels
    image_paths, audio_paths, labels = pages[page_index]
    images = [Image.open(path) for path in image_paths]

load_page(current_page)

is_playing = [False] * len(images)
patches_list = [None] * len(images)
audio_index = [0] * len(images)

def on_click(event):
    global is_playing, patches_list, audio_index
    if event.inaxes in axes:
        index = list(axes).index(event.inaxes)
        print(f"Image {index + 1} clicked, playing audio {audio_index[index] + 1}")
        if is_playing[index]:
            pygame.mixer.music.stop()
            is_playing[index] = False
            audio_index[index] = 0
            if patches_list[index] is not None:
                patches_list[index].remove()
                patches_list[index] = None
            fig.patch.set_facecolor(current_background_color)
            fig.canvas.draw()
        else:
            is_playing[index] = True
            play_audio_sequence(index)
            patches_list[index] = patches.Rectangle((-2, -2), images[index].size[0]+4, images[index].size[1]+4, linewidth=3, edgecolor=border_color, facecolor='none')
            axes[index].add_patch(patches_list[index])
            fig.patch.set_facecolor(current_background_color)
            fig.canvas.draw()

def play_audio_sequence(index):
    global audio_index, is_playing
    if audio_index[index] < len(audio_paths[index]):
        try:
            print(f"Loading audio file: {audio_paths[index][audio_index[index]]}")
            pygame.mixer.music.load(audio_paths[index][audio_index[index]])
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT + index)  # 이벤트 설정
        except pygame.error as e:
            print(f"오류 발생: {e} - 파일을 찾을 수 없습니다: {audio_paths[index][audio_index[index]]}")
    else:
        is_playing[index] = False
        audio_index[index] = 0

def check_audio_events():
    for event in pygame.event.get():
        if event.type >= pygame.USEREVENT:
            index = event.type - pygame.USEREVENT
            if is_playing[index] and audio_index[index] < len(audio_paths[index]):
                audio_index[index] += 1
                play_audio_sequence(index)
            else:
                is_playing[index] = False
                audio_index[index] = 0

def stop_audio(index):
    pygame.mixer.music.stop()
    is_playing[index] = False
    audio_index[index] = 0
    if patches_list[index] is not None:
        patches_list[index].remove()
        patches_list[index] = None
    fig.patch.set_facecolor(current_background_color)
    fig.canvas.draw()

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
    global patches_list
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

    fig.patch.set_facecolor(current_background_color)
    fig.canvas.draw()

fig, axs = plt.subplots(2, 2, figsize=(20, 20), dpi=300)
axes = axs.flatten()

# 버튼 위치 조정
button_ax_prev = plt.axes([0.05, 0.02, 0.1, 0.05])  # 이전 페이지 버튼을 왼쪽으로 이동
button_ax_next = plt.axes([0.85, 0.02, 0.1, 0.05])  # 다음 페이지 버튼을 오른쪽으로 이동
prev_button = plt.Button(button_ax_prev, 'Previous Page')
next_button = plt.Button(button_ax_next, 'Next Page')

prev_button.on_clicked(prev_page)
next_button.on_clicked(next_page)

fig.canvas.mpl_connect('button_press_event', on_click)

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

# 메인 루프에서 오디오 이벤트를 처리
while True:
    check_audio_events()
    plt.pause(0.01)
