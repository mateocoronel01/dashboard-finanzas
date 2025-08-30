import streamlit as st
import pandas as pd
import plotly.express as px

# Título del dashboard
st.title("Dashboard de Finanzas")

# Tu Google Sheet (leer en modo solo lectura CSV)
SHEET_ID = "1ZvI0Svvj12hCcMmVFg9uE7dL80p5BP76cjoyEbjihek"
SHEET_NAME = "Sheet1"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# Cargar datos
@st.cache_data
def cargar_datos(url):
    return pd.read_csv(url)

df = cargar_datos(url)

# Mostrar tabla completa
st.subheader("Datos completos")
st.dataframe(df)

# Totales y promedios
st.subheader("Resumen")
col1, col2 = st.columns(2)
if 'Monto' in df.columns:
    col1.metric("Total", f"${df['Monto'].sum():,.2f}")
    col2.metric("Promedio", f"${df['Monto'].mean():,.2f}")

# Filtro por columna
columna_filtro = st.selectbox("Filtrar por columna", df.columns)
valor_filtro = st.text_input("Valor a filtrar")
if valor_filtro:
    df_filtrado = df[df[columna_filtro].astype(str).str.contains(valor_filtro, case=False)]
else:
    df_filtrado = df

# Gráficos
st.subheader("Gráficos")
if 'Fecha' in df_filtrado.columns and 'Monto' in df_filtrado.columns:
    df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
    fig_linea = px.line(df_filtrado, x='Fecha', y='Monto', title="Monto en el tiempo")
    st.plotly_chart(fig_linea, use_container_width=True)

if 'Categoría' in df_filtrado.columns and 'Monto' in df_filtrado.columns:
    fig_barras = px.bar(df_filtrado, x='Categoría', y='Monto', title="Monto por Categoría")
    st.plotly_chart(fig_barras, use_container_width=True)
