from os import getenv, listdir, path as _path, remove
from dotenv import load_dotenv
load_dotenv()
from resources.Pdf import Pdf
from resources.PathManager import PathManager
from use_cases.MySQLDB import MySQLDB
from resources.TimeConsult import TimeConsult
from shutil import copy, move
from DB.queries import consulta_id
import json
from loguru import logger

class FilesManager:
    def __init__(self):
        self.timeconsult = TimeConsult()
        self.pathmanager = PathManager()
        self.pathmanager.path_exists()
        self.mysqldb = MySQLDB(host=getenv("HOST"), user=getenv("USER"), password=getenv("PWD"), database=getenv("DATABASE"))
        self.mysqldb.conectar()
        self.pdf = Pdf()

    def list_all_pdfs(self) -> list:
        pdfs_list = [f'{self.pathmanager.path_pdfs}\\{file}' for file in listdir(self.pathmanager.path_pdfs) if file.lower().endswith('.pdf')]
        return pdfs_list

    def manager_pdfs(self) -> str:
        pdfs = self.list_all_pdfs()
        valid = None
        if len(pdfs).__gt__(0):
            for pdf in pdfs:
                pdf_verification = self.pdf.verify_pdf(file=pdf)
                cnpj = pdf_verification[0]
                mes = pdf_verification[1]
                ano = pdf_verification[2]
                tipo = pdf_verification[3]
                recebimento = pdf_verification[4]
                id = self.mysqldb.ler_dados(query=consulta_id.format(cnpj))[0][0]
                if pdf_verification[-1]:
                    print(pdf, f'{self.pathmanager.search_path(cnpj=cnpj, mes=mes, ano=ano)}\\GIA_DESTDA\\{id} - RECIBO {tipo} {mes}.{ano}.pdf')
                    copy(pdf, f'{self.pathmanager.search_path(cnpj=cnpj, mes=mes, ano=ano)}\\GIA_DESTDA\\{id} - RECIBO {tipo} {mes}.{ano}.pdf')
                    print(pdf, f'{self.pathmanager.search_path(cnpj=cnpj, mes=mes, ano=ano)}\\GIA_DESTDA\\{id} - RECIBO {tipo} {mes}.{ano}.pdf')
                    move(pdf, f'{self.pathmanager.path_downloads}\\{id} - RECIBO {tipo} {mes}.{ano}.pdf')
                    print(f'{pdf}: {pdf_verification}')
                    valid = True
                else:
                    print(pdf, f'{self.pathmanager.search_path(cnpj=cnpj, mes=mes, ano=ano)}\\GIA_DESTDA\\{id} - RECIBO {tipo} {mes}.{ano}.pdf')
                    print(f'{pdf}: {pdf_verification}')
                    move(pdf, f'{self.pathmanager.search_path(cnpj=cnpj, mes=mes, ano=ano)}\\GIA_DESTDA\\{id} - RECIBO {tipo} {mes}.{ano} (INCONSISTENTE).pdf')
        if valid:
            return f"{tipo} {recebimento}"

    def list_all_destda(self, mes, ano):
        return {str(int(key)): f'{pasta}\\{ano}\\{mes}.{ano}\\GIA_DESTDA\\{file}'.replace("\\\\", "\\") for key, pasta in self.pathmanager.generate_paths_dict_by_id().items() if f'{str(int(key))} - RECIBO DESTDA {mes}.{ano}.pdf' in listdir(f'{pasta}\\{ano}\\{mes}.{ano}\\GIA_DESTDA') for file in listdir(f'{pasta}\\{ano}\\{mes}.{ano}\\GIA_DESTDA')}

    def clear_pdfs(self) -> None:
        [remove(pdf) for pdf in self.list_all_pdfs()]

    def list_files_cach(self, ext: str) -> list:
        return [f'{self.pathmanager.path_cach}\\{file}' for file in listdir(self.pathmanager.path_cach) if file.upper().endswith(ext.upper())]
    
    def remove_files(self, ext: str) -> None:
        [remove(file) for file in self.list_files_cach(ext=ext)]
    
    def remove_file(self, file) -> None:
        remove(file)
    
    def remove_files_any(self, files: list, ext: str, exec: list = []) -> None:
        for file in files:
            try:
                if file.split("\\")[-1] not in exec: 
                    remove(file)
                    print(f'Arquivo {file} removido com sucesso!')
            except Exception as error:
                print(f'Não conseguiu remover o arquivo: {file} === ERRO: {error}')

    def get_preferences(self) -> json.load:
        preferences_path: str = rf"{self.pathmanager.path_data}\Default\Preferences"
        if _path.exists(preferences_path):
            try:
                with open(preferences_path, "r", encoding="utf-8") as file:
                    data: json.load = json.load(file)
                    return data
            except Exception as error_x:
                logger.error(f'Erro ao ler o arquivo {preferences_path}: {error_x}')