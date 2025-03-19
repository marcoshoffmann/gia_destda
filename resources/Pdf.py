import pdfplumber as plb
from re import sub

class Pdf:
    def read_pdf(self, file_pdf: str) -> list:
        with plb.open(path_or_fp=file_pdf) as pdf_open:
            extracted_data =[]
            [extracted_data.extend(pdf_open.pages[page].extract_text().split("\n")) for page in range(len(pdf_open.pages))]
        return extracted_data
    
    def verify_pdf(self, file):
        cnpj, mes, ano, status_recebimento, status,  = None, None, None, '', False
        pdf_data = self.read_pdf(file_pdf=file)
        # input(f'PDF DATA: {pdf_data}')
        if any('GIA ' in line for line in pdf_data):
            tipo = 'GIA'
            for line in pdf_data:
                if line.__eq__('Situação da GIA: GIA ACEITA'):
                    status_recebimento = 'ACEITA'
                    status = True
                if line.__eq__('Situação da GIA: GIA ACEITA - INCONSISTENTE'):
                    status_recebimento = 'ACEITA INCONSISTENTE'
                    status = True
                if line.__contains__('CNPJ: '): cnpj = sub('\D', '', line)
                if line.__contains__('Mês de Referência: '): 
                    competencia = line.split("Mês de Referência: ")[-1]
                    mes = competencia.split("/")[0]
                    ano = competencia.split("/")[-1]
        elif any('DeSTDA' in line for line in pdf_data):
            tipo = 'DESTDA'
            for line in pdf_data:
                # input(f'LINE: |{line}|')
                if line.__eq__('DeSTDA - ACEITA.'):
                    status_recebimento = 'ACEITA'
                    status = True
                if line.__eq__('DeSTDA ACEITA. - INCONSISTENTE'):
                    status_recebimento = 'ACEITA INCONSISTENTE'
                    status = True
                if line.__contains__('CNPJ '): cnpj = f'{int(line.split(" ")[1]):014}'
                if line.__contains__(' Mês Referência '): 
                    competencia = line.split(" Mês Referência ")[-1]
                    mes = competencia.split("/")[0]
                    ano = competencia.split("/")[-1]
        return cnpj, mes, ano, tipo, status_recebimento, status
