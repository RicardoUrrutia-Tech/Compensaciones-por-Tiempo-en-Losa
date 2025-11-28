import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Compensaciones Losa", layout="wide")

st.title("📦 Aplicación de Compensaciones - Tiempo en Losa")

# --- Función para calcular compensación ---
def calcular_compensacion(minutos):
    if pd.isna(minutos):
        return 9000
    if minutos >= 50:
        return 9000
    if minutos >= 40:
        return 6000
    if minutos >= 35:
        return 3000
    return 0

# --- Subir archivo ---
uploaded_file = st.file_uploader("📤 Sube el archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Archivo cargado correctamente 🎉")

    # --- Seleccionar columnas relevantes ---
    columnas = [
        "Day of tm_start_local_at",
        "Segmento Tiempo en Losa",
        "End State",
        "id_reservation_id",
        "Service Channel",
        "Minutes Creation - Pickup",
        "User Fullname",
        "User Phone Number"
    ]
    
    df = df[columnas]

    # --- Convertir fecha ---
    df["Day of tm_start_local_at"] = pd.to_datetime(df["Day of tm_start_local_at"], errors="coerce").dt.date

    # --- Filtros de fechas ---
    st.subheader("📅 Filtro por fecha")

    fecha_min = df["Day of tm_start_local_at"].min()
    fecha_max = df["Day of tm_start_local_at"].max()

    fecha_desde, fecha_hasta = st.date_input(
        "Selecciona el rango de fechas:",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )

    df = df[(df["Day of tm_start_local_at"] >= fecha_desde) & (df["Day of tm_start_local_at"] <= fecha_hasta)]

    # --- Combobox Pagado / No Pagado ---
    st.subheader("💳 Estado de Pago")
    opcion_pago = st.selectbox("Selecciona estado general:", ["Pagado", "No Pagado"])

    df["Estado Pago"] = opcion_pago

    # --- Calcular compensación ---
    df["Monto a Reembolsar"] = df["Minutes Creation - Pickup"].apply(calcular_compensacion)

    st.subheader("📊 Resultado filtrado")
    st.dataframe(df, use_container_width=True)

    # --- Descargar Excel ---
    @st.cache_data
    def convert_to_csv(df):
        return df.to_csv(index=False).encode("utf-8")

    csv_final = convert_to_csv(df)

    st.download_button(
        label="⬇️ Descargar CSV procesado",
        data=csv_final,
        file_name="compensaciones_filtrado.csv",
        mime="text/csv"
    )

else:
    st.info("Por favor sube un archivo CSV para comenzar.")


