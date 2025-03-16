import json
import logging
import pandas as pd
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from typing import Dict, Any, Optional

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('notification')

class TelegramNotifier:
    """
    Klasse zum Senden von Benachrichtigungen über Telegram.
    """
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialisiert den TelegramNotifier.
        
        Args:
            bot_token (str): Telegram Bot-Token
            chat_id (str): Telegram Chat-ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token)
    
    async def send_message(self, message: str) -> bool:
        """
        Sendet eine Nachricht über Telegram.
        
        Args:
            message (str): Zu sendende Nachricht
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode="HTML")
            logger.info("Telegram-Nachricht erfolgreich gesendet.")
            return True
        except TelegramError as e:
            logger.error(f"Fehler beim Senden der Telegram-Nachricht: {str(e)}")
            return False
    
    async def send_stock_alert(self, top_stocks: pd.DataFrame) -> bool:
        """
        Sendet eine Benachrichtigung über die Top-Aktien.
        
        Args:
            top_stocks (pd.DataFrame): DataFrame mit den Top-Aktien
            
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            # Erstelle eine formatierte Nachricht
            message = "<b>🔔 Top-Aktien-Alert! 🔔</b>\n\n"
            message += "<b>Die besten Aktien nach Fundamentalanalyse sind:</b>\n\n"
            
            # Füge jede Aktie zur Nachricht hinzu
            for index, row in top_stocks.iterrows():
                company_name = row.get('name', index)
                score = row.get('score', 0)
                sector = row.get('sector', 'N/A')
                pe = row.get('pe_ratio', 0)
                dividend = row.get('dividend_yield', 0)
                
                message += f"<b>{company_name}</b> ({index}) - Score: {score}\n"
                message += f"Sektor: {sector}\n"
                message += f"KGV: {pe:.2f} | Div: {dividend:.2f}%\n\n"
            
            # Sende die Nachricht
            return await self.send_message(message)
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen/Senden der Aktien-Benachrichtigung: {str(e)}")
            return False


def load_config() -> Dict[str, Any]:
    """
    Lädt die Konfiguration aus der config.json-Datei.
    
    Returns:
        Dict[str, Any]: Konfigurationsdaten
    """
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Fehler beim Laden der Konfigurationsdatei: {str(e)}")
        raise


def notify_top_stocks(top_stocks: pd.DataFrame, min_score: int = 7) -> bool:
    """
    Sendet eine Benachrichtigung über Telegram, wenn Aktien einen bestimmten Score überschreiten.
    
    Args:
        top_stocks (pd.DataFrame): DataFrame mit den Top-Aktien
        min_score (int): Minimaler Score für die Benachrichtigung
        
    Returns:
        bool: True bei Erfolg, False bei Fehler
    """
    # Filtere Aktien mit Score über dem Mindestwert
    high_score_stocks = top_stocks[top_stocks['score'] >= min_score]
    
    if high_score_stocks.empty:
        logger.info(f"Keine Aktien mit Score >= {min_score} gefunden. Keine Benachrichtigung gesendet.")
        return False
    
    # Lade die Konfiguration
    config = load_config()
    telegram_config = config.get('telegram', {})
    
    bot_token = telegram_config.get('bot_token')
    chat_id = telegram_config.get('chat_id')
    
    if not bot_token or not chat_id:
        logger.error("Telegram Bot-Token oder Chat-ID nicht in der Konfigurationsdatei gefunden.")
        return False
    
    # Erstelle einen TelegramNotifier
    notifier = TelegramNotifier(bot_token, chat_id)
    
    # Sende die Benachrichtigung asynchron
    return asyncio.run(notifier.send_stock_alert(high_score_stocks))


if __name__ == "__main__":
    # Beispiel für die Nutzung
    test_data = {
        'AAPL': {'name': 'Apple Inc.', 'score': 8, 'sector': 'Technology', 'pe_ratio': 25.6, 'dividend_yield': 0.85},
        'MSFT': {'name': 'Microsoft Corp.', 'score': 9, 'sector': 'Technology', 'pe_ratio': 30.2, 'dividend_yield': 0.75}
    }
    df = pd.DataFrame.from_dict(test_data, orient='index')
    notify_top_stocks(df, min_score=7)
