import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Compensaciones Losa", layout="wide")

st.title("📦 Aplicación de Compensaciones - Tiempo en Losa")

# ===============================
# Función para calcular compensación
# ===============================
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


# ===============================
# Cargar archivo
# ===============================
uploaded_file = st.file_uploader("📤 Sube el archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Archivo cargado correctamente 🎉")
    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
        st.stop()

    # ===============================
    # Columnas requeridas
    # ===============================
    columnas_requeridas = [
        "Day of tm_start_local_at",
        "Segmento Tiempo en Losa",
        "End State",
        "id_reservation_id",
        "Service Channel",
        "Minutes Creation - Pickup",
        "User Fullname",
        "User Phone Number"
    ]

    # Validación de columnas
    faltantes = [c for c in columnas_requeridas if c not in df.columns]

    if faltantes:
        st.error(f"❌ El CSV no contiene las columnas requeridas:\n{faltantes}")
        st.stop()

    df = df[columnas_requeridas]

    # ===============================
    # Convertir columna de fecha
    # ===============================
    df["Day of tm_start_local_at"] = pd.to_datetime(
        df["Day of tm_start_local_at"],
        errors="coerce",
        infer_datetime_format=True
    ).dt.date

    if df["Day of tm_start_local_at"].isna().all():
        st.error("❌ No se pudieron convertir las fechas. Revisa el formato del CSV.")
        st.stop()

    # ===============================
    # Filtro por rango de fechas
    # ===============================
    st.subheader("📅 Filtro por fecha")

    fecha_min = df["Day of tm_start_local_at"].min()
    fecha_max = df["Day of tm_start_local_at"].max()

    fecha_desde, fecha_hasta = st.date_input(
        "Selecciona el rango de fechas:",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )

    if fecha_desde > fecha_hasta:
        st.error("❌ La fecha inicial no puede ser mayor que la fecha final.")
        st.stop()

    df = df[(df["Day of tm_start_local_at"] >= fecha_desde) &
            (df["Day of tm_start_local_at"] <= fecha_hasta)]

    if df.empty:
        st.warning("⚠️ No hay registros en ese rango de fechas.")
        st.stop()

    # ===============================
    # Estado de pago
    # ===============================
    st.subheader("💳 Estado de Pago")

    opcion_pago = st.selectbox(
        "Selecciona estado general:",
        ["Pagado", "No Pagado"]
    )

    df["Estado Pago"] = opcion_pago

    # ===============================
    # Calcular compensaciones
    # ===============================
    df["Monto a Reembolsar"] = df["Minutes Creation - Pickup"].apply(calcular_compensacion)

    # ===============================
    # Mostrar tabla
    # ===============================
    st.subheader("📊 Resultado filtrado")
    st.dataframe(df, use_container_width=True)

    # ===============================
    # Descargar CSV
    # ===============================
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



