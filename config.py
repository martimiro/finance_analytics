#config.py

'''
Parámetros globales
Centralizar todos los parámetros significa que modificar un portafolio requiere editar exactamente un solo archivo. Las declaraciones assert en la parte inferior detectan errores de configuración al momento de la importación - fallando de forma ruidosa e immediata en lugar de producir número incorrectos de manera silenciosa más adelante en el proceso.
'''   

'''
Principio de diseño
Valida siempre las entradas en el límite donde ingresan al sistema (importacion de config.py). Este es el principio de "fallar rápido" (fail test) - capturar los errores en el orígen genera mensajes de error claros e immediatos en lugar de fallas crípticas más adelante en el proceso.
'''

# Definición de portfolio

TICKERS = ["AAPL", 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
WEIGHTS = [0.25, 0.25, 0.20, 0.15, 0.15]

# Falla ruidosamente al importar si está mal configurado
assert abs(sum(WEIGHTS) - 1.0) < 1e-10, (
  f'WEIGHTS suman {sum(WEIGHTS):.6f}, no 1.0. Arregla config.py'
)

assert len(TICKERS) == len(WEIGHTS), 'Las longitudes deben coincidir'

# Datos de mercado

BENCHMARK = '^GSPC' # S&P 500 - usado para Beta, Alpha, comparación gráfica (de rendimientos)
START_DATE = '2025-01-01' # Fecha de inicio (inclusive)
END_DATE = '2026-03-31' # Fecha final (inclusive)

# Parámetros de riesgo

RISK_FEE = 0.045  # Tasa anual libre de riesgo (letras del Tesoro de EE. UU. a 3 meses)
VAR_CONFIDENCE = 0.95 # Nivel de confianza para VaR y CVaR

# Pronóstico/Predicciones
FORECAST_DAYS = 30  # Horizonte de forecast en días de trading
MA_WINDOWS = [20, 50, 200]  # Ventanas de media móvil (días)
ARIMA_ORDER = (2, 1, 2)  # Orden (p, d, q) del modelo ARIMA

# Visualización
FIGSIZE = (20, 12)  # Figura del dashboard en inches
DPI = 150 # Resolución de exportación
STYLE = 'whitegrid' # Tema de Seaborn

SECTORS = {
  'Tecnología': 'XLK',
  'Salud': 'XLV',
  'Finanzas': 'XLF',
  'Energía': 'XLE',
  'Consumo Discrecional': 'XLY',
  'Servicios Públicos': 'XLU',
  'Bienes Raíces': 'XLRE',
}