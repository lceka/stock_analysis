import json
import logging
import pandas as pd
from typing import Dict, Any, List
import argparse
import os

# Importiere die Module
from data_fetch import load_config, get_financial_data
from analysis import analyze_stocks
from notification import notify_top_stocks

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("stock_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('main')

def parse_arguments():
    """
    Parst die Befehlszeilenargumente.
    
    Returns:
        argparse.Namespace: Geparste Argumente
    """
    parser = argparse.ArgumentParser(description='Automatisierte Fundamentalanalyse von Aktien')
    
    parser.add_argument('--symbols', type=str, nargs='+',
                        help='Liste der zu analysierenden Aktiensymbole (überschreibt config.json)')
    
    parser.add_argument('--top', type=int, default=10,
                        help='Anzahl der Top-Aktien (Standard: 10)')
    
    parser.add_argument('--min-score', type=int, default=7,
                        help='Minimaler Score für Telegram-Benachrichtigungen (Standard: 7)')
    
    parser.add_argument('--notify', action='store_true',
                        help='Telegram-Benachrichtigung senden')
    
    parser.add_argument('--config', type=str, default='config.json',
                        help='Pfad zur Konfigurationsdatei (Standard: config.json)')
    
    return parser.parse_args()

def main():
    """
    Hauptfunktion des Programms.
    """
    # Parse Befehlszeilenargumente
    args = parse_arguments()
    
    try:
        # Lade die Konfiguration
        config = load_config()
        
        # Hole die Liste der zu analysierenden Aktien
        if args.symbols:
            symbols = args.symbols
        else:
            symbols = config.get('stock_analysis', {}).get('stocks_to_analyze', [])
        
        if not symbols:
            logger.error("Keine Aktien zur Analyse angegeben.")
            return
        
        logger.info(f"Starte Analyse für {len(symbols)} Aktien: {', '.join(symbols[:5])}...")
        
        # Hole die Finanzdaten
        stocks_data = get_financial_data(symbols)
        
        # Analysiere die Aktien
        top_n = args.top or config.get('stock_analysis', {}).get('top_stocks_count', 10)
        top_stocks, csv_path, viz_path = analyze_stocks(stocks_data, top_n)
        
        # Zeige die Ergebnisse
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print("\n=== Top-Aktien nach Fundamentalanalyse ===")
        print(top_stocks[['name', 'sector', 'price', 'pe_ratio', 'dividend_yield', 'revenue_growth_5y', 'debt_ratio', 'score']])
        
        # Sende Benachrichtigung, falls gewünscht
        if args.notify:
            min_score = args.min_score or config.get('stock_analysis', {}).get('min_notification_score', 7)
            notify_result = notify_top_stocks(top_stocks, min_score)
            
            if notify_result:
                logger.info(f"Telegram-Benachrichtigung für Aktien mit Score >= {min_score} gesendet.")
            else:
                logger.warning("Keine Telegram-Benachrichtigung gesendet.")
        
        # Zeige Ausgabepfade
        logger.info(f"Analyseergebnisse gespeichert in: {csv_path}")
        logger.info(f"Visualisierung gespeichert in: {viz_path}")
        
    except Exception as e:
        logger.error(f"Fehler in der Hauptfunktion: {str(e)}", exc_info=True)
        return

if __name__ == "__main__":
    main()
