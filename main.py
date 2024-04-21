
import os
import random
import schedule
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
import tkinter as tk
from tkinter import PhotoImage
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

        # Adjust font size based on scaling factor
        font_size = int(base_font_size * font_scaling_factor)
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
        left, top, right, bottom = draw.textbbox((0,0),quote, font=font)
        text_width = right - left
        text_height = bottom - top
        image_width, image_height = image.size

        # Determine position based on chosen corners
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

    def handle_gui_input(self, root, wallpaper, topic, color, corner, time_freq):
        print('bef')
        self.wallpaper = wallpaper
        self.quote_topic = topic
        self.text_color = color
        self.chosen_corner = corner
        self.time_frequency = time_freq
        root.destroy()  # Destroy the window
        self.add_newlines()
        print('aft')
        # You can schedule here if needed
        while self.running:
            # schedule.run_pending()
            quote = random.choice(self.quotes_to_select_from)
            new_image_path = self.add_quote_to_image(quote)
            print(new_image_path)
            self.delete_wallpaper()
            self.set_wallpaper(new_image_path)
            time.sleep(20)

    def mount_widgets(self):
        popup = tk.Toplevel()  # Create a popup window
        popup.title("Quotify Desktop Setup")

        # Create a frame with padding
        frame = tk.Frame(popup, padx=60, pady=60)
        frame.pack()

        # Load the image
        title_image = PhotoImage(file="/Users/edenphillips/Desktop/Projects/Quotify_Desktop/Screenshot 2024-04-20 at 21.15.42 (1).png")

        # Create a label widget to display the image
        title_label = tk.Label(frame, image=title_image)
        title_label.grid(row=0, columnspan=2, pady=30)

        wallpaper_label = tk.Label(frame, text="Background Image Path:")
        wallpaper_label.grid(row=1, column=0, sticky="w")
        wallpaper_entry = tk.Entry(frame, width=40)
        wallpaper_entry.grid(row=1, column=1, pady=10)

        topic_label = tk.Label(frame, text="Topic or subject you would like the text to be on (motivation, maths equations, ancient sayings):")
        topic_label.grid(row=2, column=0, sticky="w")
        topic_entry = tk.Entry(frame, width=40)
        topic_entry.grid(row=2, column=1, pady=10)

        color_label = tk.Label(frame, text="Text Color (red, blue, green, random):")
        color_label.grid(row=3, column=0, sticky="w")
        color_entry = tk.Entry(frame, width=40)
        color_entry.grid(row=3, column=1, pady=10)

        corner_label = tk.Label(frame, text="Location of text on screen (top-left, top-right,\n bottom-left, bottom-right):")
        corner_label.grid(row=4, column=0, sticky="w")
        corner_entry = tk.Entry(frame, width=40)
        corner_entry.grid(row=4, column=1, pady=10)

        time_label = tk.Label(frame, text="Refresh Time (HH:MM):")
        time_label.grid(row=5, column=0, sticky="w")
        time_entry = tk.Entry(frame, width=40)
        time_entry.grid(row=5, column=1, pady=10)

        submit_button = tk.Button(frame, width=40, text="Start", command=lambda: self.handle_gui_input(
            popup,
            wallpaper_entry.get(),
            topic_entry.get(),
            color_entry.get(),
            corner_entry.get(),
            time_entry.get()
        ))
        submit_button.grid(row=6, columnspan=2, pady=20)

        popup.mainloop()

    def start(self):
        self.mount_widgets()

if __name__ == "__main__":
    app = DailyWallpaperChanger()
    app.start()