# src/market_trends.py

"""
Gráfico de dispersión: rendimiento anualizado vs volatilidad anualizada por sector.
Los puntos con mayor rendimiento por unidad de volatilidad son superiores
desde una perspectiva ajustada al riesgo.
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

from config import END_DATE, SECTORS, START_DATE


def sector_risk_return_chart() -> None:
  """Descarga datos de ETFs sectoriales y genera el scatter risk-return."""

  tickers = list(SECTORS.values())

  # FIX: extraer solo 'Close' del MultiIndex que devuelve yf.download()
  # Sin esto, pct_change() opera sobre todas las columnas (Open, High, Low...)
  # y Pylance reporta "pct_change is not a known attribute of None" porque
  # el tipo del DataFrame completo es ambiguo con auto_adjust por defecto.
  raw = yf.download(tickers, start=START_DATE, end=END_DATE, auto_adjust=True, progress=False,)

  if raw is None or raw.empty:
    raise RuntimeError("[market_trends] yfinance no devolvió datos.")

  # Extraer Close según si el resultado es MultiIndex o no
  if isinstance(raw.columns, pd.MultiIndex):
    prices: pd.DataFrame = pd.DataFrame(raw["Close"])
  else:
    prices = pd.DataFrame(raw[["Close"]])
    prices.columns = pd.Index(tickers)

  ret = prices.pct_change().dropna()

  # FIX: ann_vol usaba ret.mean() * 252 — igual que ann_ret.
  # La volatilidad anualizada es std() * sqrt(252), no mean() * 252.
  ann_ret: pd.Series = pd.Series(ret.mean() * 252)
  ann_vol: pd.Series = pd.Series(ret.std() * np.sqrt(252))

  fig, ax = plt.subplots(figsize=(10, 7))

  # FIX: plt.cm.tab10 no es reconocido por Pylance como atributo de cm.
  # matplotlib.colormaps["tab10"] es la API moderna y correctamente tipada.
  cmap = matplotlib.colormaps["tab10"]
  colors = cmap(np.linspace(0, 1, len(SECTORS)))

  for i, (name, ticker) in enumerate(SECTORS.items()):
    ax.scatter(ann_vol[ticker] * 100, ann_ret[ticker] * 100, s=200, color=colors[i], zorder=3, label=name,)
    ax.annotate(name, (ann_vol[ticker] * 100 + 0.3, ann_ret[ticker] * 100), fontsize=9,)

  ax.axhline(0, color="black", lw=0.8, linestyle=":")
  ax.set_xlabel("Volatilidad anualizada (%)", fontsize=12)
  ax.set_ylabel("Rendimiento anualizado (%)", fontsize=12)
  ax.set_title("Análisis sector ETF — Risk vs Return",
                 fontsize=14, fontweight="bold")
  ax.legend(loc="lower right", fontsize=9)

  plt.tight_layout()
  plt.savefig("output/sectors.png", dpi=150, bbox_inches="tight")
  print("[market_trends] Gráfico guardado en output/sectors.png")
  #plt.show()

# Detección de régimen
def rolling_beta(port_ret:pd.Series, bench_ret: pd.Series, window: int = 63) -> pd.Series:
  """
  Calcula Beta Rolling sobre una ventana deslizante

  Beta > 1 -> portafolio amplifica movimientos del mercado (agresivo)
  Beta < 1 -> portafolio amortigua movimientos del mercado (defensivo)
  Cruce de 1.0 -> posible canvio de régimen

  Parameters
  ----------
  port_ret: retorna diarios del portfolio
  bench_ret: retorna diarios del benchmark
  window: tamaño de la ventana en días de trading
  """
  aligned = pd.concat([port_ret, bench_ret], axis=1).dropna()
  p = aligned.iloc[:,0]
  b = aligned.iloc[:,1]
  betas: list[float] = []
  
  for i in range(window, len(p)):
    p_w = p.iloc[i - window:i].to_numpy()
    b_W = b.iloc[i - window:i].to_numpy()
    cov = np.cov(p_w, b_W)
    betas.append(float(cov[0, 1] / cov[1, 1]))

  return pd.Series(betas, index = p.index[window:], name=f"Rolling Beta ({window}d")

def plot_rolling_beta(port_ret: pd.Series, bench_ret: pd.Series, window: int = 63) -> None:
  """
  Gráfica del Rolling Beta a lo largo del tiempo con zonas de régimen agresivo y defensivo
  """
  betas = rolling_beta(port_ret, bench_ret, window)
  fig, ax = plt.subplots(figsize = (14, 5))

  betas.plot(ax=ax, color = '#1D4ED8', lw = 2, label = betas.name)
  ax.axhline(1.0, color = '#DC2626', lw = 1.5, linestyle = "--", label = 'Beta = 1.0 (mercado)')
  ax.fill_between(betas.index, betas.where(betas > 1), 1.0, where=(betas > 1).to_numpy().tolist(), alpha = 0.15, color = '#DC2626', label = "Régimen agresivo (β > 1)",)
  ax.fill_between(betas.index, betas.where(betas < 1), 1.0, where=(betas < 1).to_numpy().tolist(), alpha = 0.15, color = '#16A34A', label = "Régimen defensivo (β < 1)",)
  ax.set_title('Rolling Beta (63-day Window)')
  plt.savefig('output/rolling_beta.png', dpi=150, bbox_inches='tight')
  #plt.show()

# Detección de régimen por volatilidad
def detect_regime(port_ret: pd.Series, window : int = 21, threshold: float = 0.20) -> pd.Series:
  """
  Clasifica cada día en régimen de BAJA o ALTA volatilidad según si la volatilidad rolling es anualizada supera el umbral.

  Returns
  -------
  pd.Series con valores "Alta volatilidad / Baja volatilidad"
  """
  rolling_vol = port_ret.rolling(window).std() * np.sqrt(252)
  regime = rolling_vol.apply(lambda v: "Alta volatilidad" if v > threshold else "Baja volatilidad")
  regime.name = "Régimen"
  return regime

def plot_regime(port_ret: pd.Series, cum_ret: pd.Series, window: int = 21, threshold: float = 0.20) -> None:
  """
  Gráfica el retorno acumulado con el régimen de volatilidad
  """
  regime = detect_regime(port_ret, window, threshold)
  high_vol = (regime == "Alta volatilidad")
  fig, ax = plt.subplots(figsize = (14, 5))

  (cum_ret * 100).plot(ax=ax, color = '#1D4ED8', lw = 2,  label = 'Retorno acumulado (%)')

  # Sombrear períodos de alta volatilidad
  ax.fill_between(cum_ret.index, ax.get_ylim()[0], ax.get_ylim()[1], where=high_vol.reindex(cum_ret.index, fill_value=False).to_numpy().tolist(), alpha = 0.12, color = '#DC2626', label = f'Alta volatilidad (vol > {threshold:.0%})')
  ax.set_title("Retorno acumulado con detección de régimen", fontsize = 13, fontweight = 'bold')
  ax.set_ylabel("Retorno (%)")
  ax.legend(fontsize = 9)
  
  plt.tight_layout()
  plt.savefig('output/regime.png', dpi = 150, bbox_inches = "tight")
  print("[market_trends] Guardado en output/regime.png")

  #plt.show()