# %%
import streamlit as st
import pandas as pd


st.set_page_config(layout="wide", page_title="Produção", page_icon="📃")

st.title(f"Controle da Produção 2025 - EDDI CASA")


@st.cache_data
def load_data():
    dataset = "https://docs.google.com/spreadsheets/d/1wyFQfS10j-rJEjrxGRQD4BYd2qfyacEaVIjX91CUgPI/export?format=csv&gid=0#gid=0"
    df = pd.read_csv(dataset)
    df = df.applymap(lambda x: x.title() if isinstance(x, str) else x)
    columns = df.columns
    colunas_formatadas = [coluna.title() for coluna in columns]
    df.columns = colunas_formatadas
    return df

# %%
df = load_data()
# st.dataframe(df)

df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date

# %%
col1, col2, col3, col4 = st.columns(4)

lista_meses = df['Mes'].unique().tolist()
lista_meses = lista_meses[::-1]
mes_seleionado = col1.selectbox(label='Mês', options=lista_meses)

df_filtrado_mes = df[df['Mes'] == mes_seleionado]
df_filtrado_mes['Total'] = df_filtrado_mes['Total'].str.replace(',','.').astype(float)
total_mes = df_filtrado_mes['Total'].sum()
col2.metric(label='Total', value=f'R$ {round(total_mes,2)}')

df_filtrado_mes['Producao Interna'] = df_filtrado_mes['Producao Interna'].str.replace(',','.').astype(float)
total_mes = df_filtrado_mes['Producao Interna'].sum()
col3.metric(label='Total', value=f'R$ {round(total_mes,2)}')

df_filtrado_mes['Producao Mao De Obra'] = df_filtrado_mes['Producao Mao De Obra'].str.replace(',','.').astype(float)
total_mes = df_filtrado_mes['Producao Mao De Obra'].sum()
col4.metric(label='Total', value=f'R$ {round(total_mes,2)}')

st.dataframe(df_filtrado_mes, hide_index=True)
