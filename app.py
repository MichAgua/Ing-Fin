import streamlit as st
import yfinance as yf
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# CORRECCIÓN CLAVE: DEFINIR FUNCIONES ANTES DE USARLAS
@st.cache_data
def obtener_historial(ticker_symbol: str, periodo="5y"):
    return yf.Ticker(ticker_symbol).history(period=periodo, auto_adjust=True)

@st.cache_data
def obtener_info_ticker(ticker_symbol: str):
    return yf.Ticker(ticker_symbol).info

@st.cache_data(ttl=86400)
def obtener_cierre_spy(periodo="5y"):
    try:
        return yf.Ticker("SPY").history(period=periodo)["Close"]
    except:
        return pd.Series()

@st.cache_data
def obtener_cierre_masivo(tickers: list, periodo="3y"):
    data = {}
    for t in tickers:
        try:
            precios = yf.Ticker(t).history(period=periodo, auto_adjust=True)["Close"]
            if not precios.empty:
                data[t] = precios
        except:
            continue
    return pd.DataFrame(data)

# Configuración general de la app y estilos
st.set_page_config(page_title="The Worlds Foremost and Most Advanced Analyst", layout="wide")

st.markdown("""
<style>
    body, .main, .block-container {
        background-color: #1E1E1E;
        color: white;
    }
    input, .stButton>button, .stRadio>div, .stDataFrame {
        background-color: #2C3E50 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

symbol = st.text_input('Ingrese el ticker de la emisora')

def get_company_info(ticker):
    try:
        info = obtener_info_ticker(ticker)
        if not isinstance(info, dict) or "shortName" not in info:
            return None
        return {
            'Nombre': info.get('shortName'),
            'País': info.get('country'),
            'Sector': info.get('sector'),
            'Industria': info.get('industry'),
            'Descripción': info.get('longBusinessSummary'),
            'Beta': info.get('beta'),
            'Forward PE': info.get('forwardPE'),
            'Price to Book': info.get('priceToBook'),
            'Market Cap': info.get('marketCap'),
            'Dividend Yield': info.get('dividendYield'),
            'Dividendo por Acción': info.get('dividendRate'),
        }
    except Exception as e:
        st.error(f"Error al obtener la información de la emisora: {e}")
        return {}

if symbol:
    try:
        hist = obtener_historial(symbol)
        if hist.empty:
            st.error("No se encontraron datos históricos para este ticker.")
            st.stop()
    except Exception as e:
        st.error(f"Error al obtener los datos históricos: {e}")
        st.stop()

    try:
        info = get_company_info(symbol)
        if not info:
            st.warning("No se pudo obtener información de la empresa.")
            st.stop()
    except Exception as e:
        st.error(f"Error al obtener información: {e}")
        st.stop()

    st.subheader(f"Información Básica de {info['Nombre']}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Sector", info.get("Sector", "-"))
    col2.metric("Industria", info.get("Industria", "-"))
    col3.metric("País", info.get("País", "-"))

    st.subheader("Precio de Cierre - Histórico")
    fig, ax = plt.subplots()
    hist["Close"].plot(ax=ax, color="skyblue")
    ax.set_title(f"Precio de {symbol} - últimos 5 años")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio ($)")
    st.pyplot(fig)

    st.subheader("Estadísticas del Precio")
    st.dataframe(hist["Close"].describe())

    st.subheader("Medias Móviles")
    hist["MA50"] = hist["Close"].rolling(window=50).mean()
    hist["MA200"] = hist["Close"].rolling(window=200).mean()
    fig2, ax2 = plt.subplots()
    ax2.plot(hist["Close"], label="Precio", alpha=0.6)
    ax2.plot(hist["MA50"], label="MA 50")
    ax2.plot(hist["MA200"], label="MA 200")
    ax2.set_title("Medias Móviles")
    ax2.legend()
    st.pyplot(fig2)
