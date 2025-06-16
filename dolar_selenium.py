from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime
import re

def obtener_precio_con_selenium():
    options = Options()
    options.add_argument("--headless")  # Ejecutar sin abrir ventana del navegador
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://www.dolarbluebolivia.click"
    driver.get(url)

    # Esperar 5 segundos para que cargue el precio
    time.sleep(5)

    try:
        # Buscar el div con id 'usdRate'
        div_precio = driver.find_element(By.ID, "usdRate")
        texto = div_precio.text  # Ejemplo: "Bs 16.30"
        match = re.search(r"(\d{1,3}[.,]\d{1,2})", texto)
        if not match:
            raise Exception("No se pudo extraer el precio del texto")
        precio_str = match.group(1).replace(",", ".")
        precio = float(precio_str)
        return precio
    finally:
        driver.quit()

def guardar_json(precio):
    data = {
        "precio_dolar_compra": precio,
        "fuente": "https://www.dolarbluebolivia.click",
        "actualizado": datetime.now().isoformat()
    }
    with open("dolarbolivia.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    try:
        precio = obtener_precio_con_selenium()
        guardar_json(precio)
        print(f"✅ Precio de compra guardado: Bs {precio}")
    except Exception as e:
        print("❌ Error:", e)
