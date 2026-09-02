from PIL import Image, ImageFont, ImageDraw
import os


def _fonts():
    try:
        return ImageFont.truetype('seguisb.ttf', 24), ImageFont.truetype('segoeui.ttf', 18)
    except OSError:
        return ImageFont.load_default(), ImageFont.load_default()


def write_text(path: str, info: dict) -> str:
    image = Image.open(path)
    line_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # Draw a horizontal band on the blank image
    draw = ImageDraw.Draw(line_image)
    line_color = (0, 0, 0, 200)  # Black with low opacity
    band_y = int(image.height * 0.9)
    band_h = 95
    draw.rectangle((0, band_y - band_h // 2, image.width, band_y + band_h // 2), fill=line_color)

    # Paste the band onto the original image with low opacity
    image.paste(line_image, (0, 0), line_image)
    text_draw = ImageDraw.Draw(line_image)
    boldFont, Font = _fonts()

    if info.get("character"):
        text_draw.text(xy=(image.width / 2, band_y - 20), text=info["name"], font=boldFont, fill=(255, 255, 255), anchor="ms")
        text_draw.text(xy=(image.width / 2, band_y + 5), text=info["job"], font=Font, fill=(255, 255, 255), anchor="ms")
        text_draw.text(xy=(image.width / 2, band_y + 30), text=info["character"], font=Font, fill=(255, 255, 255), anchor="ms")
    else:
        text_draw.text(xy=(image.width / 2, band_y - 10), text=info["name"], font=boldFont, fill=(255, 255, 255), anchor="ms")
        text_draw.text(xy=(image.width / 2, band_y + 30), text=info["job"], font=Font, fill=(255, 255, 255), anchor="ms")

    output_path = os.path.join(os.path.dirname(path), "{}-{}.jpg".format(info["name"], info["job"]))
    image.paste(line_image, (0, 0), line_image)
    image.save(output_path)
    os.remove(path)
    return output_path
