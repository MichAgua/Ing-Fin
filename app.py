import streamlit as st
import yfinance as yf
import seaborn as sns
import numpy as np
import pandas as pd


st.set_page_config(page_title="The Worlds Foremost and Most Advanced Analyst",layout="wide")
st.title('The Financial Analyst')

symbol = st.text_input('Ingrese el ticker de la emisora (por ejemplo, AAPL, NVDA)', 'AAPL')

def get_company_info(ticker)
    try:
        info = ticker.info
        return{
            'Nombre'
info.get('shortName', 'Falta de información'),
        'País': info.get('country', 'Falta de información')
        'Sector': info.get('sector', 'Falta de información')
        'Industria': info.get('industria', 'Falta de información')
        }