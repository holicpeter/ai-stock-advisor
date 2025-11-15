# AI Stock Advisor - Streamlit Cloud Deployment

POZOR: Streamlit Cloud **nemôže používať `.env`** súbory!

## 🚀 Nasadenie na Streamlit Cloud

### Krok 1: Push na GitHub
```powershell
git add .
git commit -m "Add Streamlit web UI"
git push origin main
```

### Krok 2: Nasadiť na Streamlit Cloud

1. Choďte na: **https://share.streamlit.io/**
2. Prihláste sa s GitHub účtom
3. Kliknite **"New app"**
4. Vyberte:
   - Repository: `radozaprazny/ai-stock-advisor`
   - Branch: `main`
   - Main file path: `app.py`

### Krok 3: Pridať API kľúč (DÔLEŽITÉ!)

V Streamlit Cloud app settings:
1. Kliknite **"⋮" → Advanced settings → Secrets**
2. Pridajte:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-api-key"
```

### Krok 4: Deploy
- Kliknite **"Deploy"**
- Počkajte 2-3 minúty
- Dostanete verejný link: `https://your-app.streamlit.app`

## 📱 Zdieľanie zákazníkovi

Link bude verejný a dostupný pre kohokoľvek.
Príklad: `https://ai-stock-advisor.streamlit.app`

## 🔒 Pre privátnu verziu (platené)

Ak chcete heslo-chránené pre Trader 2.0 Club:
- Streamlit Cloud ponúka **authentication** v paid plánoch
- Alebo použite vlastný hosting (Heroku, Railway, etc.)

## ⚙️ Aktualizácia app.py pre Streamlit Cloud

Musíme zmeniť načítanie API kľúča z `.env` na `st.secrets`:
