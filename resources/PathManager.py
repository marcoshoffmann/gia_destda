from os import getcwd, getenv, listdir, path, mkdir
from dotenv import load_dotenv
load_dotenv()

class PathManager:
    def __init__(self):
        self.path_clients = getenv("PATH_CLIENTS")
        self.path_pdfs = f'{getcwd()}\\{getenv("PATH_PDFS")}'
        self.path_downloads = getenv("PATH_DOWNLOADS")

    def path_exists(self) -> None:
        if not path.exists(self.path_pdfs): mkdir(self.path_pdfs)

    def generate_paths_dict(self) -> dict:
        paths_clients = listdir(self.path_clients)
        paths_dict = {path.split(" - ")[-1]: f'{self.path_clients}\\{path}' for path in paths_clients}
        return paths_dict
    
    def generate_paths_dict_by_id(self) -> dict:
        paths_clients = listdir(self.path_clients)
        paths_dict = {path.split(" - ")[0]: f'{self.path_clients}\\{path}' for path in paths_clients}
        return paths_dict

    def search_path(self, cnpj: str, mes: str, ano: str) -> str:
        path_clients = self.generate_paths_dict()
        return f'{path_clients[cnpj]}\\{ano}\\{mes}.{ano}'
