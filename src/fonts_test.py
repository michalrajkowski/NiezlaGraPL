# draw_multiple_truetype.py

import glob
from PIL import Image, ImageDraw, ImageFont


def truetype(input_image_path, output_path):
    image = Image.open(input_image_path)
    draw = ImageDraw.Draw(image)
    y = 10
    font = ImageFont.truetype('fonts/GidoleFont/Gidole-Regular.ttf', size=42)
    draw.text((10, y), f"ASDASazdsad (font_size=44)", font=font)
    font = ImageFont.truetype('fonts/GidoleFont/Gidole-Regular.ttf', size=43)
    draw.text((10, y), f"ASDASazdsad (font_size=44)", font=font)
    y += 55
    image.show()

if __name__ == "__main__":
    truetype("assets/arts/gradient.png", "xd.jpg")