import streamlit as st
import yfinance as yf
import seaborn as sns
import numpy as np
import pandas as pd


st.set_page_config(page_title="The Worlds Foremost and Most Advanced Analyst",layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #f0f8ff;
        }

        .info-box {
            padding: 1rem;
            border-radius: 12px;
            background: linear-gradient(135deg, #e0f8ec, #daf6f0);
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
            animation: fadeIn 0.5s ease-in-out;
        }

        .info-box h4 {
            margin-bottom: 0.5rem;
            color: #075e54;
        }

        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }

        .title-text {
            text-align: center;
            font-size: 2.5em;
            color: #075e54;
            margin-bottom: 1rem;
        }

        .subtitle {
            color: #218380;
            font-weight: 600;
            font-size: 1.2em;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("<div class='title-text'>📊 The Financial Analyst</div>", unsafe_allow_html=True)
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

    # Section: Basic Info
    st.markdown("<div class='subtitle'>📌 Información Básica</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class='info-box'>
                <h4>Nombre</h4>{info['Nombre']}
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class='info-box'>
                <h4>País</h4>{info['País']}
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class='info-box'>
                <h4>Sector</h4>{info['Sector']}
            </div>
        """, unsafe_allow_html=True)

    # Section: Industry + Description
    st.markdown("<div class='subtitle'>🏷️ Industria y Descripción</div>", unsafe_allow_html=True)
    col4, col5 = st.columns([1, 2])
    with col4:
        st.markdown(f"""
            <div class='info-box'>
                <h4>Industria</h4>{info['Industria']}
            </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
            <div class='info-box'>
                <h4>Descripción</h4>{info['Descripción']}
            </div>
        """, unsafe_allow_html=True)

    # Section: Financial Indicators
    st.markdown("<div class='subtitle'>📊 Indicadores Financieros</div>", unsafe_allow_html=True)
    col6, col7 = st.columns(2)
    with col6:
        st.markdown(f"""
            <div class='info-box'>
                <h4>Beta</h4>{info['Beta']}
            </div>
        """, unsafe_allow_html=True)
    with col7:
        st.markdown(f"""
            <div class='info-box'>
                <h4>Forward PE</h4>{info['Forward PE']}
            </div>
        """, unsafe_allow_html=True)
                
    