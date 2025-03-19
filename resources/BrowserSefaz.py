from loguru import logger
from os import getenv, getcwd
from dotenv import load_dotenv
load_dotenv()
from time import sleep
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from resources.TimeConsult import TimeConsult
from random import uniform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyautogui import keyDown
from re import sub
from resources.PathManager import PathManager

class BrowserSefaz:
    def __init__(self):
        self.pathmanager = PathManager()
        self.url_sefaz = getenv("URL_SEFAZ")
        self.path_downloads = self.pathmanager.path_pdfs.replace('\\\\', '\\')
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--start-fullscreen")
        chrome_options.user_data_dir = rf'{getcwd()}\Chrome\data_sefaz'
        chrome_options.add_argument(rf"--profile-directory=Default")
        # chrome_options.add_argument("--window-size=1920X1080")
        # chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("prefs", {
            "autofill.profile_enabled": False,
            "profile.default_content_settings.popups": 0,
            "download.default_directory": self.path_downloads,  # Caminho do diretório de download
            "directory_upgrade": True,
            "download.prompt_for_download": False,  # Desabilita o prompt de download
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.mode": "strict",
            "plugins.always_open_pdf_externally": True  # Faz o Chrome baixar PDFs automaticamente
        })
        chrome_options.add_argument(f"--load-extension=E:\\Dados\\Ti\\PROJETOS\\anti_captcha071")
        self.timeconsult = TimeConsult()
        self.navegador = uc.Chrome(headless=False, use_subprocess=False, options=chrome_options, suppress_welcome=True, driver_executable_path=f'{getenv("PATH_CHROME_DRIVER")}\\chromedriver.exe', browser_executable_path=f'{getenv("PATH_CHROME")}\\chrome.exe')
        
        self.wait = WebDriverWait(self.navegador, 40)
        self.fechou = False
        self.first_interaction = True
        self.navegador.get("chrome-extension://caokhkhhncahnamdelalpicnnelnjncn/popup_v3.html")
        self.navegador.execute_script("""let teste0 = document.getElementsByClassName('toggler')[0];
                                                            if (teste0.disabled){
                                                                teste0.click();
                                                            }""")
        sleep(6)
        self.navegador.execute_script("""let teste1 = document.getElementById("account_key");
                                                            teste1.value = "aec1b68faa12cc7b9e1c0b560a0f7bc0";
                                                            // Disparar eventos para que o site reconheça a mudança
                                                            teste1.dispatchEvent(new Event('input', { bubbles: true }));
                                                            teste1.dispatchEvent(new Event('change', { bubbles: true }));""")
        sleep(5)
        # input("CONFIGUROU ANTICAPTCHA AQUI!!!!!!!!")
        self.navegador.execute_script("""let teste2 = document.getElementsByClassName('btn btn-primary')[0];
                                                            teste2.dispatchEvent(new Event('input', { bubbles: true }));
                                                            teste2.dispatchEvent(new Event('change', { bubbles: true }));
                                                            teste2.click();""")
        sleep(10)
        
        # input("AQUIIIIII!!!!!!!!!!!!!")
        # input("AQUIIIIIIII!!!!!!!!!!!")

    def keyboard(self, element, word: str, key_down: bool) -> None:
        for caract in word:
            sleep(uniform(0.5, 1.5))
            element.send_keys(caract)
            if key_down is True:
                keyDown('right')
                element.click()

    def enter_site(self):
        self.navegador.get(self.url_sefaz)

    def login(self):
        login_info = False
        while not login_info:
            try:
                campo_login = self.wait.until(EC.element_to_be_clickable((By.ID, "LoginId")))
                self.keyboard(element=campo_login, word=getenv("CPF_CNPJ"), key_down=False)
                if sub(r"\D", "", self.navegador.find_element(By.ID, 'LoginId').get_attribute('value')) != getenv("CPF_CNPJ"): 0/1
                login_info = True
                logger.info('Informou o login')
            except Exception as error_x:
                logger.error(f'Não informou o login: {error_x}')
                sleep(1)

        senha_info = False
        while not senha_info:
            try:
                campo_senha = self.wait.until(EC.element_to_be_clickable((By.ID, "senha_ecac")))
                self.keyboard(element=campo_senha, word=getenv("PASSWORD_SEFAZ"), key_down=False)
                if sub(r"\D", "", self.navegador.find_element(By.ID, 'senha_ecac').get_attribute('value')) != getenv("PASSWORD_SEFAZ"): 0/1
                senha_info = True
                logger.info('Informou a senha')
            except Exception as error_x:
                logger.error(f'Não informou a senha: {error_x}')
                sleep(1)

        while True:
            try:
                if self.navegador.find_element(By.XPATH, '//*[@id="divRecaptcha"]/div/div/div/div/div[2]/a[1]').text.__eq__('Solved'):
                    break
                sleep(1)
            except:
                pass
            sleep(1)

        entrar = False
        while not entrar:
            try:
                self.navegador.find_element(By.XPATH, '//*[@id="btnEntrar"]').click()
                entrar = True
                logger.info('Clicou em entrar')
            except Exception as error_x:
                logger.error(f'Não clicou em entrar: {error_x}')
                sleep(1)

        lerdps = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Lerei as mensagens mais tarde. Agora eu quero acessar os serviços disponíveis no Portal e-CAC.' and @class='button']")))
        lerdps.click()

    def fecharboxxx(self):
        for _ in range(20):
            try:
                self.navegador.find_element(By.ID, 'cboxClose').click()
                self.fechou = True
                logger.info("Fechou a caixa de diálogo!")
                break
            except Exception as error_x:
                logger.error(f'Não fechou a caixa de diáogo: {error_x}')
            sleep(1)
            
    def ie_operations(self, inscEstadual) -> dict:
        self.navegador.execute_script("window.sessionStorage.clear();")
        if not self.fechou:
            self.fecharboxxx()

        if not self.first_interaction:
            dict_status = {'status': 0, 'status_erro': ''}
            for _ in range(40):
                try:
                    self.navegador.find_element(By.ID, 'btnIES').click()
                    logger.info('Clicou em "Meus Vínculos"')
                    break
                except Exception as error_x:
                    logger.error(f'Não clicou em "Meus Vínculos": {error_x}')
            sleep(1)

        if self.first_interaction: 
            self.first_interaction = False
            dict_status = {'status': 0, 'status_erro': ''}

        inscEstadual_element = self.wait.until(EC.element_to_be_clickable((By.ID, "filtroIe")))
        inscEstadual_element.send_keys(inscEstadual)
        ie = False

        for _ in range(10):
            try:
                for elemento in self.navegador.find_elements(By.TAG_NAME, 'a'):
                    if elemento.text == f'{inscEstadual[:3]}/{inscEstadual[3:]}':
                        elemento.click()
                        logger.info('Clicou na Inscrição Estadual')
                        ie = True
                        break
            except Exception as error_x:
                logger.error(f'Não clicou na Inscrição Estadual: {error_x}')
                if str(error_x).__contains__('Você não está autorizado a acessar esta informação'):
                    dict_status['status'] = 1
                    dict_status['status_erro'] = 'NÃO AUTORIZADO'
                    self.fechou = False
                    self.navegador.back()
                    return dict_status

            sleep(1)

        if not ie:
            logger.error('SEM ACESSO')
            dict_status['status'] = 1
            dict_status['status_erro'] = 'SEM ACESSO'
            return dict_status
        
        for _ in range(40):
            try:
                self.navegador.find_element(By.ID, "tab_8").click()
                logger.info("Clicou na caixa postal")
                break
            except Exception as error_x:
                logger.error(f'Não clicou em caixa postal: TENTATIVA: {_ + 1}: ERROR_X: {error_x}')
        
        for _ in range(40):
            try:
                self.navegador.find_element(By.ID, "tab_cpe_5").click()
                logger.info("Clicou em Recibo")
                break
            except Exception as error_x:
                logger.error(f'Não clicou em Recibo: TENTATIVA: {_ + 1}: ERROR_X: {error_x}')
        
        painel_comunicados = False
        while not painel_comunicados:
            try:
                rows = self.navegador.find_element(By.ID, 'CpeListaMsgs_5')
                painel_comunicados = True
                logger.info('Encontrou o painel de comunicados')
                break
            except Exception as error_x:
                logger.error(f'Não encontrou o painel de comunicados: {error_x}')
                sleep(1)

        lines = False
        while not lines:
            try:
                linhas = rows.find_elements(By.TAG_NAME, 'tr')
                lines = True
                logger.info('Encontrou as linhas')
                break
            except Exception as error_x:
                logger.error(f'Não encontrou as linhas: {error_x}')
                sleep(1)

        if len(linhas).__le__(1):
            dict_status['status'] = 1
            dict_status['status_erro'] = 'COMPETÊNCIA NÃO ENCONTRADA'
            return dict_status

        while True:
            for line in range(1, len(linhas)):
                cells = linhas[line].find_elements(By.TAG_NAME, 'td')
                if cells[1].text.split('/')[1].__eq__(self.timeconsult.updated_month) and cells[1].text.split('/')[-1].__eq__(self.timeconsult.updated_year):
                    print(f'CELLS[1].TEXT: {cells[1].text}')
                    cells[0].find_elements(By.TAG_NAME, 'a')[0].click()
                    self.make_download()
                    dict_status['status'] = 1
                    dict_status['status_erro'] = ''
                elif int(cells[1].text.split('/')[-1]) < int(self.timeconsult.updated_year) or (int(cells[1].text.split('/')[1]) < int(self.timeconsult.updated_month) and cells[1].text.split('/')[-1].__eq__(self.timeconsult.updated_year)):
                    print(f'AQUI NÃO BAIXOU CELLS[1].TEXT!!!!!!!!!!!!!!!: {cells[1].text}')
                    if dict_status['status'] == 0:
                        dict_status['status'] = 1
                        dict_status['status_erro'] = 'COMPETÊNCIA NÃO ENCONTRADA'
                    return dict_status
            return dict_status
    
    def make_download(self):
        download = False
        while not download:
            try:
                iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
                self.navegador.switch_to.frame(iframe)
                logger.info('Localizou e selecionou o iframe')
            except:
                logger.error('Não localizou o iframe')
                
            button = self.wait.until(EC.element_to_be_clickable((By.ID, "open-button")))

            if button.is_displayed() and button.is_enabled():
                button.click()
                print("Botão clicado com sucesso.")
                download = True
                sleep(5)
            else:
                print("Botão não está visível ou habilitado.")
        sleep(6)
        self.navegador.switch_to.default_content()
        self.navegador.back()
