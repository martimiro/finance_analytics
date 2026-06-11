# Base teorica
## *Los fundamentos matemáticos y teoría financiera detrás de cada métrica.*

### 1. Mercados financieros y comportamiento de los precios
#### 1.1 The *Efficient Market Hypotesis (EHM)*

La hipótesis del mercado eficiente (EHM, siglas en inglés) sostiene que los precios de los activos reflejan toda la información disponible en todo momento. Bajo esta hipótesis, superar consistentemente el rendimiento del mercado es imposible sin asumir un riesgo adicional.

- Forma débil: Los precios reflejan todos los datos históricos de precios. El análisi técnico no puede generar de forma consistente rentabilidades superiores.

- Forma semifuerte: Los precios reflejan toda la información pública disponible. El análisis fundamental no puede generar de forma consistente rentabilidades extraordinarias.

- Forma fuerte: Los precios reflejan toda la información, incluida la informaciónn privilegiada (*insider information*). Ningún tipo de análisi puede generar el alfa de forma consitente.

---
##### Aplicación práctica

La HME no significa que los mercados siempre tengan razón; significa que superar sistemáticamente al mercado requiere información superior, un análisi superior o la aceptación de un riesgo mayor.

---
##### Ejemplo práctico

Supongamos que una empresa anuncia beneficios mucho mejores de lo esperado.

Según la HME, los inversores reaccionarán rápidamente.
El precio de la acción subirá casi de inmediato.
Cuando tú leas la noticia unas horas después, probablemente el precio ya refleje esa información.

Por eso, la HME sostiene que no es fácil ganar dinero simplemente utilizando información pública que todos conocen.

---

#### 1.2 *Random Walk Theory*

*Random Walk Theory* o Teoría del Paseo Aleatorio en español dice que si los mercados son eficientes desde el punto de vista informativo, los cambios en los precios son impredecibles: el siguiente cambio de precio no contiene información proveniente de los precios pasados. El modelo de paseo aleatorio formaliza esta idea:

###### Paseo aleatorio
$$
P(t) = P(t-1) + \varepsilon(t)
$$

donde

$$
\varepsilon \sim \mathcal{N}(0, \sigma^2)
$$

Esto significa que el cambio de precio en cada período se extrae de forma independiente de una distribución normal con media cero y varianza σ<sup>2</sup>. En otras palabras, los precios pasados no contienen información útil sobre los precios futuros.

En la prática los rendimientos financieros presentan desviaciones bien documentadas respecto a este modelo:

- Colas gruesas (*fat tails*): ocurren eventos extremos con más frecuencia de la que predice una distribución normal.

- Agrupamiento de volatibilidad (*volatility clustering*): los grandes movimeientos de precios tienden a concentarse en determinados períodos.

- Ligera reversión a la media (*mean reversion*): a largo plazo, los precios muestran cierta tendencia a volver hacia valores promedio.

Estas son precisamente las características que los modelos cuantitativos intentan medir y explotar.

---

##### Interpretacion intuitiva

La teoría del paseo aleatorio afirma que:
- Si hoy una acción subió un 3%, eso no implica que mañana vaya a subir o bajar.

- Cada movimiento futuro incorpora nueva información impredecible.

- Intentar predecir el precio únicamente observando el historial de precios debería ser inútil.

Por ejemplo, si una moneda equilibrada ha salido cara cinco veces seguidas, la probabilidad de que salga cara la sexta vez sigue siendo del 50 %. La teoría del paseo aleatorio sostiene que los cambios de precios se comportan de manera similar.

---
#### Resumen en una sola frase
"Los precios reflejan toda la información disponible (HME). Por ello, los movimientos futuros de los precios son especialmente impredecibles (Random Walk)".

---

### 2. Teoría de los rendimientos (*Return Theory*)
#### 2.1 Rendimientos Simples vs. Rendimientos Logarítmicos

Existen dos formas estándard de medir los rendimientos de un activo, cada una con propiedades matemáticas distintas:

---

##### Rendimiento simple
$$
R_{simple} = \frac{P_t - P_{t-1}}{P_{t-1}}
$$

Represnta el cambio porcentual intuitivo del precio.

Es fácil de interpretar, pero **no es aditivo al tiempo**. Por ejemplo, una pérdida del 50% seguida de unas ganancias del 100% simplemente devuelve la inversión al punto de equilibrio, no produce una ganancia neta del 50%.

---

##### Rendimiento logarítmico
$$
R_{log} = \ln\left(\frac{P_t}{P_{t-1}}\right) = \ln(P_t) - \ln(P_{t-1})
$$

Representa el rendimiento con capitalización continua.

Los rendimientos logarítmicos **sí son aditivos al tiempo:** el rendimiento logarítmico de varios períodos es la suma de los rendimientos logarítmicos de cada período.

Además, suelen ser más simetricos y se aproximan mejor a una distribución normal, por lo que son preferidos en análisi estadístico y modelos cuantitativos.

---

##### ¿Cuándo usar cada uno?
- Rendimientos simples: para agregar activos dentro de una cartera (análisi transversal o *cross-sectional*).

- Rendimientos logarítmicos: para agregación temporal y modelizacion estadística.

Para rendimientos pequeños (aproximadamente inferiores al 5%), ambos son prácticamente iguales.

---

#### Resumen en una sola frase
El rendimiento simple mide el cambio porcentual directo del precio, mientras que el logarítmico mide el crecimiento continuo y es aditivo al tiempo, por lo que se usa más en el análisi estadístico.

---

#### 2.2 Rendimientos Multiperíodo y CAGR
##### Rendimiento acumulado
$$
R_{cum} = \prod (1 + R_t) - 1 = \frac{P_T}{P_0} - 1
$$

Mide la riqueza total generada durante todo el período de inversión.

Se calcula multiplicando los brutos $(1 + R_t)$ de cada período y restando 1.

Por ejemplo:
- $R_{cum} = 150$ equivale a una rentabilidad del 150%
- Significa que la inversión se duplicó y además ganó un 50% adicional.

---

#### CAGR *(Compound Annual Growth Rate)*
##### Tasa de Crecimiento Anual Compuesta
$$
\text{CAGR} = (1 + R_{cum})^{\frac{1}{T}} - 1
$$

donde

$$
T = \text{número de años}
$$

El CAGR convierte el rendimiento acumulado en una tasa anual equivalente, permitiendo comparar inversiones con diferentes horizontes temporales.

Es la **media geométrica** de los rendimientos anuales, no la media aritmética.

##### Ejemplo
Si una inversion pasa de 100€ a 200€ en 4 años

$$
R_{cum} = \frac{200}{100} - 1 = 1
$$

$$
\text{CAGR} = 2^{\frac{1}{4}} - 1
$$

$$
\text{CAGR} \approx 18.9\%
$$

Aunque la inversión ganó un 100% en total, su crecimiento equivalente fue del 18,9%.

---

#### Resumen en una sola frase
El **rendimiento acumulado** mide la rentabilidad total obtenida durante toda la inversión, mientras que el **CAGR** la convierte en una tasa anual equivalente para comparar inversiones de distinta duración, reflejando el crecimiento medio compuesto por año.

---

#### 2.3 Rendimientos de una Cartera

Para una cartera con $N$ activos y pesos $w_i$ (que deben sumar 1), el rendimiento diario de la cartera es la media ponderada de los rendimientos individuales.

##### Rendimiento de la Cartera
$$
R_p = \sum_{i=1}^{N} w_i R_i
$$

donde:

- $w_i$ = peso del activo $i$ en la cartera
- $R_i$ = rendimiento del activo $i$

El rendimiento de la cartera es el **producto escalar** entre el vector de pesos y el vector de rendimientos.

##### Ejemplo
Supón una cartera:
- 60% en Acción A
- 40% en Acción B

Si:
- Acción A gana 5%
- Acción B gana 2%

Entonces:

$$
R_p = (0.6)(0.05) + (0.4)(0.02)
$$

$$
R_p = 0.038
$$

$$
R_p = 3.8\%
$$

La cartera obtuvo una rentabilidad del **3.8%** durante ese período.

---

#### Resumen en una sola frase

El rendimiento de una cartera es la media ponderada de los rendimientos de sus activos, calculando como la suma de rendimiento multiplicado por su peso, lo que equivale a un producto escalar entre pesos y rendimientos.

---

### 3. Teoria del Riesgo
#### 3.1 Volatilidad - Riesgo Total
La volatilidad ($\sigma$) mide la dispersión de los rendimientos alrededor de su media. Se define como la **desviación estándard** de la serie de rendimientos y se anualiza multiplicando por la raíz cuadrada del número de días de negociación:

##### Volatilidad Anualizada

$$
\sigma_{anual} = \sigma_{diaria} \times \sqrt{252}
$$

La volatilidad anual se obtiene a partir de los datos diarios utilizando:

$$
\sqrt{252}
$$

porque se considera que hay aproximadamente **252 días bursátiles al año**.

Esto se deriva de la propiedad aditiva de la varianza:

$$
Var(\text{T días}) = T \times Var(\text{1 día})
$$

cuando los rendiminetos diarios son independientes.

---

##### ALERTA! Limitación de la volatilidad como media de riesgo

La volatilidad trata de forma simétrica los movimientos positivos y negativos.

Sin embargo, los inversores sulen preocuparse por las pérdidas.

Por ejemplo:
- Una acción que experimenta frecuentes subidas muy fuertes tendrá una volatilidad elevada.
- Aun así, podría no ser especialmente arriesgada desde un punto de vista económico.

Esta limitación motivó el desarrollo de medidas de riesgo asimétricas, como el **ratio de Sortino**, que penaliza únicamente la volatildad negativa.

---

#### 3.2 Teoría Moderna de Carteras (MPT)
La **Teoría Modenra de Carteras (*Modern Portfolio Theoty, MPT*)** fue desarrollada por Markowitz en 1952.

Su principal aportación fue formalizar matemáticamente el concepto de **diversificación**.

La idea clave es que el riesgo de una cartera no depende únicamente de la volatilidad individual de cada activo, sino también de las **correlaciones entre ellos**.

---

##### Varianza de una Cartera (2 activos)
$$
\sigma_{p}^{2} = w_{1}^{2}\sigma_{1}^{2} + w_{2}^{2}\sigma_{2}^{2} + 2w_{1}w_{2}\rho_{12}\sigma_{1}\sigma_{2}
$$

donde:
- $w_{1}, w_{2}$: pesos de cada activo.
- $\sigma_{1}, \sigma_{2}$: volatilidades individuales.
- $\rho_{12}$: correlación entre ambos activos.

Cuando:
$$
\rho_{12} < 1
$$

(es decir, los activos no estan perfectamente correlacionados),

la varianza de la cartera es menor que la suma ponderada de las varianzas individuales.

Esta es la demostración matemática del benedicio de la diversificación.

---

##### Frontera eficiente (*Efficient Frontier*)
La **frontera eficiente** es el conjunto de cartera que ofrecen:
- El máximo rendimiento esperado para un nivel determinado de riesgo.
- O, equivalentemente, el mínimo riesgo para un rendimiento esperado dado.

Según la MPT, un inversor racional y adverso al riesgo debería mantener únicamente carteras situadas sobre esta frotnera.

---

#### Cartera Tangente
La **cartera tangente** es el punto desde la **Línea del Mercado de Capitales (*Capital Market Line, CML*)** es tangente a la frontera eficiente.

Esta cartera es especialmente importante porque:
- Tiene el mayor **ratio de Sharpe** posible.
- Representa la mejor combinación riesgo-rentabilidad dentro de los activos de riesgos disponibles.

En términos prácticos, la cartera tangente es la que maximiza:
$$
\text{Sharpe Ratio} = \frac{R_{p} - R_{f}}{\sigma_{p}}
$$

donde:
- $R_{p}$: rendimiento esperado de la cartera.
- $R_{f}$: tasa libre de riesgo.
- $\sigma_{p}$: volatilidad de la cartera.

Por ello, en teoría, todos los inversores deberían combinar el activo libre de riesgo con la cartera tangente sgún la tolerancia al riesgo.

##### Interpretación práctica del Ratio de Sharpe
El **ratio de Sharpe** mide el rendimiento excedente obtenido por cada unidad de riesgo total asumido.

- $R_{f}$ es la tasa libre de riesgo (por ejemplo, el rendimiento de las letras del Tesoro estadounidense a 3 meses).
- Como referencia general:
  - **Sharpe > 1.0**: aceptable.
  - **Sharpe > 2.0**: muy bueno.
  - **Sharpe > 3.0**: excepcional.

##### Interpretación práctica
Un Sharpe de **1,5** significa que la cartera genera **1,5 unidades de rendimiento excedente anualizado por cada unidad de riesgo anualizado asumido**.

Comparar ratios de Sharpe elimina el efecto del apalancamiento: las estrategias más arriesgadas suelen producir mayores rendimientos absolutos, pero no necesariamente mejores de Sharpe.

---

#### 3.4 Ratio de Sortino - Riesgo a la Baja
El **ratio de Sortino** aborda la principal crítica del ratio de Sharpe:

> El ratio de Sharpe penaliza por igual la volatilidad positiva y negativa.

El ratio de Sortino solo considera la desviación estándar de los rendimientos negativos (riesgo a la baja).

##### Fórmula del Ratio de Sortino
$$
Sortino = \frac{R_{p} - R_{f}}{\sigma_{downside}} 
$$

donde:
- $R_{p}$: rendimiento de la cartera.
- $R_{f}$: tasa libre de riesgo.
- $\sigma_{downside}$: desviación estándard calculada únicamente sobre los períodos con rendimientos negativos $(R_{t} < 0)$, posteriormento anualizada $\sqrt{252}$

##### ¿Cuándo se prefiere?
Se suele preferir al ratio de Sharpe cuando:
- La distribuición de rendimientos es asimétrica.
- Existen ganancias extremas que aumentan la volatilidad total.
- La estrategia presenta sesgo positivo (*postive skweness*).

---

#### 3.5 Máximo Drawdown (*Maximum Drawndown*)
El drawndown mide la caída desde un máximo histórico hasta el mínimo posterior de la cartera.

El ***Maximum Drawdown (MDD)*** representa la peor caída sufrida durante todo el período analizado.

##### Fórmula del Maximum Drawdown
$$
\text{MDD} = \max_{t} \left( 1 - \frac{W(t)}{\max_{s \le t} W(s)} \right)
$$

donde:
- $W(t)$: valor de la cartera en el instante $t$
- $max_{s \leq t} W(s)$: máximo valor alcanzado por la cartera hasta ese momento.

La fórmula compara continuadamente el valor actual con el máximo histórico acumulado.

##### Interpretación
El MDD siempre cumple:
$$
MDD \leq 0
$$

Por ejemplo:
$$
MDD = -0.35
$$

significa que la cartera llegó a perder un **35%** respecto a su máximo anterior en algún momento del período.

---

#### Ratio de Calmar
El **ratio de Calmar** relaciona la rentabilidad anualizada con la peor pérdida histórica registrada.

##### Fórmula
$$
Calmar = \frac{CAGR}{|MDD|}
$$

donde:
- **CAGR**: tasa de crecimiento anual compuesta.
- **MDD**: máximo drawdown en valor absoluto.

##### Interpretación
Un valor más alto es mejor porque indica que la estrategia genera más rentabilidad por cada unidad de pérdida máxima soportada.

El ratio del Calmar:
- Fondos de cobertura (*hedge funds*).
- CTAs (*Commodity Trading Advisors*).
- Gestores cuantitativos.

Resulta especialmente útil para comparar estrategias con perfiles de riesgo muy diferentes y horizontes temporales muy distintos.

#### 3.6 Beta y CAPM
La **beta ($\beta$)** mide la sensibilidad de una cartera o activo frente a los movimientos generales del mercado.

Se deriva del modelo **CAPM (*Capital Asset Pricing Model*)**, que descompone el rendimiento total en:

- **Riesgo sistemático** (riesgo de mercado)
- **Riesgo idiosincrático** (riesgo específico de la empresa o activo).

---

##### Beta
$$
\beta = \frac{Cov(R_{p}, R_{m})}{Var(R_{m})}
$$

donde:
- $R_{p}$: rendimiento de la cartera o activo.
- $R_{m}$: rendimiento del mercado (*benchamark*).
- $Cov(R_{p}, R_{m})$: covarianza entre la cartera y el mercado.
- $Var(R_{m})$: varianza del mercado.

##### Interpretación
- $\beta = 1 \rightarrow$ la cartera se mueve igual que el mercado.
- $\beta > 1 \rightarrow$ amplifica los movimientos del mercado (más agresiva).
- $\beta < 1 \rightarrow$ amortigua los movimientos del mercado (más defensiva).
- $\beta < 0 \rightarrow$ tiende a moverse en dirección opuesta al mercado (cobertura o *hedge*).

##### Ejemplos
Si el mercado sube un 10%:
- $\beta = 1.5 \rightarrow$ se espera que el activo suba aproximadamente un 15%
- $\beta = 0.5 \rightarrow$ se espera que suba aproximadamente un 5%.
- $\beta = -0.5 \rightarrow$ se espera que caiga aproximadamente un 5%.

---

#### Rendimiento Esperado según CAPM
##### Fórmula
$$
E[R_{p}] = R_{f} + \beta(E[R_{m}] - R_{f})
$$

donde:
- $E[R_{p}]$: rendimiento esperado del activo o cartera.
- $R_{f}$: tasa libre de riesgo.
- $E[R_{m}]$: rendimiento esperado del mercado.
- $E[R_{m}] - R_{f}$: prima de riesgo del mercado.

##### Idea principal del CAPM
El CAPM sostiene que:

> Solo el riesgo sistemático (el riesgo de mercado) debe ser compensado con una mayor rentabilidad esperada.

El riesgo específico de cada empresa puede eliminarse mediante diversificación y, por tanto, no debería generar una prima de rentabilidad adicional.

---

##### Ejemplo
Supongamos:
- Tasa libre de riesgo = 3%.
- Rendimiento esperado del mercado = 9%.
- Beta = 1,2.

Entonces:
$$
E[R_{p}] = 3\% + 1.2(9\% - 3\%)
$$

$$
E[R_{p}] = 10.2\%
$$

Según el CAPM, una inversión con $\beta =$ 1,2 debería ofrecer aproximadamente un **10,2% anual** para compensar su riesgo de mercado.

---

#### 3.7 *Value at Risk (VaR) y Conditional Value at Risk (CVaR)*
Estas métricas intentan responder a la pregunta:
> ¿Cuánto puedo perder en un mal día?

---

##### VaR Histórico (95%)
##### Fórmula
$$
VaR_{95\%} = -2\%
$$

El VaR representa un umbral de pérdida que no debería superarse con una determinada confianza.

##### Interpretación
Si:
$$
VaR_{95\%} = -2\%
$$

significa que:
- En el 95% de los días, la pérdida no superará al 2%.
- En el 5% restante de los días, la pérdida podría ser pero que el 2%.

##### Ejemplo
Supón que analizas 100 días de rendimientos:
- En 95 días las pérdidas son menores al 2%.
- En 5 días las pérdidas superan el 2%.

Entonces:
$$
VaR_{95\%} = -2\%
$$

---

#### CVaR (*Conditional Value at Risk*)
También conocida como:
- ***Expected Downfall***
- **Pérdida Esperada Condicional**

##### Fórmula
$$
CVaR_{95\%} = E[R | R \leq VaR_{95\%}]
$$

Es la perdida promedio de los peores casos.

Mientras que el VaR te dice:
> "¿Dónde empieza la zona de pérdidas extremas?"

el CVaR responde:
> "¿Cuál es la perdida media una vez que ya estás dentro de esa zona extrema?"

---

##### Ejemplo
Supón que:
$$
VaR_{95\%} = -2\%
$$

y que los peores 5 días tuvieron pérdidas:
- -2,1%
- -2,4%
- -3,0%
- -4,0%
- -6,5%

Entonces:
$$
CVaR_{95\%} = \frac{-2.1-2.4-3.0-4.0-6.5}{5} = -3.6\%
$$

Interpetación:
- VaR 95% = -2% $\rightarrow$ el umbral de riesgo.
- CVaR 95% = -3.6% $\rightarrow$ la pérdida promedio cuando las cosas realmente salen mal.

---

##### ¿Por qué muchos gestores prefieren el CVaR?
El VaR tiene una limitación importante:
- No informa sobre la magnitud de las pérdidas extremas una vez superado el umbral.

El CVaR sí captura esa información y, además, es una medida matemáticamente más consistente (*coherent risk measure*).

---

### 4. Teoría de Predicción de Precios
#### 4.1 Medias móviles - Suavizado de Tendencias
Las **medias móviles** (*Moving Averages*) eliminan el ruido de corto plazo de una serie de precios para revelar la tendencia subyacente.

Constituyen una de las herramientas fundamentales del análisi técnico y son ampliamente utilizadas en sistemas de trading.

##### Media Móvil Simple (*SMA*)
$$
{SMA}(n,t) = \frac{1}{n}\sum_{i=0}^{n-1} P_{t-i}
$$

La *SMA* assigna el mismo peso a todas las observaciones dentro de la ventana temporal.

##### Características
- Cada dato tiene la misma importancia
- Introduce un retraso (*lag*) respecto al precio actual de aproximadamente $n/2$ períodos.
- Ventanas comunes:
  - **20 días**: tendencia a corto plazo.
  - **50 días**: tendencia a medio plazo.
  - **200 días**: tendencia a largo plazo.

---

##### *Golden Cross* y *Death Cross*
##### *Golden Cross*
Ocurre cuando la media móvil de 50 períodos cruza por encima de la media móvil de 200 períodos.

Tradicionalmente se interpreta como una señal de:
- Tendencia alcista.
- Incremento del momentum positivo.

##### *Death Cross*
Ocurre cuando la media móvil de 50 períodos cruza por debajo de la media móvil de 200 períodos.

Tradicionalmente se interpreta como una señal de:
- Tendencia bajista.
- Debilitamiento del mercado.

##### Nota importante
Según la Hipotesis del Mercado Eficiente (HME), la evidencia académica sobre la rentabilidad consistente de estas señales es mixta y debatida.

---

#### 4.2 Regresión Lineal - Extrapolación de tendencias
La regresión lineal por **Mínimos Cuadrados Ordinarios (*OLS*)** ajusta una línea recta a los datos históricos minimizando la suma de los errores cuadrados entre los valores observados y estimados.

##### Regresión *OLS* sobre precios logarítmicos
$$
\ln(P_{t}) = \alpha + \beta t +  \epsilon_{t}
$$

donde:
- $\alpha = $ intercepto.
- $\beta = $ pendiente de la tendencia.
- $\epsilon_{t} = $ término de error aleatorio.

La estimación se realiza minimizando:
$$
\sum \epsilon_{t}^{2}
$$

---

##### ¿Por qué  usar logaritmos?
Utilizar precios logarítmicos en lugar de precios brutos permite modelar correctamente el crecimiento compuesto.

En estas formulación:
- $\alpha$ representa el algoritmo del precio incial.
- $\beta$ represetna la tasa diaria de crecimiento logarítmico (rendimiento compuesto continuo de la tendencia).

---

##### Coeficiente de Determinación ($R²$)
El estadístico:
$$
R^{2}
$$

mide qué tan bien la tendencia lineal explica los datos observados.

Interpretación:
- $R² = 1 \rightarrow$ ajuste perfecto.
- $R² = 0 \rightarrow$ la tendencia no explica nada de la variación observada.
- Cuando mayor sea $R^{2}$, más fuerte y consistente es la tendencia.

---

#### ARIMA - Modelado de Series Temporales
El modelo **ARIMA(p,d,q)** es el modelo clássico de referencia para la predicción de series temporales univariantes.

Combina tres componentes:

| Parámetro | Componente | Significado | Interpretación financiera |
| --------- | ---------- | ----------- | ------------------------- |
| p | AR (Autoregresivo) | Utiliza los últimos *p* valores de la serie | Momentum del precio: el valor de hoy depende de los últimos *p* días |
| d | Integrado (diferenciación) | Se aplica *d* veces para lograr estacionariedad | d = 1 convierte precios en rendimientos (elimina la tendencia) |
| q | MA (Media Móvil) | Utiliza los últimos *q* errores de predicción | Reversión a la media basada en errores recientes de predicción |

---

##### ARIMA(p,d,q) - Forma en diferencias
$$
dY_t = c + \sum_{i=1}^{p} \phi_i \, dY_{t-i}+ \sum_{j=1}^{q} \theta_j \, e_{t-j} + e_t
$$

donde:
- $dY_t = Y_t - Y_{t-i}$ es la serie diferenciada.
- $\phi_i$ son los coeficientes autorregresivos (AR).
- $\theta_j$ son los coeficientes de media móvil (MA).
- $e_t$ representa ruido blanco (*white noise*).

Para precios de acciones, una especifiación inicial común suele ser:
$$
ARIMA(2,1,2)
$$

---

##### Requisito de estacionariedad
ARIMA requiere que la serie sea **estacionaria**, es decir:
- Media constante en el tiempo.
- Varianza constante en el tiempo.

Los precios bursátiles normalmente **no son estacionarios** porque suelen representar tendencias de largo plazo.

Los rendimientos logarítmicos, en cambio, son aproximadamente estacionarios.

Por ello, establecer:
$$
d = 1
$$

diferencia la serie de una vez, transformando los precios en rendimientos y eliminando la tendencia.

#### 4.4 Selección de Modelos - AIC y BIC
Al construir modelos ARIMA es necesario decidir cuántos parámetros incluir.

Para ello se utilizan criterios de información que equilibran:
- Calidad del ajuste.
- Complejidad del modelo.

---

##### Criterio de Información de Akaike (AIC)
$$
AIC = 2k - 2\ln(L)
$$

donde:
- $k =$ número de parámetros.
- $L =$ verosimilitud (*likehood*) del modelo.

El AIC busca un equilibrio entre:
- Un buen ajuste a los datos.
- Evitar modelos innecesariamente complejos.

##### Interpretación
- Cuando menor sea el AIC, mejor.
- Penaliza los modelos con demasiados parámetros.
- Se utiliza habitualmente para comparar distintas configuraciones ARIMA.

---

##### Criterio de Información Bayestiano (BIC)
$$
BIC = k\ln(n) - 2\ln(L)
$$

donde:
- $n =$ número de observaciones.
- $k =$ número de parámetros.
- $L =$ verosimilitud.

El BIC aplica una penalización más fuerte que el AIC a los modelos complejos.

---

#### Resumen intuitivo
El modelo ARIMA intenta responder:
> "¿Puedo predecir el proximo valor de una serie usando sus valores pasados y los errores cometidos anteriormente?"

Mientras que el AIC y BIC responden:
> "¿Qué tan complejo debe ser el modelo para capturar la información útil sin sobreajustar los datos?"

---