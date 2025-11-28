import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Compensaciones Losa", layout="wide")

st.title("📦 Aplicación de Compensaciones - Tiempo en Losa")

# -------- Función para calcular compensación --------
def calcular_compensacion(minutos):
    try:
        if pd.isna(minutos):
            return 9000
        minutos = float(minutos)
        if minutos >= 50:
            return 9000
        elif minutos >= 40:
            return 6000
        elif minutos >= 35:
            return 3000
        else:
            return 0
    except:
        return 9000


# -------- Subir archivo --------
uploaded_file = st.file_uploader("📤 Sube el archivo CSV", type=["csv"])

if uploaded_file is not None:

    # ---- Leer CSV con máxima compatibilidad ----
    try:
        df = pd.read_csv(uploaded_file, dtype=str)  # todo como texto para evitar errores
        st.success("Archivo cargado correctamente 🎉")
    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
        st.stop()

    # ---- Columnas requeridas ----
    columnas = [
        "Day of tm_start_local_at",
        "Segmento Tiempo en Losa",
        "End State",
        "id_reservation_id",
        "Service Channel",
        "Minutes Creation - Pickup",
        "User Fullname",
        "User Phone Number",
    ]

    # Validación
    faltantes = [c for c in columnas if c not in df.columns]
    if faltantes:
        st.error(f"❌ Faltan columnas requeridas:\n{faltantes}")
        st.stop()

    # ---- Trabajar solo con las columnas necesarias ----
    df = df[columnas].copy()

    # ---- Convertir fechas ----
    try:
        df["Day of tm_start_local_at"] = pd.to_datetime(
            df["Day of tm_start_local_at"],
            errors="coerce"
        ).dt.date
    except:
        st.error("❌ No se pudo convertir la columna de fechas.")
        st.stop()

    if df["Day of tm_start_local_at"].isna().all():
        st.error("❌ Ninguna fecha es válida. Revisa el formato.")
        st.stop()

    # ---- Seleccionar rango de fechas ----
    st.subheader("📅 Filtrar por fecha")

    fecha_min = df["Day of tm_start_local_at"].min()
    fecha_max = df["Day of tm_start_local_at"].max()

    fechas = st.date_input(
        "Selecciona un rango de fechas:",
        value=(fecha_min, fecha_max),
    )

    if isinstance(fechas, tuple) and len(fechas) == 2:
        df = df[(df["Day of tm_start_local_at"] >= fechas[0]) &
                (df["Day of tm_start_local_at"] <= fechas[1])]
    else:
        st.error("❌ Debes seleccionar un rango de fechas válido.")
        st.stop()

    if df.empty:
        st.warning("⚠️ No hay datos en el rango seleccionado.")
        st.stop()

    # ---- Estado de pago ----
    st.subheader("💳 Estado de Pago")

    pago = st.selectbox("Selecciona estado general:", ["Pagado", "No Pagado"])
    df["Estado Pago"] = pago

    # ---- Calcular compensación ----
    df["Minutes Creation - Pickup"] = pd.to_numeric(
        df["Minutes Creation - Pickup"], errors="coerce"
    )
    df["Monto a Reembolsar"] = df["Minutes Creation - Pickup"].apply(calcular_compensacion)

    # ---- Mostrar tabla ----
    st.subheader("📊 Resultado")
    st.dataframe(df, use_container_width=True)

    # ---- Descargar CSV ----
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar CSV procesado",
        data=csv,
        file_name="compensaciones_filtrado.csv",
        mime="text/csv"
    )

else:
    st.info("Sube un archivo CSV para comenzar.")



