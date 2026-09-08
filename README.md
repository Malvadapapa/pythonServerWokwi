<div align="center">

# 🔌 API REST de Telemetría para Simulador Wokwi

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Railway%20Cloud-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Wokwi](https://img.shields.io/badge/Wokwi-IoT%20Simulation-1877F2?style=for-the-badge)](https://wokwi.com/)

<p align="center">
  <b>API REST ligera desarrollada en Flask para la ingesta y consulta de telemetría de dispositivos embebidos simulados en Wokwi, con almacenamiento persistente en PostgreSQL (Railway).</b>
</p>

[Características](#-características) • [Endpoints](#-documentación-de-endpoints) • [Instalación](#-instalación-y-despliegue) • [Autor](#-autor)

</div>

---

## 📌 Descripción

**pythonServerWokwi** proporciona una interfaz HTTP RESTful minimalista y de alto rendimiento que permite a simulaciones de hardware en **Wokwi** (como ESP32, ESP8266 o microcontroladores con soporte HTTP) reportar eventos de telemetría, estados de pines y cambios en actuadores directamente a una base de datos relacional en la nube.

---

## ✨ Características

- 🎯 **Enfoque Minimalista y Eficiente:** Arquitectura directa pensada para microcontroladores con recursos limitados de memoria y red.
- ☁️ **Cloud Native:** Configurado para conectarse sin fricción a bases de datos PostgreSQL hosteadas en **Railway**.
- 📋 **Gestión de Contexto Seguro:** Utiliza context managers de Python (`with connect_db() as conn:`) para garantizar el cierre correcto de transacciones y pools de conexiones.
- 📦 **Formato JSON Estándar:** Respuestas y solicitudes estructuradas en formato JSON con códigos de estado HTTP semánticos (`200 OK`, `500 Internal Error`).

---

## 📡 Documentación de Endpoints

### 1. Consultar Histórico de Telemetría
- **Ruta:** `/get_data`
- **Método:** `GET`
- **Descripción:** Obtiene todos los eventos y estados registrados.
- **Respuesta:**
```json
[
  {
    "id": 1,
    "timestamp": "2024-03-08T12:00:00Z",
    "led_status": true
  },
  {
    "id": 2,
    "timestamp": "2024-03-08T12:01:30Z",
    "led_status": false
  }
]
```

### 2. Registrar Nuevo Evento
- **Ruta:** `/add_data`
- **Método:** `POST`
- **Encabezados:** `Content-Type: application/json`
- **Cuerpo (Payload):**
```json
{
  "led_status": true
}
```
- **Respuesta:**
```json
{
  "message": "Data added successfully"
}
```

---

## 🗂️ Estructura del Proyecto

```bash
pythonServerWokwi/
│
├── main.py             # Definición de rutas Flask, conexión a PostgreSQL y controladores
├── requirements.txt    # Dependencias del entorno (Flask, psycopg2-binary, etc.)
├── config.env          # Variables de entorno y cadenas de conexión seguras
└── README.md           # Documentación técnica
```

---

## 🚀 Instalación y Despliegue

### 1. Clonar el repositorio
```bash
git clone https://github.com/Malvadapapa/pythonServerWokwi.git
cd pythonServerWokwi
```

### 2. Entorno virtual e instalación
```bash
python -m venv venv
.\venv\Scripts\activate       # En Windows
source venv/bin/activate      # En Linux/macOS

pip install -r requirements.txt
```

### 3. Configuración del entorno
Configura la variable `DATABASE_URL` en tu archivo `.env`:
```env
DATABASE_URL=postgresql://postgres:password@host.railway.net:port/railway
```

### 4. Ejecución
```bash
python main.py
```

---

## 👨‍💻 Autor

**Cristian Isaac Vargas**  
- GitHub: [@Malvadapapa](https://github.com/Malvadapapa)  
- LinkedIn: [Cristian Isaac Vargas](https://www.linkedin.com/in/cristian-vargas-npm/)  

---

## 📄 Licencia

Distribuido bajo la Licencia MIT.
