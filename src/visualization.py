# src/visualization.py

"""
Módulo de visualización.
Produce un dashboard de 6 paneles guardado como PNG de alta resolución.
"""

import os
from typing import cast, Sequence

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.text as mtext
from matplotlib.axes import Axes
import seaborn as sns

from config import TICKERS, WEIGHTS, DPI, FIGSIZE, STYLE
from src.risk import var_historical

# Paleta de colores
COLORS = {
    "portfolio": "#1D4ED8",
    "benchmark": "#94A3B8",
    "positive":  "#16A34A",
    "negative":  "#DC2626",
    "drawdown":  "#F97316",
    "var_line":  "#EF4444",
    "assets":    ["#1D4ED8", "#0F766E", "#7C3AED", "#EA580C", "#16A34A"],
}


def _fill(ax: Axes, index: pd.Index, values: pd.Series,
          mask: np.ndarray, color: str, alpha: float = 0.1) -> None:
    """
    Wrapper de fill_between que convierte la máscara a list[bool].
    FIX: matplotlib-stubs declara where como Sequence[bool] | None.
    Ni Series[bool] ni ndarray satisfacen ese tipo según Pylance.
    Convertir a list[bool] es la única representación que Pylance acepta
    sin necesidad de cast(), porque list[bool] implementa Sequence[bool]
    de forma explícita en los stubs de typeshed.
    """
    where: list[bool] = mask.tolist()
    ax.fill_between(index, values, 0, where=where, alpha=alpha, color=color)


def plot_dashboard(
    cum_ret:     pd.Series,
    daily_ret:   pd.DataFrame,
    drawdown:    pd.Series,
    corr_matrix: pd.DataFrame,
    port_ret:    pd.Series,
    bench_cum:   pd.Series,
) -> None:
    """
    Renderizar y guardar el dashboard de analíticas del portfolio en 6 paneles.
    Output: output/dashboard.png
    """
    os.makedirs("output", exist_ok=True)
    sns.set_theme(style=STYLE, palette="muted")
    plt.rcParams.update({
        "font.family":      "DejaVu Sans",
        "axes.titlesize":   13,
        "axes.titleweight": "bold",
        "axes.labelsize":   11,
        "legend.fontsize":  9,
    })

    fig = plt.figure(figsize=FIGSIZE)
    fig.suptitle("Analíticas del Dashboard del Portfolio",
                 fontsize=18, fontweight="bold", y=1.01)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

    # [0,0] Retorno acumulado
    ax = fig.add_subplot(gs[0, 0])
    (cum_ret * 100).plot(ax=ax, color=COLORS["portfolio"],
                         linewidth=2.5, label="Portfolio", zorder=3)
    (bench_cum * 100).plot(ax=ax, color=COLORS["benchmark"],
                           linewidth=1.8, linestyle="--",
                           label="S&P 500", zorder=2)
    ax.axhline(0, color="black", lw=0.8, linestyle=":", alpha=0.5)

    # FIX (reportArgumentType): ni Series[bool] ni ndarray satisfacen
    # Sequence[bool] según los stubs de matplotlib. list[bool] sí lo hace
    # porque implementa Sequence explícitamente. Delegado a _fill().
    pct = cum_ret * 100
    pos_mask: np.ndarray = (pct >= 0).to_numpy()
    _fill(ax, cum_ret.index, pct, pos_mask,  COLORS["positive"])
    _fill(ax, cum_ret.index, pct, ~pos_mask, COLORS["negative"])

    ax.set_title("Retorno acumulado")
    ax.set_ylabel("Retorno (%)")
    ax.legend(loc="upper left")

    # [0,1] Distribución de retornos
    ax = fig.add_subplot(gs[0, 1])
    ret_pct = port_ret * 100
    ax.hist(ret_pct, bins=70, color=COLORS["portfolio"],
            alpha=0.75, edgecolor="white", linewidth=0.2)
    var_val = var_historical(port_ret) * 100
    ax.axvline(var_val, color=COLORS["var_line"], lw=2, linestyle="--",
               label=f"VaR 95%: {var_val:.2f}%")
    ax.axvline(ret_pct.mean(), color="black", lw=1.5, linestyle="-.",
               label=f"Media: {ret_pct.mean():.3f}%")
    ax.set_title("Distribución rendimiento diario")
    ax.set_xlabel("Retorno Diario (%)")
    ax.set_ylabel("Frecuencia")
    ax.legend()

    # [0,2] Drawdown
    ax = fig.add_subplot(gs[0, 2])
    dd_pct = drawdown * 100
    ax.plot(dd_pct.index, dd_pct, color=COLORS["drawdown"], lw=1.5)
    dd_mask: np.ndarray = (dd_pct < 0).to_numpy()
    _fill(ax, dd_pct.index, dd_pct, dd_mask, COLORS["drawdown"], alpha=0.35)
    ax.axhline(dd_pct.min(), color=COLORS["negative"], lw=1,
               linestyle=":", label=f"Max DD: {dd_pct.min():.1f}%")
    ax.set_title("Drawdown del portfolio")
    ax.set_ylabel("Drawdown (%)")
    ax.legend()

    # [1,0] Correlation Heatmap
    ax = fig.add_subplot(gs[1, 0])
    sns.heatmap(corr_matrix, ax=ax,
                annot=True, fmt=".2f", cmap="RdYlGn",
                vmin=-1, vmax=1, center=0,
                linewidths=0.5, linecolor="white",
                annot_kws={"size": 9}, cbar_kws={"shrink": 0.8})
    ax.set_title("Matriz de correlación de activos")

    # [1,1] Portfolio Weights Pie Chart
    ax = fig.add_subplot(gs[1, 1])
    # FIX (reportAssignmentType + index out of range):
    # ax.pie() está tipado como tuple[list[Wedge], list[Text]] (2 elementos)
    # cuando Pylance no puede inferir que autopct produce un tercer elemento.
    # cast() a la tupla completa de 3 elementos resuelve tanto el índice [2]
    # como el tipo de sus contenidos (list[Text]), permitiendo set_fontsize().
    pie_raw = ax.pie(
        WEIGHTS, labels=TICKERS, autopct="%1.1f%%",
        startangle=90, colors=COLORS["assets"],
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    pie_result = cast(
        tuple[list, list, list[mtext.Text]],
        pie_raw,
    )
    for autotext in pie_result[2]:
        autotext.set_fontsize(9)
    ax.set_title("Pesos del portfolio")

    # [1,2] Volatilidad móvil 30 días
    ax = fig.add_subplot(gs[1, 2])
    rv = daily_ret[TICKERS].rolling(30).std() * np.sqrt(252) * 100
    for i, ticker in enumerate(TICKERS):
        rv[ticker].plot(ax=ax, label=ticker,
                        color=COLORS["assets"][i], lw=1.5, alpha=0.85)
    ax.set_title("Volatilidad móvil 30d (anualizada)")
    ax.set_ylabel("Volatilidad (%)")
    ax.legend(ncol=2, loc="upper right")

    plt.tight_layout()
    path = "output/dashboard.png"
    plt.savefig(path, dpi=DPI, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    print(f"[viz] Dashboard guardado en {path}")
    #plt.show()