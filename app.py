import streamlit as st
import yfinance as yf
import seaborn as sns
import numpy as np
import pandas as pd


st.set_page_config(page_title="The Worlds Foremost and Most Advanced Analyst",layout="wide")

st.markdown("<h1 style='text-align: center;'> The Financial Analyst</h1>", unsafe_allowed_html=True)
symbol = st.text_input('Ingrese el ticker de la emisora (por ejemplo, AAPL, NVDA)', 'AAPL')

def get_company_info(ticker):
    try:
        info = ticker.info
        return {
        'Nombre':info.get('shortName', 'Falta de información'),
        'País': info.get('country', 'Falta de información'),
        'Sector': info.get('sector', 'Falta de información'),
        'Industria': info.get('industria', 'Falta de información'),
        'Descripción': info.get('longBusinessSummary', 'Falta de información'),
        'Beta': info.get('beta', 'Falta de información'),
        'Forward PE': info.get('forwardPE', 'Falta de información'),
        'Price to Book': info.get('priceToBook', 'Falta de información'),
        'Market Cap': info.get('marketCap', 'Falta de información'),
        'Dividend Yield': info.get('dividendYield', 'Falta de información')
        }
    except Exception as e:
        st.error(f'Error al obtener la información de la emisora: {e}')
        return {}
    
if symbol:
    info = get_company_info(yf.Ticker(symbol))

    st.markdown("### Información Básica")
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Nombre:** {info['Nombre']}")
    col2.markdown(f"**País:** {info['País']}")
    col3.markdown(f"**Sector:** {info['Sector']}")

    st.markdown("### Infustria y Descripción")
    col4, col5 = st.columns([1, 2])
    col4.markdown(f"**Industria:** {info['Industria']}")
    col5.markdown(f"**Descripción:** {info['Descripción']}")
    
    st.markdown ("### Indicadores financieros")
    col6, col7, col8, col9, col10 = st.columns(5)
    col6.markdown(f"**Beta:** {info['Beta']}")
    col7.markdown(f"**Forward PE:** {info['Forward PE']}")
    col8.markdown()
                
    