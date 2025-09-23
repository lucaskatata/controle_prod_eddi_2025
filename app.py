# %%
import streamlit as st
import pandas as pd


st.set_page_config(layout="wide", page_title="Controle da Produção 2025", page_icon="📃")

st.title(f"Controle da Produção 2025 - EDDI CASA")

dataset = "https://docs.google.com/spreadsheets/d/1wyFQfS10j-rJEjrxGRQD4BYd2qfyacEaVIjX91CUgPI/export?format=csv&gid=0#gid=0"

dataset_custos = "https://docs.google.com/spreadsheets/d/1wyFQfS10j-rJEjrxGRQD4BYd2qfyacEaVIjX91CUgPI/export?format=csv&gid=810711903#gid=810711903"

df = pd.read_csv(dataset)
df_custos = pd.read_csv(dataset_custos)
df_custos = df_custos.rename(columns={'Unnamed: 0': 'Mes'})

df_custos['Bonus'] = df_custos['Bonus'].str.replace(',','.').astype(float)
df_custos['Total'] = df_custos['Total'].str.replace(',','.').astype(float)

df = df.applymap(lambda x: x.title() if isinstance(x, str) else x)
columns = df.columns
colunas_formatadas = [coluna.title() for coluna in columns]
df.columns = colunas_formatadas

df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date

col1, col2, col3, col4 = st.columns(4)

lista_meses = df['Mes'].unique().tolist()
lista_meses = lista_meses[::-1]
mes_selecionado = col1.selectbox(label='Mês', options=lista_meses)

df_filtrado_mes = df[df['Mes'] == mes_selecionado]
df_filtrado_mes['Total'] = df_filtrado_mes['Total'].str.replace(',','.').astype(float)
total_mes = df_filtrado_mes['Total'].sum()
col2.metric(label='Total', value=f'R$ {round(total_mes,2)}')

df_filtrado_mes['Producao Interna'] = df_filtrado_mes['Producao Interna'].str.replace(',','.').astype(float)
total_mes_prod_int = df_filtrado_mes['Producao Interna'].sum()
col3.metric(label='Prod. Interna', value=f'R$ {round(total_mes_prod_int,2)}')

df_filtrado_mes['Producao Mao De Obra'] = df_filtrado_mes['Producao Mao De Obra'].str.replace(',','.').astype(float)
total_mes_mo = df_filtrado_mes['Producao Mao De Obra'].sum()
col4.metric(label='Prod. Mão de obra', value=f'R$ {round(total_mes_mo,2)}')


col5, col6, col7, col8 = st.columns(4)

df_custos_filtrado = df_custos[df_custos['Mes'] == mes_selecionado].sum()
bonus_selecionado = df_custos_filtrado['Bonus']
col7.metric(label='Bonus', value=f'R$ {round(bonus_selecionado, 2)}')

total_selecionado = df_custos_filtrado['Total'].sum()
total_selecionado = round(total_selecionado, 2)
col6.metric(label='Custo Total', value=f'R$ {round(total_selecionado, 2)}')

diferenca = total_mes - total_selecionado
diferenca = round(diferenca,2)
col5.metric(label='Diferença', value=f'R$ {diferenca}')

st.dataframe(df_filtrado_mes, hide_index=True)

