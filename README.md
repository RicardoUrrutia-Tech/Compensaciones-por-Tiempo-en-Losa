# 📦 Aplicación de Compensaciones por Tiempo en Losa

Esta aplicación en Streamlit permite cargar un archivo CSV y generar un reporte de compensaciones según el tiempo transcurrido entre la creación y el retiro de una reserva.

---

## 🚀 Funcionalidades

### ✔️ Selección automática de columnas relevantes
El sistema toma solo los siguientes campos del CSV:

- Day of tm_start_local_at  
- Segmento Tiempo en Losa  
- End State  
- id_reservation_id  
- Service Channel  
- Minutes Creation - Pickup  
- User Fullname  
- User Phone Number  

### ✔️ Filtro por rango de fechas
Basado en `Day of tm_start_local_at`.

### ✔️ Estado de pago (Pagado / No Pagado)
Agrega un campo editable para todos los registros.

### ✔️ Cálculo automático del monto a reembolsar

| Condición | Monto |
|----------|--------|
| ≥ 35 y < 40 min | $3.000 |
| ≥ 40 y < 50 min | $6.000 |
| ≥ 50 min | $9.000 |
| Null | $9.000 |
| < 35 min | excluido del reporte |

**Solo se incluyen registros con compensación > 0.**

### ✔️ Descarga de archivo procesado
Se genera un CSV listo para reportes.

---

## 🛠️ Instalación

```bash
pip install -r requirements.txt
