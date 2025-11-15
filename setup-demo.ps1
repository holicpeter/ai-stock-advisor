# AI Stock Advisor - Setup Demo

Write-Host "=== AI Stock Advisor - Priprava ===" -ForegroundColor Cyan
Write-Host ""

# 1. Kontrola Python verzie
Write-Host "1. Kontrolujem Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python nie je nainstalovany!" -ForegroundColor Red
    exit 1
}
Write-Host "OK: Python nainstalovany" -ForegroundColor Green
Write-Host ""

# 2. Instalacia zavislosti
Write-Host "2. Instalujem zavislosti..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install openai python-dotenv yfinance curl-cffi
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Chyba pri instalacii!" -ForegroundColor Red
    exit 1
}
Write-Host "OK: Zavislosti nainstalovane" -ForegroundColor Green
Write-Host ""

# 3. Kontrola .env suboru
Write-Host "3. Kontrolujem API kluc..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "OK: .env subor existuje" -ForegroundColor Green
    
    # Skontroluj ci obsahuje API kluc
    $envContent = Get-Content .env -Raw
    if ($envContent -match "OPENAI_API_KEY=sk-") {
        Write-Host "OK: OpenAI API kluc je nastaveny" -ForegroundColor Green
    } else {
        Write-Host "WARNING: API kluc mozno nie je spravne nastaveny" -ForegroundColor Yellow
    }
} else {
    Write-Host "WARNING: .env subor neexistuje!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Vytovaram ukazkovy .env subor..." -ForegroundColor Yellow
    @"
OPENAI_API_KEY=sk-your-api-key-here
"@ | Out-File -FilePath ".env" -Encoding utf8
    Write-Host "OK: .env subor vytvoreny - MUSITE doplnit vas API kluc!" -ForegroundColor Yellow
    Write-Host "   Upravte subor .env a doplnte vas OpenAI API kluc" -ForegroundColor Yellow
}
Write-Host ""

# 4. Test spustenia
Write-Host "4. Hotovo! Mozete spustit ukazku:" -ForegroundColor Yellow
Write-Host "   python main.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pre viac informacii si precitajte DEMO.md" -ForegroundColor Magenta
Write-Host ""
