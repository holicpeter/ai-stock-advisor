import os
import json
import yfinance as yf
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# --- Utility function to get timestamp ---
def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

# --- Tool functions ---

def get_user_input(prompt: str) -> dict:
    user_response = input(prompt)
    return {"user_input": user_response}

def get_stock_data(ticker: str) -> dict:
    try:
        ticker_obj = yf.Ticker(ticker)
        ticker_info = ticker_obj.info

        current_price = ticker_info.get("currentPrice")
        target_price = ticker_info.get("targetMeanPrice")

        # Fallback: try to get last close price if current price missing
        if current_price is None:
            hist = ticker_obj.history(period="1d")
            if not hist.empty:
                current_price = hist["Close"].iloc[-1]
            else:
                current_price = None

        if current_price is None or target_price is None:
            return {
                "ticker": ticker,
                "current_price": current_price,
                "target_price": target_price,
                "error": "Price data unavailable or ticker not supported."
            }

        return {
            "ticker": ticker,
            "current_price": current_price,
            "target_price": target_price,
            "error": None
        }
    
    except Exception as e:
        error_msg = str(e)
        if "Rate limited" in error_msg or "Too Many Requests" in error_msg:
            error_msg = "Yahoo Finance rate limit exceeded. Please try again in a few minutes."
        elif "Invalid ticker" in error_msg:
            error_msg = f"Invalid ticker symbol: {ticker}"
        else:
            error_msg = f"Error fetching data for {ticker}: {str(e)}"
        
        return {
            "ticker": ticker,
            "current_price": None,
            "target_price": None,
            "error": error_msg
        }

def get_recommendation(ticker: str, current_price: float, target_price: float) -> dict:
    # Simple rule-based recommendation for demo
    price_diff_pct = ((target_price - current_price) / current_price) * 100
    
    if price_diff_pct > 15:
        recommendation = "BUY"
        reasoning = f"Akcia {ticker} je výrazne pod cieľovou cenou analytikov. Aktuálna cena je ${current_price:.2f}, zatiaľ čo analytici očakávajú ${target_price:.2f} (potenciálny rast {price_diff_pct:.1f}%). To naznačuje významnú príležitosť na zhodnotenie."
    elif price_diff_pct > 5:
        recommendation = "HOLD"
        reasoning = f"Akcia {ticker} je mierne pod cieľovou cenou analytikov. Aktuálna cena ${current_price:.2f} má potenciál rastu na ${target_price:.2f} (približne {price_diff_pct:.1f}%), čo naznačuje miernu príležitosť. Odporúčame držať a monitorovať."
    elif price_diff_pct > -5:
        recommendation = "HOLD"
        reasoning = f"Akcia {ticker} je blízko cieľovej ceny analytikov. Aktuálna cena ${current_price:.2f} je v rovnováhe s cieľom ${target_price:.2f} ({price_diff_pct:+.1f}%). Držte pozíciu a sledujte vývoj."
    else:
        recommendation = "SELL"
        reasoning = f"Akcia {ticker} je nad cieľovou cenou analytikov. Aktuálna cena ${current_price:.2f} presahuje cieľ ${target_price:.2f} o {abs(price_diff_pct):.1f}%, čo môže naznačovať prekúpenosť. Zvážte realizáciu zisku."
    
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_recommendation = f"""[{ts}] 
    
📊 ANALÝZA AKCIE {ticker}
{'='*50}
💰 Aktuálna cena: ${current_price:.2f}
🎯 Cieľová cena analytikov: ${target_price:.2f}
📈 Potenciál: {price_diff_pct:+.1f}%

🔔 ODPORÚČANIE: {recommendation}

💡 Zdôvodnenie:
{reasoning}

⚠️ Disclaimer: Toto odporúčanie je len informačné a nepredstavuje finančné poradenstvo. 
Vždy konzultujte s kvalifikovaným finančným poradcom pred investičnými rozhodnutiami."""
    
    print(f"{timestamp()} 📊 Recommendation analysis completed")
    
    return {"recommendation": full_recommendation}

# --- Agent loop ---
def agent_loop():
    # Get user input
    function_args = {"prompt": "Please input a stock ticker (e.g., NVDA) or a company name (e.g., NVIDIA Corporation): "}
    function_response = get_user_input(**function_args)

    print(f"\n{timestamp()} ✅ Tool result [get_user_input]: {function_response}")

    user_input = function_response["user_input"]

    # For demo, assume it's a ticker (can be enhanced with AI ticker detection)
    ticker = user_input.upper()

    # Get stock data
    stock_data = get_stock_data(ticker)
    print(f"{timestamp()} ✅ Tool result [get_stock_data]: {stock_data}")

    if stock_data["error"]:
        print(f"\n❌ Could not retrieve stock data for {ticker}: {stock_data['error']}")
        return

    # Check target price availability
    if stock_data["target_price"] is None:
        print(f"\n❌ Could not retrieve analyst target price for {ticker}. Cannot generate recommendation.")
        return

    # Get recommendation
    reco_response = get_recommendation(
        ticker=ticker,
        current_price=stock_data["current_price"],
        target_price=stock_data["target_price"]
    )

    print("\n" + "="*60)
    print(reco_response["recommendation"])
    print("="*60)

# --- Run the agent ---
if __name__ == "__main__":
    agent_loop()
