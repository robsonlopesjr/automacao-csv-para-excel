from datetime import datetime
import os
import pandas as pd
import win32com.client as win32

caminho = "datasets"
arquivos = os.listdir(caminho)

tabela_consolidada = pd.DataFrame()

for nome_arquivo in arquivos:
    tabela_vendas = pd.read_csv(os.path.join(caminho, nome_arquivo))
    tabela_vendas["Data de Venda"] = pd.to_datetime("01/01/1900") + pd.to_timedelta(tabela_vendas["Data de Venda"],
                                                                                    unit="d")

    tabela_consolidada = pd.concat([tabela_consolidada, tabela_vendas])

tabela_consolidada = tabela_consolidada.sort_values(by="Data de Venda")
tabela_consolidada = tabela_consolidada.reset_index(drop=True)

# Transformar a consolidação dos arquivos .csv para um único arquivo excel .xlsx
tabela_consolidada.to_excel("Vendas.xlsx", index=False)

# Conectando ao Outlook
outlook = win32.Dispatch("outlook.application")

# Criando o E-mail
email = outlook.CreateItem(0)
email.To = ""
data_hoje = datetime.today().strftime("%d/%m/%Y")
email.Subject = f"Relatório de Vendas {data_hoje}"
email.Body = f"""
Prezados,

Segue em anexo o Relatório de Vendas de {data_hoje} atualizado.
Qualquer coisa estou à disposição.

Atenciosamente,
xxx
"""
caminho = os.getcwd()
anexo = os.path.join(caminho, "Vendas.xlsx")
email.Attachments.Add(anexo)

email.Send()
