from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('--headless')  # Executar o Firefox em modo headless
service = Service('/home/bigdata/IGTI/pos_engenharia_dados/projeto_aplicado/src/libs/geckodriver')

try:
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://www.google.com")
    print("Página aberta com sucesso!")
except Exception as e:
    print(f"Erro: {e}")
finally:
    try:
        driver.quit()
    except NameError:
        print("O driver não foi iniciado.")
