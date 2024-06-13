Quotify Desktop is an application designed to automatically update your desktop wallpaper with quotes generated from a given input. Using the OpenAI API, it fetches quotes based on a specified topic and overlays them on a chosen background image at a scheduled time.

Features

Fetches quotes based on a user-defined topic using the OpenAI API.

Customizable text color and position on the wallpaper.

Automatic daily updates of the desktop wallpaper with new quotes.

Simple and intuitive GUI.

Usage

Clone the repository:

git clone https://github.com/F0xhopper/quotify-desktop
cd quotify-desktop

Install the required Python packages:

pip install -r requirements.txt

Set your OpenAI API key:

export OPENAI_API_KEY='your-api-key'

Run the application:

python quotify_desktop.py
