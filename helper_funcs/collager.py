from PIL import Image, ImageFont, ImageDraw
import os

    
def write_text(path: str, info: str) -> str:
    image = Image.open(path)
    line_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # Draw a horizontal line on the blank image
    draw = ImageDraw.Draw(line_image)
    line_color = (0, 0, 0, 200)  # Black color with low opacity
    line_width = 95
    line_position = (500, 405, 0, 405)
    draw.line(line_position, fill=line_color, width=line_width)

    # Paste the line image onto the original image with low opacity
    image.paste(line_image, (0, 0), line_image)
    text_draw = ImageDraw.Draw(line_image)
    boldFont = ImageFont.truetype('seguisb.ttf', 24)
    Font = ImageFont.truetype('segoeui.ttf', 18)
    if info.get("character"):
        text_draw.text(xy=(image.width/2, 385), text=info["name"], font=boldFont, fill =(255, 255, 255), anchor="ms")
        text_draw.text(xy=(image.width/2, 410), text=info["job"], font=Font, fill =(255, 255, 255), anchor="ms")
        text_draw.text(xy=(image.width/2, 435), text=info["character"], font=Font, fill =(255, 255, 255), anchor="ms")
    else:
        text_draw.text(xy=(image.width/2, 395), text=info["name"], font=boldFont, fill =(255, 255, 255), anchor="ms")
        text_draw.text(xy=(image.width/2, 435), text=info["job"], font=Font, fill =(255, 255, 255), anchor="ms")
    output_path = os.path.join(os.path.dirname(path), "{}-{}.jpg".format(info["name"], info["job"]))
    image.paste(line_image, (0, 0), line_image)
    image.save(output_path)
    os.remove(path)
    return output_path