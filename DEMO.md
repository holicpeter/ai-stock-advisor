# 🎯 Návod na ukázku AI Stock Advisor agenta

## 📋 Príprava pred ukázkou

### 1. Overenie inštalácie

```powershell
# Skontrolujte, či máte Python 3.12+
python --version

# Skontrolujte inštalované balíčky
pip list
```

### 2. Nastavenie API kľúča

Vytvorte súbor `.env` v hlavnom adresári projektu s vaším OpenAI API kľúčom:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Inštalácia závislostí (ak ešte neboli nainštalované)

```powershell
pip install openai python-dotenv yfinance curl-cffi
```

## 🚀 Spustenie ukázky

### Jednoduchý spôsob

```powershell
cd c:\AI-agents\AI-stock\ai-stock-advisor
python main.py
```

## 💡 Príklady na ukázku zákazníkovi

### 1. Technologické akcie
- **NVIDIA** - Agent automaticky identifikuje ticker NVDA
- **Microsoft** - Ticker MSFT
- **Apple** - Ticker AAPL

### 2. Slovenské/Európske akcie (ak sú na burze)
- **Volkswagen** - Ticker VOW.DE (musíte zadať ticker priamo)
- **Tesla** - Agent vie identifikovať ticker TSLA

### 3. Priamy ticker
- **GOOGL** - Google/Alphabet
- **AMZN** - Amazon

## 📝 Scenár ukázky pre zákazníka

### Krok 1: Úvod (30 sekúnd)
Vysvetlite: "Toto je AI agent, ktorý kombinuje OpenAI GPT model s real-time dátami z Yahoo Finance na poskytovanie odporúčaní pre akcie."

### Krok 2: Ukázka funkčnosti (2-3 minúty)

```
Spustíte: python main.py
Agent sa opýta: "What company or stock ticker symbol are you interested in?"
Zadáte: NVIDIA
```

Agent ukáže:
1. ✅ Identifikáciu ticker symbolu (NVDA)
2. 📊 Aktuálnu cenu akcie
3. 🎯 Cieľovú cenu od analytikov
4. 💡 AI odporúčanie (BUY/HOLD/SELL)
5. 📝 Zdôvodnenie rozhodnutia

### Krok 3: Ukázka ďalších príkladov (1-2 minúty)
Spustite znova s inými firmami:
- Microsoft
- Tesla
- Apple

### Krok 4: Výhody riešenia
- ⚡ **Rýchlosť**: Odpoveď do 5 sekúnd
- 🤖 **AI inteligencia**: GPT-4 analýza
- 📊 **Real-time dáta**: Aktuálne tržné informácie
- 🎯 **Presnosť**: Porovnanie s analytickými cieľmi
- 🔢 **Transparentnosť**: Vidíte token usage a reasoning

## ⚠️ Dôležité upozornenia

### Pred ukázkou skontrolujte:
- ✅ Máte aktívny OpenAI API kľúč s kreditom
- ✅ Máte stabilné internetové pripojenie
- ✅ Yahoo Finance API nie je rate-limited (skúste pár testov pred ukázkou)

### Čo povedať zákazníkovi:
- ℹ️ Toto je demo verzia - production verzia by mala web rozhranie
- ℹ️ Odporúčania sú len informačné, nie finančné poradenstvo
- ℹ️ Dáta sú real-time z Yahoo Finance
- ℹ️ Agent vie spracovať názvy firiem aj ticker symboly

## 🎬 Alternatívy pre prezentáciu

### Možnosť A: Live demo
Najlepšie - ukazujete reálne fungovanie s aktuálnymi dátami.

### Možnosť B: Nahraná ukázka
Ak sa obávate internetového pripojenia, nahrať video vopred.

### Možnosť C: Jupyter Notebook
Vytvoriť interaktívny notebook s výstupmi pre lepšiu prezentáciu.

### Možnosť D: Web rozhranie (vyžaduje vývoj)
Profesionálne riešenie s Streamlit alebo Flask.

## 🔧 Troubleshooting

### Problém: "Rate limit exceeded"
**Riešenie**: Počkajte 1-2 minúty, Yahoo Finance má limity na dotazy.

### Problém: OpenAI API error
**Riešenie**: Skontrolujte API kľúč a kredit na OpenAI účte.

### Problém: "Invalid ticker"
**Riešenie**: Použite známu firmu (NVIDIA, Microsoft, Apple).

## 📊 Čo zdôrazniť zákazníkovi

1. **Automatizácia**: Agent sám zistí ticker z názvu firmy
2. **AI reasoning**: Vidíte kompletné zdôvodnenie rozhodnutia
3. **Rýchlosť**: Výsledok do pár sekúnd
4. **Presnosť**: Porovnanie s analytickými odhadmi
5. **Rozšíriteľnosť**: Môže sa integrovať do väčšieho systému

## 🚀 Ďalšie kroky po ukázke

Ak zákazník prejaví záujem:
- Vytvoriť web rozhranie (Streamlit/Flask)
- Pridať historické grafy a technickú analýzu
- Rozšíriť o portfólio management
- Pridať notifikácie a alerting
- Integrovať viacero dátových zdrojov
