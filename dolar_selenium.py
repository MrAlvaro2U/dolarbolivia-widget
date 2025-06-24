from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
from datetime import datetime
import os

# Configurar navegador sin interfaz
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Iniciar navegador
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Ir a la página
driver.get("https://www.dolarbluebolivia.click")

# Esperar que cargue el precio
driver.implicitly_wait(10)

# Obtener el precio
precio_texto = driver.find_element(By.CLASS_NAME, "exchange-rate").text.strip()
precio_dolar = float(precio_texto.replace(',', '.'))

# Fuente y hora
fuente = driver.current_url
ahora = datetime.utcnow().isoformat()

# Guardar solo el último precio
data = {
    "precio_dolar_compra": precio_dolar,
    "fuente": fuente,
    "actualizado": ahora
}
with open("dolarbolivia.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Manejo del historial
historial_path = "historial_dolarbolivia.json"

if os.path.exists(historial_path):
    with open(historial_path, "r") as f:
        historial = json.load(f)
else:
    historial = []

historial.append(data)

with open(historial_path, "w") as f:
    json.dump(historial, f, indent=2, ensure_ascii=False)

# Cerrar navegador
driver.quit()
