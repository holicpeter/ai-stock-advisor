# 📈 AI Stock Advisor Agent

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![Yahoo Finance](https://img.shields.io/badge/Yahoo-Finance-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Overview

An intelligent Python-based stock advisor agent that combines the power of OpenAI's GPT models with real-time Yahoo Finance data to provide automated stock recommendations. The agent can process both company names and stock ticker symbols, fetch current market data, and generate AI-driven BUY/HOLD/SELL recommendations.

## ✨ Features

- **🔍 Smart Ticker Recognition:** Automatically identifies stock ticker symbols from company names using OpenAI GPT-4
- **📊 Real-Time Market Data:** Fetches current and analyst target prices using Yahoo Finance API
- **🤖 AI-Powered Recommendations:** Generates BUY/HOLD/SELL recommendations based on price analysis
- **📋 Token Usage Tracking:** Monitors and logs OpenAI API token consumption
- **⚡ Fast Processing:** Optimized for quick response times
- **🛡️ Error Handling:** Robust error handling for invalid tickers and API failures

## 🛠️ Installation

### Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Internet connection for real-time data

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/ai-stock-advisor.git
   cd ai-stock-advisor
   ```

2. **Install dependencies using UV (recommended):**

   ```bash
   # Install UV if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Sync dependencies
   uv sync
   ```

   **Or using pip with pyproject.toml:**

   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**

   Copy the example environment file and add your OpenAI API key:

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

## 🎯 Usage

### Basic Usage

```bash
# Using UV (recommended)
uv run python main.py

# Using regular Python
python main.py
```

### Example Session

```text
Please input a stock ticker (e.g., NVDA) or a company name (e.g., NVIDIA Corporation): Tesla

[2025-07-10 00:22:30] ✅ Tool result [get_user_input]: {'user_input': 'tesla'}
[2025-07-10 00:22:32] 🔢 Token usage [get_ticker_from_llm]: CompletionUsage(completion_tokens=2, prompt_tokens=57, total_tokens=59)
[2025-07-10 00:22:32] ✅ Tool result [get_ticker_from_llm]: {'ticker': 'TSLA'}
[2025-07-10 00:22:33] ✅ Tool result [get_stock_data]: {'ticker': 'TSLA', 'current_price': 295.88, 'target_price': 306.07172, 'error': None}

--- Final Recommendation ---
[2025-07-10 00:22:35] Recommendation: HOLD

The current price of TSLA is $295.88, which is close to the target price of $306.07172.

⚠️ Disclaimer: This recommendation is for informational purposes only and does not constitute financial advice.
```

### Input Options

- **Stock Ticker:** Direct ticker symbols (e.g., `AAPL`, `GOOGL`, `MSFT`)
- **Company Name:** Full company names (e.g., `Apple Inc.`, `Google`, `Microsoft Corporation`)

## 🏗️ Architecture

The agent consists of several key components:

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Ticker Lookup  │───▶│  Stock Data     │
│                 │    │   (OpenAI)      │    │  (Yahoo Finance)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐             │
│ Recommendation  │◀───│   AI Analysis   │◀────────────┘
│    Output       │    │   (OpenAI)      │
└─────────────────┘    └─────────────────┘
```

### Core Functions

- `get_user_input()`: Handles user input for ticker/company name
- `get_ticker_from_llm()`: Converts company names to ticker symbols
- `get_stock_data()`: Fetches real-time stock data from Yahoo Finance
- `get_recommendation()`: Generates AI-powered buy/hold/sell recommendations

## 📁 Project Structure

```text
ai-stock-advisor/
├── main.py              # Main application entry point
├── pyproject.toml       # Project dependencies and configuration
├── uv.lock             # UV lock file for reproducible builds
├── .env.example        # Example environment variables file
├── .env                # Environment variables (not tracked)
├── .gitignore          # Git ignore file
├── .python-version     # Python version specification
├── LICENSE             # MIT License
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### Dependencies

- `openai>=1.66.3` - OpenAI API client
- `yfinance>=0.2.54` - Yahoo Finance data fetcher
- `python-dotenv>=1.0.1` - Environment variable loader
- `curl-cffi>=0.11.4` - HTTP client for enhanced performance

## 🚨 Error Handling

The agent includes comprehensive error handling for:

- Invalid or non-existent stock tickers
- API rate limiting and timeouts
- Network connectivity issues
- Missing environment variables
- Malformed user input

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT:** The recommendations provided by this agent are for informational and educational purposes only and do not constitute financial advice. Stock market investments carry inherent risks, and past performance does not guarantee future results.

Please consult with a qualified financial advisor before making any investment decisions. The developers of this tool are not responsible for any financial losses that may occur from using this software.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT API
- [Yahoo Finance](https://finance.yahoo.com/) for real-time stock data
- [UV](https://github.com/astral-sh/uv) for modern Python packaging
