# main.py

"""
Analíticas de Portfolio
"""

import sys
import os
from datetime import datetime
import matplotlib.pyplot as plt

from src.data_loader    import load_prices, price_summary
from src.returns        import (daily_returns, portfolio_returns, cumulative_returns,
                                cagr, return_summary, filter_period)
from src.risk           import (risk_sumary, drawndown_series, correlation_matrix)
from src.visualization  import plot_dashboard
from src.forecasting    import plot_forecast
from src.market_trends  import sector_risk_return_chart, plot_rolling_beta, plot_regime
from src.optimization   import plot_efficient_frontier, plot_monte_carlo
from config             import TICKERS, BENCHMARK, WEIGHTS, START_DATE, END_DATE


def main(force_download: bool = False) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 58)
    print("  Python Análisis de Finanzas — Reporte de Cartera")
    print(f"  Generado: {ts}")
    print("=" * 58)

    # [1/11] Cargar datos del mercado
    print("\n[1/11] Cargando datos del mercado...")
    prices = load_prices(force_download=force_download)
    print(price_summary(prices).to_string())

    # [2/11] Calcular retornos (período config; precios extendidos solo para MA/forecast)
    print("\n[2/11] Calculando retornos...")
    daily_all = daily_returns(prices[TICKERS])
    bench_all = daily_returns(prices[[BENCHMARK]])[BENCHMARK]
    daily     = filter_period(daily_all)
    bench_ret = filter_period(bench_all)
    port_ret  = portfolio_returns(daily)
    cum_ret   = cumulative_returns(port_ret)
    bench_cum = cumulative_returns(bench_ret)
    cagr_val  = cagr(port_ret)
    ret_met   = return_summary(daily, port_ret)

    for k, v in ret_met.items():
        print(f"  {k:<32} {v}")

    # [3/11] Calcular métricas de riesgo
    print("\n[3/11] Calculando métricas de riesgo...")
    dd      = drawndown_series(cum_ret)
    corr    = correlation_matrix(daily)
    metrics = risk_sumary(port_ret, bench_ret, cum_ret, cagr_val)

    print("  +------ RESUMEN DE RIESGO Y RETORNOS ----------------+")
    for k, v in metrics.items():
        print(f"  |  {k:<34} {v:<10}  |")
    print("  +-----------------------------------------------------+")

    # [4/11] Guardar reporte en texto
    print("\n[4/11] Guardando texto de reporte...")
    os.makedirs("output", exist_ok=True)
    lines = [
        f"Reporte del análisis de cartera — {ts}",
        f"Período: {START_DATE} → {END_DATE}",
        f"Tickers: {TICKERS}",
        f"Weights: {WEIGHTS}",
        "\n=== MÉTRICAS DE RETORNO ===",
        *[f"{k}: {v}" for k, v in ret_met.items()],
        "\n=== MÉTRICAS DE RIESGO ===",
        *[f"{k}: {v}" for k, v in metrics.items()],
    ]
    with open("output/report.txt", "w") as f:
        f.write("\n".join(lines))
    print("  Guardado -> output/report.txt")

    # [5/11] Renderizar dashboard
    print("\n[5/11] Renderizando dashboard...")
    plot_dashboard(cum_ret, daily, dd, corr, port_ret, bench_cum)

    # [6/11] Modelos de forecasting
    print("\n[6/11] Corriendo modelos forecasting...")
    plot_forecast(prices[TICKERS[0]], ticker=TICKERS[0])

    # [7/11] Tendencias de mercado — sectores
    print("\n[7/11] Corriendo tendencias de mercado...")
    sector_risk_return_chart()

    # [8/11] Rolling Beta — detección de régimen
    print("\n[8/11] Calculando Rolling Beta...")
    plot_rolling_beta(port_ret, bench_ret, window=63)

    # [9/11] Detección de régimen por volatilidad
    print("\n[9/11] Detectando régimen de volatilidad...")
    plot_regime(port_ret, cum_ret, window=10, percentile=70)

    # [10/11] Frontera eficiente - pesos optimos de máximo Sharpe
    print("\n[10/11] Calculado frontera eficiente...")
    plot_efficient_frontier(daily, n_portfolios=5_000)

    # [11/11] Simulación Monte Carlo - distribución caminos futuros
    print("\n[11/11] Corriendo simulación Monte Carlo...")
    plot_monte_carlo(port_ret, n_simulations=1_000, n_days=252)

    print("\n" + "=" * 58)
    print("  Todos los outputs guardados en output/")
    print("  dashboard.png  |  forecasts.png  |  report.txt")
    print("  sectors.png    |  rolling_beta.png  |  regime.png")
    print("  efficient_frontier.png  |  monte_carlo.png")
    print("=" * 58)

    # Mantener todas las ventanas de gráficos abiertas simultáneamente
    print("\nAbriendo todos los gráficos en ventanas independientes...")
    plt.show()


if __name__ == "__main__":
    force = "--force-download" in sys.argv
    main(force_download=force)