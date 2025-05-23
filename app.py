import streamlit as st
import yfinance as yf
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="The Worlds Foremost and Most Advanced Analyst",layout="wide")

st.markdown("""
    <style>
        /* Fondo principal oscuro */
        .main {
            background-color: #1E1E1E;
        }
        /* Encabezados y texto */
        h1, h2, h3, h4, h5, h6, p, div {
            color: #FFFFFF !important;
        }
        /* Input de texto (ticker) */
        input {
            background-color: #2C3E50 !important;
            color: white !important;
            border: 1px solid #4B5563;
        }
        /* Botones y radio buttons */
        .stButton>button {
            background-color: #2C3E50;
            color: white;
            border: 1px solid #4B5563;
        }
        .stRadio > div {
            color: white;
        }
        /* Tablas */
        .stDataFrame {
            background-color: #2C3E50;
            color: white;
        }
        /* Cuadros y contenedores */
        .block-container {
            padding-top: 2rem;
            background-color: #1E1E1E;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Share Tech Mono', monospace;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white;'> The Financial Analyst </h1>", unsafe_allow_html=True)

def caja_palantir(texto):
    st.markdown(
        f"""
        <div style='
            background-color: #E5E7EB;
            padding: 1rem;
            border-left: 4px solid #2C3E50;
            border-radius: 8px;
            margin-bottom: 1rem;
            font-size: 15px;
        '>
            {texto}
        </div>
        """, unsafe_allow_html=True)

symbol = st.text_input('Ingrese el ticker de la emisora')

@st.cache_data(ttl=86400)
def get_company_info(ticker_symbol: str):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        if not isinstance(info, dict) or "shortName" not in info:
            return {"error": "Ticker no válido o sin información disponible."}

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
        'Dividend Yield': info.get('dividendYield', 'Falta de información'),
        'Dividendo por Acción': info.get('dividendRate', 'Falta de información'),
        }
    except Exception as e:
        st.error(f'Error al obtener la información de la emisora: {e}')
        return {}
info = get_company_info(symbol)

if symbol:
    info = get_company_info(symbol)
    
    if symbol == 'HACK':
        st.markdown("<h1 style='color: lime;'>Sistema Infiltrado</h1>", unsafe_allow_html=True)
        st.balloons()
        st.stop()

    if "error" in info:
        st.error(f"Error al obtener la información: {info['error']}")
        st.stop()

    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="5y")
    if hist.empty:
        st.error("No se encontraron datos históricos para este ticker.")
        st.stop()

def limpiar_valor(valor):
    if valor in [None, ..., Ellipsis]:
        return "No disponible"
    return valor

if symbol:
    if symbol == 'HACK':
        st.markdown("<h1 style='color: lime;'>Sistema Infiltrado</h1>", unsafe_allow_html=True)
        st.balloons()
        st.stop()

    try:
        ticker = yf.Ticker(symbol)
        info = get_company_info(ticker)

        if not info or info is None:
            raise ValueError("No se pudo obtener la información del ticker.")
    except Exception as e:
        st.error(f"Error al obtener la información de la emisora: {e}")
        st.stop()

    try:
        hist = ticker.history(period="5y")
        if hist.empty:
            st.error("No se encontraron datos históricos para este ticker.")
            st.stop()
    except Exception as e:
        st.error(f"Error al obtener datos históricos: {e}")
        st.stop()

    except Exception as e:
        st.error(f"Error al obtener la información de la emisora: {e}")
        st.stop()

st.markdown("""
    <style>
        body {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .main {
            background-color: #1E1E1E;
        }
        h1, h2, h3, h4 {
            color: #FFFFFF;
        }
        .stTextInput>div>div>input {
            background-color: #2C3E50;
            color: white;
        }
        .stradio>div {
            color: white;
        }
        .css-1d391kg { /* scrollable container (default streamlit container class) */
            background-color: #2C3E50
        }
        .stDataFrame {
            background-color: #2C3E50;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)
    
def calcular_cagr(precios, años):
    try:
        inicio = precios["Close"].iloc[-252*años]
        fin = precios["Close"].iloc[-1]
        return ((fin / inicio) ** (1 / años)) - 1
    except:
        return np.nan
    
def formato_dinero(valor):
    try:
        if valor >= 1e15:
            return f"{valor / 1e16: .2f} trillones USD"
        elif valor >= 1e12:
            return f"{valor / 1e12: .2f} billones USD"
        elif valor >= 1e9:
            return f"{valor / 1e9: .2f} mil millones USD"
        elif valor >= 1e6:
            return f"{valor / 1e6: .2f} millones USD"
        else:
            return f"${valor:,.2f}"
    except:
        return "N/A"
    
def interpretar_forward_pe(pe):
    try:
        pe = float(pe)
    except:
        return "No Disponible"
    if pe < 10:
        return "Muy bajo (posible infravaloración o riesgo)"
    elif 10 <= pe <= 20:
        return "Rango Saludable"
    elif 20 < pe <= 40:
        return "Expectativas altas"
    else:
        return "Muy alto (hay gran riesgo si no cumple expectativas)"

def interpretar_price_to_book(pb):
    try:
        pb = float(pb)
    except:
        return "No Disponible"
    if pb <1:
        return "Bajo (posible oportunidad de inversion o problemas)"
    elif 1 <= pb <= 3:
        return "Rango Razonable"
    else:
        return "Alto (se paga una prima por crecimiento/intangibles)"
    
pb_sector_avg = {
    "Technology": 8.0,
    "Financial Services": 1.3,
    "Industrials": 2.0,
    "Consumer Defensive": 3.0,
    "Consumer Cyclical": 4.0,
    "Healthcare": 4.0,
    "Energy": 1.5,
    "Utilities": 1.2,
    "Basic Materials": 1.8,
    "Communication Services": 2.5,
    "Real Estate": 1.4,
    "Falta de información": None
}

def comparar_pb_sector(pb, sector):
    try:
        pb = float(pb)
        sector_pb = pb_sector_avg.get(sector, None)

        if sector_pb is None:
            return "No hay promedio disponible para el sector"

        diferencia = pb - sector_pb
        if diferencia < -0.5:
            return f"Bajo vs. su sector (prom: {sector_pb}) – Podría estar infravalorada"
        elif -0.5 <= diferencia <= 0.5:
            return f"En línea con su sector (prom: {sector_pb})"
        else:
            return f"Alto vs. su sector (prom: {sector_pb}) – Mercado espera crecimiento o intangibles"
    except:
        return "Información no disponible"
    
if symbol:
    ticker = yf.Ticker(symbol)
    
    hist = ticker.history(period="5y")

    seccion = st.radio(
    "Selecciona lo que te gustaria visualizar:",
    (
        "Información Basica",
        "Industria y Descripción",
        "Indicadores Financieros",
        "Gráfico de Precios Historicos",
        "Rendimientos CAGR",
        "Volatilidad Histórica",
        "Simulación de Monte Carlo",
        "Análisis Estadístico",
        "Comparación Contra Índice",
        "Medias Móviles",
        "Cartera Eficiente"
    ),
    horizontal=True
)

    if seccion == "Información Basica":
        st.markdown(f"### {info.get('Nombre', 'Nombre no disponible')}")
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Nombre:** {info['Nombre']}")
        col2.markdown(f"**País:** {info['País']}")
        col3.markdown(f"**Sector:** {info['Sector']}")

    elif seccion == "Industria y Descripción":
        st.markdown("### Industria y Descripción")
        col4, col5 = st.columns([1, 2])
        col4.markdown(f"**Industria:** {info['Industria']}")
        col5.markdown(f"**Descripción:** {info['Descripción']}")
    
    elif seccion == "Indicadores Financieros":    
        st.markdown ("### Indicadores Financieros")
        col6, col7, col8, col9, col10 = st.columns(5)
        with col6:
            st.markdown(f"**Beta:** {info['Beta']}")
            st.markdown(
                "<div style='text-align: center; font size 12px; '>Mide la volatilidad comparada con el mercado (1.0 = promedio)</div",
            unsafe_allow_html=True)

        with col7:
            forward_pe = info['Forward PE']
            interpretacion_pe = interpretar_forward_pe(forward_pe)
            st.markdown(f"**Forward PE:** {forward_pe}")
            st.markdown(str(interpretacion_pe))

        with col8:
            pb = info['Price to Book']
            st.markdown(f"**Price to Book:** {pb}")
            st.markdown(interpretar_price_to_book(pb))
            st.markdown(comparar_pb_sector(pb, info['Sector']))


        with col9:
            st.markdown(f"**Market Cap:** {formato_dinero(info['Market Cap'])}")
            st.markdown(
                "<div style='text-align: center; font size 12px; '>Valor total de mercado de la empresa</div",
            unsafe_allow_html=True)

        with col10:
            dy = info['Dividend Yield']
            dr = info.get('dividendRate', None)

            dy_pct = f"{round(dy * 100, 2)}%" if isinstance(dy, (float, int)) else dy
            dr_texto = f"${round(dr, 2)} por acción" if isinstance(dr, (float, int)) else "No Disponible"

            st.markdown(f"**Dividend Yield:** {dy_pct}")
            st.markdown(f"**Dividendo por acción:$** {dy}")
            st.markdown(
                "<div style='text-align: center; font size 12px; '>Porcentaje del precio pagado como dividendo anual</div",
            unsafe_allow_html=True)

    elif seccion == "Gráfico de Precios Historicos":
        st.markdown("### Gráfico de precios historicos (ultimos 5 años)")
        st.markdown("Este grafico muestra la evolución del precio de cierre ajustado en los últimos cinco años.")
        hist = ticker.history(period="5y")

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

    elif seccion == "Rendimientos CAGR":
        st.markdown("### Rendimientos Anualizados (CAGR)")
        st.markdown("Se calcula el rendimiento compuesto anual (CAGR) para los ultimos 1, 3 y 5 años:")
        st.markdown("Este cálculo considera el precio al inicio y al final del periodo para determinar el rendimiento anualizado")

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

    elif seccion == "Volatilidad Histórica":
        st.markdown("### Volatilidad historica (riesgo)")
        st.markdown("La volatilidad anualizada se calcula usando al desviación estandar de los rendimientos diarios multiplicada por la raíz de 252.")

        retornos = hist["Close"].pct_change().dropna()
        volatilidad = retornos.std() * np.sqrt(252)

        st.markdown(f"**Volatilidad anualizada:** {round(volatilidad * 100, 2)}%")
        st.markdown("Este valor representa la variabilidad histórica del precio del activo. Una mayor volatilidad indica mayor riesgo.")

    elif seccion == "Simulación de Monte Carlo":
        st.markdown("### Simulación de Monte Carlo")
        st.markdown("""
        Esta simulación estima posibles trayectorias futuras del precio basandose en la volatilidad historica y rendimiento promedio diario.
        Sirve para visualizar escenarios de riesgo y retorno. 
        """)

        retornos = hist["Close"].pct_change().dropna()
        num_simulaciones = 100
        dias = st.slider("Selecciona el número de días a simular", 30, 365, 252)

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

    elif seccion == "Análisis Estadístico":
        st.markdown("### Análisis estadístico del precio de cierre")
        st.write("Este análisis resume el comportamiento histórico del precio.")

        resumen = hist["Close"].describe()
        st.write(resumen)

        fig_stats, ax_stats = plt.subplots()
        sns.histplot(hist["Close"], kde=True, ax=ax_stats)
        ax_stats.set_title("Distribución de precios de cierre")
        st.pyplot(fig_stats)

    elif seccion == "Comparación Contra Índice":
        st.markdown("### Comparación contra S&P 500")
        st.write("Se compara el rendimiento del ticker con el índice SPY.")

        spy = yf.Ticker("SPY").history(period="5y")["Close"]
        merged = pd.DataFrame({
            symbol: hist["Close"],
            "SPY": spy
        }).dropna()

        normalized = merged / merged.iloc[0] * 100

        fig_cmp, ax_cmp = plt.subplots()
        normalized.plot(ax=ax_cmp)
        ax_cmp.set_title(f"Comparación de {symbol} contra SPY")
        ax_cmp.set_ylabel("Precio Normalizado")
        st.pyplot(fig_cmp)