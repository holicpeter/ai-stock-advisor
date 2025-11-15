import os
import streamlit as st
import yfinance as yf
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime
import plotly.graph_objects as go
from pdf_generator import create_pdf_report

# Load environment variables (for local dev)
load_dotenv()

# Initialize Anthropic client
@st.cache_resource
def get_ai_client():
    # Try Streamlit secrets first (for cloud), then env variable (for local)
    api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY nie je nastavený! Skontrolujte Streamlit Cloud secrets.")
        st.stop()
    return Anthropic(api_key=api_key)

client = get_ai_client()

# Page config
st.set_page_config(
    page_title="AI Stock Advisor - Trader 2.0 Club",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional trading look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2127;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2e3137;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .recommendation-buy {
        background-color: #1a4d2e;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4caf50;
    }
    .recommendation-sell {
        background-color: #4d1a1a;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #f44336;
    }
    .recommendation-hold {
        background-color: #4d3d1a;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff9800;
    }
    .header-box {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-box">
    <h1 style="color: white; margin: 0;">📈 AI Stock Advisor</h1>
    <p style="color: #e0e0e0; margin: 5px 0 0 0;">Powered by Claude AI & Real-Time Market Data</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/stocks.png", width=80)
    st.title("Trader 2.0 Club")
    st.markdown("---")
    st.markdown("### 🎯 Ako to funguje:")
    st.markdown("""
    1. Zadajte ticker alebo názov firmy
    2. AI získa real-time dáta
    3. Dostanete BUY/HOLD/SELL odporúčanie
    4. S detailným zdôvodnením
    """)
    st.markdown("---")
    st.markdown("### 📊 Príklady:")
    st.code("NVDA")
    st.code("Microsoft")
    st.code("TSLA")
    st.code("Apple")
    
    st.markdown("---")
    st.info("💡 **Premium služba** pre členov Trader 2.0 Club")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🔍 Zadajte akciu na analýzu")
    user_input = st.text_input(
        "Ticker symbol alebo názov firmy",
        placeholder="Napr. NVDA, Microsoft, Tesla...",
        help="Môžete zadať priamo ticker (NVDA) alebo názov firmy (NVIDIA)"
    )
    
    analyze_button = st.button("🚀 Analyzovať", type="primary", use_container_width=True)

with col2:
    st.markdown("### ⚡ Rýchle akcie")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("NVDA", use_container_width=True):
            user_input = "NVDA"
            analyze_button = True
        if st.button("MSFT", use_container_width=True):
            user_input = "MSFT"
            analyze_button = True
    with col_b:
        if st.button("TSLA", use_container_width=True):
            user_input = "TSLA"
            analyze_button = True
        if st.button("AAPL", use_container_width=True):
            user_input = "AAPL"
            analyze_button = True

st.markdown("---")

# Analysis section
if analyze_button and user_input:
    with st.spinner("🔄 Analyzujem akciu..."):
        
        # Determine if input is ticker or company name
        if user_input.isupper() and 1 <= len(user_input) <= 5:
            ticker = user_input
            st.info(f"✅ Používam ticker: **{ticker}**")
        else:
            # Use AI to get ticker
            st.info(f"🤖 Zisťujem ticker pre: **{user_input}**...")
            try:
                response = client.messages.create(
                    model="claude-3-5-haiku-20241022",
                    max_tokens=100,
                    system="You are a financial assistant. Given a company name, return ONLY its exact stock ticker symbol. Return only the ticker text (e.g., 'NVDA'). No extra explanation.",
                    messages=[{"role": "user", "content": f"What is the stock ticker symbol for {user_input}?"}]
                )
                ticker = response.content[0].text.strip().upper()
                st.success(f"✅ Ticker identifikovaný: **{ticker}**")
            except Exception as e:
                st.error(f"❌ Chyba pri identifikácii tickeru: {str(e)}")
                st.stop()
        
        # Get stock data
        st.info(f"📊 Získavam real-time dáta pre **{ticker}**...")
        try:
            ticker_obj = yf.Ticker(ticker)
            ticker_info = ticker_obj.info
            
            current_price = ticker_info.get("currentPrice")
            target_price = ticker_info.get("targetMeanPrice")
            
            # Fallback
            if current_price is None:
                hist = ticker_obj.history(period="1d")
                if not hist.empty:
                    current_price = hist["Close"].iloc[-1]
            
            if current_price is None or target_price is None:
                st.error(f"❌ Nedostupné cenové dáta pre {ticker}")
                st.stop()
            
            st.success(f"✅ Dáta získané úspešne!")
            
        except Exception as e:
            st.error(f"❌ Chyba pri získavaní dát: {str(e)}")
            st.stop()
        
        # Company Info Header
        company_name = ticker_info.get("longName", ticker)
        sector = ticker_info.get("sector", "N/A")
        industry = ticker_info.get("industry", "N/A")
        
        st.markdown(f"## 🏢 {company_name} ({ticker})")
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"**📂 Sektor:** {sector}")
        with col_info2:
            st.markdown(f"**🏭 Odvetvie:** {industry}")
        
        st.markdown("---")
        
        # Display price metrics
        st.markdown("### 💰 Kľúčové cenové metriky")
        col1, col2, col3, col4 = st.columns(4)
        
        price_diff = target_price - current_price
        price_diff_pct = (price_diff / current_price) * 100
        
        with col1:
            st.metric("💵 Aktuálna cena", f"${current_price:.2f}")
        with col2:
            st.metric("🎯 Cieľová cena analytikov", f"${target_price:.2f}")
        with col3:
            st.metric("📈 Potenciálny rast", f"{price_diff_pct:+.2f}%", 
                     delta=f"${price_diff:+.2f}")
        with col4:
            market_cap = ticker_info.get("marketCap")
            if market_cap:
                market_cap_b = market_cap / 1e9
                st.metric("💼 Market Cap", f"${market_cap_b:.1f}B")
        
        # Create price chart
        st.markdown("### 📊 Porovnanie cien")
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=['Aktuálna cena', 'Cieľová cena'],
            y=[current_price, target_price],
            marker_color=['#4a90e2', '#50c878'],
            text=[f'${current_price:.2f}', f'${target_price:.2f}'],
            textposition='auto',
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=300,
            showlegend=False,
            yaxis_title="Cena (USD)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Get AI recommendation
        st.markdown("### 🤖 AI Analýza")
        with st.spinner("⚡ Claude AI analyzuje..."):
            try:
                response = client.messages.create(
                    model="claude-3-5-haiku-20241022",
                    max_tokens=500,
                    system="You are a financial assistant. Make a BUY/HOLD/SELL recommendation: BUY if current price much lower than target price, HOLD if close, SELL if higher.",
                    messages=[{
                        "role": "user",
                        "content": f"Ticker: {ticker}, Current price: {current_price}, Target price: {target_price}."
                    }]
                )
                recommendation_text = response.content[0].text.strip()
                
                # Determine recommendation type
                if "BUY" in recommendation_text.upper()[:50]:
                    rec_type = "BUY"
                    rec_emoji = "🟢"
                    rec_class = "recommendation-buy"
                elif "SELL" in recommendation_text.upper()[:50]:
                    rec_type = "SELL"
                    rec_emoji = "🔴"
                    rec_class = "recommendation-sell"
                else:
                    rec_type = "HOLD"
                    rec_emoji = "🟡"
                    rec_class = "recommendation-hold"
                
                # Display recommendation with detailed breakdown
                st.markdown(f"""
                <div class="{rec_class}">
                    <h2 style="margin: 0;">{rec_emoji} ODPORÚČANIE: {rec_type}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Summary box
                col_sum1, col_sum2 = st.columns(2)
                with col_sum1:
                    st.markdown("#### 📊 Zhrnutie analýzy")
                    st.markdown(f"""
                    - **Ticker:** {ticker}
                    - **Aktuálna cena:** ${current_price:.2f}
                    - **Cieľová cena:** ${target_price:.2f}
                    - **Cenový rozdiel:** ${price_diff:+.2f} ({price_diff_pct:+.1f}%)
                    """)
                
                with col_sum2:
                    st.markdown("#### 🎯 Investičný potenciál")
                    if price_diff_pct > 20:
                        st.success("🔥 Vysoký potenciál rastu (20%+)")
                    elif price_diff_pct > 10:
                        st.info("📈 Stredný potenciál rastu (10-20%)")
                    elif price_diff_pct > 0:
                        st.warning("⚖️ Nízky potenciál rastu (0-10%)")
                    else:
                        st.error("📉 Akcia nad cieľovou cenou")
                
                st.markdown("---")
                
                st.markdown("#### 💡 Detailné zdôvodnenie AI:")
                st.markdown(recommendation_text)
                
                st.markdown("---")
                
                # Rationale breakdown
                st.markdown("#### 🧠 Racionále:")
                rationale_col1, rationale_col2 = st.columns(2)
                
                with rationale_col1:
                    st.markdown("**✅ Pozitívne faktory:**")
                    if price_diff_pct > 15:
                        st.markdown("- Výrazne pod cieľovou cenou")
                    if sector in ["Technology", "Healthcare", "Financial Services"]:
                        st.markdown(f"- Silný sektor ({sector})")
                    if market_cap and market_cap > 100e9:
                        st.markdown("- Veľká kapitalizácia (stabilita)")
                
                with rationale_col2:
                    st.markdown("**⚠️ Body na zváženie:**")
                    if price_diff_pct < 5:
                        st.markdown("- Malý priestor na rast")
                    if price_diff_pct < 0:
                        st.markdown("- Možné prekúpenie")
                    st.markdown("- Trhové podmienky sa menia")
                
                st.info(f"⚡ Claude AI - Token usage: {response.usage.input_tokens} vstup / {response.usage.output_tokens} výstup")
                
                # PDF Download Button
                st.markdown("---")
                st.markdown("### 📄 Stiahnuť kompletný report")
                
                try:
                    pdf_data = create_pdf_report(
                        ticker=ticker,
                        company_name=company_name,
                        sector=sector,
                        industry=industry,
                        current_price=current_price,
                        target_price=target_price,
                        recommendation=rec_type,
                        recommendation_text=recommendation_text,
                        ticker_info=ticker_info,
                        price_diff_pct=price_diff_pct
                    )
                    
                    st.download_button(
                        label="📥 Download Full Report (PDF)",
                        data=pdf_data,
                        file_name=f"{ticker}_AI_Stock_Analysis_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
                    
                    st.success("✅ PDF report je pripravený na stiahnutie!")
                    
                except Exception as pdf_error:
                    st.warning(f"⚠️ PDF report momentálne nie je dostupný: {str(pdf_error)}")
                
            except Exception as e:
                st.error(f"❌ Chyba pri AI analýze: {str(e)}")
        
        # Disclaimer
        st.markdown("---")
        st.warning("""
        ⚠️ **DISCLAIMER:** Toto odporúčanie je len informačné a nepredstavuje finančné poradenstvo. 
        Investovanie v akciách nesie riziko. Vždy konzultujte s kvalifikovaným finančným poradcom 
        pred investičnými rozhodnutiami.
        """)
        
        # Additional financial metrics
        with st.expander("📈 Ďalšie finančné metriky"):
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.markdown("**📊 Valuácia**")
                pe_ratio = ticker_info.get("trailingPE")
                if pe_ratio:
                    st.metric("P/E Ratio", f"{pe_ratio:.2f}")
                pb_ratio = ticker_info.get("priceToBook")
                if pb_ratio:
                    st.metric("P/B Ratio", f"{pb_ratio:.2f}")
            
            with metric_col2:
                st.markdown("**💰 Dividendy**")
                div_yield = ticker_info.get("dividendYield")
                if div_yield:
                    st.metric("Dividend Yield", f"{div_yield*100:.2f}%")
                else:
                    st.metric("Dividend Yield", "N/A")
            
            with metric_col3:
                st.markdown("**📉 Volatilita**")
                beta = ticker_info.get("beta")
                if beta:
                    st.metric("Beta", f"{beta:.2f}")
                volume = ticker_info.get("volume")
                if volume:
                    st.metric("Objem", f"{volume:,.0f}")
        
        # Company details
        with st.expander("🏢 Detaily o spoločnosti"):
            st.markdown(f"**Názov:** {ticker_info.get('longName', 'N/A')}")
            st.markdown(f"**Ticker:** {ticker}")
            st.markdown(f"**Sektor:** {ticker_info.get('sector', 'N/A')}")
            st.markdown(f"**Odvetvie:** {ticker_info.get('industry', 'N/A')}")
            st.markdown(f"**Krajina:** {ticker_info.get('country', 'N/A')}")
            st.markdown(f"**Website:** {ticker_info.get('website', 'N/A')}")
            
            business_summary = ticker_info.get('longBusinessSummary')
            if business_summary:
                st.markdown("**Popis podnikania:**")
                st.markdown(business_summary[:500] + "..." if len(business_summary) > 500 else business_summary)
            
            st.markdown(f"**Čas analýzy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

else:
    # Landing state
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2>👋 Vitajte v AI Stock Advisor</h2>
        <p style="font-size: 18px; color: #888;">
            Zadajte ticker symbol alebo názov firmy a získajte AI-powered odporúčanie<br>
            s real-time tržnými dátami.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show example
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**📈 Real-time dáta**\nYahoo Finance API")
    with col2:
        st.success("**🤖 AI analýza**\nClaude 3.5 Haiku")
    with col3:
        st.warning("**⚡ Okamžitý výsledok**\nDo 5 sekúnd")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🔒 Premium služba pre členov <strong>Trader 2.0 Club</strong></p>
    <p style="font-size: 12px;">Powered by Claude AI & Yahoo Finance | © 2025</p>
</div>
""", unsafe_allow_html=True)
