from PIL import Image, ImageFont, ImageDraw


def get_text_size(text, image, font):
    im = Image.new("RGB", (image.width, image.height))
    draw = ImageDraw.Draw(im)
    return draw.textbbox((0, 0), text, font)[2:]


def find_font_size(text, font_family, image, target_width_ratio):
    tested_font_size = 100
    tested_font = ImageFont.truetype(font_family, tested_font_size)
    observed_width, observed_height = get_text_size(text, image, tested_font)
    estimated_font_size = tested_font_size / (observed_width / image.width) * target_width_ratio
    return round(estimated_font_size)


def write_icon(text, size=80, bgcolor="white", fontcolor="black"):
    """Add text over an image"""
    image = Image.new("RGB", (size, size), color=bgcolor)

    draw = ImageDraw.Draw(image)
    font_size = 2
    font_family = "assets/OpenSans-Bold.ttf"
    width_ratio = 0.9
    font_size = find_font_size(text, font_family, image, width_ratio)
    font = ImageFont.truetype(font_family, font_size)
    draw.text((size, size), text, font=font, fill=fontcolor, anchor="mm", align="center")
    return image
