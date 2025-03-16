# Automatisierte Fundamentalanalyse mit Financial Modeling Prep API

Dieses Projekt ermöglicht die automatisierte Analyse und Bewertung von Aktien basierend auf fundamentalen Kennzahlen. Es ruft Finanzdaten über die Financial Modeling Prep API ab, berechnet verschiedene Kennzahlen, bewertet die Aktien nach einem Scoring-Modell und sendet Benachrichtigungen über Telegram.

## Features

- **Datenbeschaffung**: Abrufen von Finanzdaten über die Financial Modeling Prep API
- **Berechnung von Fundamentalkennzahlen**:
  - KGV (Kurs-Gewinn-Verhältnis)
  - KUV (Kurs-Umsatz-Verhältnis)
  - KBV (Kurs-Buchwert-Verhältnis)
  - Dividendenrendite
  - EPS (Earnings Per Share)
  - Umsatzwachstum der letzten 5 Jahre
  - Eigenkapitalrendite (ROE)
  - Verschuldungsquote
- **Scoring-Modell**: Bewertung der Aktien nach verschiedenen Kriterien
- **Visualisierung**: Erstellung von Balkendiagrammen mit den besten Aktien
- **Telegram-Benachrichtigung**: Versand von Benachrichtigungen bei überdurchschnittlichen Aktien

## Installation

1. Klone das Repository:
   ```
   git clone https://github.com/yourusername/stock-analysis.git
   cd stock-analysis
   ```

2. Installiere die Abhängigkeiten:
   ```
   pip install -r requirements.txt
   ```

3. Erstelle eine `config.json` Datei mit deinen API-Schlüsseln:
   ```json
   {
       "fmp_api_key": "DEIN_FMP_API_KEY",
       "telegram": {
           "bot_token": "DEIN_TELEGRAM_BOT_TOKEN",
           "chat_id": "DEINE_TELEGRAM_CHAT_ID"
       },
       "stock_analysis": {
           "min_notification_score": 7,
           "top_stocks_count": 10,
           "stocks_to_analyze": [
               "AAPL", "MSFT", "AMZN", "GOOG", "META", 
               "NVDA", "TSLA", "V", "JPM", "JNJ"
           ]
       }
   }
   ```

## Verwendung

### Grundlegende Verwendung

```bash
python main.py
```

Dies analysiert die in der `config.json` angegebenen Aktien und gibt die Top-10-Aktien aus.

### Optionen

- `--symbols`: Liste der zu analysierenden Aktiensymbole (überschreibt `config.json`)
  ```bash
  python main.py --symbols AAPL MSFT GOOG
  ```

- `--top`: Anzahl der Top-Aktien (Standard: 10)
  ```bash
  python main.py --top 5
  ```

- `--min-score`: Minimaler Score für Telegram-Benachrichtigungen (Standard: 7)
  ```bash
  python main.py --min-score 8
  ```

- `--notify`: Telegram-Benachrichtigung senden
  ```bash
  python main.py --notify
  ```

- `--config`: Pfad zur Konfigurationsdatei (Standard: `config.json`)
  ```bash
  python main.py --config custom_config.json
  ```

## Projektstruktur

- `main.py`: Hauptprogramm, das alle Module ausführt
- `data_fetch.py`: Abrufen der Aktien-Daten von der FMP API
- `analysis.py`: Berechnung der Kennzahlen und Bewertung
- `notification.py`: Senden der Telegram-Benachrichtigung
- `config.json`: Speichert den FMP API-Key, den Telegram Bot-Token und die Chat-ID
- `results/`: Verzeichnis mit den gespeicherten CSV-Dateien
- `visualizations/`: Verzeichnis mit den gespeicherten Diagrammen

## Telegram-Bot einrichten

1. Erstelle einen neuen Bot über den [BotFather](https://t.me/botfather) und notiere dir den Bot-Token.
2. Starte einen Chat mit deinem Bot.
3. Finde deine Chat-ID heraus, indem du mit deinem Bot chattest und dann die folgende URL aufrufst:
   ```
   https://api.telegram.org/bot<DEIN_BOT_TOKEN>/getUpdates
   ```
4. Trage den Bot-Token und die Chat-ID in deine `config.json` ein.

## FMP API-Key erhalten

1. Registriere dich bei [Financial Modeling Prep](https://financialmodelingprep.com/).
2. Nach der Registrierung erhältst du einen API-Key.
3. Trage den API-Key in deine `config.json` ein.

## Anpassung des Scoring-Modells

Das Scoring-Modell kann in der `analysis.py` angepasst werden, um andere Kennzahlen einzubeziehen oder die Gewichtung zu ändern.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die LICENSE-Datei für Details.
