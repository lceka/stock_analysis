import json
import requests
import logging
import time
from typing import Dict, List, Any, Optional, Union

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data_fetch')

class FinancialDataFetcher:
    """
    Klasse zum Abrufen von Finanzdaten von der Financial Modeling Prep API (FMP).
    """
    
    def __init__(self, api_key: str, max_retries: int = 3, retry_delay: int = 2):
        """
        Initialisiert den FinancialDataFetcher.
        
        Args:
            api_key (str): FMP API-Key
            max_retries (int): Maximale Anzahl an Wiederholungen bei API-Fehlern
            retry_delay (int): Verzögerung zwischen Wiederholungen in Sekunden
        """
        self.api_key = api_key
        self.base_url = "https://financialmodelingprep.com/api/v3"
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
    def _make_api_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Führt einen API-Request durch mit Wiederholungslogik bei Fehlern.
        
        Args:
            endpoint (str): API-Endpunkt
            params (Dict[str, Any], optional): Zusätzliche Parameter
            
        Returns:
            Dict[str, Any]: API-Antwort als Dictionary
            
        Raises:
            Exception: Bei anhaltenden API-Fehlern
        """
        if params is None:
            params = {}
            
        # Füge API-Key zu Parametern hinzu
        params['apikey'] = self.api_key
        
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Wirft eine Exception bei HTTP-Fehlern
                
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"API-Fehler (Versuch {attempt+1}/{self.max_retries}): {str(e)}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"API-Anfrage fehlgeschlagen nach {self.max_retries} Versuchen.")
                    raise Exception(f"API-Anfrage fehlgeschlagen: {str(e)}")
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Abrufen des Unternehmensprofils für ein bestimmtes Symbol.
        
        Args:
            symbol (str): Aktiensymbol (z.B. "AAPL")
            
        Returns:
            Dict[str, Any]: Unternehmensprofil-Daten
        """
        endpoint = f"profile/{symbol}"
        data = self._make_api_request(endpoint)
        
        return data[0] if data else {}
    
    def get_income_statement(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Abrufen der Gewinn- und Verlustrechnung für ein Symbol.
        
        Args:
            symbol (str): Aktiensymbol (z.B. "AAPL")
            period (str): Zeitraum ('annual' oder 'quarter')
            limit (int): Anzahl der letzten Abschlüsse
            
        Returns:
            List[Dict[str, Any]]: Liste der Gewinn- und Verlustrechnungen
        """
        endpoint = f"income-statement/{symbol}"
        params = {
            'period': period,
            'limit': limit
        }
        
        return self._make_api_request(endpoint, params)
    
    def get_balance_sheet(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Abrufen der Bilanz für ein Symbol.
        
        Args:
            symbol (str): Aktiensymbol (z.B. "AAPL")
            period (str): Zeitraum ('annual' oder 'quarter')
            limit (int): Anzahl der letzten Abschlüsse
            
        Returns:
            List[Dict[str, Any]]: Liste der Bilanzen
        """
        endpoint = f"balance-sheet-statement/{symbol}"
        params = {
            'period': period,
            'limit': limit
        }
        
        return self._make_api_request(endpoint, params)
    
    def get_cash_flow(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Abrufen der Kapitalflussrechnung für ein Symbol.
        
        Args:
            symbol (str): Aktiensymbol (z.B. "AAPL")
            period (str): Zeitraum ('annual' oder 'quarter')
            limit (int): Anzahl der letzten Abschlüsse
            
        Returns:
            List[Dict[str, Any]]: Liste der Kapitalflussrechnungen
        """
        endpoint = f"cash-flow-statement/{symbol}"
        params = {
            'period': period,
            'limit': limit
        }
        
        return self._make_api_request(endpoint, params)
    
    def get_key_metrics(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Abrufen der Schlüsselkennzahlen für ein Symbol.
        
        Args:
            symbol (str): Aktiensymbol (z.B. "AAPL")
            period (str): Zeitraum ('annual' oder 'quarter')
            limit (int): Anzahl der letzten Perioden
            
        Returns:
            List[Dict[str, Any]]: Liste der Schlüsselkennzahlen
        """
        endpoint = f"key-metrics/{symbol}"
        params = {
            'period': period,
            'limit': limit
        }
        
        return self._make_api_request(endpoint, params)
    
    def get_ratios(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Abrufen der Finanzkennzahlen für ein Symbol.
        
        Args:
            symbol (str): Aktiensymbol (z.B. "AAPL")
            period (str): Zeitraum ('annual' oder 'quarter')
            limit (int): Anzahl der letzten Perioden
            
        Returns:
            List[Dict[str, Any]]: Liste der Finanzkennzahlen
        """
        endpoint = f"ratios/{symbol}"
        params = {
            'period': period,
            'limit': limit
        }
        
        return self._make_api_request(endpoint, params)
    
    def get_growth(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Abrufen der Wachstumskennzahlen für ein Symbol.
        
        Args:
            symbol (str): Aktiensymbol (z.B. "AAPL")
            period (str): Zeitraum ('annual' oder 'quarter')
            limit (int): Anzahl der letzten Perioden
            
        Returns:
            List[Dict[str, Any]]: Liste der Wachstumskennzahlen
        """
        endpoint = f"financial-growth/{symbol}"
        params = {
            'period': period,
            'limit': limit
        }
        
        return self._make_api_request(endpoint, params)
    
    def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Abrufen des aktuellen Aktienkurses für ein Symbol.
        
        Args:
            symbol (str): Aktiensymbol (z.B. "AAPL")
            
        Returns:
            Dict[str, Any]: Aktienkursdaten
        """
        endpoint = f"quote/{symbol}"
        data = self._make_api_request(endpoint)
        
        return data[0] if data else {}
    
    def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        """
        Abrufen aller relevanten Daten für ein Symbol.
        
        Args:
            symbol (str): Aktiensymbol (z.B. "AAPL")
            
        Returns:
            Dict[str, Any]: Alle relevanten Daten
        """
        logger.info(f"Hole Daten für {symbol}...")
        
        try:
            # Hole alle Daten in parallelen Anfragen
            company_profile = self.get_company_profile(symbol)
            income_statements = self.get_income_statement(symbol)
            balance_sheets = self.get_balance_sheet(symbol)
            key_metrics = self.get_key_metrics(symbol)
            ratios = self.get_ratios(symbol)
            growth = self.get_growth(symbol)
            quote = self.get_stock_quote(symbol)
            
            # Fasse alle Daten zusammen
            stock_data = {
                'symbol': symbol,
                'company_profile': company_profile,
                'income_statements': income_statements,
                'balance_sheets': balance_sheets,
                'key_metrics': key_metrics,
                'ratios': ratios,
                'growth': growth,
                'quote': quote
            }
            
            return stock_data
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Daten für {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'error': str(e)
            }
    
    def get_stocks_data(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Abrufen aller relevanten Daten für mehrere Symbole.
        
        Args:
            symbols (List[str]): Liste der Aktiensymbole
            
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary mit Daten für alle Symbole
        """
        stocks_data = {}
        
        for symbol in symbols:
            stock_data = self.get_stock_data(symbol)
            stocks_data[symbol] = stock_data
            
            # Kleine Verzögerung um API-Limits zu berücksichtigen
            time.sleep(0.5)
        
        return stocks_data


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


def get_financial_data(symbols: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Hauptfunktion zum Abrufen der Finanzdaten.
    
    Args:
        symbols (List[str]): Liste der Aktiensymbole
    
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary mit Finanzdaten für alle Symbole
    """
    config = load_config()
    api_key = config.get('fmp_api_key')
    
    if not api_key:
        raise ValueError("Kein FMP API-Key in der Konfigurationsdatei gefunden.")
    
    fetcher = FinancialDataFetcher(api_key)
    return fetcher.get_stocks_data(symbols)


if __name__ == "__main__":
    # Beispiel für die Nutzung
    config = load_config()
    symbols = config.get('stock_analysis', {}).get('stocks_to_analyze', ['AAPL', 'MSFT', 'GOOG'])
    data = get_financial_data(symbols[:3])  # Nur die ersten 3 für den Test
    
    print(f"Daten für {len(data)} Aktien abgerufen.")
