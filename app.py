import streamlit as st
import yfinance as yf
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="The Worlds Foremost and Most Advanced Analyst",layout="wide")

st.markdown("<h1 style='text-align: center;'> The Financial Analyst</h1>", unsafe_allow_html=True)
symbol = st.text_input('Ingrese el ticker de la emisora (por ejemplo, AAPL, NVDA)', 'AAPL').upper()

def get_company_info(ticker):
    try:
        info = ticker.info
        return {
        'Nombre':info.get('shortName', 'Falta de información'),
        'País': info.get('country', 'Falta de información'),
        'Sector': info.get('sector', 'Falta de información'),
        'Industria': info.get('industry', 'Falta de información'),
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
    
def calcular_cagr(precios, años):
    try:
        inicio = precios["Close"].iloc[-252*años]
        fin = precios["Close"].iloc[-1]
        return ((fin / inicio) ** (1 / años)) - 1
    except:
        return np.nan
    
if symbol:
    ticker = yf.Ticker(symbol)
    info = get_company_info(ticker)

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
    col8.markdown(f"**Price to Book:** {info['Price to Book']}")
    col9.markdown(f"**Market Cap:** {info['Market Cap']}")
    col10.markdown(f"**Dividend Yield:** {info['Dividend Yield']}")

st.markdown("### Gráfico de precios historicos (ultimos 5 años)")
st.markdown("Este grafico muestra la evolución del precio de cierre ajustado en los últimos cinco años.")
hist = ticker.history(period="5y")

import seaborn as sns

fig, ax = plt.subplots(figsize=(6, 3))
sns.lineplot(data=hist, x=hist.index, y="Close", ax=ax, color='royalblue')
ax.set_title(f"Precio Historico de Cierre - {symbol}", fontsize=14)
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio ($)")
ax.tick_params(axis='x', rotation=45)
ax.grid(True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.pyplot(fig)

st.markdown("### Rendimientos Anualizados (CAGR)")
st.markdown("Se calcula el rendimiento compuesto anual (CAGR) para los ultimos 1, 3 y 5 años:")

cagr_1 = calcular_cagr(hist, 1)
cagr_3 = calcular_cagr(hist, 3)
cagr_5 = calcular_cagr(hist, 5)

df_cagr = pd.DataFrame({
    "Periodo": ["1 año", "3 años", "5 años"],
    "Rendimiento (%)": [cagr_1, cagr_3, cagr_5]
})
df_cagr["Rendimiento (%)"] = (df_cagr["Rendimiento (%)"] * 100).round(2)
st.dataframe(df_cagr, use_container_width=True)

st.markdown("**Nota:** El rendimiento compuesto anual (CAGR) considera el precio al final y al inicio del periodo para calcular el crecimiento promedio anual.")

st.markdown("### Volatilidad historica (riesgo)")
st.markdown("La volatilidad anualizada se calcula usando al desviación estandar de los rendimientos diarios multiplicada por la raíz de 252.")

retornos = hist["Close"].pct_change().dropna()
volatilidad = retornos.std() * np.sqrt(252)

st.markdown(f"**Volatilidad anualizada:** {round(volatilidad * 100, 2)}%")
st.markdown("Este valor representa la variabilidad histórica del precio del activo. Una mayor volatilidad indica mayor riesgo.")

st.markdown("### Simulación de Monte Carlo")
st.markdown("""
Esta simulación estima posibles trayectorias futuras del precio basandose en la volatilidad historica y rendimiento promedio diario.
Sirve para visualizar escenarios de riesgo y retorno. 
""")

num_simulaciones = 100
dias = 252

ultimo_precio = hist["Close"].iloc[-1]
media_retornos = retornos.mean()
std_retornos = retornos.std()

simulaciones = np.zeros((dias, num_simulaciones))

for i in range(num_simulaciones):
    precios = [ultimo_precio]
    for d in range(1, dias):
        drift = media_retornos - 0.5 *std_retornos**2
        shock = np.random.normal(loc=0, scale=std_retornos)
        precio = precios[-1] * np.exp(drift + shock)
        precios.append(precio)
    simulaciones[:, i] = precios

fig_mc, ax_mc = plt.subplots(figsize=(8,4))
ax_mc.plot(simulaciones)
ax_mc.set_title(f"Simulación de Monte Carlo de precios futuros - {symbol}")
ax_mc.set_ylabel("Precio estimado ($)")
ax_mc.grid(True)

st.pyplot(fig_mc)
