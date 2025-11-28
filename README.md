# 📦 Aplicación de Compensaciones por Tiempo en Losa

Esta aplicación permite cargar un archivo CSV con información de reservas y generar un reporte filtrado con:

- Selección automática de columnas relevantes  
- Filtro por fecha (rango de fechas)  
- Selección de estado de pago (Pagado / No Pagado)  
- Cálculo automático del monto a reembolsar según reglas de negocio  
- Descarga del archivo final procesado  

---

## 🚀 Funcionalidades

### ✔️ Columnas seleccionadas automáticamente
La aplicación toma solo los siguientes atributos:

- Day of tm_start_local_at  
- Segmento Tiempo en Losa  
- End State  
- id_reservation_id  
- Service Channel  
- Minutes Creation - Pickup  
- User Fullname  
- User Phone Number  

### ✔️ Filtro por fecha  
Basado en **Day of tm_start_local_at**.

### ✔️ Estado de pago (combobox)  
Agrega un campo adicional:  
- Pagado  
- No Pagado  

### ✔️ Cálculo de compensación  
Reglas:

| Minutes Creation - Pickup | Monto |
|--------------------------|--------|
| >= 35 y < 40             | $3.000 |
| >= 40 y < 50             | $6.000 |
| ≥ 50                     | $9.000 |
| Null                     | $9.000 |

### ✔️ Exportación  
Descarga en formato CSV procesado.

---

## 🛠️ Instalación

```bash
pip install -r requirements.txt
