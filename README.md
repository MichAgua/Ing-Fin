# The Financial Analyst - Palantir Edition 📊🧠

Bienvenido a **The Financial Analyst - Palantir Edition**, una aplicación interactiva desarrollada con Streamlit que ofrece un análisis financiero profundo y visualmente atractivo de **Palantir Technologies (ticker: PLTR)**.

Esta herramienta fue diseñada con una interfaz temática inspirada en Palantir, integrando gráficos, simulaciones y métricas financieras esenciales para inversionistas, estudiantes de finanzas o curiosos del mercado.

## 🎯 Objetivo del proyecto

Esta aplicación fue desarrollada como parte de un proyecto académico para demostrar habilidades en análisis financiero, desarrollo web con Python y visualización de datos. 

## ⚠️ Limitaciones

Esta aplicación fue diseñada exclusivamente para analizar **Palantir Technologies (ticker: PLTR)**. El ingreso de otros tickers no está habilitado en esta versión.

## 🚀 Características principales

- Visualización del logo, nombre, país, sector e industria de Palantir.
- Explicación interactiva y detallada de:
  - Beta
  - Forward PE
  - Price to Book con comparativa sectorial
  - Capitalización de mercado
  - Rendimiento de dividendos
- Gráfico histórico del precio de la acción (últimos 5 años)
- Cálculo de CAGR (rendimientos anualizados) a 1, 3 y 5 años
- Volatilidad histórica anualizada
- **Simulación de Monte Carlo** con selector de días para estimar precios futuros

## 🛠 Tecnologías utilizadas

- **Streamlit**
- **Python**
- **yFinance**
- **Pandas / NumPy**
- **Seaborn / Matplotlib**
- Estilizado con CSS y Google Fonts (`Share Tech Mono`)

## 📦 Requisitos

Asegúrate de tener instaladas las siguientes librerías. Puedes instalar todas con:

```bash
pip install -r requirements.txt
```

Contenido del `requirements.txt`:

```
streamlit
yfinance
pandas
numpy
matplotlib
seaborn
```

## ▶️ ¿Cómo ejecutarlo?

## ☁️ Despliegue en Streamlit Cloud

Puedes acceder a la app en línea en el siguiente enlace:

🔗 [https://ing-fin-pltr-up.streamlit.app/]

## 📂 Estructura del proyecto

```
📁 proyecto-streamlit-finanzas/
├── app.py
├── requirements.txt
└── README.md
```

## 👤 Autor

Desarrollado por [Michel H] como parte de un proyecto académico para análisis financiero aplicado.

---

> 💡 Nota: Esta app fue diseñada exclusivamente para analizar el ticker **PLTR**. Si se ingresa otro ticker, se muestra un mensaje personalizado.