# Import required modules
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

# Function to get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = "98b128222d1a47e7a82229c17d4fe396"
    url = f"http://api.openweathermap.org/data/2.5/forecast?id={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox. showerror("Error", "City not found")
        return None

    # Parse the response JSON to get weather information
    weather = res.json()
    icon_id = weather['weather'] [0] ['icon']
    temperature = weather['main'] ['temp'] - 273.15
    description = weather['weather'] [0] ['description']
    city = weather['name' ]
    country = weather['sys'] ['country' ]

    # Get the icon URL and return all the weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return(icon_url, temperature, description, city, country)

# Function to seatch weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    #if the city is found, unpack  the  weather information
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    # Get the weather icon image from the URL and update the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # Update the temperature and description labels
    temperature_label. configure(text=f"Temperature: {temperature :. 2f} C")
    description_label.configure(text=f"Description: {description}")

root = ttkbootstrap.Window(themename="morph")
root. title("Weather App")
root.geometry("400x400")

# Entry widget -> to enter the city name
city_entry = ttkbootstrap. Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# Button widget -> to search for the weather informatIon
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Label widget -> to show the city/country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# Label widget -> to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget -> to show the temperature
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label. pack()

# Label widget -> = to show the weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()
