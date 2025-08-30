import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Configuración del Dashboard
# -------------------------------
st.set_page_config(page_title="Dashboard de Finanzas Mensuales", layout="wide")
st.title("💰 Dashboard de Finanzas Mensuales")
st.write("Actualiza tu Google Sheet y el dashboard se actualizará automáticamente.")

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

# Convertir columna Fecha a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

# -------------------------------
# Selección de mes a mostrar
# -------------------------------
mes_seleccionado = st.selectbox(
    "Selecciona el mes",
    df['Fecha'].dt.to_period("M").sort_values(ascending=False).astype(str).unique()
)

df_mes = df[df['Fecha'].dt.to_period("M").astype(str) == mes_seleccionado]

# -------------------------------
# Totales de ingresos y gastos
# -------------------------------
total_ingresos = df_mes[df_mes['Tipo'] == "Ingreso"]['Monto'].sum()
total_gastos = df_mes[df_mes['Tipo'] == "Gasto"]['Monto'].sum()

st.metric("Total Ingresos 💵", f"{total_ingresos} €")
st.metric("Total Gastos 🛒", f"{total_gastos} €")
st.metric("Balance 🏦", f"{total_ingresos - total_gastos} €")

# -------------------------------
# Gráfico circular de gastos por categoría
# -------------------------------
df_gastos = df_mes[df_mes['Tipo'] == "Gasto"]
if not df_gastos.empty:
    df_gastos_agg = df_gastos.groupby("Categoría")['Monto'].sum().reset_index()
    fig_pie = px.pie(
        df_gastos_agg,
        names="Categoría",
        values="Monto",
        color="Categoría",
        hole=0.3,
        title=f"Gastos por categoría - {mes_seleccionado}"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------------
# Gráfico de barras de gastos
# -------------------------------
if not df_gastos.empty:
    fig_bar = px.bar(
        df_gastos_agg,
        x="Categoría",
        y="Monto",
        color="Categoría",
        title=f"Gastos por categoría (barras) - {mes_seleccionado}"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------
# Tabla interactiva de todos los movimientos
# -------------------------------
st.subheader(f"Movimientos del mes {mes_seleccionado}")
st.dataframe(df_mes.sort_values(by="Fecha", ascending=False))
