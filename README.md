# RWE & EON Aktien-Tracker

Eine interaktive Streamlit-Webanwendung zur Visualisierung und zum Vergleich der Aktienkurse von RWE und E.ON - zwei der wichtigsten deutschen Energieunternehmen.

## Features

- **Echtzeit-Kursdaten**: Aktuelle Aktienkurse mit Tagesveränderung
- **Flexible Zeiträume**: Auswahl von 1 Monat bis 5 Jahre
- **Interaktive Charts**: Kursverlauf mit Plotly-Visualisierungen
- **Vergleichsansicht**: Direkter Kursvergleich beider Aktien
- **Prozentuale Entwicklung**: Performance-Vergleich über Zeit
- **Handelsvolumen**: Volumen-Analyse im gewählten Zeitraum
- **Wichtige Kennzahlen**: 52-Wochen-Hoch/Tief, Marktkapitalisierung

## Installation

```bash
pip install streamlit yfinance plotly pandas
```

## Verwendung

```bash
streamlit run app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`.

## Datenquelle

Die Aktiendaten werden über Yahoo Finance bereitgestellt. Die Daten werden gecacht, um API-Rate-Limits zu vermeiden.

## Technologien

- **Streamlit**: Web-Framework für die Benutzeroberfläche
- **yfinance**: Yahoo Finance API für Aktiendaten
- **Plotly**: Interaktive Chartbibliothek
- **Pandas**: Datenverarbeitung
