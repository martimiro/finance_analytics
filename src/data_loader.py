# src/data_loader.py

"""
Módulo de adquisición de datos.

Descarga los precios de cierre ajustados a través de yfinance, limpia,
valida y almacena en caché.

Compatibilidad: yfinance >= 0.2 (MultiIndex columns con auto_adjust=True)
"""

import os
import yfinance as yf
import pandas as pd

from config import TICKERS, BENCHMARK, START_DATE, END_DATE
from datetime import datetime, timedelta

CACHE_PATH = "data/prices.csv"


def load_prices(force_download: bool = False) -> pd.DataFrame:
    """
    Carga los precios de cierre ajustados para todos los tickers + benchmark.
    Pre-carga 200 días históricos ANTES de START_DATE para asegurar que 
    indicadores técnicos como MA 200 se grafiquen completos desde el inicio.

    Parameters
    ----------
    force_download : bool
        Omitir la caché local y volver a descargar desde Yahoo Finance.

    Returns
    -------
    pd.DataFrame
        Index  : DatetimeIndex (días hábiles / laborables)
        Columns: TICKERS + BENCHMARK
        Values : float – precios de cierre ajustados (todos positivos)
    """
    os.makedirs("data", exist_ok=True)

    # Cargar desde caché si está disponible
    if os.path.exists(CACHE_PATH) and not force_download:
        df = pd.read_csv(CACHE_PATH, index_col=0, parse_dates=True)
        _validate(df)
        print(f"[loader] Cargadas {len(df):,} filas desde caché ({CACHE_PATH})")
        return df

    # Descargar desde Yahoo Finance con 200 días previos
    all_tickers = TICKERS + [BENCHMARK]
    print(f"[loader] Descargando {len(all_tickers)} tickers ...")

    # Calcular fecha de inicio extendida (200 días hábiles antes)
    start_dt = datetime.strptime(START_DATE, '%Y-%m-%d')
    # Aproximación: 200 días / 5*252 = 40 semanas = ~280 días calendario
    extended_start = (start_dt - timedelta(days=280)).strftime('%Y-%m-%d')

    raw = yf.download(
        all_tickers,
        start=extended_start,
        end=END_DATE,
        auto_adjust=True,   # ajusta splits + dividendos; campo correcto = "Close"
        progress=False,
        threads=True,
    )

    # Detectar descarga fallida antes de acceder a columnas
    if raw is None or raw.empty:
        raise RuntimeError(
            "[loader] yfinance no devolvió datos. "
            "Comprueba tu conexión a internet y que los tickers sean válidos."
        )

    # FIX (Pylance reportArgumentType / reportReturnType):
    # raw["Close"] es tipado como DataFrame | Series por Pylance porque con un
    # único ticker yfinance puede devolver una Series. Envolver con pd.DataFrame()
    # garantiza el tipo DataFrame en ambos casos y satisface al type-checker.
    if isinstance(raw.columns, pd.MultiIndex):
        # Múltiples tickers → MultiIndex: nivel 0 = campo, nivel 1 = ticker
        df = pd.DataFrame(raw["Close"])
    else:
        # Único ticker → columnas simples; tomamos solo "Close" y renombramos
        df = pd.DataFrame(raw[["Close"]])
        df.columns = pd.Index(all_tickers)

    # Limpiar
    n_before = len(df)
    df = df.ffill()     # rellenar hacia adelante los huecos de días festivos
    df = df.dropna()    # eliminar filas que sigan con NaN tras el ffill
    n_dropped = n_before - len(df)

    if n_dropped > 5:
        print(f"[loader] ALERTA: se eliminaron {n_dropped} filas con NaN")

    # Validar y guardar caché
    _validate(df)
    df.to_csv(CACHE_PATH)
    print(f"[loader] {len(df):,} filas guardadas en {CACHE_PATH}")
    return df


def _validate(df: pd.DataFrame) -> None:
    """Lanza errores informativos ante datos malformados."""
    missing = [t for t in (TICKERS + [BENCHMARK]) if t not in df.columns]
    if missing:
        raise ValueError(f"Faltan tickers en los datos: {missing}")

    assert len(df) >= 252, (
        f"Solo {len(df)} filas — se necesitan >= 252 (1 año de trading)"
    )

    nan_counts = df.isnull().sum()
    if nan_counts.any():
        raise ValueError(
            f"Valores NaN restantes tras la limpieza:\n"
            f"{nan_counts[nan_counts > 0]}"
        )

    assert (df > 0).all().all(), "Se encontraron precios no positivos (cero o negativos)"


def price_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna estadísticas descriptivas para un chequeo de sanidad rápido."""
    return pd.DataFrame({
        "Start Price":  df.iloc[0].round(2),
        "End Price":    df.iloc[-1].round(2),
        "Min":          df.min().round(2),
        "Max":          df.max().round(2),
        "Trading Days": len(df),
    }).T