import streamlit as st
import pandas as pd

# ID del Google Sheet
sheet_id = "1ZvI0Svvj12hCcMmVFg9uE7dL80p5BP76cjoyEbjihek"
sheet_name = "Sheet1"  # Cambia esto si tu hoja tiene otro nombre

# URL de exportación como CSV
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Leer los datos
df = pd.read_csv(url)

# Mostrar en Streamlit
st.title("Dashboard de Finanzas")
st.write("Datos desde Google Sheets:")
st.dataframe(df)
