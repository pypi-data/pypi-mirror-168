from PIL import Image, ImageFont

from src.icon_writer import get_text_size, find_font_size, write_icon


def test_get_text_size():
    text = "AZURE"
    image = Image.new("RGB", (80, 80))
    font = ImageFont.truetype("assets/OpenSans-Bold.ttf", 100)
    assert get_text_size(text, image, font) == (325, 108)


def test_find_font_size():
    text = "AZURE"
    font_family = "assets/OpenSans-Bold.ttf"
    image = Image.new("RGB", (80, 80))
    width_ratio = 0.7
    assert find_font_size(text, font_family, image, width_ratio) == 17


def test_write_icon():
    image = write_icon("hi")
    assert image.size == (80, 80)
    assert image.getpixel((0, 0)) == (255, 255, 255)
    assert image.getpixel((20, 35)) == (0, 0, 0)
