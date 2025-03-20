from os import getenv
from dotenv import load_dotenv
load_dotenv()
from resources.PathManager import PathManager
from resources.TimeConsult import TimeConsult
import undetected_chromedriver as uc
from random import uniform
from selenium.webdriver.support.ui import WebDriverWait
from pyautogui import keyDown
from time import sleep
from resources.PathManager import PathManager
from resources.FilesManager import FilesManager

class Browser:
    def __init__(self, headless: bool = True, extension: bool = True):
        self.pathmanager = PathManager()
        self.filesmanager = FilesManager()
        self.pathmanager.remove_data_chrome()
        self.pathmanager = PathManager()
        self.url_sefaz = getenv("URL_SEFAZ")
        self.path_downloads = self.pathmanager.path_pdfs.replace('\\\\', '\\')
        self.path_api = self.pathmanager.path_api.replace('\\\\', '\\')
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--start-fullscreen")
        chrome_options.user_data_dir = self.pathmanager.path_data
        chrome_options.add_argument(rf"--profile-directory=Default")
        if headless:
            chrome_options.add_argument("--window-size=1920X1080")
            chrome_options.add_argument("--headless")
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
        chrome_options.add_argument(f"--load-extension={self.path_api}")
        self.timeconsult = TimeConsult()
        self.navegador = uc.Chrome(headless=False, use_subprocess=False, options=chrome_options, suppress_welcome=True, driver_executable_path=f'{getenv("PATH_CHROME_DRIVER")}\\chromedriver.exe', browser_executable_path=f'{getenv("PATH_CHROME")}\\chrome.exe')
        
        self.wait = WebDriverWait(self.navegador, 40)

        sleep(10)
        # input("AQUI ACHOU A EXTENSÃO?")

        # Defina o caminho do arquivo Preferences

        # Verifica se o arquivo existe
        if extension:
            data = self.filesmanager.get_preferences()
            if data:
                extensions = data.get("extensions", {}).get("settings", {})
                found = False
                for ext_id, details in extensions.items():
                    path = details.get("path", "").lower()  # Caminho da extensão
                    if "anti" in path:
                        found = True
                        break
                    if not found:
                        print("Nenhuma extensão com 'anti' no caminho foi encontrada.")

                        for ext_id, details in extensions.items():
                            print(f"ID: {ext_id} | Caminho: {details.get('path', 'Desconhecido')}")

            self.navegador.get(f"chrome-extension://{ext_id}/popup_v3.html")
            sleep(10)
            self.navegador.execute_script("""var teste = document.getElementById('enable_checkbox');
                                            var teste2 = document.getElementsByName('auto_submit_form')
                                                                teste.disabled = false;
                                                                if (teste2[1].disabled)
                                                                {
                                                                    teste.click();
                                                                }""")
            sleep(6)
            self.navegador.execute_script(f"""var teste1 = document.getElementById("account_key");
                                                                teste1.value = '{getenv("API_KEY")}';
                                                                // Disparar eventos para que o site reconheça a mudança
                                                                teste1.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                                                teste1.dispatchEvent(new Event('change', {{ bubbles: true }}));""")
            sleep(5)
            self.navegador.execute_script("""let teste2 = document.getElementsByClassName('btn btn-primary')[0];
                                                                teste2.dispatchEvent(new Event('input', { bubbles: true }));
                                                                teste2.dispatchEvent(new Event('change', { bubbles: true }));
                                                                teste2.click();""")
            sleep(20)

    def keyboard(self, element, word: str, key_down: bool) -> None:
        for caract in word:
            sleep(uniform(0.5, 1.5))
            element.send_keys(caract)
            if key_down is True:
                keyDown('right')
                element.click()
