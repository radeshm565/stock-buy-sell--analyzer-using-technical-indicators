import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# Page config
st.set_page_config(
    page_title="StockTrade Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful modern theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .main, .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Text colors - specific elements only */
    body, .stMarkdown, .stMarkdown p, .stText, div[data-testid="stMarkdownContainer"] {
        color: #1e293b !important;
    }
    
    /* Headers with gradient - but not for login hero */
    h1:not(.login-hero h1) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
    }
    h2:not(.login-hero h2), h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Login/Signup hero section - white text */
    .login-hero h1, .login-hero h2, .login-hero p, .login-hero div {
        color: white !important;
        -webkit-text-fill-color: white !important;
    }
    
    /* But keep button text white */
    .stButton>button, .stButton>button * {
        color: white !important;
    }
    
    /* Beautiful cards with glass effect */
    .metric-card, .stock-card {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    .metric-card:hover, .stock-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Gradient buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Input fields with modern styling */
    .stTextInput input, .stNumberInput input {
        background: white !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: white !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }
    
    /* Metric values */
    [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 500 !important;
    }
    
    /* Positive/Negative colors */
    .positive { 
        color: #10b981 !important; 
        font-weight: 600 !important;
    }
    .negative { 
        color: #ef4444 !important; 
        font-weight: 600 !important;
    }
    
    /* Info boxes with gradient */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        color: #1e293b !important;
        background: white !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Navigation selectbox */
    .stSelectbox {
        background: rgba(255,255,255,0.9) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
    }
    
    /* Placeholder text */
    ::placeholder {
        color: #94a3b8 !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.5);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'users' not in st.session_state:
    st.session_state.users = {}

# Sample stock data
STOCKS = {
    'RELIANCE': {'name': 'Reliance Industries', 'price': 2456.30, 'change': 1.25, 'sector': 'Energy', 'market_cap': '16.5T'},
    'TCS': {'name': 'Tata Consultancy', 'price': 3456.80, 'change': -0.45, 'sector': 'IT', 'market_cap': '12.8T'},
    'HDFCBANK': {'name': 'HDFC Bank', 'price': 1567.45, 'change': 0.85, 'sector': 'Banking', 'market_cap': '8.9T'},
    'INFY': {'name': 'Infosys', 'price': 1456.60, 'change': 1.15, 'sector': 'IT', 'market_cap': '6.2T'},
    'ICICIBANK': {'name': 'ICICI Bank', 'price': 945.75, 'change': -0.25, 'sector': 'Banking', 'market_cap': '6.6T'},
    'HINDUNILVR': {'name': 'Hindustan Unilever', 'price': 2456.90, 'change': 0.35, 'sector': 'FMCG', 'market_cap': '5.8T'},
    'SBIN': {'name': 'State Bank of India', 'price': 567.45, 'change': 1.85, 'sector': 'Banking', 'market_cap': '5.1T'},
    'BHARTIARTL': {'name': 'Bharti Airtel', 'price': 856.30, 'change': -0.65, 'sector': 'Telecom', 'market_cap': '4.8T'},
    'ITC': {'name': 'ITC Limited', 'price': 445.60, 'change': 0.95, 'sector': 'FMCG', 'market_cap': '5.5T'},
    'KOTAKBANK': {'name': 'Kotak Mahindra Bank', 'price': 1756.25, 'change': -0.15, 'sector': 'Banking', 'market_cap': '3.5T'},
    'LT': {'name': 'Larsen & Toubro', 'price': 2345.60, 'change': 1.25, 'sector': 'Infrastructure', 'market_cap': '3.2T'},
    'AXISBANK': {'name': 'Axis Bank', 'price': 945.30, 'change': 0.75, 'sector': 'Banking', 'market_cap': '2.9T'},
}

INDICES = {
    'NIFTY 50': {'value': 19856.30, 'change': 125.45, 'change_pct': 0.63},
    'SENSEX': {'value': 65890.50, 'change': 456.80, 'change_pct': 0.70},
    'BANK NIFTY': {'value': 44567.80, 'change': -89.45, 'change_pct': -0.20},
    'NIFTY IT': {'value': 32567.40, 'change': 234.60, 'change_pct': 0.72},
}

NEWS = [
    {'title': 'RBI keeps repo rate unchanged at 6.5%', 'category': 'Economy', 'time': '2 hours ago', 'source': 'Economic Times'},
    {'title': 'Reliance announces new green energy project', 'category': 'Corporate', 'time': '4 hours ago', 'source': 'Business Standard'},
    {'title': 'IT stocks rally on strong quarterly results', 'category': 'Markets', 'time': '5 hours ago', 'source': 'Moneycontrol'},
    {'title': 'Government announces new infrastructure push', 'category': 'Policy', 'time': '6 hours ago', 'source': 'Livemint'},
    {'title': 'Foreign investors pump $2B into Indian markets', 'category': 'Markets', 'time': '8 hours ago', 'source': 'CNBC-TV18'},
    {'title': 'TCS wins major deal from European bank', 'category': 'Corporate', 'time': '10 hours ago', 'source': 'Reuters'},
    {'title': 'Inflation data shows cooling trend', 'category': 'Economy', 'time': '12 hours ago', 'source': 'Bloomberg'},
]

def get_user_data(email):
    """Get or initialize user data"""
    if email not in st.session_state.users:
        st.session_state.users[email] = {
            'balance': 0,
            'portfolio': [],
            'transactions': [],
            'orders': [],
            'watchlist': ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK']
        }
    return st.session_state.users[email]

def format_inr(amount):
    """Format amount in Indian Rupees"""
    return f"₹{amount:,.2f}"

def nav_header():
    """Navigation header for logged-in pages"""
    # Title
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>📈 StockTrade Pro</h2>", unsafe_allow_html=True)
    
    # Navigation menu using selectbox for reliability
    nav_options = {
        '📊 Dashboard': 'dashboard',
        '📈 Markets': 'markets',
        '💼 Portfolio': 'portfolio',
        '💱 Trade': 'trade',
        '📜 History': 'history',
        '📰 News': 'news',
        '💻 DSA Analyzer': 'analyzer',
        '⚙️ Settings': 'settings',
        '🚪 Logout': 'logout'
    }
    
    # Find current page label
    current_label = [k for k, v in nav_options.items() if v == st.session_state.page][0] if st.session_state.page in nav_options.values() else '📊 Dashboard'
    
    selected = st.selectbox("Navigation", list(nav_options.keys()), 
                           index=list(nav_options.keys()).index(current_label) if current_label in nav_options else 0,
                           label_visibility="collapsed")
    
    if nav_options[selected] == 'logout':
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.page = 'login'
        st.rerun()
    elif nav_options[selected] != st.session_state.page:
        st.session_state.page = nav_options[selected]
        st.rerun()
    
    # Show balance
    user_data = get_user_data(st.session_state.current_user)
    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem; background: white; border-radius: 8px; margin-top: 0.5rem;">
        <span style="color: #64748b;">Balance: </span>
        <span style="color: #059669; font-weight: 600; font-size: 1.1rem;">{format_inr(user_data['balance'])}</span>
        <span style="color: #94a3b8; margin-left: 1rem;">|</span>
        <span style="color: #475569; margin-left: 1rem;">{st.session_state.current_user.split('@')[0].title()}</span>
    </div>
    """, unsafe_allow_html=True)

def login_page():
    """Login page"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="login-hero" style="padding: 3rem;">
            <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem;">📈 StockTrade Pro</h1>
            <h2 style="font-size: 2rem; margin-bottom: 1.5rem;">Smart Trading Starts Here</h2>
            <p style="font-size: 1.125rem; opacity: 0.9; margin-bottom: 2rem;">
                Analyze markets, track stocks, and maximize your profits with our advanced trading platform.
            </p>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div>⚡ Real-time Market Data</div>
                <div>🧠 AI-Powered Analysis</div>
                <div>🛡️ Secure Trading</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### Welcome Back")
        st.markdown("Sign in to access your portfolio")
        
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🔐 Sign In", use_container_width=True)
            
            if submitted and email:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                get_user_data(email)
                st.session_state.page = 'dashboard'
                st.rerun()
        
        st.markdown("---")
        st.markdown("**or continue with**")
        
        col_g, col_a = st.columns(2)
        with col_g:
            if st.button("🔍 Google", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.current_user = "user@gmail.com"
                get_user_data("user@gmail.com")
                st.session_state.page = 'dashboard'
                st.rerun()
        with col_a:
            if st.button("🍎 Apple", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.current_user = "user@icloud.com"
                get_user_data("user@icloud.com")
                st.session_state.page = 'dashboard'
                st.rerun()
        
        st.markdown("---")
        st.markdown("Don't have an account? **Sign up below**")
        if st.button("📝 Create Account", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()

def signup_page():
    """Signup page"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="login-hero" style="padding: 3rem;">
            <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem;">📈 StockTrade Pro</h1>
            <h2 style="font-size: 2rem; margin-bottom: 1.5rem;">Start Your Trading Journey</h2>
            <p style="font-size: 1.125rem; opacity: 0.9; margin-bottom: 2rem;">
                Join thousands of traders and investors. Create your free account today.
            </p>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div>✓ Zero Account Opening Fee</div>
                <div>✓ Free Research Reports</div>
                <div>✓ 24/7 Customer Support</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### Create Account")
        st.markdown("Join StockTrade Pro today")
        
        with st.form("signup_form"):
            col_f, col_l = st.columns(2)
            with col_f:
                first_name = st.text_input("First Name", placeholder="John")
            with col_l:
                last_name = st.text_input("Last Name", placeholder="Doe")
            
            email = st.text_input("Email Address", placeholder="john@example.com")
            phone = st.text_input("Phone Number", placeholder="+91 98765 43210")
            password = st.text_input("Password", type="password", placeholder="Create password")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            
            submitted = st.form_submit_button("🚀 Create Account", use_container_width=True)
            
            if submitted and email and first_name:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                get_user_data(email)
                st.session_state.page = 'dashboard'
                st.rerun()
        
        st.markdown("---")
        st.markdown("Already have an account? **Sign in below**")
        if st.button("🔐 Sign In", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()

def dashboard_page():
    """Dashboard page"""
    nav_header()
    
    st.markdown("## 📊 Dashboard")
    
    # Market Overview
    cols = st.columns(4)
    for i, (name, data) in enumerate(INDICES.items()):
        with cols[i]:
            color = "#10b981" if data['change'] >= 0 else "#ef4444"
            arrow = "▲" if data['change'] >= 0 else "▼"
            st.markdown(f"""
            <div class="metric-card">
                <p style="color: #94a3b8; margin: 0; font-size: 0.875rem;">{name}</p>
                <h3 style="margin: 0.5rem 0;">{data['value']:,.2f}</h3>
                <p style="color: {color}; margin: 0; font-size: 0.875rem;">
                    {arrow} {abs(data['change']):,.2f} ({data['change_pct']:.2f}%)
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    user_data = get_user_data(st.session_state.current_user)
    
    # Portfolio Summary
    col_portfolio, col_cash = st.columns([2, 1])
    
    with col_portfolio:
        st.markdown("### 💼 Portfolio Summary")
        
        total_value = sum([holding['qty'] * STOCKS[holding['stock']]['price'] 
                          for holding in user_data['portfolio']])
        invested = sum([holding['qty'] * holding['avg_price'] 
                       for holding in user_data['portfolio']])
        pnl = total_value - invested
        
        cols = st.columns(3)
        with cols[0]:
            st.metric("Total Value", format_inr(total_value))
        with cols[1]:
            st.metric("Invested", format_inr(invested))
        with cols[2]:
            st.metric("P&L", format_inr(pnl), f"{((pnl/invested)*100 if invested else 0):.2f}%")
    
    with col_cash:
        st.markdown("### 💰 Cash Balance")
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <h2 style="color: #10b981;">{format_inr(user_data['balance'])}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Watchlist & Top Movers
    col_watchlist, col_movers = st.columns([2, 1])
    
    with col_watchlist:
        st.markdown("### ⭐ Watchlist")
        for code in user_data['watchlist'][:5]:
            if code in STOCKS:
                stock = STOCKS[code]
                color = "#10b981" if stock['change'] >= 0 else "#ef4444"
                arrow = "▲" if stock['change'] >= 0 else "▼"
                st.markdown(f"""
                <div class="stock-card">
                    <div style="display: flex; justify-content: space-between;">
                        <div><strong>{code}</strong><br><small>{stock['name']}</small></div>
                        <div style="text-align: right;">
                            {format_inr(stock['price'])}<br>
                            <span style="color: {color};">{arrow} {abs(stock['change']):.2f}%</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col_movers:
        st.markdown("### 🚀 Top Movers")
        sorted_stocks = sorted(STOCKS.items(), key=lambda x: abs(x[1]['change']), reverse=True)[:5]
        for code, stock in sorted_stocks:
            color = "#10b981" if stock['change'] >= 0 else "#ef4444"
            st.markdown(f"""
            <div class="stock-card">
                <div style="display: flex; justify-content: space-between;">
                    <span><strong>{code}</strong></span>
                    <span style="color: {color};">{stock['change']:+.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def markets_page():
    """Markets page"""
    nav_header()
    
    st.markdown("## 📈 Markets")
    
    # Search and Filter
    col_search, col_sector, col_sort = st.columns([2, 1, 1])
    
    with col_search:
        search = st.text_input("🔍 Search stocks", placeholder="Search by name or symbol")
    with col_sector:
        sector = st.selectbox("Sector", ["All", "Banking", "IT", "FMCG", "Energy", "Telecom", "Infrastructure"])
    with col_sort:
        sort_by = st.selectbox("Sort by", ["Market Cap", "Price", "Change %"])
    
    # Filter stocks
    filtered_stocks = STOCKS.items()
    if search:
        filtered_stocks = [(k, v) for k, v in filtered_stocks 
                          if search.upper() in k or search.lower() in v['name'].lower()]
    if sector != "All":
        filtered_stocks = [(k, v) for k, v in filtered_stocks if v['sector'] == sector]
    
    # Display stocks
    st.markdown("### All Stocks")
    for code, stock in filtered_stocks:
        color = "#10b981" if stock['change'] >= 0 else "#ef4444"
        arrow = "▲" if stock['change'] >= 0 else "▼"
        
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
        with col1:
            st.markdown(f"**{code}**<br><small>{stock['name']}</small>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<small>Sector: {stock['sector']}</small>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"**{format_inr(stock['price'])}**")
        with col4:
            st.markdown(f"<span style='color: {color};'>{arrow} {abs(stock['change']):.2f}%</span>", unsafe_allow_html=True)
        with col5:
            if st.button("Trade", key=f"trade_{code}"):
                st.session_state.selected_stock = code
                st.session_state.page = 'trade'
                st.rerun()
        st.markdown("---")

def portfolio_page():
    """Portfolio page"""
    nav_header()
    
    st.markdown("## 💼 Portfolio")
    
    user_data = get_user_data(st.session_state.current_user)
    
    if not user_data['portfolio']:
        st.info("📭 Your portfolio is empty. Start trading to build your portfolio!")
        if st.button("🚀 Start Trading"):
            st.session_state.page = 'trade'
            st.rerun()
        return
    
    # Portfolio Summary
    total_value = sum([holding['qty'] * STOCKS[holding['stock']]['price'] 
                      for holding in user_data['portfolio']])
    invested = sum([holding['qty'] * holding['avg_price'] 
                   for holding in user_data['portfolio']])
    pnl = total_value - invested
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Total Value", format_inr(total_value))
    with cols[1]:
        st.metric("Invested", format_inr(invested))
    with cols[2]:
        st.metric("P&L", format_inr(pnl), f"{((pnl/invested)*100 if invested else 0):.2f}%")
    with cols[3]:
        st.metric("Holdings", len(user_data['portfolio']))
    
    st.markdown("---")
    st.markdown("### Holdings")
    
    for holding in user_data['portfolio']:
        stock = STOCKS.get(holding['stock'], {})
        current_price = stock.get('price', 0)
        current_value = holding['qty'] * current_price
        invested_value = holding['qty'] * holding['avg_price']
        pnl = current_value - invested_value
        pnl_pct = (pnl / invested_value * 100) if invested_value else 0
        color = "#10b981" if pnl >= 0 else "#ef4444"
        
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
        with col1:
            st.markdown(f"**{holding['stock']}**<br><small>{stock.get('name', '')}</small>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"Qty: **{holding['qty']}**")
        with col3:
            st.markdown(f"Avg: {format_inr(holding['avg_price'])}")
        with col4:
            st.markdown(f"LTP: {format_inr(current_price)}")
        with col5:
            st.markdown(f"Value: **{format_inr(current_value)}**<br><span style='color: {color};'>P&L: {format_inr(pnl)} ({pnl_pct:+.2f}%)</span>", unsafe_allow_html=True)
        
        col_buy, col_sell = st.columns(2)
        with col_buy:
            if st.button(f"Buy More {holding['stock']}", key=f"buy_{holding['stock']}"):
                st.session_state.selected_stock = holding['stock']
                st.session_state.page = 'trade'
                st.rerun()
        with col_sell:
            if st.button(f"Sell {holding['stock']}", key=f"sell_{holding['stock']}"):
                st.session_state.selected_stock = holding['stock']
                st.session_state.page = 'trade'
                st.rerun()
        st.markdown("---")

def trade_page():
    """Trade page"""
    nav_header()
    
    st.markdown("## 💱 Trade")
    
    user_data = get_user_data(st.session_state.current_user)
    
    # Stock selector
    selected = st.session_state.get('selected_stock', 'RELIANCE')
    stock_code = st.selectbox("Select Stock", list(STOCKS.keys()), 
                              index=list(STOCKS.keys()).index(selected) if selected in STOCKS else 0)
    
    stock = STOCKS[stock_code]
    
    col_info, col_chart = st.columns([1, 2])
    
    with col_info:
        st.markdown(f"### {stock_code}")
        st.markdown(f"**{stock['name']}**")
        st.markdown(f"Sector: {stock['sector']}")
        
        color = "#10b981" if stock['change'] >= 0 else "#ef4444"
        st.markdown(f"""
        <div class="metric-card">
            <h2 style="margin: 0;">{format_inr(stock['price'])}</h2>
            <p style="color: {color}; margin: 0;">{stock['change']:+.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"Market Cap: {stock['market_cap']}")
    
    with col_chart:
        # Generate chart data
        days = 30
        prices = [stock['price'] * (1 + np.random.randn() * 0.02) for _ in range(days)]
        prices[-1] = stock['price']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(days)),
            y=prices,
            mode='lines',
            name='Price',
            line=dict(color='#ffffff', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 255, 255, 0.2)'
        ))
        fig.update_layout(
            title=dict(
                text=f"{stock_code} - 30 Day Chart",
                font=dict(color='white', size=16)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                showgrid=False, 
                title='',
                tickfont=dict(color='white'),
                zeroline=False
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.2)', 
                title=dict(text='Price (₹)', font=dict(color='white')),
                tickfont=dict(color='white'),
                zeroline=False
            ),
            margin=dict(l=60, r=40, t=50, b=40),
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Order Form
    st.markdown("### Place Order")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        order_type = st.radio("Order Type", ["Buy", "Sell"])
    with col2:
        quantity = st.number_input("Quantity", min_value=1, value=10, step=1)
    with col3:
        price = stock['price']
        st.markdown(f"**Price:** {format_inr(price)}")
        total = quantity * price
        st.markdown(f"**Total:** {format_inr(total)}")
    
    if st.button(f"🚀 Place {order_type} Order", use_container_width=True):
        if order_type == "Buy":
            if total > user_data['balance']:
                st.error(f"Insufficient balance! You need {format_inr(total)} but have {format_inr(user_data['balance'])}")
            else:
                # Deduct balance
                user_data['balance'] -= total
                
                # Add to portfolio
                existing = next((h for h in user_data['portfolio'] if h['stock'] == stock_code), None)
                if existing:
                    total_qty = existing['qty'] + quantity
                    total_invested = (existing['qty'] * existing['avg_price']) + total
                    existing['qty'] = total_qty
                    existing['avg_price'] = total_invested / total_qty
                else:
                    user_data['portfolio'].append({
                        'stock': stock_code,
                        'qty': quantity,
                        'avg_price': price
                    })
                
                # Add to orders
                user_data['orders'].append({
                    'type': 'BUY',
                    'stock': stock_code,
                    'qty': quantity,
                    'price': price,
                    'total': total,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                st.success(f"✅ Buy order placed! Bought {quantity} shares of {stock_code} for {format_inr(total)}")
                st.rerun()
        else:
            # Sell logic
            existing = next((h for h in user_data['portfolio'] if h['stock'] == stock_code), None)
            if not existing or existing['qty'] < quantity:
                st.error(f"Insufficient shares! You have {existing['qty'] if existing else 0} shares")
            else:
                # Add to balance
                user_data['balance'] += total
                
                # Update portfolio
                existing['qty'] -= quantity
                if existing['qty'] == 0:
                    user_data['portfolio'] = [h for h in user_data['portfolio'] if h['stock'] != stock_code]
                
                # Add to orders
                user_data['orders'].append({
                    'type': 'SELL',
                    'stock': stock_code,
                    'qty': quantity,
                    'price': price,
                    'total': total,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                st.success(f"✅ Sell order placed! Sold {quantity} shares of {stock_code} for {format_inr(total)}")
                st.rerun()

def history_page():
    """History page"""
    nav_header()
    
    st.markdown("## 📜 Order History")
    
    user_data = get_user_data(st.session_state.current_user)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("Filter", ["All", "Buy", "Sell"])
    with col2:
        date_range = st.selectbox("Date Range", ["All Time", "Today", "Last 7 Days", "Last 30 Days"])
    with col3:
        status = st.selectbox("Status", ["All", "Completed", "Pending"])
    
    if not user_data['orders']:
        st.info("📭 No orders yet. Start trading to see your order history!")
        if st.button("🚀 Start Trading"):
            st.session_state.page = 'trade'
            st.rerun()
        return
    
    # Filter orders
    filtered_orders = user_data['orders']
    if filter_type != "All":
        filtered_orders = [o for o in filtered_orders if o['type'] == filter_type.upper()]
    
    # Display orders
    st.markdown("### Recent Orders")
    
    for order in reversed(filtered_orders[-20:]):  # Show last 20
        color = "#10b981" if order['type'] == 'BUY' else "#ef4444"
        
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        with col1:
            st.markdown(f"<span style='color: {color}; font-weight: bold;'>{order['type']}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{order['stock']}** - {STOCKS.get(order['stock'], {}).get('name', '')}")
        with col3:
            st.markdown(f"Qty: {order['qty']}")
        with col4:
            st.markdown(f"{format_inr(order['total'])}")
        with col5:
            st.markdown(f"<small>{order['date']}</small>", unsafe_allow_html=True)
        st.markdown("---")

def news_page():
    """News page"""
    nav_header()
    
    st.markdown("## 📰 Market News")
    
    # Category filter
    category = st.selectbox("Category", ["All", "Markets", "Economy", "Corporate", "Policy"])
    
    filtered_news = NEWS
    if category != "All":
        filtered_news = [n for n in filtered_news if n['category'] == category]
    
    for news in filtered_news:
        st.markdown(f"""
        <div class="stock-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h4 style="margin: 0 0 0.5rem 0;">{news['title']}</h4>
                    <p style="color: #94a3b8; margin: 0; font-size: 0.875rem;">
                        <span style="background: #6366f1; padding: 2px 8px; border-radius: 4px; color: white;">{news['category']}</span>
                        <span style="margin-left: 1rem;">{news['source']}</span>
                        <span style="margin-left: 1rem;">🕐 {news['time']}</span>
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def settings_page():
    """Settings page"""
    nav_header()
    
    st.markdown("## ⚙️ Settings")
    
    tab_profile, tab_payment, tab_security = st.tabs(["👤 Profile", "💳 Payment", "🔒 Security"])
    
    user_data = get_user_data(st.session_state.current_user)
    
    with tab_profile:
        st.markdown("### Profile Settings")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("First Name", value=st.session_state.current_user.split('@')[0].title())
        with col2:
            st.text_input("Last Name", value="User")
        st.text_input("Email", value=st.session_state.current_user, disabled=True)
        st.text_input("Phone", value="+91 98765 43210")
        if st.button("💾 Save Profile"):
            st.success("Profile saved!")
    
    with tab_payment:
        st.markdown("### Payment Methods")
        st.markdown(f"**Current Balance:** {format_inr(user_data['balance'])}")
        
        st.markdown("---")
        st.markdown("#### Add Money")
        amount = st.number_input("Amount (₹)", min_value=100, value=1000, step=100)
        method = st.selectbox("Payment Method", ["UPI", "Credit/Debit Card", "Net Banking"])
        
        if method == "UPI":
            st.text_input("UPI ID", placeholder="yourname@upi")
        
        if st.button("➕ Add Money"):
            user_data['balance'] += amount
            user_data['transactions'].append({
                'type': 'credit',
                'amount': amount,
                'description': 'Money Added',
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success(f"₹{amount:,} added successfully! New balance: {format_inr(user_data['balance'])}")
            st.rerun()
        
        st.markdown("---")
        st.markdown("#### Withdraw Money")
        withdraw_amount = st.number_input("Withdraw Amount (₹)", min_value=100, value=500, step=100)
        if st.button("➖ Withdraw"):
            if withdraw_amount > user_data['balance']:
                st.error("Insufficient balance!")
            else:
                user_data['balance'] -= withdraw_amount
                user_data['transactions'].append({
                    'type': 'debit',
                    'amount': withdraw_amount,
                    'description': 'Money Withdrawn',
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success(f"₹{withdraw_amount:,} withdrawn! New balance: {format_inr(user_data['balance'])}")
                st.rerun()
        
        # Transaction History
        st.markdown("---")
        st.markdown("#### Transaction History")
        if user_data['transactions']:
            for trans in reversed(user_data['transactions'][-10:]):
                color = "#10b981" if trans['type'] == 'credit' else "#ef4444"
                sign = "+" if trans['type'] == 'credit' else "-"
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.5rem; border-bottom: 1px solid #334155;">
                    <span>{trans['description']}</span>
                    <span style="color: {color};">{sign}{format_inr(trans['amount'])}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No transactions yet")
    
    with tab_security:
        st.markdown("### Security Settings")
        st.text_input("Current Password", type="password")
        st.text_input("New Password", type="password")
        st.text_input("Confirm New Password", type="password")
        if st.button("🔐 Change Password"):
            st.success("Password changed successfully!")
        
        st.markdown("---")
        st.checkbox("Enable Two-Factor Authentication")
        st.checkbox("Enable Email Notifications")

def analyzer_page():
    """C++ DSA Stock Analyzer page with 3 algorithms"""
    nav_header()
    
    st.markdown("## 💻 C++ DSA Stock Analyzers")
    st.markdown("Choose from 3 different algorithms to analyze stock prices")
    
    # Algorithm selector
    algo_type = st.selectbox(
        "Select Analysis Type",
        [
            "🔹 Single Transaction - O(n) Kadane's Algorithm",
            "🔹 Multiple Transactions - O(n) Peak Valley",
            "🔹 Maximum k Transactions - O(nk) DP Algorithm"
        ]
    )
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        if "Single Transaction" in algo_type:
            st.markdown("""
            <div class="stock-card">
                <h4>📋 Single Transaction (O(n))</h4>
                <p>Find the best day to buy and sell for maximum profit with <strong>one transaction</strong>.</p>
                <ul>
                    <li><strong>Time:</strong> O(n) - Single pass</li>
                    <li><strong>Space:</strong> O(1) - Constant</li>
                    <li><strong>Method:</strong> Kadane's Algorithm</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif "Multiple Transactions" in algo_type:
            st.markdown("""
            <div class="stock-card">
                <h4>📋 Multiple Transactions (O(n))</h4>
                <p>Find all profitable buy/sell pairs with <strong>unlimited transactions</strong>.</p>
                <ul>
                    <li><strong>Time:</strong> O(n) - Single pass</li>
                    <li><strong>Space:</strong> O(1) - Constant</li>
                    <li><strong>Method:</strong> Peak Valley Approach</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="stock-card">
                <h4>📋 Maximum k Transactions (O(nk))</h4>
                <p>Find maximum profit with <strong>at most k transactions</strong>.</p>
                <ul>
                    <li><strong>Time:</strong> O(n × k) - Dynamic Programming</li>
                    <li><strong>Space:</strong> O(k) - Linear</li>
                    <li><strong>Method:</strong> DP with State Tracking</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("#### Enter Stock Prices")
        st.markdown("Enter prices separated by commas (e.g., 100, 180, 260, 310, 40, 535, 695)")
        
        prices_input = st.text_input("Stock Prices", placeholder="100, 180, 260, 310, 40, 535, 695", key="price_input")
        
        # k input for k transactions
        k_value = 2
        if "k Transactions" in algo_type:
            k_value = st.number_input("Maximum Transactions (k)", min_value=1, max_value=10, value=2)
        
        if st.button("🔍 Analyze", use_container_width=True):
            if prices_input:
                try:
                    prices = [float(p.strip()) for p in prices_input.split(",")]
                    st.session_state.analyzer_prices = prices
                    st.session_state.analyzer_type = algo_type
                    st.session_state.k_value = k_value
                    st.rerun()
                except:
                    st.error("Invalid input! Please enter numbers separated by commas.")
    
    with col_right:
        if 'analyzer_prices' in st.session_state and st.session_state.analyzer_prices:
            prices = st.session_state.analyzer_prices
            algo = st.session_state.get('analyzer_type', algo_type)
            k = st.session_state.get('k_value', 2)
            
            # ALGORITHM 1: Single Transaction O(n)
            if "Single Transaction" in algo:
                min_price = float('inf')
                max_profit = 0
                buy_day = 0
                sell_day = 0
                temp_buy_day = 0
                
                for i, price in enumerate(prices):
                    if price < min_price:
                        min_price = price
                        temp_buy_day = i
                    profit = price - min_price
                    if profit > max_profit:
                        max_profit = profit
                        buy_day = temp_buy_day
                        sell_day = i
                
                st.markdown("""
                <div class="metric-card" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white;">
                    <h3 style="color: white; margin: 0;">📊 Single Transaction Result</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if max_profit > 0:
                    st.success(f"✅ Maximum Profit: ₹{max_profit:.2f}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Buy Day", f"Day {buy_day + 1}", f"₹{prices[buy_day]:.2f}")
                    with col2:
                        st.metric("Sell Day", f"Day {sell_day + 1}", f"₹{prices[sell_day]:.2f}")
                    return_pct = (max_profit / prices[buy_day]) * 100
                    st.info(f"📈 ROI: {return_pct:.2f}%")
                else:
                    st.warning("⚠️ No profit possible")
                
                # Chart with buy/sell points
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=list(range(1, len(prices)+1)), y=prices, mode='lines+markers', name='Price', line=dict(color='#6366f1')))
                if max_profit > 0:
                    fig.add_trace(go.Scatter(x=[buy_day+1], y=[prices[buy_day]], mode='markers', name='Buy', marker=dict(color='green', size=15)))
                    fig.add_trace(go.Scatter(x=[sell_day+1], y=[prices[sell_day]], mode='markers', name='Sell', marker=dict(color='red', size=15)))
                st.plotly_chart(fig, use_container_width=True)
            
            # ALGORITHM 2: Multiple Transactions O(n)
            elif "Multiple Transactions" in algo:
                total_profit = 0
                transactions = []
                i = 0
                n = len(prices)
                
                while i < n - 1:
                    # Find local min (buy point)
                    while i < n - 1 and prices[i+1] <= prices[i]:
                        i += 1
                    if i == n - 1:
                        break
                    buy_day = i
                    buy_price = prices[i]
                    
                    # Find local max (sell point)
                    i += 1
                    while i < n and prices[i] >= prices[i-1]:
                        i += 1
                    sell_day = i - 1
                    sell_price = prices[sell_day]
                    
                    profit = sell_price - buy_price
                    if profit > 0:
                        total_profit += profit
                        transactions.append({'buy_day': buy_day, 'sell_day': sell_day, 'profit': profit})
                
                st.markdown("""
                <div class="metric-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white;">
                    <h3 style="color: white; margin: 0;">📊 Multiple Transactions Result</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.success(f"✅ Total Profit: ₹{total_profit:.2f}")
                st.info(f"📈 Number of Transactions: {len(transactions)}")
                
                if transactions:
                    st.markdown("#### Transaction Details")
                    for i, t in enumerate(transactions, 1):
                        st.markdown(f"**Transaction {i}:** Buy Day {t['buy_day']+1} → Sell Day {t['sell_day']+1} | Profit: ₹{t['profit']:.2f}")
                
                # Chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=list(range(1, len(prices)+1)), y=prices, mode='lines+markers', name='Price', line=dict(color='#10b981')))
                for t in transactions:
                    fig.add_trace(go.Scatter(x=[t['buy_day']+1], y=[prices[t['buy_day']]], mode='markers', marker=dict(color='green', size=12)))
                    fig.add_trace(go.Scatter(x=[t['sell_day']+1], y=[prices[t['sell_day']]], mode='markers', marker=dict(color='red', size=12)))
                st.plotly_chart(fig, use_container_width=True)
            
            # ALGORITHM 3: k Transactions O(nk)
            else:
                n = len(prices)
                if n == 0 or k == 0:
                    max_profit = 0
                else:
                    # DP approach
                    dp = [[0] * n for _ in range(k + 1)]
                    
                    for i in range(1, k + 1):
                        max_diff = -prices[0]
                        for j in range(1, n):
                            dp[i][j] = max(dp[i][j-1], prices[j] + max_diff)
                            max_diff = max(max_diff, dp[i-1][j] - prices[j])
                    
                    max_profit = dp[k][n-1]
                
                st.markdown("""
                <div class="metric-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white;">
                    <h3 style="color: white; margin: 0;">📊 k-Transactions DP Result</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.success(f"✅ Maximum Profit with {k} transactions: ₹{max_profit:.2f}")
                st.info(f"📊 Algorithm: Dynamic Programming O(n×k)")
                
                # Chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=list(range(1, len(prices)+1)), y=prices, mode='lines+markers', name='Price', line=dict(color='#f59e0b')))
                st.plotly_chart(fig, use_container_width=True)
            
            # Price table
            st.markdown("#### Price Data")
            price_df = pd.DataFrame({
                'Day': [f"Day {i+1}" for i in range(len(prices))],
                'Price': [f"₹{p:.2f}" for p in prices]
            })
            st.dataframe(price_df, use_container_width=True, hide_index=True)
        else:
            st.info("👆 Enter stock prices and click Analyze")
    
# Main app logic
if not st.session_state.logged_in:
    if st.session_state.page == 'login':
        login_page()
    else:
        signup_page()
else:
    if st.session_state.page == 'dashboard':
        dashboard_page()
    elif st.session_state.page == 'markets':
        markets_page()
    elif st.session_state.page == 'portfolio':
        portfolio_page()
    elif st.session_state.page == 'trade':
        trade_page()
    elif st.session_state.page == 'history':
        history_page()
    elif st.session_state.page == 'news':
        news_page()
    elif st.session_state.page == 'settings':
        settings_page()
    elif st.session_state.page == 'analyzer':
        analyzer_page()
    else:
        dashboard_page()
