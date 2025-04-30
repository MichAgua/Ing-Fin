import streamlit as st
import yfinance as yf
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def limpiar_valor(valor):
    if valor in [None, ..., Ellipsis]:
        return "No disponible"
    return valor

def get_company_info(ticker):
    try:
        info = obtener_info_ticker(symbol)
        if not isinstance(info, dict) or "shortName" not in info:
            return None
        ...
        
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

if symbol:
    if symbol == 'HACK':
        st.markdown("<h1 style='color: lime;'>Sistema Infiltrado</h1>", unsafe_allow_html=True)
        st.balloons()
        st.stop()

    if not symbol.strip():
        st.warning("⚠️ Ingresa un ticker válido antes de continuar.")
        st.stop()

    try:
        hist = obtener_historial(symbol)
        if hist is None or hist.empty or len(hist) < 10:
            st.error("No se encontraron datos históricos para este ticker. Verifica que el símbolo sea correcto y exista en Yahoo Finance.")
            st.stop()
    except Exception as e:
        if "rate limit" in str(e).lower():
            st.warning("Yahoo Finance está limitando las consultas. Espera unos minutos y vuelve a intentarlo.")
        else:
            st.error(f"Error al obtener el historial: {e}")
        st.stop()

    try:
        info = get_company_info(symbol)
        if not info:
            raise ValueError("No se pudo obtener la información del ticker.")
    except Exception as e:
        st.error(f"Error al obtener la información de la emisora: {e}")
        st.stop()
    try:
        if not info or info is None:
            raise ValueError("No se pudo obtener la información del ticker.")

        if hist is None or hist.empty:
            raise ValueError("No se encontraron datos históricos para este ticker.")

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
    
    info = get_company_info(symbol)

    if info is None:
        try:
            info = obtener_info_ticker(symbol)
        except Exception as e:
            st.warning("⚠️ No se pudo cargar la información detallada. Posible límite de uso.")
            st.stop()

    if seccion == "Información Basica":
        st.markdown(f"### {info.get('Nombre', 'Nombre no disponible')}")
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Nombre:** {info['Nombre']}")
        col2.markdown(f"**País:** {info['País']}")
        col3.markdown(f"**Sector:** {info['Sector']}")

    if info is None:
        try:
            info = obtener_info_ticker(symbol)
        except Exception as e:
            st.warning("⚠️ No se pudo cargar la información detallada. Posible límite de uso.")
            st.stop()

    elif seccion == "Industria y Descripción":
        st.markdown("<h3 style='color:#4ade80'> Industria y Descripción </h3>", unsafe_allow_html=True)
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

            if info is None:
                try:
                    info = obtener_info_ticker(symbol)
                except Exception as e:
                    st.warning("⚠️ No se pudo cargar la información detallada. Posible límite de uso.")
                    st.stop()
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
        st.markdown("<h3 style='color:#4ade80'> Gráfico de Precios Historicos (ultimos 5 años) </h3>", unsafe_allow_html=True)
        st.markdown("Este grafico muestra la evolución del precio de cierre ajustado en los últimos cinco años.")

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
        st.markdown("<h3 style='color:#4ade80'> Rendimientos Anualizados (CAGR) </h3>", unsafe_allow_html=True)
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
        st.data_editor(df_cagr, use_container_width=True, num_rows="dynamic", disabled=True)

        st.markdown("**Nota:** El rendimiento compuesto anual (CAGR) considera el precio al final y al inicio del periodo para calcular el crecimiento promedio anual.")

    elif seccion == "Volatilidad Histórica":
        st.markdown("<h3 style='color:#4ade80'> Volatilidad Historica (riesgo) </h3>", unsafe_allow_html=True)
        st.markdown("La volatilidad anualizada se calcula usando al desviación estandar de los rendimientos diarios multiplicada por la raíz de 252.")

        retornos = hist["Close"].pct_change().dropna()
        volatilidad = retornos.std() * np.sqrt(252)

        st.markdown(f"**Volatilidad anualizada:** {round(volatilidad * 100, 2)}%")
        st.markdown("Este valor representa la variabilidad histórica del precio del activo. Una mayor volatilidad indica mayor riesgo.")

    elif seccion == "Simulación de Monte Carlo":
        st.markdown("<h3 style='color:#4ade80'> Simulación de Monte Carlo </h3>", unsafe_allow_html=True)
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
        st.markdown("<h3 style='color:#4ade80'> Análisis Estadístico de Precios del Cierre</h3>", unsafe_allow_html=True)
        st.write("Este análisis resume el comportamiento histórico del precio.")

        resumen = hist["Close"].describe()
        st.write(resumen)

        fig_stats, ax_stats = plt.subplots()
        sns.histplot(hist["Close"], kde=True, ax=ax_stats)
        ax_stats.set_title("Distribución de precios de cierre")
        st.pyplot(fig_stats)

    elif seccion == "Comparación Contra Índice":
        st.markdown("<h3 style='color:#4ade80'> Comparación contra S&P 500 </h3>", unsafe_allow_html=True)
        st.write("Se compara el rendimiento del ticker con el índice SPY.")

    try:
        spy = obtener_cierre_spy()
        if spy.empty:
            raise ValueError("No se pudieron obtener datos del índice SPY.")
        
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

    except Exception as e:
        st.warning("⚠️ No se pudo obtener la comparación con SPY. Puede ser por límite de consultas.")
        st.error(f"Detalle técnico: {e}")

    if seccion == "Medias Móviles":
        st.markdown("<h3 style='color:#4ade80'> Medias Móviles </h3>", unsafe_allow_html=True)
        st.write("Promedios móviles de corto y largo plazo.")

        hist["MA50"] = hist["Close"].rolling(window=50).mean()
        hist["MA200"] = hist["Close"].rolling(window=200).mean()

        fig_ma, ax_ma = plt.subplots()
        ax_ma.plot(hist["Close"], label="Precio")
        ax_ma.plot(hist["MA50"], label="MA50")
        ax_ma.plot(hist["MA200"], label="MA200")
        ax_ma.set_title("Medias Móviles")
        ax_ma.legend()
        st.pyplot(fig_ma)

    elif seccion == "Cartera Eficiente":
        st.markdown("<h3 style='color:#4ade80'> Cartera Eficiente (Teoria de Markowitz) </h3>", unsafe_allow_html=True)
        tickers_input = st.text_input("Ingresa tickers separados por comas (ej: AAPL,MSFT,NVDA)")

    if tickers_input:
        tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
        data = obtener_cierre_masivo(tickers)

        data = data.dropna()
        st.markdown("#### Últimos precios históricos de los activos seleccionados")
        st.data_editor(
            data.tail(),
            use_container_width=True,
            num_rows="dynamic",
            disabled=True
        )
        returns = data.pct_change().dropna()

        n_assets = len(tickers)
        n_portfolios = 2000
        results = np.zeros((3, n_portfolios))

        for i in range(n_portfolios):
            weights = np.random.random(n_assets)
            weights /= np.sum(weights)
            ret = np.dot(weights, returns.mean()) * 252
            vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
            sharpe = ret / vol
            results[0, i] = ret
            results[1, i] = vol
            results[2, i] = sharpe

        fig_port, ax_port = plt.subplots()
        sc = ax_port.scatter(results[1], results[0], c=results[2], cmap="viridis")
        ax_port.set_xlabel("Volatilidad")
        ax_port.set_ylabel("Retorno Esperado")
        ax_port.set_title("Frontera eficiente")
        fig_port.colorbar(sc, label="Sharpe Ratio")
        st.pyplot(fig_port)

st.markdown("""
    <style>
        .logo-palantir {
            position: fixed;
            right: 20px;
            bottom: 20px;
            width: 55px;
            opacity: 0.3;
            z-index: 100;
        }

        .logo-palantir:hover {
            opacity: 0.8;
            transform: scale(1.1);
            transition: 0.3s ease-in-out;
        }
    </style>
    <a href="https://seekvectorlogo.com/palantir-vector-logo-svg/" target="_blank">
        <img src="https://seekvectorlogo.com/wp-content/uploads/2018/01/palantir-vector-logo.png" class="logo-palantir">
    </a>
""", unsafe_allow_html=True)