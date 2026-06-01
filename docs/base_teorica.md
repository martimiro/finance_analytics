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