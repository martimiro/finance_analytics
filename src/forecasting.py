# src/forecasting.py

"""
Módulo de forecasting.
Implementa Media Móvil, Regresión Lineal y ARIMA para la predicción de precios.
"""

import os
import warnings
from typing import cast

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

from config import FORECAST_DAYS, MA_WINDOWS, ARIMA_ORDER, DPI

warnings.filterwarnings("ignore")

# MODELO 1 — Media Móvil
def moving_average_signals(prices: pd.Series) -> pd.DataFrame:
    """
    Calcula la SMA para cada ventana en MA_WINDOWS.
    Genera señales Golden Cross / Death Cross para MA_50 vs MA_200.

    Devuelve DataFrame con columnas: Precio, MA_20, MA_50, MA_200,
                                     Golden_Cross, Death_Cross
    """
    df = prices.to_frame("Precio")
    for w in MA_WINDOWS:
        df[f"MA_{w}"] = prices.rolling(w).mean()

    if 50 in MA_WINDOWS and 200 in MA_WINDOWS:
        # FIX (reportAttributeAccessIssue): np.sign() devuelve NDArray,
        # que no tiene el método .diff(). Envolver en pd.Series() restaura
        # todos los métodos pandas y elimina el error de Pylance.
        cross: pd.Series = pd.Series(
            np.sign(df["MA_50"] - df["MA_200"]), index=df.index
        )
        change = cross.diff()                   # ahora .diff() existe → OK
        df["Golden_Cross"] = change > 0         # MA_50 cruza sobre MA_200
        df["Death_Cross"]  = change < 0         # MA_50 cruza bajo MA_200

    return df

# MODELO 2 — Regresión Lineal
def linear_regression_forecast(prices: pd.Series) -> dict:
    """
    Ajusta regresión OLS sobre logaritmos de precios (correcto geométricamente).
    Predice FORECAST_DAYS días con intervalo de predicción al 95%.
    """
    log_p: pd.Series = pd.Series(np.log(prices.values), index=prices.index)

    X = np.arange(len(log_p)).reshape(-1, 1)
    y = log_p.to_numpy()

    model  = LinearRegression().fit(X, y)
    y_pred = model.predict(X)
    r2     = r2_score(y, y_pred)
    rmse   = float(np.sqrt(mean_squared_error(y, y_pred)))

    n       = len(prices)
    fut_idx = np.arange(n, n + FORECAST_DAYS).reshape(-1, 1)
    log_fc  = model.predict(fut_idx)

    t_crit = 1.96
    se = rmse * np.sqrt(
        1 + 1 / n
        + (fut_idx.flatten() - float(X.mean())) ** 2
        / float(np.sum((X - X.mean()) ** 2))
    )

    future_dates = pd.bdate_range(
        start=prices.index[-1], periods=FORECAST_DAYS + 1
    )[1:]

    return {
        "forecast":  pd.Series(np.exp(log_fc),               index=future_dates),
        "lower_95":  pd.Series(np.exp(log_fc - t_crit * se), index=future_dates),
        "upper_95":  pd.Series(np.exp(log_fc + t_crit * se), index=future_dates),
        "r2":        r2,
        "slope_pct": float(np.exp(model.coef_[0]) - 1),
    }

# MODELO 3 — ARIMA
def check_stationarity(series: pd.Series) -> dict:
    """
    Test Augmented Dickey-Fuller.
    H0: la serie tiene raíz unitaria (no estacionaria).
    p < 0.05 → rechazar H0 → serie estacionaria.
    """
    result = adfuller(series.dropna())
    return {
        "ADF Statistic": round(cast(float, result[0]), 4),
        "p-value":       round(cast(float, result[1]), 4),
        "Stationary":    bool(result[1] < 0.05),
    }


def arima_forecast(prices: pd.Series, order: tuple = ARIMA_ORDER) -> dict:
    """
    Ajusta ARIMA(p,d,q) sobre log-precios y predice FORECAST_DAYS días.
    Devuelve forecast, IC al 95%, fechas, AIC y BIC.
    """
    log_prices: pd.Series = pd.Series(
        np.log(prices.values), index=prices.index
    )

    stat = check_stationarity(log_prices.diff().dropna())
    print(
        f"[ARIMA] ADF={stat['ADF Statistic']}, "
        f"p={stat['p-value']}, "
        f"Stationary={stat['Stationary']}"
    )

    result = ARIMA(log_prices, order=order).fit()
    fc_obj = result.get_forecast(steps=FORECAST_DAYS)
    ci     = fc_obj.conf_int(alpha=0.05)

    future_dates = pd.bdate_range(
        start=prices.index[-1], periods=FORECAST_DAYS + 1
    )[1:]

    return {
        "forecast": np.exp(fc_obj.predicted_mean.values),
        "lower_95": np.exp(ci.iloc[:, 0].values),
        "upper_95": np.exp(ci.iloc[:, 1].values),
        "dates":    future_dates,
        "aic":      result.aic,
        "bic":      result.bic,
        "order":    order,
    }

# GRÁFICO COMPARATIVO DE FORECASTS
def plot_forecast(prices: pd.Series, ticker: str = "Asset") -> None:
    """
    Gráfico de comparación de 3 paneles:
    Panel 1: Media móvil con marcadores Golden/Death Cross
    Panel 2: Regresión Lineal con intervalo de predicción al 95%
    Panel 3: ARIMA forecast con intervalo de confianza al 95%
    """
    os.makedirs("output", exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(21, 6))
    fig.suptitle(
        f"{ticker} — Comparación Forecast ({FORECAST_DAYS} días de horizonte)",
        fontsize=15, fontweight="bold",
    )

    hist_c  = "#64748B"
    fc_c    = "#1D4ED8"
    arima_c = "#0F766E"
    mc      = ["#F97316", "#DC2626", "#7C3AED"]

    # Panel 1 — Media Móvil
    ax = axes[0]
    ma = moving_average_signals(prices)
    ma["Precio"].plot(ax=ax, color=hist_c, lw=1.5, label="Precio", alpha=0.8)
    for w, c in zip(MA_WINDOWS, mc):
        ma[f"MA_{w}"].plot(ax=ax, color=c, lw=1.5,
                           linestyle="--", label=f"MA {w}")
    if "Golden_Cross" in ma.columns:
        gc = ma[ma["Golden_Cross"]]["Precio"]
        dc = ma[ma["Death_Cross"]]["Precio"]
        ax.scatter(gc.index, gc, marker="^", color="#16A34A",
                   s=120, zorder=5, label="Golden Cross")
        ax.scatter(dc.index, dc, marker="v", color="#DC2626",
                   s=120, zorder=5, label="Death Cross")
    ax.set_title("Media Móvil y Señales Cross")
    ax.set_ylabel("Precio ($)")
    ax.legend(fontsize=8, ncol=2)

    # Panel 2 — Regresión Lineal
    ax = axes[1]
    lr = linear_regression_forecast(prices)
    prices.plot(ax=ax, color=hist_c, lw=1.5, label="Histórico")
    lr["forecast"].plot(ax=ax, color=fc_c, lw=2.5, linestyle="--",
                        label=f"LR Forecast (R²={lr['r2']:.3f})")
    ax.fill_between(
        lr["forecast"].index, lr["lower_95"], lr["upper_95"],
        alpha=0.15, color=fc_c, label="Intervalo pred. 95%",
    )
    ax.axvline(prices.index[-1], color="black", lw=1,
               linestyle=":", alpha=0.5, label="Inicio forecast")
    ax.set_title("Forecast Regresión Lineal")
    ax.set_ylabel("Precio ($)")
    ax.legend(fontsize=8)

    # Panel 3 — ARIMA
    ax = axes[2]
    arima = arima_forecast(prices)
    prices.iloc[-120:].plot(ax=ax, color=hist_c, lw=1.5,
                            label="Histórico (últimos 120d)")
    ax.plot(arima["dates"], arima["forecast"],
            color=arima_c, lw=2.5, label=f"ARIMA{arima['order']}")
    ax.fill_between(arima["dates"], arima["lower_95"], arima["upper_95"],
                    alpha=0.2, color=arima_c, label="IC 95%")
    ax.axvline(prices.index[-1], color="black", lw=1,
               linestyle=":", alpha=0.5, label="Inicio forecast")
    ax.set_title(
        f"ARIMA Forecast  AIC={arima['aic']:.0f}  BIC={arima['bic']:.0f}"
    )
    ax.set_ylabel("Precio ($)")
    ax.legend(fontsize=8)

    plt.tight_layout()
    path = "output/forecasts.png"
    plt.savefig(path, dpi=DPI, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    print(f"[forecast] Gráfico guardado en {path}")
    #plt.show()