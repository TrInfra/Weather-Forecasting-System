import tkinter as tk
import requests
import ttkbootstrap
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

# Function to fetch weather information from the OpenWeatherMap API
def get_weather(city):
    API_key = "98b128222d1a47e7a82229c17d4fe396"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    weather = res.json()

    # Check if necessary keys are present in the API response
    if 'weather' not in weather or 'main' not in weather or 'sys' not in weather:
        messagebox.showerror("Error", "Invalid API response")
        return None

    # Normalize weather description for easier mapping
    description = weather['weather'][0]['description'].lower().replace(' ', '_')
    temperature = weather['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
    city_name = weather['name']
    country = weather['sys']['country']

    # Return description, temperature, city name, and country
    return description, temperature, city_name, country

# Function to get the appropriate weather icon based on description and time of day
def get_icon(description):
    # Determine time of day based on local time
    current_time = datetime.now().time()
    time_of_day = "day" if current_time >= datetime.strptime("06:00:00", "%H:%M:%S").time() and current_time <= datetime.strptime("18:00:00", "%H:%M:%S").time() else "night"

    # Path to the icons directory
    base_dir = os.path.dirname(__file__)
    icon_dir = os.path.join(base_dir, "icons")

    # Define path to the icon based on description and time of day
    icon_path = os.path.join(icon_dir, f"{description}_{time_of_day}.png")

    # Check if the icon file exists, otherwise use a default icon
    if not os.path.exists(icon_path):
        icon_path = os.path.join(icon_dir, f"default_{time_of_day}.png")

    # Return the path to the icon file
    return icon_path

# Function to search for weather information for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    
    # Unpack the results from get_weather function
    description, temperature, city_name, country = result
    location_label.configure(text=f"{city_name}, {country}")

    # Get the icon path based on description and time of day
    icon_path = get_icon(description)

    # Load and resize the weather icon
    try:
        icon_image = Image.open(icon_path).convert("RGBA")
        icon_image = icon_image.resize((110, 100), Image.LANCZOS)  # Resize using LANCZOS
        icon = ImageTk.PhotoImage(icon_image)
        icon_label.configure(image=icon)
        icon_label.image = icon
    except FileNotFoundError:
        messagebox.showerror("Error", f"Icon not found: {icon_path}")

    # Update temperature and description labels with current data
    temperature_label.configure(text=f"Temperature: {temperature:.0f} °C")
    description_label.configure(text=f"Description: {description.replace('_', ' ').capitalize()}")

# Configure the main window
root = ttkbootstrap.Window(themename="superhero")
root.title("Weather App")
root.geometry("400x400")

# Entry widget to enter the city name
city_entry = tk.Entry(root, font="Helvetica 18")
city_entry.pack(pady=10)

# Button to search for weather information
search_button = tk.Button(root, text="Search", command=search)
search_button.pack(pady=10)

# Label to display city/country name
location_label = tk.Label(root, font="Helvetica 25")
location_label.pack(pady=20)

# Label to display weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label to display temperature
temperature_label = tk.Label(root, font="Helvetica 20")
temperature_label.pack()

# Label to display weather description
description_label = tk.Label(root, font="Helvetica 20")
description_label.pack()

root.mainloop()
