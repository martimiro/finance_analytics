# src/optimization.py

"""
Módulo de optimización de portafolio.
- Frontera eficiente y portafolio de máximo de Sharpe
- Simulación Monte Carlo de caminos futuros del portafolio
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.optimize import OptimizeResult
from config import TICKERS, RISK_FEE, DPI

# Frontera eficiente - Máximo Sharpe
def _portfolio_stats(weights: np.ndarray, mean_ret: pd.Series, cov_mat: pd.DataFrame) -> tuple[float, float, float]:
    """
    Calcula retorno, volatilidad y Sharpe anualizado para un vector de pesos

    Returns
    -------
    (retorno_anual, volatilidad_anual, sharpe)
    """
    ret = float(np.dot(weights, mean_ret))
    vol = float(np.sqrt(weights @ cov_mat.to_numpy() @ weights))
    sharpe = (ret - RISK_FEE) / vol if vol > 0 else 0.0
    return ret, vol, sharpe

def max_sharpe_weights(daily_ret: pd.DataFrame) -> dict:
    """
    Encuentra los pesos del portfolio de máximo Sharpe usando optimización SLSQP
    con restricciones de suma 1 y máximo 35% por activo (límite de diversificación).
    """
    mean_ret = daily_ret.mean() * 252
    cov_mat = daily_ret.cov() * 252
    n = len(daily_ret.columns)

    def neg_sharpe(w: np.ndarray) -> float:
        _, _, sharpe = _portfolio_stats(w, mean_ret, cov_mat)
        return -sharpe
  
    result: OptimizeResult = minimize(
        neg_sharpe, 
        x0=np.ones(n) / n, 
        method='SLSQP', 
        bounds=[(0.05, 0.35) for _ in range(n)],  # Min 5%, Max 35% por activo
        constraints=[{"type": 'eq', 'fun': lambda w: np.sum(w) - 1}], 
        options={'maxiter': 1000, 'ftol': 1e-12}
    )

    if not result.success:
        raise RuntimeError(f'[Optimization] Optimización no convergió {result.message}')
  
    opt_w = result.x
    ret, vol, sharpe = _portfolio_stats(opt_w, mean_ret, cov_mat)

    return {
        'weights': opt_w, 
        'tickers': list(mean_ret.index),
        "return": ret, 
        "volatility": vol, 
        'sharpe': sharpe
    }

def plot_efficient_frontier(daily_ret: pd.DataFrame, n_portfolios: int = 5_000) -> None:
    """
    Genera la Frontera Eficiente simulando n_portfolios aleatorios y marca el portafolio de máximo Sharpe y el de mínima volatilidad.
    """
    os.makedirs('output', exist_ok=True)

    mean_ret = daily_ret.mean() * 252
    cov_mat = daily_ret.cov() * 252
    n = len(daily_ret.columns)

    rets, vols, sharpes = [], [], []

    # Para asegurar que la frontera eficiente muestre los extremos reales del optimizador,
    # inyectamos los pesos individuales de cada activo (100% en un solo activo) en la simulación.
    for i in range(n):
        w_single = np.zeros(n)
        w_single[i] = 1.0
        r, v, s = _portfolio_stats(w_single, mean_ret, cov_mat)
        rets.append(r)
        vols.append(v)
        sharpes.append(s)

    # Simular el resto de portafolios aleatorios distribuidos uniformemente
    for _ in range(n_portfolios - n):
        w = np.random.dirichlet(np.ones(n))
        r, v, s = _portfolio_stats(w, mean_ret, cov_mat)
        rets.append(r)
        vols.append(v)
        sharpes.append(s)

    rets = np.array(rets)
    vols = np.array(vols)
    sharpes = np.array(sharpes)

    # Portafolio óptimo calculado vía SciPy SLSQP
    opt = max_sharpe_weights(daily_ret)
    opt_ret = opt['return']
    opt_vol = opt['volatility']
    opt_w = opt['weights']

    # Portafolio de mínima volatilidad de la muestra simulada
    min_val_idx = int(np.argmin(vols))

    # Gráfico de Frontera Eficiente
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Optimización de Portafolio - Frontera eficiente", fontsize=14, fontweight="bold")

    # Panel izquierdo: Scatter plot de la frontera
    ax = axes[0]
    sc = ax.scatter(vols * 100, rets * 100, c=sharpes, cmap="RdYlGn", alpha=0.4, s=8)
    plt.colorbar(sc, ax=ax, label='Sharpe Ratio')

    # Marcar máximo sharpe real y mínima vol
    ax.scatter(opt_vol * 100, opt_ret * 100, marker='*', s=400, color='#1D4ED8', zorder=5, label=f"Máx. Sharpe real ({opt['sharpe']:.2f})")
    ax.scatter(vols[min_val_idx] * 100, rets[min_val_idx] * 100, marker='D', color='#DC2626', zorder=5, label=f'Mín. Volatilidad ({vols[min_val_idx] * 100:.1f}%)')
    ax.set_xlabel("Volatilidad anualizada (%)")
    ax.set_ylabel("Retorno anualizado (%)")
    ax.set_title("Frontera Eficiente")
    ax.legend(fontsize=9)

    # Panel derecho: Pesos del portfolio óptimo
    ax = axes[1]
    colors = ['#1D4ED8', '#0F766E', '#7C3AED', '#EA580C', '#16A34A']
    bars = ax.bar(opt['tickers'], opt_w * 100, color=colors[:n], edgecolor='white', linewidth=1.5)
  
    for bar, w in zip(bars, opt_w):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f'{w*100:.1f}%', ha='center', va='bottom', fontsize=10)
  
    ax.set_ylabel("Peso (%)")
    ax.set_title(f"Pesos óptimos (Sharpe: {opt['sharpe']:.2f})\n"
                 f"Retorno: {opt_ret*100:.1f}% | Vol: {opt_vol*100:.1f}%\n"
                 f"(Portafolio teórico óptimo - no es tu cartera actual)")
    ax.set_ylim(0, max(opt_w * 100) * 1.2)

    plt.tight_layout()
    path = 'output/efficient_frontier.png'
    plt.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white", edgecolor="none")
    print(f'[optimization] Guardado en {path}')


# Simulación Monte Carlo
def monte_carlo_simulation(port_ret: pd.Series, n_simulations: int = 1_000, n_days: int = 252) -> np.ndarray:
    """
    Simula n_simulations caminos futuros del portafolio usando bootstrap.
    """
    rng = np.random.default_rng(seed=42)
    hist = port_ret.to_numpy()
    sims = np.zeros((n_simulations, n_days))

    for i in range(n_simulations):
        sampled = rng.choice(hist, size=n_days, replace=True)
        sims[i] = (1 + sampled).cumprod() - 1

    return sims

def plot_monte_carlo(port_ret: pd.Series, n_simulations: int = 1_000, n_days: int = 252, confidence: float = 0.95) -> None:
    """
    Grafica los caminos Monte Carlo con bandas de percentiles e histograma final.
    """
    os.makedirs('output', exist_ok=True)

    sims = monte_carlo_simulation(port_ret, n_simulations, n_days)

    # Percentiles de la distribución de caminos
    lo = (1 - confidence) / 2 * 100
    hi = 100 - lo
    p_lo, p25, p50, p75, p_hi = np.percentile(sims, [lo, 25, 50, 75, hi], axis=0)

    # Distribución de retornos finales
    final = sims[:, -1]
    prob_positive = float((final > 0).mean())
    var_final = float(np.percentile(final, (1 - confidence) * 100))
    cvar_final = float(final[final <= var_final].mean())

    # Gráfico de Monte Carlo
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(f'Simulación Monte Carlo - {n_simulations:,} caminos |\n'
                 f'Horizonte: {n_days}d', fontsize=14, fontweight="bold")
  
    # Panel izquierdo: Caminos futuros con bandas de confianza corregidas
    ax = axes[0]
    days = np.arange(n_days)

    # CORREGIDO: Ahora fill_between recibe explícitamente el límite inferior y el superior
    ax.fill_between(days, p_lo * 100, p_hi * 100, alpha=0.15, color='#1D4ED8', label=f'IC {confidence:.0%} ({lo:.1f}% - {hi:.1f}%)')
    ax.fill_between(days, p25 * 100, p75 * 100, alpha=0.25, color='#1D4ED8', lw=0, label='Rango intercuartílico (25-75p)')
    ax.plot(days, p50 * 100, color='#1D4ED8', lw=2.5, label='Mediana')
    ax.axhline(0, color='black', lw=0.8, linestyle=':', alpha=0.6)
    ax.set_xlabel('Días de trading')
    ax.set_ylabel('Retorno acumulado (%)')
    ax.set_title("Distribución de caminos futuros")
    ax.legend(fontsize=9)

    # Panel derecho: Histograma de distribución final
    ax = axes[1]
    ax.hist(final * 100, bins=60, color='#1D4ED8', alpha=0.7, edgecolor='white', linewidth=0.3)
    ax.axvline(float(np.median(final)) * 100, color="black", lw=2, linestyle="-.", label=f"Mediana: {float(np.median(final))*100:.1f}%")
    ax.axvline(var_final * 100, color="#DC2626", lw=2, linestyle="--", label=f"VaR {confidence:.0%}: {var_final*100:.1f}%")
    ax.axvline(cvar_final * 100, color="#EA580C", lw=1.5, linestyle=":", label=f"CVaR {confidence:.0%}: {cvar_final*100:.1f}%")

    # Anotación flotante de probabilidad de éxito
    ax.text(0.97, 0.95, f'P(retorno > 0): {prob_positive:.1%}', transform=ax.transAxes, ha='right', va='top', fontsize=11, fontweight='bold', bbox={"boxstyle": "round,pad=0.3", 'facecolor': '#D8EAFE', 'edgecolor': '#1D4ED8', 'alpha': 0.9})
    ax.set_xlabel(f'Retorno acumulado a {n_days}d (%)')
    ax.set_ylabel("Frecuencia")
    ax.set_title("Distribución del retorno final")
    ax.legend(fontsize=9)

    plt.tight_layout()
    path = 'output/monte_carlo.png'
    plt.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"[optimization] Guardado en {path}")