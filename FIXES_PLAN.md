# Plan de Correcciones - Finance Analytics

## 1. Errores de Escala y Datos (Críticos)

### 1.1 VaR Monte Carlo mal escalado
**Archivo:** `src/optimization.py` (line 177)
**Problema:** VaR de -1.6% para 252 días es matemáticamente inconsistente con vol 21%
**Solución:** El código calcula correctamente, pero la PRESENTACIÓN es confusa. 
- El VaR actual ya está en términos de retorno acumulado a 252 días (línea 177: `np.percentile(final, ...)`)
- Es correcto, pero debe aclararse que es VaR del retorno acumulado, no diario

### 1.2 Datos sectoriales erróneos  
**Archivo:** `src/market_trends.py` + `config.py`
**Problema:** Energía 35%, Tecnología 12% - parece invertido
**Causa:** El ticker XLK es "Utilities" pero config lo etiqueta como "Tecnología"
**Solución:** Corregir mapping en config.py - XLK debe ser "Energía" y XLE es "Utilities" (está invertido)

### 1.3 Inconsistencia de métricas en frontera eficiente
**Archivo:** `src/optimization.py` (lines 136-137)
**Problema:** Header muestra "42.0% | 22.6%" pero reporta "34.19% | 21.66%"
**Causa:** La frontera muestra el portfolio ÓPTIMO teórico, no el actual
**Solución:** Añadir etiqueta clarificadora "(Óptimo teórico)" en el título

---

## 2. Errores de Modelado Financiero

### 2.1 ARIMA predicción plana
**Archivo:** `src/forecasting.py` (lines 104-136)
**Problema:** ARIMA converge a media - random walk sobre log-precios
**Raíz:** El modelo ARIMA(2,1,2) sobre log-precios tiende a este comportamiento con datos estacionarios
**Solución:** 
- Cambiar a ARIMA(1,1,1) para simplificar
- Usar diferenciación de log-retornos en lugar de log-precios directamente

### 2.2 Regresión lineal viola estacionariedad
**Archivo:** `src/forecasting.py` (lines 51-87)
**Problema:** R² = 0.773 es falso positivo por cointegración
**Solución:** Cambiar a regresión sobre LOG-RETORNOS (ya hace cov/log pero predice mal)
- Usar la pendiente como factor de drift
- Aplicar bootstrapping de residuos para predicción más realista

### 2.3 Efecto arrastre en detección de régimen
**Archivo:** `src/market_trends.py` (line 121)
**Problema:** Window=21 es muy largo, arrastra volatilidad de caídas pasadas
**Solución:** Cambiar window a 10 días para respuesta más rápida

---

## 3. Errores Estéticos y de Consistencia Visual

### 3.1 Eje Y cortado en rolling_beta.png
**Archivo:** `src/market_trends.py` (line 102)
**Problema:** ylim auto genera límite inferior en 1.0, línea roja queda pisada
**Solución:** Establecer `ax.set_ylim([0.9, ylim_max])` para dejar espacio

### 3.2 MA 200 incompleta
**Archivo:** `src/forecasting.py` (lines 25-35 + data_loader.py)
**Problema:** MA empieza a graficarse a mitad del gráfico
**Causa:** No hay suficientes datos históricos previos a START_DATE
**Solución:** 
- Modificar data_loader para cargar 200 días ANTES de START_DATE
- O usar `min_periods` en rolling() para graficar desde primer día

### 3.3 Spanglish en sectors.png
**Archivo:** `config.py` (SECTORS dict) + `src/market_trends.py`
**Problema:** Mix de español/inglés en etiquetas (Finanzas + Utilities)
**Solución:** Normalizar a ESPAÑOL en config.py

---

## Orden de Implementación

1. **Config.py** - Corregir SECTORS mapping y normalizarlo a español
2. **market_trends.py** - Fijar eje Y, corregir window de régimen, actualizar etiquetas
3. **optimization.py** - Añadir etiqueta clarificadora, revisar VaR (está bien)
4. **forecasting.py** - Mejorar ARIMA, cambiar regresión, cargar más datos históricos
5. **visualization.py** - Ajustar rangos de ejes si es necesario
6. **data_loader.py** - Modificar para pre-cargar 200 días previos

