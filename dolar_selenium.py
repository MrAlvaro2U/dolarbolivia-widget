from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime
import os

def obtener_precio_con_selenium():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://www.dolarbluebolivia.click"
    driver.get(url)

    driver.implicitly_wait(10)  # Esperar que cargue el precio

    try:
        # Obtener el precio usando ID correcto
        precio_texto = driver.find_element(By.ID, "usdRate").text.strip()
        precio_dolar = float(precio_texto.replace(',', '.').replace('Bs', '').strip())
        return precio_dolar
    finally:
        driver.quit()

def guardar_json(precio):
    data = {
        "precio_dolar_compra": precio,
        "fuente": "https://www.dolarbluebolivia.click",
        "actualizado": datetime.utcnow().isoformat()
    }

    with open("dolarbolivia.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    historial_path = "historial_dolarbolivia.json"
    if os.path.exists(historial_path):
        with open(historial_path, "r") as f:
            historial = json.load(f)
    else:
        historial = []

    historial.append(data)

    with open(historial_path, "w") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    try:
        precio = obtener_precio_con_selenium()
        guardar_json(precio)
        print(f"✅ Precio de compra guardado: Bs {precio}")
    except Exception as e:
        print("❌ Error:", e)
