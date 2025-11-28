import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.datavalidation import DataValidation

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

    # Seleccionar columnas
    df = df[columnas].copy()

    # Convertir fechas
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
    # Estado pago por defecto = Pagado
    # ------------------------------
    df["Estado Pago"] = "Pagado"

    # ------------------------------
    # Cálculo compensación
    # ------------------------------
    df["Minutes Creation - Pickup"] = pd.to_numeric(
        df["Minutes Creation - Pickup"], errors="coerce"
    )

    df["Monto a Reembolsar"] = df["Minutes Creation - Pickup"].apply(calcular_compensacion)

    # Eliminar registros con compensación = 0
    df = df[df["Monto a Reembolsar"] > 0]

    if df.empty:
        st.warning("⚠️ No quedan registros con compensación > 0.")
        st.stop()

    # Mostrar en pantalla
    st.subheader("📊 Registros procesados")
    st.dataframe(df, use_container_width=True)

    # ------------------------------
    # Crear Excel con COMBOBOX
    # ------------------------------
    output = BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Compensaciones"

    # Escribir DataFrame en Excel
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Crear validación de datos (lista desplegable)
    dv = DataValidation(
        type="list",
        formula1='"Pagado,No Pagado"',
        allow_blank=False
    )

    # Agregar validación a toda la columna "Estado Pago"
    col_estado_pago = df.columns.get_loc("Estado Pago") + 1  
    # +1 porque Excel indexa desde 1, no desde 0

    dv.ranges.append(f"{chr(64 + col_estado_pago)}2:{chr(64 + col_estado_pago)}1048576")
    ws.add_data_validation(dv)

    wb.save(output)
    output.seek(0)

    # ------------------------------
    # Botón para descargar Excel
    # ------------------------------
    st.download_button(
        "⬇️ Descargar Excel con selector de Pagado / No Pagado",
        data=output,
        file_name="compensaciones_losa.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Sube un archivo CSV para comenzar.")



