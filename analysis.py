import json
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Tuple
import os
from datetime import datetime

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('analysis')

class StockAnalyzer:
    """
    Klasse zur Analyse und Bewertung von Aktien basierend auf fundamentalen Kennzahlen.
    """
    
    def __init__(self, stocks_data: Dict[str, Dict[str, Any]]):
        """
        Initialisiert den StockAnalyzer.
        
        Args:
            stocks_data (Dict[str, Dict[str, Any]]): Dictionary mit Finanzdaten für alle Symbole
        """
        self.stocks_data = stocks_data
        self.results = {}
        
    def _calculate_metrics(self) -> None:
        """
        Berechnet die fundamentalen Kennzahlen für jede Aktie.
        """
        for symbol, data in self.stocks_data.items():
            logger.info(f"Analysiere {symbol}...")
            
            # Überprüfe, ob die Daten korrekt abgerufen wurden
            if 'error' in data:
                logger.warning(f"Überspringe {symbol} wegen Datenabruffehler: {data['error']}")
                continue
                
            try:
                # Extrahiere relevante Daten
                profile = data.get('company_profile', {})
                income = data.get('income_statements', [{}])[0] if data.get('income_statements') else {}
                balance = data.get('balance_sheets', [{}])[0] if data.get('balance_sheets') else {}
                metrics = data.get('key_metrics', [{}])[0] if data.get('key_metrics') else {}
                ratios = data.get('ratios', [{}])[0] if data.get('ratios') else {}
                growth_data = data.get('growth', []) if data.get('growth') else []
                quote = data.get('quote', {})
                
                # Extrahiere und berechne die fundamentalen Kennzahlen
                # 1. Aktueller Preis
                price = quote.get('price', 0)
                
                # 2. KGV (Kurs-Gewinn-Verhältnis)
                pe_ratio = ratios.get('priceEarningsRatio', 0)
                
                # 3. KUV (Kurs-Umsatz-Verhältnis)
                ps_ratio = ratios.get('priceToSalesRatio', 0)
                
                # 4. KBV (Kurs-Buchwert-Verhältnis)
                pb_ratio = ratios.get('priceToBookRatio', 0)
                
                # 5. Dividendenrendite
                dividend_yield = ratios.get('dividendYield', 0) * 100  # Umwandlung in Prozent
                
                # 6. EPS (Earnings Per Share)
                eps = income.get('eps', 0)
                
                # 7. Umsatzwachstum der letzten 5 Jahre
                revenue_growth_5y = 0
                if len(growth_data) >= 5:
                    # Berechne das durchschnittliche jährliche Wachstum
                    growth_rates = [g.get('revenueGrowth', 0) for g in growth_data[:5]]
                    valid_rates = [r for r in growth_rates if r is not None]
                    revenue_growth_5y = np.mean(valid_rates) * 100 if valid_rates else 0
                
                # 8. Eigenkapitalrendite (ROE)
                roe = ratios.get('returnOnEquity', 0) * 100  # Umwandlung in Prozent
                
                # 9. Verschuldungsquote (Debt-to-Assets)
                debt_ratio = ratios.get('debtRatio', 0) * 100  # Umwandlung in Prozent
                
                # Speichere die berechneten Kennzahlen
                self.results[symbol] = {
                    'name': profile.get('companyName', symbol),
                    'sector': profile.get('sector', 'N/A'),
                    'price': price,
                    'pe_ratio': pe_ratio,
                    'ps_ratio': ps_ratio,
                    'pb_ratio': pb_ratio,
                    'dividend_yield': dividend_yield,
                    'eps': eps,
                    'revenue_growth_5y': revenue_growth_5y,
                    'roe': roe,
                    'debt_ratio': debt_ratio,
                    'score': 0  # Initialisiere Score mit 0
                }
            
            except Exception as e:
                logger.error(f"Fehler bei der Analyse von {symbol}: {str(e)}")
                continue
    
    def _calculate_scores(self) -> None:
        """
        Berechnet den Score für jede Aktie basierend auf den fundamentalen Kennzahlen.
        """
        for symbol, metrics in self.results.items():
            score = 0
            
            # 1. Niedriges KGV (<15) → 3 Punkte
            if metrics['pe_ratio'] > 0 and metrics['pe_ratio'] < 15:
                score += 3
                
            # 2. Hohe Dividendenrendite (>3%) → 2 Punkte
            if metrics['dividend_yield'] > 3:
                score += 2
                
            # 3. Hohes Umsatzwachstum (>10%) → 3 Punkte
            if metrics['revenue_growth_5y'] > 10:
                score += 3
                
            # 4. Geringe Verschuldung (<40%) → 2 Punkte
            if metrics['debt_ratio'] < 40:
                score += 2
            
            # Aktualisiere den Score
            self.results[symbol]['score'] = score
    
    def analyze(self) -> Dict[str, Dict[str, Any]]:
        """
        Führt die Analyse durch.
        
        Returns:
            Dict[str, Dict[str, Any]]: Analyseergebnisse
        """
        self._calculate_metrics()
        self._calculate_scores()
        return self.results
    
    def get_top_stocks(self, top_n: int = 10) -> pd.DataFrame:
        """
        Gibt die Top-N-Aktien nach Score zurück.
        
        Args:
            top_n (int): Anzahl der Top-Aktien
            
        Returns:
            pd.DataFrame: DataFrame mit den Top-Aktien
        """
        # Konvertiere die Ergebnisse in einen DataFrame
        df = pd.DataFrame.from_dict(self.results, orient='index')
        
        # Sortiere nach Score absteigend
        df = df.sort_values(by='score', ascending=False)
        
        # Gib die Top-N-Aktien zurück
        return df.head(top_n)


def save_results(results_df: pd.DataFrame, filename: str = None) -> str:
    """
    Speichert die Analyseergebnisse als CSV-Datei.
    
    Args:
        results_df (pd.DataFrame): DataFrame mit den Analyseergebnissen
        filename (str, optional): Name der Ausgabedatei
        
    Returns:
        str: Pfad zur gespeicherten Datei
    """
    # Erstelle einen Ordner für die Ergebnisse, falls dieser nicht existiert
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generiere einen Dateinamen mit Zeitstempel, falls keiner angegeben wurde
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"stock_analysis_{timestamp}.csv"
    
    # Vollständiger Pfad zur Ausgabedatei
    output_path = os.path.join(output_dir, filename)
    
    # Speichere die Ergebnisse als CSV-Datei
    results_df.to_csv(output_path)
    logger.info(f"Ergebnisse in {output_path} gespeichert")
    
    return output_path


def create_visualization(results_df: pd.DataFrame, output_path: str = None) -> str:
    """
    Erstellt ein Balkendiagramm mit den Top-Aktien und ihrem Score.
    
    Args:
        results_df (pd.DataFrame): DataFrame mit den Analyseergebnissen
        output_path (str, optional): Pfad zur Ausgabedatei
        
    Returns:
        str: Pfad zur gespeicherten Visualisierung
    """
    # Erstelle einen Ordner für die Visualisierungen, falls dieser nicht existiert
    output_dir = "visualizations"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generiere einen Dateinamen mit Zeitstempel, falls keiner angegeben wurde
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"top_stocks_{timestamp}.png")
    
    # Erstelle das Balkendiagramm
    plt.figure(figsize=(12, 8))
    
    # Verwende die Unternehmensnamen als Beschriftungen, falls verfügbar
    labels = results_df['name'] if 'name' in results_df.columns else results_df.index
    scores = results_df['score']
    
    # Erstelle Balken mit Farbverlauf basierend auf dem Score
    bars = plt.barh(labels, scores, color='skyblue')
    
    # Füge Werte am Ende der Balken hinzu
    for i, (bar, score) in enumerate(zip(bars, scores)):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                 f'{score:.1f}', va='center')
    
    # Füge Titel und Beschriftungen hinzu
    plt.title('Top-Aktien nach Fundamentalanalyse', fontsize=16)
    plt.xlabel('Score', fontsize=12)
    plt.ylabel('Aktie', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Speichere das Diagramm
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Visualisierung in {output_path} gespeichert")
    
    return output_path


def analyze_stocks(stocks_data: Dict[str, Dict[str, Any]], top_n: int = 10) -> Tuple[pd.DataFrame, str, str]:
    """
    Hauptfunktion zur Analyse der Aktiendaten.
    
    Args:
        stocks_data (Dict[str, Dict[str, Any]]): Dictionary mit Finanzdaten für alle Symbole
        top_n (int): Anzahl der Top-Aktien
        
    Returns:
        Tuple[pd.DataFrame, str, str]: (DataFrame mit Top-Aktien, Pfad zur CSV-Datei, Pfad zur Visualisierung)
    """
    # Erstelle einen StockAnalyzer
    analyzer = StockAnalyzer(stocks_data)
    
    # Führe die Analyse durch
    analyzer.analyze()
    
    # Hole die Top-N-Aktien
    top_stocks = analyzer.get_top_stocks(top_n)
    
    # Speichere die Ergebnisse
    csv_path = save_results(top_stocks)
    
    # Erstelle die Visualisierung
    viz_path = create_visualization(top_stocks)
    
    return top_stocks, csv_path, viz_path


if __name__ == "__main__":
    # Beispiel für die Nutzung
    from data_fetch import load_config, get_financial_data
    
    config = load_config()
    symbols = config.get('stock_analysis', {}).get('stocks_to_analyze', ['AAPL', 'MSFT', 'GOOG'])
    stocks_data = get_financial_data(symbols[:5])  # Nur die ersten 5 für den Test
    
    top_stocks, csv_path, viz_path = analyze_stocks(stocks_data)
    print(top_stocks)
