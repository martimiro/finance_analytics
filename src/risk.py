# src/risk.py

"""
Módulo de análisi de riesgo
Implementa todas la métricas de riesgo estandard usadas en finanzas profesionales
"""

import numpy as np
import pandas as pd
from config import RISK_FEE, VAR_CONFIDENCE

# Volatilidad
def annualized_volatility(returns: pd.Series) -> float:
  """
  Annualized std deviation: sigma_daily * sqrt(252)
  """

  return float(returns.std() * np.sqrt(252))

def rolling_volatility(returns: pd.Series, window: int = 30) -> pd.Series:
  """
  Volatilidad móvil anualizada
  """

  return returns.rolling(window).std() * np.sqrt(252)

# Sharpe y Sortino
def sharpe_ratio(returns: pd.Series) -> float:
  """
  Sharpe Ratio
  """

  excess = returns.mean() * 252 - RISK_FEE
  vol = annualized_volatility(returns)
  return float(excess/vol) if vol != 0 else float('nan')

def sortino_ratio(returns: pd.Series) -> float:
  """
  Sortino Ratio
  """
  neg = returns[returns < 0]

  if len(neg) == 0:
    return float('inf')
  
  downside_vol = neg.std() * np.sqrt(252)
  excess = returns.mean() * 252 - RISK_FEE

  return float(excess / downside_vol)

# Drawdown
def drawndown_series(cum_returns: pd.Series) -> pd.Series:
  """
  Serie temporal de "drawndown": % respecto al máximo anterior en cada punto
  Siempre <= 0. Cero significa que está en un "all-time high"
  """

  wealth = 1 + cum_returns
  peak = wealth.cummax()
  return (wealth - peak) / peak

def max_drawdown(cum_returns: pd.Series) -> float:
  """
  Retorna el peor drawdown de todo el período.
  Siempre <= 0.
  """
  return float(drawndown_series(cum_returns).min())

def max_drawdown_duration(cum_returns: pd.Series) -> int:
  """
  Número de días de negocio consecutivos donde el portfolio está "underwater"
  """

  dd = drawndown_series(cum_returns)
  underwater = dd < 0
  max_dur, cur_dur = 0, 0
  for v in underwater:
    cur_dur = cur_dur + 1 if v else 0
    max_dur = max(max_dur, cur_dur)

  return max_dur

def calmar_ratio(cagr_val: float, mdd: float) -> float:
  """
  Calmar ratio -> Valor alto = mejor
  """

  return float(cagr_val / abs(mdd)) if mdd != 0 else float('nan')

# Riesgo de mercado
def beta(portfolio_ret: pd.Series, benchmark_ret: pd.Series) -> float:
    """
    Beta de la cartera
    """

    aligned = pd.concat([portfolio_ret, benchmark_ret], axis=1).dropna()
    cov = np.cov(aligned.iloc[:,0], aligned.iloc[:,1])
    return float(cov[0,1] / cov[1,1])

def jensens_alpha(portfolio_ret: pd.Series, benchmark_ret: pd.Series) -> float:
  """
  Jensen's Alpha = R_p - [R_f + beta * (R_m - R_f)].
  """

  b = beta(portfolio_ret, benchmark_ret)
  r_p = portfolio_ret.mean() * 252
  r_m = benchmark_ret.mean() * 252

  return float(r_p - (RISK_FEE + b * (r_m - RISK_FEE)))

# Tail Risk
def var_historical(returns: pd.Series, confidence: float = VAR_CONFIDENCE) -> float:
  """
  Value at Risk (VaR) histórico
  """

  return float(np.percentile(returns, (1 - confidence) * 100))

def cvar_historical(returns: pd.Series, confidence: float = VAR_CONFIDENCE) -> float:
  """
  Conditional Value at Risk (CVaR)
  """

  var = var_historical(returns, confidence)
  tail =  returns[returns <= var]
  return float(tail.mean()) if len(tail) > 0 else float('nan')

def correlation_matrix(daily_ret: pd.DataFrame) -> pd.DataFrame:
  """
  Matriz de correlación de Pearson de los rendimientos diarios de los activos
  """

  return daily_ret.corr()

# Resumen completo
def risk_sumary(port_ret: pd.Series, bench_ret: pd.Series, cum_ret: pd.Series, cagr_val: float) -> dict:
  """
  Todas las métricas ordenadas en un diccionario
  """

  mdd = max_drawdown(cum_ret)
  return {
    'Volatilidad anual': f'{annualized_volatility(port_ret):.2%}',
    'Sharpe Ratio': f'{sharpe_ratio(port_ret):.3f}',
    'Sortino Ratio': f'{sortino_ratio(port_ret):.3f}',
    'Max Drawdown': f'{mdd:.2%}',
    'Max DD Duration': f'{max_drawdown_duration(cum_ret)}',
    'Calamar Ratio': f'{calmar_ratio(cagr_val, mdd):.3f}',
    'Beta (vs S&P 500)': f'{beta(port_ret, bench_ret):.3f}',
    "Jensen's alpha": f'{jensens_alpha(port_ret, bench_ret):.3f}',
    'VaR 95% (daily)': f'{var_historical(port_ret):.2%}',
    'CVaR 95% (daily)': f'{cvar_historical(port_ret):.2%}',
  }