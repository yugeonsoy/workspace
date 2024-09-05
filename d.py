from PIL import Image, ImageDraw

# 1. 부엌 배경 (간단한 벽과 바닥으로 구성된 배경)
def create_kitchen_background():
    width, height = 800, 600
    image = Image.new("RGBA", (width, height), (200, 200, 200, 255))  # 회색 배경
    draw = ImageDraw.Draw(image)
    
    # 바닥
    draw.rectangle([0, height * 0.7, width, height], fill=(150, 150, 150, 255))
    
    return image

# 2. 냄비 이미지
def create_pot():
    width, height = 400, 300
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 투명 배경
    draw = ImageDraw.Draw(image)
    
    # 냄비 몸체
    draw.rectangle([50, 100, 350, 250], fill=(100, 100, 100, 255), outline=(50, 50, 50, 255), width=5)
    # 손잡이
    draw.rectangle([0, 140, 50, 210], fill=(80, 80, 80, 255))
    draw.rectangle([350, 140, 400, 210], fill=(80, 80, 80, 255))
    
    return image

# 3. 라면 이미지
def create_noodle():
    width, height = 200, 100
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 투명 배경
    draw = ImageDraw.Draw(image)
    
    # 라면 면 모양
    draw.ellipse([0, 0, width, height], fill=(255, 200, 0, 255))
    draw.line([0, 50, width, 50], fill=(255, 180, 0, 255), width=5)
    
    return image

# 4. 스프 이미지
def create_seasoning():
    width, height = 100, 100
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 투명 배경
    draw = ImageDraw.Draw(image)
    
    # 스프 패킷
    draw.rectangle([10, 10, 90, 90], fill=(200, 0, 0, 255), outline=(150, 0, 0, 255), width=5)
    draw.line([10, 10, 90, 90], fill=(255, 255, 255, 255), width=2)
    draw.line([90, 10, 10, 90], fill=(255, 255, 255, 255), width=2)
    
    return image

# 5. 불 이미지
def create_fire():
    width, height = 400, 150
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 투명 배경
    draw = ImageDraw.Draw(image)
    
    # 불꽃 모양
    draw.polygon([(200, 0), (150, 75), (250, 75)], fill=(255, 100, 0, 255))
    draw.polygon([(150, 50), (100, 125), (200, 125)], fill=(255, 150, 0, 255))
    draw.polygon([(250, 50), (300, 125), (200, 125)], fill=(255, 150, 0, 255))
    
    return image

# 6. 물 끓는 상태 이미지
def create_water():
    width, height = 400, 300
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 투명 배경
    draw = ImageDraw.Draw(image)
    
    # 물결 모양
    draw.ellipse([50, 100, 350, 250], fill=(0, 150, 255, 150))
    draw.arc([50, 100, 350, 250], start=180, end=360, fill=(0, 100, 200, 255), width=5)
    
    return image

# 이미지 저장
create_kitchen_background().save("kitchen_background.png")
create_pot().save("pot.png")
create_noodle().save("noodle.png")
create_seasoning().save("seasoning.png")
create_fire().save("fire.png")
create_water().save("water.png")
