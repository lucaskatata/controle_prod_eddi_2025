# %%
import pandas as pd
from pathlib import Path

def retorna_mes(caminho_pasta):
    meses = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Março",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro",
    }
    pasta = Path(caminho_pasta)
    mes = pasta.name.split(" - ")[0]
    mes = meses.get(mes)
    return mes

def retorna_mes1(caminho_pasta):
    meses = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Março",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro",
    }
    pasta = Path(caminho_pasta)
    mes = pasta.name.split('-')[0]
    mes = meses.get(mes)
    return mes

def df_diario_producao_interna(arquivo):
    df_final = pd.DataFrame()
    lista_df = []
    df = pd.read_excel(arquivo, sheet_name="CAPA", usecols="B:E", nrows=12, skiprows=5)
    df["PROCESSO"] = df["PROCESSO"].str.split("-").str[-1].str.title()
    df = df.round(2)
    df["PROCESSO"] = df["PROCESSO"].str.strip()

    colunas = df.columns.str.title().str.strip()
    df = (
        df.drop(columns=colunas[2:])
        .rename(
            columns={"VALOR": f'{arquivo.stem.replace("-","/")}', "PROCESSO": "Data"}
        )
        .set_index("Data")
        .T
    )
    df["Producao Interna"] = df.sum(axis=1)
    colunas = df.columns
    nova_ordem_colunas = [colunas[-1]]
    colunas = colunas[:-1]
    for c in colunas:
        nova_ordem_colunas.append(c)
    df = df[nova_ordem_colunas]
    return df


def criar_df_producao_interna(caminho_pasta, df_diario_producao_interna):
    lista_df = []
    df_final = pd.DataFrame()
    for arquivo in caminho_pasta.iterdir():
        df = df_diario_producao_interna(arquivo)
        lista_df.append(df)
        df_final = pd.concat(lista_df)

    df_final.index.name = "Data"
    return df_final


def df_diario_mao_de_obra(arquivo):
    df_final = pd.DataFrame()
    lista_df = []
    df = pd.read_excel(arquivo, sheet_name="CAPA", usecols="B:E", nrows=12, skiprows=5)
    df["PROCESSO"] = df["PROCESSO"].str.split("-").str[-1].str.title()
    df = df.round(2)
    df["PROCESSO"] = df["PROCESSO"].str.strip()

    colunas = df.columns.str.title().str.strip()
    df = (
        df.drop(columns=colunas[2:])
        .rename(
            columns={"VALOR": f'{arquivo.stem.replace("-","/")}', "PROCESSO": "Data"}
        )
        .set_index("Data")
        .T
    )
    df["Producao Mao de Obra"] = df.sum(axis=1)
    colunas = df.columns
    nova_ordem_colunas = [colunas[-1]]
    colunas = colunas[:-1]
    for c in colunas:
        nova_ordem_colunas.append(c)
    df = df[nova_ordem_colunas]
    return df


def criar_df_mao_de_obra(caminho_pasta, df_diario_mao_de_obra):
    lista_df = []
    df_final = pd.DataFrame()
    for arquivo in caminho_pasta.iterdir():
        df = df_diario_mao_de_obra(arquivo)
        lista_df.append(df)
        df_final = pd.concat(lista_df)
    df_final.index = df_final.index.str.replace(" M.O", "")
    df_mo = df_final.drop(
        columns=[
            "Corte",
            "Corte Voil",
            "Bainha Continua",
            "Barrado",
            "Emenda",
            "Overloque",
            "Paleteira",
            "Acabamento",
            "Furo",
            "Ilhos",
            "Dobra",
            "Embalagem",
        ],
        axis=1,
    )
    df_mo.index = df_mo.index.astype(str).str.extract(r"(\d{2}/\d{2}/\d{4})")[0]
    df_mo.index.name = "Data"
    return df_mo


def merge(df_producao_interna, df_mao_de_obra, caminho_pasta):
    df = pd.merge(df_producao_interna, df_mao_de_obra, on="Data", how="outer").fillna(0)
    df["Total"] = df["Producao Interna"] + df["Producao Mao de Obra"]
    df = df[
        [
            "Total",
            "Producao Interna",
            "Producao Mao de Obra",
            "Corte",
            "Corte Voil",
            "Bainha Continua",
            "Barrado",
            "Emenda",
            "Overloque",
            "Paleteira",
            "Acabamento",
            "Furo",
            "Ilhos",
            "Dobra",
            "Embalagem",
        ]
    ]
    df["Mes"] = retorna_mes(caminho_pasta)
    return df


def concatena_meses(pasta):
    lista_df = []

    for c in pasta.iterdir():
        df = pd.read_csv(c)
        lista_df.append(df)

    df = pd.concat(lista_df)

    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
    df = df.sort_values(by="Data").reset_index(drop=True)
    return df


pasta = Path(input('Caminho da pasta da produção interna ').replace('"',''))
prod_int = criar_df_producao_interna(pasta, df_diario_producao_interna)

pasta_mo = Path(input('Caminho da pasta da produção da mão de obra ').replace('"',''))
mo = criar_df_mao_de_obra(pasta_mo, df_diario_mao_de_obra)
mo

mes = retorna_mes1(pasta)
codigo_mes = pasta.name.split('-')[0]

df = pd.merge(prod_int, mo, on="Data", how="outer").fillna(0)

df['Total'] = df['Producao Interna'] + df['Producao Mao de Obra']

df = df[
    [
        "Total",
        "Producao Interna",
        "Producao Mao de Obra",
        "Corte",
        "Corte Voil",
        "Bainha Continua",
        "Barrado",
        "Emenda",
        "Overloque",
        "Paleteira",
        "Acabamento",
        "Furo",
        "Ilhos",
        "Dobra",
        "Embalagem",
    ]
]

df1 = df

df1 = df1.reset_index()

df2 = df1

df2['Data'] = pd.to_datetime(df2['Data'],format='%d/%m/%Y')

df2['Mes'] = df2["Data"].dt.month

df2.set_index(['Data'])

dic_mes = {
    1: 'janeiro',
    2: 'fevereiro',
    3: 'março',
    4: 'abril',
    5: 'maio',
    6: 'junho',
    7: 'julho',
    8: 'agosto',
    9: 'setembro',
    10: 'outubro',
    11: 'novembro',
    12: 'dezembro'
}
df2['Mes'] = df2['Mes'].map(dic_mes)

df2['Mes'] = df2['Mes'].str.title()

df2['Data'] = df2['Data'].dt.strftime('%d/%m/%Y')

df2 = df2.set_index('Data')

df2.to_excel(f'Controle da produção - {codigo_mes} {mes} 2025.xlsx')

df2.to_csv(f'Controle da produção - {codigo_mes} {mes} 2025.csv')
