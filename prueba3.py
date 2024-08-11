from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Configuración específica para esta prueba
nombre_prueba = "prueba_03"
objetivo_prueba = "Verify that a registered user can log in successfully on Netflix, select the 'Johan' profile, and navigate to the 'Dramas' genre."

# Configuración de las rutas
directorio_actual = os.path.dirname(os.path.abspath(__file__))
path_capturas = os.path.join(directorio_actual, "resultados", "capturas", nombre_prueba)
os.makedirs(path_capturas, exist_ok=True)

path_reporte = os.path.join(directorio_actual, "resultados", "reportes", f"reporte_{nombre_prueba}.txt")
os.makedirs(os.path.dirname(path_reporte), exist_ok=True)

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
    # Descripción del objetivo de la prueba
    report.append(f"Objective of the test: {objetivo_prueba}")

    # 1. Abrir Netflix
    driver.get("https://www.netflix.com/")
    take_screenshot("01_open_netflix")

    # 2. Navegar a la página de inicio de sesión
    login_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.LINK_TEXT, "Sign In"))
    )
    login_link.click()
    take_screenshot("02_navigate_to_login")

    # 3. Ingresar correo electrónico
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='userLoginId']"))
    )
    email_field.send_keys("rodriguezjohanmichael@gmail.com")
    take_screenshot("03_enter_email")
    
    # 4. Ingresar contraseña
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
    )
    password_field.send_keys("J@han12345")
    take_screenshot("04_enter_password")

    # 5. Hacer clic en "Iniciar sesión"
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-uia='login-submit-button']"))
    )
    login_button.click()
    take_screenshot("05_click_login")

    # 6. Verificar que el inicio de sesión fue exitoso y tomar captura de la página de perfiles
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.profile-gate-label"))
    )
    take_screenshot("06_profiles_page")

    # 7. Seleccionar el perfil de Johan
    johan_profile = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Johan']"))
    )
    johan_profile.click()
    take_screenshot("07_select_johan_profile")

    # 8. Esperar a que la página principal de Netflix se cargue y tomar captura
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class*='mainView']"))
    )
    take_screenshot("08_main_content_page")

    # 9. Navegar a la página de Series
    series_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Series"))
    )
    series_tab.click()
    take_screenshot("09_navigate_to_series")

    # 10. Seleccionar "Géneros" desde la página de Series
    genres_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.nfDropDown.theme-lakira .label"))
    )
    genres_button.click()
    take_screenshot("10_click_genres")

    # 11. Esperar a que la lista de géneros se expanda y seleccionar "Dramas"
    dramas_genre = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Dramas']"))
    )
    dramas_genre.click()
    take_screenshot("11_select_dramas_genre")

except Exception as e:
    report.append(f"An error occurred during automation: {str(e)}")

finally:
    driver.quit()

    # Guarda el reporte en un archivo de texto
    with open(path_reporte, 'w') as f:
        for line in report:
            f.write(line + "\n")

    print(f"Automation completed. Report saved to '{path_reporte}'.")
