# TRABAJO PRÁCTICO: ANÁLISIS INTEGRAL DE INVERSIONES

**Universidad Tecnológica Nacional - Facultad Regional La Plata**  
**Materia:** Finanzas para Control Empresario  
**Carrera:** Ingeniería Industrial  
**Año:** 2025  

---

## OBJETIVOS

Al finalizar este trabajo práctico, el estudiante será capaz de:

1. **Aplicar la Teoría Moderna de Portfolios** para optimizar carteras de inversión
2. **Implementar análisis técnico** para timing de mercado
3. **Realizar análisis fundamental** para valuación de empresas
4. **Integrar múltiples enfoques** para tomar decisiones de inversión fundamentadas
5. **Desarrollar criterio propio** basado en análisis cuantitativo y cualitativo

---

## EMPRESAS ASIGNADAS

| Empresa | Alumno | Ticker | Sector |
|---------|--------|--------|--------|
| BYMA | Shortreder | BYMA.BA | Servicios Financieros |
| MercadoLibre | Malacalza | MELI | E-commerce/Fintech |
| Ternium | Griffo | TX | Siderúrgico |
| Coca Cola | Moya | KO | Bebidas |
| Apple | Villaverde | AAPL | Tecnología |
| YPF | Serrano | YPF.BA | Energía |
| Loma Negra | Sack | LOMA.BA | Materiales |

---

## PARTE I: ANÁLISIS DE CARTERA DE ACCIONES (40 puntos)

### **Consigna General**
Construir y analizar una cartera de 5 acciones que incluya tu empresa asignada más 4 empresas comparables del mismo sector o mercado relevante.

### **Tareas Específicas**

#### **1. Construcción del Dataset (8 puntos)**
- Obtener datos históricos diarios de los últimos 5 años
- **Justificar la selección** de las 4 empresas comparables basándose en:
  - Sector económico
  - Capitalización de mercado similar
  - Mercado de cotización relevante
- Documentar fuentes de datos y metodología de limpieza
- Incluir índice de referencia (MERVAL, S&P500, etc.)

**Pregunta Crítica:** *¿Qué criterios utilizaste para seleccionar empresas comparables y por qué estos criterios son relevantes para un inversor argentino?*

#### **2. Análisis Descriptivo Avanzado (10 puntos)**
- Gráficos de precios normalizados (base 100)
- **Identificar y explicar 3 eventos** (macroeconómicos/corporativos) que impactaron significativamente en los precios
- Análisis de estacionalidad por trimestres
- Cálculo de métricas de riesgo:
  - VaR 95%
  - CVaR (Expected Shortfall)
  - Drawdown máximo
- **Test de normalidad** (Jarque-Bera) y análisis de colas

**Pregunta Crítica:** *¿Los retornos de las acciones argentinas siguen patrones diferentes a las internacionales? ¿Qué implicancias tiene esto para la gestión de riesgo?*

#### **3. Análisis de Correlaciones (8 puntos)**
- Matriz de correlaciones con visualización
- **Análisis temporal:** Correlaciones en períodos de crisis vs. normales
- **Efecto contagio:** ¿Aumentan las correlaciones en crisis?
- Implicancias para diversificación

**Pregunta Crítica:** *¿Por qué ciertas acciones están más correlacionadas que otras y cómo afecta esto tu estrategia de diversificación?*

#### **4. Optimización de Portfolio (14 puntos)**
- Simulación de 2000+ portfolios aleatorios
- **Restricciones realistas:**
  - Máximo 40% en un solo activo
  - Mínimo 5% en cada activo seleccionado
  - Costos de transacción 0.5%
- Cálculo de portfolios específicos:
  - Máximo Sharpe Ratio
  - Mínimo riesgo
  - **Tu elección personal**
- Frontera eficiente graficada

**Pregunta Crítica:** *Justificar tu elección de portfolio considerando tu perfil de riesgo personal, horizonte de inversión y expectativas macroeconómicas. ¿Por qué elegiste ese punto específico de la frontera eficiente?*

---

## PARTE II: ANÁLISIS TÉCNICO (25 puntos)

### **Consigna General**
Realizar análisis técnico completo de tu empresa asignada desarrollando una estrategia de trading fundamentada.

### **Tareas Específicas**

#### **1. Análisis de Tendencias (6 puntos)**
- Medias móviles simples: 50 y 200 períodos
- Identificar cruces Golden Cross y Death Cross
- **Backtesting:** Rentabilidad de estrategia de cruces vs. buy & hold

#### **2. Indicadores de Momentum (8 puntos)**
- **MACD:** Cálculo y análisis de divergencias
- **RSI:** Identificar niveles de sobrecompra/sobreventa
- **ADX:** Determinar fortaleza de tendencia
- **Optimización:** Encontrar parámetros óptimos para tu activo específico

#### **3. Análisis de Volatilidad (6 puntos)**
- **Bandas de Bollinger:** Análisis de compresión/expansión
- Calcular % de tiempo fuera de bandas
- Identificar señales de compra/venta

#### **4. Estrategia Integral y Backtesting (5 puntos)**
- **Combinar todos los indicadores** en una estrategia coherente
- Backtesting con métricas:
  - Sharpe Ratio
  - Calmar Ratio
  - Win Rate
  - Drawdown máximo

**Pregunta Crítica:** *¿Por qué el análisis técnico podría ser más o menos efectivo en el mercado argentino comparado con mercados desarrollados? Considerar liquidez, volatilidad e información disponible.*

---

## PARTE III: ANÁLISIS FUNDAMENTAL (35 puntos)

### **Consigna General**
Realizar análisis fundamental completo comparando tu empresa con el sector y desarrollando una recomendación de inversión.

### **Tareas Específicas**

#### **1. Dashboard Sectorial (15 puntos)**
Crear tabla comparativa con todas las empresas del sector incluyendo:

**Ratios de Valuación:**
- Enterprise Value/EBITDA
- Enterprise Value/Revenue
- Forward P/E y Trailing P/E
- PEG Ratio
- Price/Book
- Price/Sales

**Ratios de Rentabilidad:**
- Operating Margin
- Profit Margin
- Return on Assets (ROA)
- Return on Equity (ROE)

**Ratios de Solvencia:**
- Total Debt/Equity
- Interest Coverage

**Ratios de Mercado:**
- Market Cap
- 52 Week High/Low
- 52-Week Change
- Beta

#### **2. Análisis de Calidad y Riesgo (10 puntos)**
- **Análisis FODA** de tu empresa asignada
- **Ventajas competitivas** sostenibles (moat económico)
- **Riesgos específicos:**
  - Regulatorios
  - Cambiarios (para empresas argentinas)
  - Operativos
  - De mercado

**Pregunta Crítica:** *¿Cómo impacta el contexto macroeconómico argentino actual en la valuación de tu empresa comparada con competidores internacionales?*

#### **3. Valuación y Decisión de Inversión (10 puntos)**
- **DCF simplificado** para tu empresa principal
- **Análisis de sensibilidad:** Impacto de cambios en WACC
- **Target Price** y fundamentación
- **Recomendación final:** Comprar/Mantener/Vender

**Pregunta Crítica:** *Considerando tu análisis de cartera, técnico y fundamental, ¿cuál sería tu estrategia completa de inversión? ¿Contra qué benchmark compararías el performance y por qué?*

---

## ENTREGABLES Y FORMATO

### **Estructura de Entrega**

1. **Repositorio GitHub** con estructura definida
2. **Notebooks Jupyter** documentados por sección
3. **Informe ejecutivo** (máximo 10 páginas) con:
   - Resumen ejecutivo
   - Metodología utilizada
   - Principales hallazgos
   - Recomendación de inversión
   - Anexos con gráficos y tablas

### **Criterios de Evaluación**

| Aspecto | Peso | Descripción |
|---------|------|-------------|
| **Metodología** | 25% | Rigurosidad en análisis y justificación de decisiones |
| **Análisis Crítico** | 30% | Capacidad de interpretación y síntesis |
| **Implementación Técnica** | 25% | Calidad del código y visualizaciones |
| **Presentación** | 20% | Claridad en comunicación de resultados |

### **Fechas Importantes**

- **Entrega:** [Fecha a definir]
- **Presentación oral:** [Fecha a definir]
- **Consultas:** Horarios de consulta + Issues en GitHub

---

## CONSIDERACIONES ESPECIALES

### **Contexto Argentino**
- Considerar impacto de inflación en valuaciones
- Analizar riesgo país y tipo de cambio
- Comparar ADRs vs. acciones locales cuando aplique

### **Originalidad**
- **Se requiere análisis propio y fundamentado**
- **Las respuestas automáticas generadas por IA serán penalizadas**
- **Valoraremos el criterio personal y la capacidad de síntesis**

### **Recursos Disponibles**
- Material teórico en repositorio GitHub
- Código base proporcionado
- Horarios de consulta presencial y virtual
- Issues de GitHub para consultas específicas

---

## PREGUNTAS ORIENTADORAS FINALES

1. **¿Tu estrategia sería diferente si fueras un inversor institucional vs. retail?**

2. **¿Cómo adaptarías tu análisis considerando un horizonte de inversión de 10 años vs. 1 año?**

3. **¿Qué papel juega la inflación argentina en tus decisiones de portfolio?**

4. **¿Por qué un inversor extranjero invertiría en tu empresa recomendada?**

5. **¿Cuáles son los 3 riesgos principales que podrían invalidar tu análisis?**

---

*"La meta del análisis financiero no es predecir el futuro, sino entender el presente lo suficientemente bien como para tomar decisiones racionales bajo incertidumbre."*

**¡Éxitos en el desarrollo del trabajo práctico!**