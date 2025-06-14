import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--headless")
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_options.add_argument(r"--user-data-dir=C:\Users\Gaming\AppData\Local\Google\Chrome\User Data\Profile 2")
chrome_options.add_argument("--profile-directory=Profile 2")

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=chrome_options)

# Caminho do arquivo JSON
json_path = "bot_data.json"

# Última modificação do arquivo
last_modified = 0

reproducao_aba = None
discord_aba = None

def try_login():
    campo_login = navegador.find_elements(By.XPATH,'//*[@id="uid_38"]')
    campo_senha = navegador.find_elements(By.XPATH,'//*[@id="uid_40"]')
    if campo_login and campo_senha:





def entrar_no_canal(navegador, canal_nome):
    time.sleep(3)

    try:
        # Encontrar todos os canais com base no XPath fornecido
        canais = navegador.find_elements(By.XPATH,
                                         "/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/nav/div[4]/ul/li")

        if canais:
            for canal in canais:
                # Obter o nome do canal diretamente
                nome = canal.get_attribute("data-dnd-name")
                if nome:
                    nome = nome.strip()  # Remove espaços extras ao redor do nome do canal

                    print(f"Verificando canal: {nome}")

                    # Comparação exata sem converter para minúsculas
                    if nome == canal_nome:
                        print(f"Entrando no canal: {canal_nome}")

                        # Clicar no texto do canal (modificar para garantir que clicamos no canal correto)
                        try:
                            # Supondo que o texto do canal esteja dentro de um <div> específico
                            texto_canal = canal.find_element(By.XPATH, ".//div[1]/div[2]")
                            texto_canal.click()
                            time.sleep(1)  # Reduzir o tempo de espera para 1 segundo
                            return
                        except Exception as click_error:
                            print("Erro ao tentar clicar no canal:", click_error)

            print(f"Canal '{canal_nome}' não encontrado!")
        else:
            print("Nenhum canal encontrado.")

    except Exception as e:
        print("Erro ao tentar entrar no canal:", e)


while True:
    # Verifica se o arquivo foi modificado
    modified_time = os.path.getmtime(json_path)

    if modified_time > last_modified:
        last_modified = modified_time  # Atualiza a referência de modificação

        # Lê o JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            link = data.get("Link")  # Obtém o link do YouTube
            canal_url = data.get("Canal URL")  # Obtém o link do canal de voz do Discord
            plataforma = data.get("Plataforma")  # Nome da plataforma
            horario = data.get("Horário")  # Horário (se necessário)

        if link:
            print(f"Abrindo link da plataforma {plataforma}: {link}")
            if reproducao_aba is None:
                # Abre o link do YouTube na aba inicial
                navegador.get(link)
                reproducao_aba = navegador.current_window_handle
            else:
                # Caso a aba de reprodução já tenha sido aberta, só faz ela continuar lá
                navegador.switch_to.window(reproducao_aba)
                navegador.get(link)  # Recarrega a página, se necessário

        if canal_url:
            print(f"Abrindo canal de voz no Discord: {canal_url}")
            if discord_aba is None:
                # Primeira vez: abre o Discord em uma nova aba
                navegador.execute_script("window.open(arguments[0]);", canal_url)
                navegador.switch_to.window(navegador.window_handles[-1])  # Alterna para a nova aba
                discord_aba = navegador.current_window_handle  # Salva o identificador da aba
            else:
                # Se a aba já foi aberta, apenas alterna para ela (sem abrir nova)
                navegador.switch_to.window(discord_aba)

            # Espera um pouco para o Discord carregar
            time.sleep(5)

            # Entra no canal especificado no JSON
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                canal_nome = data.get("Canal de Voz")  # Obtém o nome do canal de voz

                if canal_nome:
                    print(f"Tentando entrar no canal: {canal_nome}")
                    entrar_no_canal(navegador, canal_nome)
    time.sleep(5)
    #TESTE: para deixar em fullScreen no youtube
