import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.gallito.com.uy/vacio-panoramico-posibilidad-de-rentar-garaje-inmuebles-23895956"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}

def is_valid_image_extension(url):
    # Verifica si la URL termina en alguna de las extensiones válidas
    return any(url.endswith(ext) for ext in [".jpg", ".jpeg", ".png"])

def download_images():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    img_tags = soup.find_all("img")

    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

    for img in img_tags:
        img_url = img.get("src", "")
        # Ignora las imágenes codificadas en base64 y verifica la extensión
        if img_url.startswith("http") and is_valid_image_extension(img_url):
            img_name = os.path.basename(img_url)
            with open(f"imagenes/{img_name}", "wb") as img_file:
                img_data = requests.get(img_url).content
                img_file.write(img_data)

if __name__ == "__main__":
    download_images()
    

# docker build -t scraper .
# docker run --name scraper -v "$(pwd)/imagenes:/app/imagenes" scraper python scraper.py