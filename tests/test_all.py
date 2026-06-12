"""
Suite de tests de validación para Python Finance Analytics.
Ejecutar con:  python tests/test_all.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import Any

import numpy as np
import pandas as pd

from config import TICKERS, WEIGHTS, BENCHMARK, RISK_FEE, VAR_CONFIDENCE
from src.data_loader  import load_prices, price_summary
from src.returns      import (daily_returns, log_returns, portfolio_returns,
                               cumulative_returns, cagr, annualized_return,
                               monthly_returns, return_summary, filter_period)
from src.risk         import (annualized_volatility, sharpe_ratio, sortino_ratio,
                               drawndown_series, max_drawdown, max_drawdown_duration,
                               calmar_ratio, beta, jensens_alpha,
                               var_historical, cvar_historical,
                               correlation_matrix, risk_sumary)
from src.forecasting  import (moving_average_signals, linear_regression_forecast,
                               check_stationarity, arima_forecast)
from src.optimization import max_sharpe_weights, monte_carlo_simulation

PASS = "  [PASS]"
FAIL = "  [FAIL]"


def section(title: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


def check(condition: Any, description: str) -> bool:
    result = bool(condition)

    if result:
        print(f"{PASS} {description}")
    else:
        print(f"{FAIL} {description}")

    return result


# 1. CONFIG
def test_config() -> bool:
    section("1. config.py")
    results = []

    results.append(check(len(TICKERS) > 0,
                         "TICKERS no está vacío"))
    results.append(check(len(TICKERS) == len(WEIGHTS),
                         "TICKERS y WEIGHTS tienen la misma longitud"))
    results.append(check(abs(sum(WEIGHTS) - 1.0) < 1e-10,
                         f"WEIGHTS suman 1.0 (actual: {sum(WEIGHTS):.10f})"))
    results.append(check(all(w >= 0 for w in WEIGHTS),
                         "Todos los pesos son >= 0 (long-only)"))
    results.append(check(0.0 < RISK_FEE < 0.20,
                         f"RISK_FREE en rango razonable (actual: {RISK_FEE:.3f})"))
    results.append(check(0.90 <= VAR_CONFIDENCE < 1.0,
                         f"VAR_CONFIDENCE en rango razonable (actual: {VAR_CONFIDENCE})"))
    results.append(check(BENCHMARK.startswith("^") or len(BENCHMARK) <= 6,
                         f"BENCHMARK parece válido (actual: {BENCHMARK})"))

    return all(results)


# 2. DATA LOADER
def test_data_loader(prices: pd.DataFrame) -> bool:
    section("2. data_loader.py")
    results = []

    results.append(check(isinstance(prices, pd.DataFrame),
                         "load_prices() devuelve un DataFrame"))
    results.append(check(len(prices) >= 252,
                         f"Al menos 252 filas (actual: {len(prices):,})"))
    results.append(check(prices.isnull().sum().sum() == 0,
                         "Sin valores NaN"))
    results.append(check((prices > 0).all().all(),
                         "Todos los precios son positivos"))
    results.append(check(all(t in prices.columns for t in TICKERS),
                         f"Todos los TICKERS presentes en columnas"))
    results.append(check(BENCHMARK in prices.columns,
                         f"BENCHMARK '{BENCHMARK}' presente"))
    results.append(check(isinstance(prices.index, pd.DatetimeIndex),
                         "Index es DatetimeIndex"))

    summary = price_summary(prices)
    results.append(check(isinstance(summary, pd.DataFrame),
                         "price_summary() devuelve DataFrame"))

    return all(results)


# 3. RETURNS
def test_returns(prices: pd.DataFrame) -> tuple[bool, pd.Series, pd.Series]:
    section("3. returns.py")
    results = []

    daily    = filter_period(daily_returns(prices[TICKERS]))
    port_ret = portfolio_returns(daily)
    cum_ret  = cumulative_returns(port_ret)
    cagr_val = cagr(port_ret)
    ann_ret  = annualized_return(port_ret)

    results.append(check(isinstance(daily, pd.DataFrame),
                         "daily_returns() devuelve DataFrame"))
    results.append(check(len(daily_returns(prices[TICKERS])) == len(prices) - 1,
                         f"daily_returns() tiene n-1 filas"))
    results.append(check(len(daily) >= 20,
                         f"filter_period() devuelve datos del período (actual: {len(daily)} filas)"))
    results.append(check(daily.isnull().sum().sum() == 0,
                         "Sin NaN en daily_returns()"))
    results.append(check(isinstance(port_ret, pd.Series),
                         "portfolio_returns() devuelve Series"))
    results.append(check(port_ret.name == "Portfolio",
                         "portfolio_returns() tiene nombre 'Portfolio'"))
    results.append(check(not port_ret.isnull().any(),
                         "Sin NaN en portfolio_returns()"))
    results.append(check(isinstance(cum_ret, pd.Series),
                         "cumulative_returns() devuelve Series"))
    results.append(check(not cum_ret.isnull().any(),
                         "Sin NaN en cumulative_returns()"))
    results.append(check(isinstance(cagr_val, float),
                         f"cagr() devuelve float (actual: {cagr_val:.4f})"))
    results.append(check(-0.5 < cagr_val < 5.0,
                         f"CAGR en rango razonable (actual: {cagr_val:.2%})"))
    results.append(check(isinstance(ann_ret, float),
                         f"annualized_return() devuelve float"))

    log_ret = log_returns(prices[TICKERS])
    results.append(check(isinstance(log_ret, pd.DataFrame),
                         "log_returns() devuelve DataFrame"))
    results.append(check(log_ret.isnull().sum().sum() == 0,
                         "Sin NaN en log_returns()"))

    monthly = monthly_returns(port_ret)
    results.append(check(isinstance(monthly, pd.Series),
                         "monthly_returns() devuelve Series"))
    results.append(check(len(monthly) < len(port_ret),
                         "monthly_returns() tiene menos filas que daily"))

    summary = return_summary(daily, port_ret)
    results.append(check(isinstance(summary, dict),
                         "return_summary() devuelve dict"))
    results.append(check(len(summary) == 6,
                         f"return_summary() tiene 6 claves (actual: {len(summary)})"))

    return all(results), port_ret, cum_ret


# 4. RISK
def test_risk(prices: pd.DataFrame, port_ret: pd.Series,
              cum_ret: pd.Series) -> bool:
    section("4. risk.py")
    results = []

    daily     = filter_period(daily_returns(prices[TICKERS]))
    bench_ret = filter_period(daily_returns(prices[[BENCHMARK]])[BENCHMARK])
    cagr_val  = cagr(port_ret)

    vol    = annualized_volatility(port_ret)
    sharpe = sharpe_ratio(port_ret)
    sortino= sortino_ratio(port_ret)
    mdd    = max_drawdown(cum_ret)
    mdd_dur= max_drawdown_duration(cum_ret)
    calmar = calmar_ratio(cagr_val, mdd)
    b      = beta(port_ret, bench_ret)
    alpha  = jensens_alpha(port_ret, bench_ret)
    var    = var_historical(port_ret)
    cvar   = cvar_historical(port_ret)
    corr   = correlation_matrix(daily)
    dd_ser = drawndown_series(cum_ret)

    results.append(check(isinstance(vol, float) and 0.01 < vol < 2.0,
                         f"Volatilidad en rango razonable (actual: {vol:.2%})"))
    results.append(check(isinstance(sharpe, float) and -5 < sharpe < 15,
                         f"Sharpe en rango razonable (actual: {sharpe:.3f})"))
    results.append(check(isinstance(sortino, float),
                         f"Sortino devuelve float (actual: {sortino:.3f})"))
    results.append(check(isinstance(mdd, float) and -1.0 <= mdd <= 0.0,
                         f"Max Drawdown en rango [-1, 0] (actual: {mdd:.2%})"))
    results.append(check(isinstance(mdd_dur, int) and mdd_dur >= 0,
                         f"Max DD Duration >= 0 (actual: {mdd_dur} días)"))
    results.append(check(isinstance(calmar, float),
                         f"Calmar devuelve float (actual: {calmar:.3f})"))
    results.append(check(isinstance(b, float) and -5 < b < 10,
                         f"Beta en rango razonable (actual: {b:.3f})"))
    results.append(check(isinstance(alpha, float),
                         f"Alpha devuelve float (actual: {alpha:.4f})"))
    results.append(check(isinstance(var, float) and var < 0,
                         f"VaR es negativo (actual: {var:.2%})"))
    results.append(check(isinstance(cvar, float) and cvar <= var,
                         f"CVaR <= VaR (CVaR: {cvar:.2%}, VaR: {var:.2%})"))
    results.append(check(isinstance(corr, pd.DataFrame),
                         "correlation_matrix() devuelve DataFrame"))
    results.append(check(corr.shape == (len(TICKERS), len(TICKERS)),
                         f"Correlation matrix shape correcta: {corr.shape}"))
    results.append(check(((corr >= -1) & (corr <= 1)).all().all(),
                         "Todos los valores de correlación en [-1, 1]"))
    results.append(check((dd_ser <= 0).all(),
                         "drawdown_series() siempre <= 0"))

    metrics = risk_sumary(port_ret, bench_ret, cum_ret, cagr_val)
    results.append(check(isinstance(metrics, dict) and len(metrics) == 10,
                         f"risk_summary() tiene 10 claves (actual: {len(metrics)})"))

    return all(results)


# 5. FORECASTING
def test_forecasting(prices: pd.DataFrame) -> bool:
    section("5. forecasting.py")
    results = []

    sample = prices[TICKERS[0]]

    ma = moving_average_signals(sample)
    results.append(check(isinstance(ma, pd.DataFrame),
                         "moving_average_signals() devuelve DataFrame"))
    results.append(check("Precio" in ma.columns,
                         "Columna 'Precio' presente"))
    results.append(check(all(f"MA_{w}" in ma.columns for w in [20, 50, 200]),
                         "Columnas MA_20, MA_50, MA_200 presentes"))

    from src.returns import log_returns as lr
    log_r = lr(sample.to_frame()).iloc[:, 0]
    stat  = check_stationarity(log_r)
    results.append(check(isinstance(stat, dict),
                         "check_stationarity() devuelve dict"))
    results.append(check("ADF Statistic" in stat and "p-value" in stat,
                         "check_stationarity() tiene claves correctas"))

    lr_result = linear_regression_forecast(sample)
    results.append(check(isinstance(lr_result, dict),
                         "linear_regression_forecast() devuelve dict"))
    results.append(check("forecast" in lr_result and "r2" in lr_result,
                         "linear_regression_forecast() tiene claves 'forecast' y 'r2'"))
    results.append(check(0.0 <= lr_result["r2"] <= 1.0,
                         f"R² en [0, 1] (actual: {lr_result['r2']:.4f})"))
    results.append(check(len(lr_result["forecast"]) == 30,
                         f"Forecast tiene 30 días (actual: {len(lr_result['forecast'])})"))

    return all(results)


# 6. OPTIMIZATION
def test_optimization(prices: pd.DataFrame, port_ret: pd.Series) -> bool:
    section("6. optimization.py")
    results = []

    daily = filter_period(daily_returns(prices[TICKERS]))

    opt = max_sharpe_weights(daily)
    results.append(check(isinstance(opt, dict),
                         "max_sharpe_weights() devuelve dict"))
    results.append(check(abs(sum(opt["weights"]) - 1.0) < 1e-6,
                         f"Pesos óptimos suman 1.0 (actual: {sum(opt['weights']):.8f})"))
    results.append(check(all(w >= -1e-8 for w in opt["weights"]),
                         "Todos los pesos óptimos >= 0 (long-only)"))
    results.append(check(isinstance(opt["sharpe"], float) and opt["sharpe"] > 0,
                         f"Sharpe óptimo > 0 (actual: {opt['sharpe']:.3f})"))
    results.append(check(0 < opt["volatility"] < 2.0,
                         f"Volatilidad óptima en rango (actual: {opt['volatility']:.2%})"))

    sims = monte_carlo_simulation(port_ret, n_simulations=100, n_days=252)
    results.append(check(isinstance(sims, np.ndarray),
                         "monte_carlo_simulation() devuelve ndarray"))
    results.append(check(sims.shape == (100, 252),
                         f"Shape correcta (100, 252) (actual: {sims.shape})"))
    results.append(check(not np.isnan(sims).any(),
                         "Sin NaN en simulaciones Monte Carlo"))

    sims2 = monte_carlo_simulation(port_ret, n_simulations=100, n_days=252)
    results.append(check(np.allclose(sims, sims2),
                         "Monte Carlo es reproducible (semilla fija)"))

    return all(results)


def main() -> None:
    print("=" * 50)
    print("  Python Finance Analytics — Test Suite")
    print("=" * 50)

    all_passed: list[bool] = []

    all_passed.append(test_config())

    print("\n  Cargando datos (puede tardar en la primera ejecución)...")
    prices = load_prices()

    all_passed.append(test_data_loader(prices))

    passed, port_ret, cum_ret = test_returns(prices)
    all_passed.append(passed)

    all_passed.append(test_risk(prices, port_ret, cum_ret))
    all_passed.append(test_forecasting(prices))
    all_passed.append(test_optimization(prices, port_ret))

    total = len(all_passed)
    passed = sum(all_passed)

    print(f"\n{'=' * 50}")
    if passed == total:
        print(f"TODOS LOS TESTS PASARON ({passed}/{total})")
    else:
        print(f"{total - passed} MÓDULO(S) CON FALLOS ({passed}/{total} OK)")
    print(f"{'=' * 50}\n")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()