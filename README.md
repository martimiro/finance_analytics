# Python Finance Analytics

Análisis de portafolios de acciones con Python — retornos, riesgo, visualizaciones y forecasting.

## Instalación

```bash
git clone https://github.com/tu-usuario/finance-analytics.git
cd finance-analytics
pip install -r requirements.txt
```

## Uso

```bash
python main.py

# Forzar re-descarga de datos
python main.py --force-download
```

## Configuración

Edita `config.py` para cambiar el portafolio:

```python
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
WEIGHTS = [0.25, 0.25, 0.20, 0.15, 0.15]   # deben sumar 1.0
START_DATE = "2024-01-01"
END_DATE   = "2025-01-31"
```

## Estructura

```
├── config.py          # Parámetros del portafolio
├── main.py            # Punto de entrada
├── src/
│   ├── data_loader.py # Descarga y caché de datos
│   ├── returns.py     # Cálculo de retornos
│   ├── risk.py        # Métricas de riesgo
│   ├── visualization.py  # Dashboard 6 paneles
│   └── forecasting.py    # MA, Regresión Lineal, ARIMA
└── output/            # Gráficos y reporte generados
```

## Outputs

- `output/dashboard.png` — dashboard de 6 paneles
- `output/forecasts.png` — comparación de 3 modelos de forecasting
- `output/report.txt` — métricas de retorno y riesgo

## Dependencias

```
yfinance pandas numpy matplotlib seaborn scipy statsmodels scikit-learn
```

---

> Para uso educativo únicamente. No constituye asesoramiento financiero.