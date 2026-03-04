import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration
st.set_page_config(page_title="Eden's Investment Agent", layout="wide")

# Helper Functions
def color_daily_change(val):
    try:
        num = float(val.replace('%', ''))
        if num <= -3: return 'background-color: #ffcccc'
        if num >= 3: return 'background-color: #ccffcc'
    except: pass
    return ''

def get_ai_summary(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    if not news: return "Technical volatility detected. No specific news headlines."
    return f"Insight: {news[0]['title']}"

# Persistent Data Structure (Eden & Osher Portfolios)
if 'portfolios' not in st.session_state:
    st.session_state.portfolios = {
        "התיק של עדן": {
            'stocks': {
                'ORCL': [{'qty': 3, 'price': 100}],
                'AMZN': [{'qty': 6, 'price': 120}],
                'TSLA': [{'qty': 8, 'price': 150}],
                'SOFI': [{'qty': 50, 'price': 8}],
                'NVDA': [{'qty': 20, 'price': 150}],
                'META': [{'qty': 8, 'price': 95}],
                'DNN': [{'qty': 160, 'price': 2}],
                'GOOGL': [{'qty': 6, 'price': 100}]
            },
            'goals': "Aggressive growth, focusing on AI and Semiconductors.",
            'notes': "Monitor Meta's weight in the portfolio."
        },
        "התיק של אושר": {
            'stocks': {
                'BBAI': [{'qty': 138, 'price': 7.2}],
                'PYPL': [{'qty': 9, 'price': 68}],
                'NVO': [{'qty': 30, 'price': 53}],
                'UBER': [{'qty': 11, 'price': 83.7}],
                'AMZN': [{'qty': 5, 'price': 173}],
                'BA': [{'qty': 7, 'price': 33.4}],
                'UNH': [{'qty': 2, 'price': 241}],
                'GOOGL': [{'qty': 5, 'price': 163}],
                'SOFI': [{'qty': 100, 'price': 11}]
            },
            'goals': "Capital building with sector diversification.",
            'notes': "Track PayPal earnings and Uber's profitability trends."
        }
    }

# --- Sidebar ---
st.sidebar.title("🚀 Intelligence Agent")
selected_name = st.sidebar.selectbox("Active Portfolio", list(st.session_state.portfolios.keys()))
current_data = st.session_state.portfolios[selected_name]

# --- UI Tabs ---
tab1, tab2, tab3 = st.tabs(["📈 Portfolio Lab", "🔬 מחשבון הערכת שווי", "📝 Strategy Board"])

with tab1:
    st.header(f"Portfolio Lab: {selected_name}")
    
    if current_data['stocks']:
        tickers = list(current_data['stocks'].keys())
        data = yf.download(tickers + ['SPY', 'QQQ'], period="2d")['Close']
        live_prices = data.iloc[-1]
        prev_prices = data.iloc[-2]

        rows = []
        for t in tickers:
            txs = current_data['stocks'][t]
            qty = sum(x['qty'] for x in txs)
            avg_cost = sum(x['qty'] * x['price'] for x in txs) / qty
            curr_p = live_prices[t]
            
            info = yf.Ticker(t).info
            total_ret = ((curr_p / avg_cost) - 1) * 100
            daily_chg = ((curr_p / prev_prices[t]) - 1) * 100

            if total_ret <= -8:
                st.error(f"🚨 ALERT: {t} at {total_ret:.2f}%. {get_ai_summary(t)}")

            rows.append({
                "Ticker": t, "Qty": qty, "Avg Cost": f"${avg_cost:.2f}",
