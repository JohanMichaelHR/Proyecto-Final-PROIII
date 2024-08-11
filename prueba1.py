from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Configuración
nombre_prueba = "prueba1_abrir_netflix"

# Obtén el directorio actual donde se ejecuta el script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Define las rutas absolutas para las capturas y el reporte
path_capturas = os.path.join(directorio_actual, "resultados", "capturas", nombre_prueba)
os.makedirs(path_capturas, exist_ok=True)

path_reporte = os.path.join(directorio_actual, "resultados", "reportes", f"reporte_{nombre_prueba}.txt")

# Lista para registrar los resultados
report = []

def take_screenshot(step_name):
    try:
        screenshot_path = os.path.join(path_capturas, f"{step_name}.png")
        driver.save_screenshot(screenshot_path)
        report.append(f"Step '{step_name}' passed, screenshot saved at {screenshot_path}")
    except Exception as e:
        report.append(f"Step '{step_name}' failed: {str(e)}")

# Inicializa el WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Abre Netflix
    driver.get("https://www.netflix.com/")
    take_screenshot("01_abrir_netflix")
    
    # Aquí puedes agregar más pasos, como iniciar sesión, navegar por el contenido, etc.
    
except Exception as e:
    report.append(f"An error occurred during automation: {str(e)}")

finally:
    driver.quit()

    # Guarda el reporte en un archivo de texto
    with open(path_reporte, 'w') as f:
        for line in report:
            f.write(line + "\n")

    print(f"Automation completed. Report saved to '{path_reporte}'.")
