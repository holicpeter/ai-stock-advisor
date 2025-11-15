# 🚀 Deployment na Streamlit Cloud - Krok po kroku

## ✅ Čo je už pripravené:
- ✅ `app.py` - hlavný Streamlit web UI
- ✅ `requirements.txt` - všetky závislosti
- ✅ `.streamlit/config.toml` - profesionálny dark theme
- ✅ Kód je commit-nutý a pripravený na push

## 📤 KROK 1: Nahrajte na GitHub

```powershell
# Ak ešte nemáte nahrané, spustite:
git push origin main
```

**POZNÁMKA:** Ak dostanete 403 error, možno používate iný GitHub účet. Skontrolujte:
```powershell
git config user.name
git config user.email
```

## 🌐 KROK 2: Nasadenie na Streamlit Cloud

### 1. Choďte na Streamlit Cloud
```
https://share.streamlit.io/
```

### 2. Prihláste sa
- Kliknite **"Sign in with GitHub"**
- Použite účet: **radozaprazny**

### 3. Vytvorte novú aplikáciu
- Kliknite **"New app"**
- Vyberte:
  - **Repository:** `radozaprazny/ai-stock-advisor`
  - **Branch:** `main`
  - **Main file path:** `app.py`
  - **App URL (optional):** `ai-stock-advisor-trader20` (alebo čokoľvek)

### 4. Pridajte API kľúč (KRITICKÉ!)
Pred deployment:
1. Kliknite **"Advanced settings"**
2. V sekcii **"Secrets"** pridajte:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-VÁŠE-SKUTOČNÉ-API-KEY"
```

⚠️ **BEZ ÚVODZOVIEK V HODNOTE!** Správne:
```toml
ANTHROPIC_API_KEY = "sk-ant-api03-xxxxx"
```

### 5. Deploy!
- Kliknite **"Deploy!"**
- Počkajte 2-3 minúty

## 🎉 Hotovo!

Dostanete verejný link, niečo ako:
```
https://ai-stock-advisor-trader20.streamlit.app
```

## 📱 Zdieľanie zákazníkovi

Tento link môžete poslať komukoľvek:
- ✅ Funguje na mobile aj desktop
- ✅ Žiadna inštalácia
- ✅ Real-time AI analýza
- ✅ Professional trading UI

## 🔒 Pre privátny prístup (len pre Trader 2.0 Club)

Ak chcete heslo-chránený prístup:

### Možnosť 1: Streamlit Cloud Authentication (paid)
- Upgrade na paid plán
- Pridajte email whitelist

### Možnosť 2: Vlastné heslo (free)
Pridajte do `app.py`:

```python
def check_password():
    def password_entered():
        if st.session_state["password"] == "trader2024":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Heslo pre Trader 2.0 Club:", 
                     type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Heslo pre Trader 2.0 Club:", 
                     type="password", on_change=password_entered, key="password")
        st.error("❌ Nesprávne heslo")
        return False
    else:
        return True

# Na začiatku app.py pridajte:
if not check_password():
    st.stop()
```

## 🔧 Troubleshooting

### Problém: "API key not found"
**Riešenie:** Skontrolujte secrets v Streamlit Cloud dashboard

### Problém: "ModuleNotFoundError"
**Riešenie:** Skontrolujte `requirements.txt` - všetky balíčky musia byť tam

### Problém: App sa načítava pomaly
**Riešenie:** Normálne - prvé spustenie trvá 2-3 minúty. Potom je rýchle.

## 📊 Čo ukázať zákazníkovi

1. **Otvorte link** - krásne profesionálne UI
2. **Zadajte "NVDA"** - okamžitá analýza
3. **Zadajte "Microsoft"** - AI identifikuje ticker
4. **Ukážte graf** - visual porovnanie cien
5. **Zdôraznite BUY/HOLD/SELL** - jasné odporúčanie

## 💰 Cena

- **Streamlit Cloud:** FREE (verejné apps)
- **Claude API:** Pay-as-you-go (cca $0.001 na analýzu)
- **Yahoo Finance:** FREE

Pre club s 100 členmi = cca $5-10/mesiac Claude API.

## 🚀 Ďalšie kroky po úspešnom demo

1. Pridať historické grafy
2. Pridať viacero akcií naraz
3. Pridať portfolio tracking
4. Email notifikácie
5. Vlastná doména (trader20.club)
