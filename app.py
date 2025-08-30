import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Título y bienvenida
# -------------------------------
st.set_page_config(page_title="Dashboard de Finanzas", layout="wide")
st.title("💰 Mi Dashboard de Finanzas")
st.write("Aquí puedes ver y analizar los gastos que tienes en tu Google Sheet en tiempo real.")

# -------------------------------
# Cargar datos desde Google Sheets
# -------------------------------
sheet_id = "1ZvI0Svvj12hCcMmVFg9uE7dL80p5BP76cjoyEbjihek"
url_datos = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=datos"

try:
    df = pd.read_csv(url_datos)
    st.success("Datos cargados correctamente ✅")
except Exception as e:
    st.error(f"No se pudo cargar la hoja de cálculo: {e}")
    st.stop()

# -------------------------------
# Mostrar tabla de datos
# -------------------------------
st.subheader("Tabla de gastos")
st.dataframe(df)

# -------------------------------
# Agrupar por tipo de gasto
# -------------------------------
if "Tipo de Gasto" not in df.columns or "Monto" not in df.columns:
    st.warning("Tu Google Sheet debe tener columnas llamadas 'Tipo de Gasto' y 'Monto'")
else:
    df_agg = df.groupby("Tipo de Gasto")["Monto"].sum().reset_index()

    # -------------------------------
    # Gráfico circular interactivo
    # -------------------------------
    st.subheader("Distribución de gastos por tipo")
    fig = px.pie(
        df_agg,
        names="Tipo de Gasto",
        values="Monto",
        color="Tipo de Gasto",
        hole=0.3,
        title="Gastos por categoría"
    )
    st.plotly_chart(fig, use_container_width=True)
