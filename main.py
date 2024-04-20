import os
import random
import schedule
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI

class DailyWallpaperChanger:
    def __init__(self):
        self.wallpaper = ''
        self.quote_topic = ''
        self.text_color = ''
        self.chosen_corner = ''
        self.time_frequency = '12:00'
        self.client = OpenAI(api_key='asd')
        self.quotes_to_select_from = [
    "Pythagorean Theorem: a^2 + b^2 = c^2", 
    "Quadratic Formula: x = (-b ± √(b² - 4ac)) / (2a)", 
    "Slope-intercept Form: y = mx + b", 
    "Area of a Circle: A = πr²", 
    "Volume of a Sphere: V = (4/3)πr³", 
    "Newton's Second Law of Motion: F = ma", 
    "Einstein's Mass-Energy Equivalence: E = mc²", 
    "Fundamental Theorem of Calculus: ∫(a to b) f(x) dx = F(b) - F(a)", 
    "Law of Cosines: c² = a² + b² - 2ab cos(C)", 
    "Normal Distribution Probability Density Function: f(x) = (1 / (σ√(2π))) e^(-((x - μ)² / (2σ²)))"
]

        self.running = True

    def add_newlines(self):
        result_list = []
        for string in self.quotes_to_select_from:
            # Split the string into words
            words = string.split()
            new_string = ''
            count = 0
            for word in words:
                new_string += word + ' '
                count += 1
                if count % 13 == 0:  # Add newline every end of 13th word
                    new_string += '\n'
            result_list.append(new_string)
        self.quotes_to_select_from = result_list

    def stop(self):
        self.running = False
        print("Wallpaper changer stopped.")

    def get_quotes(self, subject, num_quotes=10):
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Give 50 quotes on {subject}",
            max_tokens=550
        )
        for choice in response.choices:
            self.quotes_to_select_from.append(choice.text.strip())

    def delete_wallpaper(self):
        script = """
        tell application "System Events"
            tell current desktop
                set desktopPicture to picture
                return desktopPicture as text
            end tell
        end tell
        """
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
        current_path = result.stdout.strip()
            
     
        if os.path.exists(self.wallpaper) and os.path.exists(current_path) and current_path != self.wallpaper:
            os.remove(current_path)

    def set_wallpaper(self, image_path):
        script = f'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
        try:
            subprocess.run(['osascript', '-e', script], check=True)
            print("Wallpaper set successfully!")
        except subprocess.CalledProcessError as e:
            print("Error setting wallpaper:", e)

    def add_quote_to_image(self, quote):
        image = Image.open(self.wallpaper)
        draw = ImageDraw.Draw(image)
        base_font_size = 21  # Base font size
        font_scaling_factor = min(image.width, image.height) / 1000  # Adjust as needed

        # Adjust font size based on scaling factor/Users/edenphillips/Downloads/f4e56a94f2e39a593ab7b170129f1925.jpg
        font_size = int(base_font_size * font_scaling_factor)

        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size) 
        left, top, right, bottom = draw.textbbox((0,0),quote, font=font)
        text_width = right - left
        text_height = bottom - top
        image_width, image_height = image.size
        
        # Determine position based on chosen cornersdfg
        if self.chosen_corner == "top-left":
            position = (int(0.1 * image_width), int(0.1 * image_height))
        elif self.chosen_corner == "top-right":
            position = (int(0.9 * image_width) - text_width, int(0.1 * image_height))
        elif self.chosen_corner == "bottom-left":
            position = (int(0.1 * image_width), int(0.9 * image_height - text_height))
        elif self.chosen_corner == "bottom-right":
            position = (int(0.9 * image_width - text_width), int(0.9 * image_height - text_height))
        elif self.chosen_corner == 'random':
            position = random.choice([(int(0.1 * image_width), int(0.1 * image_height)),(int(0.9 * image_width) - text_width, int(0.1 * image_height)),(int(0.1 * image_width), int(0.9 * image_height - text_height)),(int(0.9 * image_width - text_width), int(0.9 * image_height - text_height))])
        
        if self.text_color == "random":
            fill = tuple(random.randint(0, 255) for _ in range(3))  # Generate a random RGB color
        else:
            fill = self.text_color 
        draw.text(position, quote, fill=(fill), font=font)
        new_image_path = os.path.splitext(self.wallpaper)[0] + f"_quote{random.randrange(1,50)}.jpg"
        image.save(new_image_path)
        return new_image_path

    def daily_task(self):
        # self.get_quotes("bible verses")  # Change subject as needed
        quote = random.choice(self.quotes_to_select_from)
        new_image_path = self.add_quote_to_image(quote)
        self.delete_wallpaper()
        self.set_wallpaper(new_image_path)

    def start(self):
        print("""  ___              _   _  __           ____            _    _              
    / _ \ _   _  ___ | |_(_)/ _|_   _    |  _ \  ___  ___| | _| |_ ___  _ __  
    | | | | | | |/ _ \| __| | |_| | | |   | | | |/ _ \/ __| |/ / __/ _ \| '_ \ 
    | |_| | |_| | (_) | |_| |  _| |_| |   | |_| |  __/\__ \   <| || (_) | |_) |
    \__\_\\__,_|\___/ \__|_|_|  \__, |___|____/ \___||___/_|\_\\__\___/| .__/ 
                                |___/_____|                            |_|    
    """)
        print('Hello, welcome to quotify_desktop we just need to setup a few of your prefrences before we start.')
        self.wallpaper = input('Please give the path of the background image you would like to use:')
        self.quote_topic = input('Please give the topic or subject would you like the quotes to be on:')
        self.text_color = input('Please give the color you would like the text to be (blue, red, green, white, random):')
        self.chosen_corner = input('Please give the location on the screen in which you would like the text (top-left, top-right, bottom-left, bottom-right, random):')
        self.time_frequency = input('Please give the time each day you would like to refresh the quote (00:00):')
        self.add_newlines()
        # schedule.every().day.at("19:39").do(self.daily_task)
        while self.running:
            # schedule.run_pending()
            quote = random.choice(self.quotes_to_select_from)
            new_image_path = self.add_quote_to_image(quote)
            self.delete_wallpaper()
            self.set_wallpaper(new_image_path)
            time.sleep(5)
# Example usage:
if __name__ == "__main__":
    app = DailyWallpaperChanger()
    app.start()
    stop_input = input("Type 'stop' to stop the wallpaper changer from running: ")
    if stop_input.lower() == "stop":
        app.stop()