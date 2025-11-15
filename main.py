import os
import json
import yfinance as yf
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# --- Utility function to get timestamp ---
def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

# --- Tool functions ---

def get_user_input(prompt: str) -> dict:
    user_response = input(prompt)
    return {"user_input": user_response}

def get_ticker_from_llm(company_name: str) -> dict:
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=100,
        system="You are a financial assistant. Given a company name, return ONLY its exact stock ticker symbol. Return only the ticker text (e.g., 'NVDA'). No extra explanation.",
        messages=[
            {
                "role": "user",
                "content": f"What is the stock ticker symbol for {company_name}?"
            }
        ]
    )
    ticker = response.content[0].text.strip().upper()

    # Print token usage
    print(f"{timestamp()} 🔢 Token usage [get_ticker_from_llm]: input={response.usage.input_tokens}, output={response.usage.output_tokens}")

    return {"ticker": ticker}

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
        # Handle rate limiting and other errors
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
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=500,
        system="You are a financial assistant. Make a BUY/HOLD/SELL recommendation: BUY if current price much lower than target price, HOLD if close, SELL if higher.",
        messages=[
            {
                "role": "user",
                "content": f"Ticker: {ticker}, Current price: {current_price}, Target price: {target_price}."
            }
        ]
    )
    recommendation_body = response.content[0].text.strip()

    # Print token usage
    print(f"{timestamp()} 🔢 Token usage [get_recommendation]: input={response.usage.input_tokens}, output={response.usage.output_tokens}")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_recommendation = f"[{ts}] Recommendation: {recommendation_body}\n\n⚠️ Disclaimer: This recommendation is for informational purposes only and does not constitute financial advice. Please consult a qualified financial advisor before making investment decisions."
    
    return {"recommendation": full_recommendation}

# --- Function schemas for OpenAI ---

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_user_input",
            "description": "Get user input for ticker or company name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Prompt to show to the user."
                    }
                },
                "required": ["prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticker_from_llm",
            "description": "Get ticker symbol from LLM given a company name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "Company name to find the ticker for."
                    }
                },
                "required": ["company_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_data",
            "description": "Fetch current and target price for a given ticker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Ticker symbol of the stock."
                    }
                },
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_recommendation",
            "description": "Make a stock recommendation based on prices.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker"},
                    "current_price": {"type": "number", "description": "Current price"},
                    "target_price": {"type": "number", "description": "Target mean price"}
                },
                "required": ["ticker", "current_price", "target_price"]
            }
        }
    }
]

# --- Map of local functions ---
available_functions = {
    "get_user_input": get_user_input,
    "get_ticker_from_llm": get_ticker_from_llm,
    "get_stock_data": get_stock_data,
    "get_recommendation": get_recommendation,
}

# --- Agent loop ---
def agent_loop():
    messages = [
        {
            "role": "system",
            "content": (
                "You are a stock advisor agent. Ask the user to input either a stock ticker directly (e.g., NVDA) or a company name (e.g., NVIDIA Corporation). "
                "If the input looks like a ticker (all uppercase, 1–5 letters), use it directly. "
                "Otherwise, use your tool to get the ticker from the company name. Then fetch stock data and give a recommendation."
            )
        }
    ]

    # Always use consistent prompt
    function_args = {"prompt": "Please input a stock ticker (e.g., NVDA) or a company name (e.g., NVIDIA Corporation): "}
    function_response = get_user_input(**function_args)

    print(f"\n{timestamp()} ✅ Tool result [get_user_input]: {function_response}")

    user_input = function_response["user_input"]

    if user_input.isupper() and 1 <= len(user_input) <= 5:
        ticker = user_input
    else:
        function_response = get_ticker_from_llm(user_input)
        print(f"{timestamp()} ✅ Tool result [get_ticker_from_llm]: {function_response}")

        # Check ticker validity
        if not (function_response["ticker"].isupper() and 1 <= len(function_response["ticker"]) <= 5):
            print(f"\n❌ The company '{user_input}' does not appear to have a valid stock ticker symbol or it is not publicly traded.")
            return

        ticker = function_response["ticker"]

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
    print(f"{timestamp()} ✅ Tool result [get_recommendation]: {reco_response}")

    print("\n--- Final Recommendation ---")
    print(reco_response["recommendation"])

# --- Run the agent ---
if __name__ == "__main__":
    agent_loop()
