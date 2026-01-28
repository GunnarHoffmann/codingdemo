import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

# Seitenkonfiguration
st.set_page_config(
    page_title="RWE & EON Aktien-Tracker",
    page_icon="📈",
    layout="wide"
)

# Titel
st.title("📈 RWE & EON Aktien-Tracker")
st.markdown("---")

# Aktien-Ticker
STOCKS = {
    "RWE": "RWE.DE",
    "EON": "EOAN.DE"
}

# Zeitraum-Auswahl in der Sidebar
st.sidebar.header("Einstellungen")
time_period = st.sidebar.selectbox(
    "Zeitraum auswählen",
    options=["1 Monat", "3 Monate", "6 Monate", "1 Jahr", "2 Jahre", "5 Jahre"],
    index=3
)

# Zeitraum-Mapping
period_mapping = {
    "1 Monat": "1mo",
    "3 Monate": "3mo",
    "6 Monate": "6mo",
    "1 Jahr": "1y",
    "2 Jahre": "2y",
    "5 Jahre": "5y"
}

selected_period = period_mapping[time_period]


@st.cache_data(ttl=300)  # Cache für 5 Minuten
def get_stock_data(ticker: str, period: str) -> pd.DataFrame:
    """Lädt Aktiendaten von Yahoo Finance."""
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


@st.cache_data(ttl=300)
def get_stock_info(ticker: str) -> dict:
    """Lädt Aktieninformationen von Yahoo Finance."""
    stock = yf.Ticker(ticker)
    return stock.info


def format_number(number: float, decimals: int = 2) -> str:
    """Formatiert eine Zahl mit Tausendertrennzeichen."""
    if number is None:
        return "N/A"
    return f"{number:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_currency(number: float, currency: str = "EUR") -> str:
    """Formatiert einen Währungsbetrag."""
    if number is None:
        return "N/A"
    formatted = format_number(number)
    return f"{formatted} {currency}"


# Aktuelle Kursinformationen laden
col1, col2 = st.columns(2)

for idx, (name, ticker) in enumerate(STOCKS.items()):
    with col1 if idx == 0 else col2:
        st.subheader(f"🏢 {name}")

        try:
            info = get_stock_info(ticker)
            data = get_stock_data(ticker, selected_period)

            if not data.empty:
                current_price = data['Close'].iloc[-1]
                previous_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
                price_change = current_price - previous_price
                price_change_pct = (price_change / previous_price) * 100

                # Metriken anzeigen
                metric_col1, metric_col2, metric_col3 = st.columns(3)

                with metric_col1:
                    st.metric(
                        label="Aktueller Kurs",
                        value=format_currency(current_price),
                        delta=f"{price_change_pct:.2f}%"
                    )

                with metric_col2:
                    st.metric(
                        label="Tageshoch",
                        value=format_currency(data['High'].iloc[-1])
                    )

                with metric_col3:
                    st.metric(
                        label="Tagestief",
                        value=format_currency(data['Low'].iloc[-1])
                    )

                # Weitere Informationen
                info_col1, info_col2 = st.columns(2)

                with info_col1:
                    st.markdown(f"**52-Wochen-Hoch:** {format_currency(info.get('fiftyTwoWeekHigh'))}")
                    st.markdown(f"**52-Wochen-Tief:** {format_currency(info.get('fiftyTwoWeekLow'))}")

                with info_col2:
                    market_cap = info.get('marketCap')
                    if market_cap:
                        market_cap_mrd = market_cap / 1e9
                        st.markdown(f"**Marktkapitalisierung:** {format_number(market_cap_mrd)} Mrd. EUR")
                    st.markdown(f"**Volumen:** {format_number(data['Volume'].iloc[-1], 0)}")

        except Exception as e:
            st.error(f"Fehler beim Laden der Daten für {name}: {str(e)}")

st.markdown("---")

# Kursverlauf-Charts
st.header("📊 Kursverlauf")

# Daten für beide Aktien laden
chart_data = {}
for name, ticker in STOCKS.items():
    try:
        data = get_stock_data(ticker, selected_period)
        if not data.empty:
            chart_data[name] = data
    except Exception as e:
        st.error(f"Fehler beim Laden der Chart-Daten für {name}: {str(e)}")

# Chart-Tabs
tab1, tab2, tab3 = st.tabs(["Einzelne Charts", "Vergleich", "Prozentuale Entwicklung"])

with tab1:
    col1, col2 = st.columns(2)

    for idx, (name, data) in enumerate(chart_data.items()):
        with col1 if idx == 0 else col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name=name,
                line=dict(color='#1f77b4' if idx == 0 else '#ff7f0e', width=2),
                fill='tozeroy',
                fillcolor='rgba(31, 119, 180, 0.1)' if idx == 0 else 'rgba(255, 127, 14, 0.1)'
            ))

            fig.update_layout(
                title=f"{name} Kursverlauf ({time_period})",
                xaxis_title="Datum",
                yaxis_title="Kurs (EUR)",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = go.Figure()

    colors = ['#1f77b4', '#ff7f0e']
    for idx, (name, data) in enumerate(chart_data.items()):
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name=name,
            line=dict(color=colors[idx], width=2)
        ))

    fig.update_layout(
        title=f"RWE vs EON Kursvergleich ({time_period})",
        xaxis_title="Datum",
        yaxis_title="Kurs (EUR)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = go.Figure()

    colors = ['#1f77b4', '#ff7f0e']
    for idx, (name, data) in enumerate(chart_data.items()):
        # Prozentuale Veränderung berechnen
        pct_change = ((data['Close'] / data['Close'].iloc[0]) - 1) * 100

        fig.add_trace(go.Scatter(
            x=data.index,
            y=pct_change,
            mode='lines',
            name=name,
            line=dict(color=colors[idx], width=2)
        ))

    fig.update_layout(
        title=f"Prozentuale Entwicklung seit Periodenbeginn ({time_period})",
        xaxis_title="Datum",
        yaxis_title="Veränderung (%)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # Nulllinie hinzufügen
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Volumen-Chart
st.header("📊 Handelsvolumen")

fig = go.Figure()

for idx, (name, data) in enumerate(chart_data.items()):
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name=name,
        opacity=0.7
    ))

fig.update_layout(
    title=f"Handelsvolumen ({time_period})",
    xaxis_title="Datum",
    yaxis_title="Volumen",
    barmode='group',
    template='plotly_white',
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Daten bereitgestellt von Yahoo Finance. Alle Angaben ohne Gewähr.</p>
        <p>Letzte Aktualisierung: {}</p>
    </div>
    """.format(datetime.now().strftime("%d.%m.%Y %H:%M:%S")),
    unsafe_allow_html=True
)
