import subprocess
import os
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI

client = OpenAI(api_key='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')
import requests
def get_quotes(subject, num_quotes=100):
    # Set your OpenAI API key

    # Initialize an empty list to store the quotes
    quotes = []



    response = client.completions.create(model="davinci-002",prompt=f"Generate 10 quotes about '{subject}':",
    max_tokens=150, 
 
   )

 
    print(response.choices[0].text.strip().split("\n"))
    # Return the list of quotes
    return quotes.extend(response.choices[0].text.strip().split("\n")) # Return only the required number of quotes

# Example usage:
subject = "programming"  # Change this to your desired subject
quotes = get_quotes(subject)
print(quotes)


def delete_wallpaper():
    current_wallpaper_path = subprocess.run(["osascript", "-e", "tell application \"Finder\" to get POSIX path of (get desktop picture as alias)"], capture_output=True, text=True).stdout.strip()
    if current_wallpaper_path != wallpaper:
        os.remove(current_wallpaper_path)

def set_wallpaper(image_path):
    script = f'tell application \"Finder\"  to set desktop picture to POSIX file "{image_path}"'
    try:
        subprocess.run(['osascript', '-e', script], check=True)
        print("Wallpaper set successfully!")
    except subprocess.CalledProcessError as e:
        print("Error setting wallpaper:", e)

def add_quote_to_image(image_path, quote, corner="bottom-right"):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font_size = 46  # Change this to adjust the font size
    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size) 


    text_bbox = draw.textbbox((0, 0), quote, font=font)

    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    image_width, image_height = image.size

    # Determine position based on corner
    if corner == "top-left":
        position = (10, 10)
    elif corner == "top-right":
        position = (image_width - text_width - 10, 10)
    elif corner == "bottom-left":
        position = (10, image_height - text_height - 10)
    elif corner == "bottom-right":
        position = (image_width - text_width - 70, image_height - text_height - 480)
    else:
        raise ValueError("Invalid corner specified")



    draw.text((position), quote, fill=(255, 255, 255), font=font)
    new_image_path = os.path.splitext(image_path)[0] + "_quote.jpg"
    image.save(new_image_path)
    return new_image_path
# Example usage
wallpaper = '/Users/edenphillips/Downloads/056 (1).jpg'
quote = "“I have told you these thine world.”"
chosen_corner = "bottom-right"  # Change this to the desired corner
new_image_path = add_quote_to_image(wallpaper, quote, corner=chosen_corner)
set_wallpaper(new_image_path)
