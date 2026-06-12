# src/returns.py

"""
Módulo de computación de retornos.
Convierte precios brutos en retornos simples, logarítmicos y agregaciones a nivel de cartera.
"""

import numpy as np
import pandas as pd
from typing import cast, overload
from config import WEIGHTS, TICKERS, START_DATE, END_DATE


@overload
def filter_period(
    data: pd.Series,
    start: str | None = None,
    end: str | None = None,
) -> pd.Series: ...


@overload
def filter_period(
    data: pd.DataFrame,
    start: str | None = None,
    end: str | None = None,
) -> pd.DataFrame: ...


def filter_period(
    data: pd.Series | pd.DataFrame,
    start: str | None = None,
    end: str | None = None,
) -> pd.Series | pd.DataFrame:
    """
    Restringe una serie o DataFrame al período de análisis (START_DATE–END_DATE).
    Los datos extendidos del loader se usan solo para indicadores (p. ej. MA 200).
    """
    return data.loc[start or START_DATE : end or END_DATE]


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Retorno simple diario: R_t = (P_t - P_{t-1}) / P_{t-1}
    """
    return prices.pct_change().dropna()


def log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Retorno logarítmico diario: R_t = ln(P_t / P_{t-1})
    Preferible para análisis estadístico — es aditivo en el tiempo.
    """
    # np.log(DataFrame) devuelve NDArray — .apply(np.log) preserva el tipo DataFrame
    ratio = prices / prices.shift(1)
    return ratio.apply(np.log).dropna()


def portfolio_returns(daily_ret: pd.DataFrame,
                      weights: list | None = None) -> pd.Series:
    """
    Rentabilidad diaria de la cartera como suma ponderada de los activos.
    R_p(t) = SUM w_i * R_i(t)

    Parameters
    ----------
    daily_ret : pd.DataFrame — rendimientos diarios individuales de cada activo
    weights   : list | None — pesos de la cartera; si None usa config.WEIGHTS
    """
    w = weights if weights is not None else WEIGHTS
    assert abs(sum(w) - 1.0) < 1e-10, "Los pesos deben sumar 1.0"
    port = (daily_ret[TICKERS] * w).sum(axis=1)
    port.name = "Portfolio"
    return port


def cumulative_returns(returns: pd.Series) -> pd.Series:
    """
    Retorno acumulado: seguimiento del crecimiento de $1 invertido el primer día.
    R_cum(t) = PROD(1 + R_i) - 1
    """
    return (1 + returns).cumprod() - 1


def cagr(returns: pd.Series) -> float:
    """
    Compound Annual Growth Rate (Tasa de Crecimiento Anual Compuesta).
    CAGR = (1 + R_total) ^ (252 / n_días) - 1
    """
    # pandas-stubs tipa .prod() y .item() como una unión amplia que incluye
    # complex, date, timedelta, None, etc. Ni float() ni la anotación `total: float`
    # son suficientes porque Pylance evalúa el lado derecho antes de aplicar la
    # anotación y rechaza la asignación (reportAssignmentType).
    #
    # cast(float, x) es la solución correcta: es una no-op en runtime (devuelve x
    # sin modificarlo) pero le indica al type-checker que trate x como float,
    # eliminando la unión sin introducir conversión real ni riesgo de excepción.
    total = cast(float, (1 + returns).prod())
    years = len(returns) / 252
    return float(total ** (1 / years) - 1)


def annualized_return(returns: pd.Series) -> float:
    """
    Anualización alternativa: media del retorno diario × 252.
    """
    return float(cast(float, returns.mean()) * 252)


def rolling_returns(returns: pd.Series, window: int = 252) -> pd.Series:
    """
    Retorno anualizado acumulado en una ventana móvil.
    Útil para detectar cambios de régimen en el rendimiento a lo largo del tiempo.
    """
    return returns.rolling(window).apply(
        lambda r: (1 + r).prod() ** (252 / window) - 1,
        raw=False,
    )


def monthly_returns(returns: pd.Series) -> pd.Series:
    """
    Resample de retornos diarios a mensuales mediante compounding.
    """
    result = returns.resample("ME").apply(lambda r: (1 + r).prod() - 1)
    return pd.Series(result)


def return_summary(daily_ret: pd.DataFrame, port_ret: pd.Series) -> dict:
    """
    Métricas clave de retorno formateadas para el reporte.
    """
    cum = cumulative_returns(port_ret)
    return {
        "Rendimiento total (Portfolio)": f"{float(cum.iloc[-1]):.2%}",
        "CAGR":                          f"{cagr(port_ret):.2%}",
        "Rendimiento anualizado":        f"{annualized_return(port_ret):.2%}",
        "Mejor día":                     f"{port_ret.max():.2%}",
        "Peor día":                      f"{port_ret.min():.2%}",
        "Días positivos":                f"{(port_ret > 0).mean():.1%}",
    }