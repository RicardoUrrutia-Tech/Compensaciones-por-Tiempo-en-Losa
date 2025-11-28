import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Compensaciones por Tiempo en Losa", layout="wide")

st.title("📦 Compensaciones por Tiempo en Losa")

# ------------------------------
# Función para calcular compensación
# ------------------------------
def calcular_compensacion(minutos):
    if pd.isna(minutos):
        return 9000
    try:
        minutos = float(minutos)
    except:
        return 9000

    if minutos >= 50:
        return 9000
    elif minutos >= 40:
        return 6000
    elif minutos >= 35:
        return 3000
    else:
        return 0


# ------------------------------
# Subir archivo CSV
# ------------------------------
uploaded_file = st.file_uploader("📤 Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:

    # Leer CSV en modo seguro
    try:
        df = pd.read_csv(uploaded_file, dtype=str)
        st.success("Archivo cargado correctamente 🎉")
    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
        st.stop()

    # Columnas necesarias
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

    # Validar columnas
    faltantes = [c for c in columnas if c not in df.columns]
    if faltantes:
        st.error(f"❌ Faltan columnas requeridas: {faltantes}")
        st.stop()

    # Seleccionar solo columnas requeridas
    df = df[columnas].copy()

    # Convertir fecha
    df["Day of tm_start_local_at"] = pd.to_datetime(
        df["Day of tm_start_local_at"],
        errors="coerce"
    ).dt.date

    if df["Day of tm_start_local_at"].isna().all():
        st.error("❌ Las fechas no se pudieron convertir. Verifica el formato.")
        st.stop()

    # ------------------------------
    # Filtro de fechas
    # ------------------------------
    st.subheader("📅 Filtro de fechas")

    fecha_min = df["Day of tm_start_local_at"].min()
    fecha_max = df["Day of tm_start_local_at"].max()

    fecha_desde, fecha_hasta = st.date_input(
        "Selecciona rango de fechas:",
        value=(fecha_min, fecha_max)
    )

    if fecha_desde > fecha_hasta:
        st.error("❌ La fecha inicial no puede ser mayor que la final.")
        st.stop()

    df = df[
        (df["Day of tm_start_local_at"] >= fecha_desde) &
        (df["Day of tm_start_local_at"] <= fecha_hasta)
    ]

    if df.empty:
        st.warning("⚠️ No hay registros en ese rango de fechas.")
        st.stop()

    # ------------------------------
    # Estado de Pago (combobox)
    # ------------------------------
    st.subheader("💳 Estado de Pago para TODOS los registros")

    estado_pago = st.selectbox(
        "Selecciona estado de pago aplicado a todos los registros:",
        ["Pagado", "No Pagado"]
    )

    df["Estado Pago"] = estado_pago

    # ------------------------------
    # Cálculo compensación
    # ------------------------------
    df["Minutes Creation - Pickup"] = pd.to_numeric(
        df["Minutes Creation - Pickup"], errors="coerce"
    )

    df["Monto a Reembolsar"] = df["Minutes Creation - Pickup"].apply(calcular_compensacion)

    # Eliminar registros con compensación 0
    df = df[df["Monto a Reembolsar"] > 0]

    if df.empty:
        st.warning("⚠️ No quedan registros con compensación > 0.")
        st.stop()

    # Mostrar resultado
    st.subheader("📊 Registros procesados")
    st.dataframe(df, use_container_width=True)

    # ------------------------------
    # Descargar CSV
    # ------------------------------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Descargar CSV procesado",
        data=csv,
        file_name="compensaciones_filtrado.csv",
        mime="text/csv"
    )

else:
    st.info("Sube un archivo CSV para comenzar.")



