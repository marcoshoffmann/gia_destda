consulta_gia_destda = """SELECT empresas.ie FROM gia_destda inner join empresas on gia_destda.id = empresas.id where (gia_destda.status = 0 or gia_destda.status_erro = 'COMPETÊNCIA NÃO ENCONTRADA') and month(gia_destda.competencia) = {} and year(gia_destda.competencia) = {} and gia_destda.tipo = '{}' AND (DATE(gia_destda.data_execucao) != CURDATE() or DATE(gia_destda.data_execucao) IS NULL);"""
atualizar_status = """UPDATE gia_destda INNER JOIN empresas ON gia_destda.id = empresas.id SET gia_destda.status = {}, gia_destda.status_erro = '{}', gia_destda.status_arquivo = '{}', data_execucao = '{}' WHERE MONTH(gia_destda.competencia) = {} and YEAR(gia_destda.competencia) = {} and empresas.ie = '{}';"""
atualizar_gia_destda = """INSERT IGNORE INTO gia_destda SELECT id, (CASE WHEN id in (325, 954) OR empresas.tf != 'SN' THEN 'GIA' WHEN empresas.tf ='SN' THEN 'DESTDA' END), '{}-{}-01', 0, '', '', '', '' FROM empresas WHERE uf = 'RS' and ie != '';"""
consulta_id = """SELECT id FROM empresas WHERE cpf_cnpj = '{}';"""
