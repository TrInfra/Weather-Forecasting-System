import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
import os

# Função para obter informações meteorológicas da API OpenWeatherMap
def get_weather(city):
    API_key = "98b128222d1a47e7a82229c17d4fe396"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Erro", "Cidade não encontrada")
        return None

    weather = res.json()

    # Verifica se as chaves necessárias estão presentes na resposta
    if 'weather' not in weather or 'main' not in weather or 'sys' not in weather:
        messagebox.showerror("Erro", "Resposta inválida da API")
        return None

    # Normaliza a descrição do tempo para facilitar o mapeamento
    description = weather['weather'][0]['description'].lower().replace(' ', '_')
    temperature = weather['main']['temp'] - 273.15  # Converte de Kelvin para Celsius
    city_name = weather['name']
    country = weather['sys']['country']

    # Retorna a descrição, temperatura, nome da cidade e país
    return description, temperature, city_name, country

# Função para obter o ícone apropriado com base na descrição do tempo
def get_icon(description):
    # Caminho para o diretório de ícones
    base_dir = os.path.dirname(__file__)
    icon_dir = os.path.join(base_dir, "icons")

    # Define o caminho para o ícone com base na descrição
    icon_path = os.path.join(icon_dir, f"{description}.png")

    # Verifica se o arquivo do ícone existe, caso contrário, usa um padrão (default)
    if not os.path.exists(icon_path):
        icon_path = os.path.join(icon_dir, "default.png")

    # Retorna o caminho do arquivo de ícone
    return icon_path

# Função para buscar as informações meteorológicas para uma cidade
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    
    # Descompacta os resultados da função get_weather
    description, temperature, city_name, country = result
    location_label.configure(text=f"{city_name}, {country}")

    # Obtém o caminho do ícone com base na descrição
    icon_path = get_icon(description)

    # Carrega e redimensiona o ícone do tempo
    try:
        icon_image = Image.open(icon_path).convert("RGBA")
        icon_image = icon_image.resize((100, 100), Image.LANCZOS)  # Redimensiona usando LANCZOS
        icon = ImageTk.PhotoImage(icon_image)
        icon_label.configure(image=icon)
        icon_label.image = icon
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Ícone não encontrado: {icon_path}")

    # Atualiza as labels de temperatura e descrição com os dados atuais
    temperature_label.configure(text=f"Temperatura: {temperature:.0f} °C")
    description_label.configure(text=f"Descrição: {description.replace('_', ' ').capitalize()}")

# Configura a janela principal

root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

# Widget de entrada -> para inserir o nome da cidade
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# Botão -> para buscar as informações meteorológicas
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Label -> para mostrar o nome da cidade/país
location_label = tk.Label(root, font="Helvetica, 25", bg='white')
location_label.pack(pady=20)

# Label -> para mostrar o ícone do tempo
icon_label = tk.Label(root, bg='white')
icon_label.pack()

# Label -> para mostrar a temperatura
temperature_label = tk.Label(root, font="Helvetica, 20", bg='white')
temperature_label.pack()

# Label -> para mostrar a descrição do tempo
description_label = tk.Label(root, font="Helvetica, 20", bg='white')
description_label.pack()

root.mainloop()
