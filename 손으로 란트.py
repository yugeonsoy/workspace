import matplotlib.pyplot as plt
from PIL import Image
import cairosvg

def svg_to_png(svg_path, png_path):
    """
    SVG 파일을 PNG 파일로 변환합니다.
    """
    cairosvg.svg2png(url=svg_path, write_to=png_path)

def display_image(image_path):
    """
    PNG 파일을 Matplotlib을 사용하여 표시합니다.
    """
    img = Image.open(image_path)
    plt.figure(figsize=(10, 5))
    plt.imshow(img)
    plt.axis('off')  # 축 숨기기
    plt.title('발로란트의 고스트', fontsize=16, fontweight='bold')
    plt.show()

# SVG 파일 경로와 PNG로 변환할 파일 경로 설정
svg_path = 'path_to_your_ghost_image.svg'  # SVG 파일 경로를 여기에 입력하세요.
png_path = 'ghost_image.png'  # PNG로 저장할 파일 경로

# SVG를 PNG로 변환하고 Matplotlib으로 표시합니다.
svg_to_png(svg_path, png_path)
display_image(png_path)
