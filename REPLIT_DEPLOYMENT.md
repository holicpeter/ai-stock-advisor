# Replit Deployment Guide

## Rýchly návod na nasadenie AI Stock Advisor na Replit

### 1. Vytvorte Replit účet
- Choďte na https://replit.com
- Zaregistrujte sa alebo sa prihláste

### 2. Importujte GitHub repozitár
1. Kliknite na **"Create Repl"**
2. Vyberte **"Import from GitHub"**
3. Zadajte URL: `https://github.com/holicpeter/ai-stock-advisor`
4. Kliknite **"Import from GitHub"**

### 3. Nastavte Secrets (API kľúč)
1. V ľavom menu kliknite na **🔒 Secrets** (zámok)
2. Pridajte nový secret:
   - **Key**: `ANTHROPIC_API_KEY`
   - **Value**: `váš_anthropic_api_kľúč`
3. Kliknite **"Add secret"**

### 4. Nainštalujte závislosti
V **Shell** tab zadajte:
```bash
pip install -r requirements.txt
```

### 5. Spustite aplikáciu
Kliknite na veľké zelené tlačidlo **"Run"** hore.

### 6. Zdieľajte link zákazníkovi
- Po spustení sa zobrazí URL (napr. `https://ai-stock-advisor.username.repl.co`)
- Túto URL môžete poslať zákazníkovi z Trader 2.0 Club
- Aplikácia bude vždy dostupná na tejto adrese

## Výhody Replit vs Streamlit Cloud
✅ Jednoduchšie nasadenie (bez konfliktov závislostí)  
✅ Stabilnejšie prostredie  
✅ Automatická inštalácia závislostí  
✅ Rýchlejšie reštarty  
✅ Žiadne problémy s libpython  

## Dôležité poznámky

### Bezplatný plán
- Aplikácia sa uspí po 30 minútach nečinnosti
- Pri prvom prístupe trvá 10-15 sekúnd prebúdzanie
- Pre nepretržitý chod potrebujete Replit **Hacker Plan** ($7/mesiac)

### Yahoo Finance Rate Limits
- Bezplatné API má limit 2000 požiadaviek/hodinu
- Aplikácia má implementované cachovanie (5 minút)
- Pri prekročení limitu sa zobrazí hlásenie s pokusmi o opätovné pripojenie

### Debugging
Ak niečo nefunguje:
1. Skontrolujte **Console** tab pre chyby
2. Overte že `ANTHROPIC_API_KEY` je správne nastavený v Secrets
3. Reštartujte aplikáciu tlačidlom **Stop** a potom **Run**

## Alternatívne deployments
Ak Replit nefunguje, máte ešte tieto možnosti:
- **Railway**: https://railway.app (podobné ako Replit)
- **Heroku**: Robustnejšie ale platené
- **Lokálny hosting + ngrok**: Pre krátkodobé demo
