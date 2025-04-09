import streamlit as st
import yfinance as yf
import seaborn as sns
import numpy as np
import pandas as pd


st.set_page_config(page_title="The Worlds Foremost and Most Advanced Analyst",layout="wide")
st.title('The Financial Analyst')

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
    for key, value in info.items():
        st.markdown(f"**{key}**: {value}")
    