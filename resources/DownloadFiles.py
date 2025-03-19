from os import getenv
from resources.TimeConsult import TimeConsult
from resources.BrowserSefaz import BrowserSefaz
from use_cases.MySQLDB import MySQLDB
from DB.queries import consulta_gia_destda, atualizar_status, atualizar_gia_destda
from resources.FilesManager import FilesManager
from datetime import datetime

class DownloadFiles:
    def __init__(self):
        self.timeconsult = TimeConsult()
        self.mysqldb = MySQLDB(host=getenv("HOST"), user=getenv("USER"), password=getenv("PWD"), database=getenv("DATABASE"))
        self.filesmanager = FilesManager()
        self.iniciou = False

    def iniciar(self):
        self.dict_way = {"GIA": False, "DESTDA": False}
        if len(self.mysqldb.ler_dados(query=consulta_gia_destda.format(int(self.timeconsult.actual_month), int(self.timeconsult.actual_year), 'GIA'))).__gt__(0):
            self.dict_way['GIA'] = True
        if len(self.mysqldb.ler_dados(query=consulta_gia_destda.format(int(self.timeconsult.actual_month), int(self.timeconsult.actual_year), 'DESTDA'))).__gt__(0):
            self.dict_way['DESTDA'] = True
        
    def create_browser(self):
        if any(self.dict_way[key] is True for key in self.dict_way.keys()):
            self.browsersefaz = BrowserSefaz()
            self.browsersefaz.enter_site()
            self.browsersefaz.login()
            self.iniciou = True

    def download_files(self, tipo: str):
        self.iniciar()
        if self.dict_way[tipo] and not self.iniciou:
            self.create_browser()
        try:
            self.mysqldb.inserir_dados(query=atualizar_gia_destda.format(self.timeconsult.actual_year, self.timeconsult.actual_month))
            if len(self.mysqldb.ler_dados(query=consulta_gia_destda.format(int(self.timeconsult.actual_month), int(self.timeconsult.actual_year), tipo))).__gt__(0):
                for data in self.mysqldb.ler_dados(query=consulta_gia_destda.format(int(self.timeconsult.actual_month), int(self.timeconsult.actual_year), tipo)):
                    print(f'DATA: {data}')
                    ie = data[0]
                    print(f'IE: {ie}')
                    self.filesmanager.clear_pdfs()
                    atualizacao = self.browsersefaz.ie_operations(inscEstadual=ie)
                    status_arquivo = self.filesmanager.manager_pdfs()
                    self.mysqldb.atualizar_dados(query=atualizar_status.format(atualizacao['status'], atualizacao['status_erro'], status_arquivo, str(datetime.now())[:-7], int(self.timeconsult.actual_month), int(self.timeconsult.actual_year), ie))
        except Exception as error_x:
            print(f'ERROR_X: {error_x}')
        return
