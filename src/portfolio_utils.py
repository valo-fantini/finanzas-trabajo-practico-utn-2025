"""
Módulo de Análisis de Portfolios
Trabajo Práctico - Análisis Integral de Inversiones

Implementa la Teoría Moderna de Portfolios de Markowitz

Funciones principales:
- calcular_metricas_riesgo(): VaR, CVaR, drawdown, etc.
- simular_portfolios(): Simulación Monte Carlo
- optimizar_portfolio(): Optimización con restricciones
- graficar_frontera_eficiente(): Visualización de resultados
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def calcular_metricas_riesgo(retornos, confianza=0.05, ventana_vol=252):
    """
    Calcula métricas de riesgo avanzadas para cada activo
    
    TAREA CRÍTICA: Los estudiantes deben interpretar resultados en contexto argentino
    
    Parámetros:
    -----------
    retornos : pandas.DataFrame
        Retornos diarios de los activos
    confianza : float, opcional
        Nivel de confianza para VaR (default: 0.05 = 95%)
    ventana_vol : int, opcional
        Ventana para anualizar volatilidad (default: 252 días)
    
    Retorna:
    --------
    pandas.DataFrame : Métricas de riesgo por activo
    """
    
    print(f"📊 Calculando métricas de riesgo (confianza: {(1-confianza)*100}%)...")
    
    metricas = {}
    
    for activo in retornos.columns:
        ret_activo = retornos[activo].dropna()
        
        if len(ret_activo) == 0:
            print(f"⚠️  No hay datos para {activo}")
            continue
        
        # 1. Estadísticas básicas
        media_diaria = ret_activo.mean()
        std_diaria = ret_activo.std()
        
        # 2. Métricas anualizadas
        retorno_anual = media_diaria * ventana_vol
        volatilidad_anual = std_diaria * np.sqrt(ventana_vol)
        
        # 3. Value at Risk (VaR)
        var_parametrico = stats.norm.ppf(confianza, media_diaria, std_diaria)
        var_historico = np.percentile(ret_activo, confianza * 100)
        
        # 4. Conditional Value at Risk (Expected Shortfall)
        cvar_historico = ret_activo[ret_activo <= var_historico].mean()
        
        # 5. Drawdown máximo
        precio_cum = (1 + ret_activo).cumprod()
        rolling_max = precio_cum.expanding().max()
        drawdown = (precio_cum - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        # 6. Ratio de Sharpe (asumiendo rf=0)
        sharpe_ratio = retorno_anual / volatilidad_anual if volatilidad_anual > 0 else 0
        
        # 7. Sesgo y curtosis
        sesgo = stats.skew(ret_activo)
        curtosis = stats.kurtosis(ret_activo)
        
        # 8. Test de normalidad (Jarque-Bera)
        try:
            jb_stat, jb_pvalue = stats.jarque_bera(ret_activo)
            es_normal = jb_pvalue > 0.05
        except:
            jb_stat, jb_pvalue, es_normal = np.nan, np.nan, False
        
        metricas[activo] = {
            'Retorno_Anual': retorno_anual,
            'Volatilidad_Anual': volatilidad_anual,
            'Sharpe_Ratio': sharpe_ratio,
            'VaR_95_Parametrico': var_parametrico,
            'VaR_95_Historico': var_historico,
            'CVaR_95': cvar_historico,
            'Max_Drawdown': max_drawdown,
            'Sesgo': sesgo,
            'Curtosis': curtosis,
            'JB_Stat': jb_stat,
            'JB_PValue': jb_pvalue,
            'Es_Normal': es_normal
        }
    
    df_metricas = pd.DataFrame(metricas).T
    
    print(f"✅ Métricas calculadas para {len(df_metricas)} activos")
    print(f"📈 Retorno anual promedio: {df_metricas['Retorno_Anual'].mean():.2%}")
    print(f"📊 Volatilidad anual promedio: {df_metricas['Volatilidad_Anual'].mean():.2%}")
    
    return df_metricas

def calcular_matriz_correlacion(retornos, metodo='pearson', ventana_movil=None):
    """
    Calcula matriz de correlaciones con análisis temporal
    
    Parámetros:
    -----------
    retornos : pandas.DataFrame
        Retornos de los activos
    metodo : str, opcional
        Método de correlación: 'pearson', 'spearman', 'kendall'
    ventana_movil : int, opcional
        Si se especifica, calcula correlaciones móviles
    
    Retorna:
    --------
    pandas.DataFrame : Matriz de correlaciones
    """
    
    print(f"🔗 Calculando matriz de correlaciones ({metodo})...")
    
    if ventana_movil:
        # Correlaciones móviles
        correlaciones = retornos.rolling(ventana_movil).corr()
        print(f"📊 Correlaciones móviles con ventana de {ventana_movil} días")
        return correlaciones
    else:
        # Correlación estática
        correlaciones = retornos.corr(method=metodo)
        
        # Estadísticas de correlación
        corr_values = correlaciones.values[np.triu_indices_from(correlaciones.values, k=1)]
        print(f"📊 Correlación promedio: {np.mean(corr_values):.3f}")
        print(f"📊 Correlación mínima: {np.min(corr_values):.3f}")
        print(f"📊 Correlación máxima: {np.max(corr_values):.3f}")
        
        return correlaciones

def simular_portfolios(retornos, num_simulaciones=10000, restricciones=None):
    """
    Simula portfolios aleatorios usando Monte Carlo
    
    Parámetros:
    -----------
    retornos : pandas.DataFrame
        Retornos históricos de los activos
    num_simulaciones : int, opcional
        Número de portfolios a simular (default: 10000)
    restricciones : dict, opcional
        Restricciones de peso: {'peso_min': 0.05, 'peso_max': 0.4}
    
    Retorna:
    --------
    pandas.DataFrame : Resultados de simulación
    """
    
    print(f"🎲 Simulando {num_simulaciones:,} portfolios aleatorios...")
    
    num_activos = len(retornos.columns)
    
    # Configurar restricciones por defecto
    if restricciones is None:
        restricciones = {'peso_min': 0.0, 'peso_max': 1.0}
    
    peso_min = restricciones.get('peso_min', 0.0)
    peso_max = restricciones.get('peso_max', 1.0)
    
    # Calcular estadísticas necesarias
    retornos_medios = retornos.mean() * 252  # Anualizados
    matriz_cov = retornos.cov() * 252  # Anualizada
    
    # Arrays para almacenar resultados
    resultados = {
        'Retorno': [],
        'Volatilidad': [],
        'Sharpe': [],
        'Pesos': []
    }
    
    simulaciones_exitosas = 0
    intentos = 0
    max_intentos = num_simulaciones * 10  # Limite de seguridad
    
    while simulaciones_exitosas < num_simulaciones and intentos < max_intentos:
        intentos += 1
        
        # Generar pesos aleatorios
        pesos = np.random.random(num_activos)
        pesos = pesos / np.sum(pesos)  # Normalizar a suma = 1
        
        # Verificar restricciones
        if np.any(pesos < peso_min) or np.any(pesos > peso_max):
            continue
        
        # Calcular métricas del portfolio
        ret_portfolio = np.sum(retornos_medios * pesos)
        vol_portfolio = np.sqrt(np.dot(pesos.T, np.dot(matriz_cov, pesos)))
        sharpe_portfolio = ret_portfolio / vol_portfolio if vol_portfolio > 0 else 0
        
        # Almacenar resultados
        resultados['Retorno'].append(ret_portfolio)
        resultados['Volatilidad'].append(vol_portfolio)
        resultados['Sharpe'].append(sharpe_portfolio)
        resultados['Pesos'].append(pesos.copy())
        
        simulaciones_exitosas += 1
        
        # Progreso cada 1000 simulaciones
        if simulaciones_exitosas % 1000 == 0:
            print(f"   📊 {simulaciones_exitosas:,} portfolios simulados...")
    
    # Convertir a DataFrame
    df_simulacion = pd.DataFrame({
        'Retorno': resultados['Retorno'],
        'Volatilidad': resultados['Volatilidad'],
        'Sharpe': resultados['Sharpe']
    })
    
    # Agregar pesos como columnas separadas
    pesos_df = pd.DataFrame(resultados['Pesos'], columns=retornos.columns)
    df_simulacion = pd.concat([df_simulacion, pesos_df], axis=1)
    
    print(f"✅ Simulación completada:")
    print(f"   🎯 {simulaciones_exitosas:,} portfolios válidos generados")
    print(f"   📈 Retorno máximo: {df_simulacion['Retorno'].max():.2%}")
    print(f"   📉 Volatilidad mínima: {df_simulacion['Volatilidad'].min():.2%}")
    print(f"   ⚡ Sharpe máximo: {df_simulacion['Sharpe'].max():.3f}")
    
    return df_simulacion

def optimizar_portfolio(retornos, objetivo='sharpe_max', restricciones=None):
    """
    Optimización de portfolio con restricciones realistas
    
    TAREA CRÍTICA: Justificar restricciones elegidas y interpretar resultados
    
    Parámetros:
    -----------
    retornos : pandas.DataFrame
        Retornos históricos
    objetivo : str, opcional
        Función objetivo: 'sharpe_max', 'vol_min', 'retorno_max'
    restricciones : dict, opcional
        Restricciones adicionales
    
    Retorna:
    --------
    dict : Resultados de optimización
    """
    
    print(f"🎯 Optimizando portfolio (objetivo: {objetivo})...")
    
    num_activos = len(retornos.columns)
    
    # Configurar restricciones por defecto
    if restricciones is None:
        restricciones = {
            'peso_min': 0.05,  # Mínimo 5% por activo
            'peso_max': 0.40,  # Máximo 40% por activo
            'costos_transaccion': 0.005  # 0.5% de costos
        }
    
    # Calcular estadísticas
    retornos_medios = retornos.mean() * 252
    matriz_cov = retornos.cov() * 252
    
    # Función objetivo
    def objetivo_sharpe(pesos):
        ret = np.sum(retornos_medios * pesos)
        vol = np.sqrt(np.dot(pesos.T, np.dot(matriz_cov, pesos)))
        # Incluir costos de transacción
        costos = restricciones.get('costos_transaccion', 0) * np.sum(np.abs(pesos))
        return -(ret - costos) / vol if vol > 0 else -np.inf
    
    def objetivo_volatilidad(pesos):
        return np.sqrt(np.dot(pesos.T, np.dot(matriz_cov, pesos)))
    
    def objetivo_retorno(pesos):
        costos = restricciones.get('costos_transaccion', 0) * np.sum(np.abs(pesos))
        return -(np.sum(retornos_medios * pesos) - costos)
    
    # Seleccionar función objetivo
    if objetivo == 'sharpe_max':
        fun_objetivo = objetivo_sharpe
    elif objetivo == 'vol_min':
        fun_objetivo = objetivo_volatilidad
    elif objetivo == 'retorno_max':
        fun_objetivo = objetivo_retorno
    else:
        raise ValueError("Objetivo debe ser 'sharpe_max', 'vol_min' o 'retorno_max'")
    
    # Restricciones de optimización
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Suma de pesos = 1
    ]
    
    # Límites de pesos
    peso_min = restricciones.get('peso_min', 0.0)
    peso_max = restricciones.get('peso_max', 1.0)
    bounds = [(peso_min, peso_max) for _ in range(num_activos)]
    
    # Pesos iniciales (equiponderado)
    x0 = np.array([1/num_activos] * num_activos)
    
    # Optimización
    try:
        resultado = minimize(
            fun_objetivo,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000}
        )
        
        if resultado.success:
            pesos_optimos = resultado.x
            
            # Calcular métricas del portfolio óptimo
            ret_optimo = np.sum(retornos_medios * pesos_optimos)
            vol_optimo = np.sqrt(np.dot(pesos_optimos.T, np.dot(matriz_cov, pesos_optimos)))
            sharpe_optimo = ret_optimo / vol_optimo if vol_optimo > 0 else 0
            
            # Incluir costos
            costos = restricciones.get('costos_transaccion', 0) * np.sum(np.abs(pesos_optimos))
            ret_neto = ret_optimo - costos
            
            resultado_dict = {
                'exito': True,
                'pesos': pd.Series(pesos_optimos, index=retornos.columns),
                'retorno_bruto': ret_optimo,
                'retorno_neto': ret_neto,
                'volatilidad': vol_optimo,
                'sharpe_bruto': sharpe_optimo,
                'sharpe_neto': ret_neto / vol_optimo if vol_optimo > 0 else 0,
                'costos_estimados': costos,
                'objetivo': objetivo,
                'restricciones_aplicadas': restricciones
            }
            
            print(f"✅ Optimización exitosa:")
            print(f"   📈 Retorno esperado: {ret_optimo:.2%} (neto: {ret_neto:.2%})")
            print(f"   📊 Volatilidad: {vol_optimo:.2%}")
            print(f"   ⚡ Sharpe ratio: {sharpe_optimo:.3f}")
            print(f"   💰 Costos estimados: {costos:.2%}")
            
            return resultado_dict
        
        else:
            print(f"❌ Optimización falló: {resultado.message}")
            return {'exito': False, 'error': resultado.message}
    
    except Exception as e:
        print(f"❌ Error en optimización: {str(e)}")
        return {'exito': False, 'error': str(e)}

def calcular_frontera_eficiente(retornos, num_puntos=50, restricciones=None):
    """
    Calcula la frontera eficiente de Markowitz
    
    Parámetros:
    -----------
    retornos : pandas.DataFrame
        Retornos históricos
    num_puntos : int, opcional
        Número de puntos en la frontera
    restricciones : dict, opcional
        Restricciones de optimización
    
    Retorna:
    --------
    pandas.DataFrame : Puntos de la frontera eficiente
    """
    
    print(f"📊 Calculando frontera eficiente ({num_puntos} puntos)...")
    
    # Calcular portfolios de referencia
    portfolio_min_vol = optimizar_portfolio(retornos, 'vol_min', restricciones)
    portfolio_max_ret = optimizar_portfolio(retornos, 'retorno_max', restricciones)
    
    if not (portfolio_min_vol['exito'] and portfolio_max_ret['exito']):
        print("❌ No se pudieron calcular portfolios de referencia")
        return None
    
    # Rango de retornos objetivo
    ret_min = portfolio_min_vol['retorno_neto']
    ret_max = portfolio_max_ret['retorno_neto']
    retornos_objetivo = np.linspace(ret_min, ret_max, num_puntos)
    
    frontera = {
        'Retorno': [],
        'Volatilidad': [],
        'Sharpe': [],
        'Pesos': []
    }
    
    retornos_medios = retornos.mean() * 252
    matriz_cov = retornos.cov() * 252
    num_activos = len(retornos.columns)
    
    for ret_target in retornos_objetivo:
        # Minimizar volatilidad sujeto a retorno objetivo
        def objetivo(pesos):
            return np.sqrt(np.dot(pesos.T, np.dot(matriz_cov, pesos)))
        
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Suma = 1
            {'type': 'eq', 'fun': lambda x: np.sum(retornos_medios * x) - ret_target}  # Retorno objetivo
        ]
        
        # Límites
        if restricciones:
            peso_min = restricciones.get('peso_min', 0.0)
            peso_max = restricciones.get('peso_max', 1.0)
        else:
            peso_min, peso_max = 0.0, 1.0
        
        bounds = [(peso_min, peso_max) for _ in range(num_activos)]
        x0 = np.array([1/num_activos] * num_activos)
        
        try:
            resultado = minimize(objetivo, x0, method='SLSQP', bounds=bounds, constraints=constraints)
            
            if resultado.success:
                pesos = resultado.x
                vol = objetivo(pesos)
                sharpe = ret_target / vol if vol > 0 else 0
                
                frontera['Retorno'].append(ret_target)
                frontera['Volatilidad'].append(vol)
                frontera['Sharpe'].append(sharpe)
                frontera['Pesos'].append(pesos.copy())
        
        except:
            continue
    
    if len(frontera['Retorno']) == 0:
        print("❌ No se pudo calcular la frontera eficiente")
        return None
    
    # Convertir a DataFrame
    df_frontera = pd.DataFrame({
        'Retorno': frontera['Retorno'],
        'Volatilidad': frontera['Volatilidad'],
        'Sharpe': frontera['Sharpe']
    })
    
    # Agregar pesos
    pesos_df = pd.DataFrame(frontera['Pesos'], columns=retornos.columns)
    df_frontera = pd.concat([df_frontera, pesos_df], axis=1)
    
    print(f"✅ Frontera eficiente calculada: {len(df_frontera)} puntos válidos")
    
    return df_frontera

def graficar_frontera_eficiente(simulacion, frontera=None, portfolios_especiales=None, titulo="Frontera Eficiente"):
    """
    Gráfica la frontera eficiente con portfolios simulados
    
    TAREA CRÍTICA: Marcar portfolio elegido y justificar posición
    """
    
    plt.figure(figsize=(12, 8))
    
    # Gráfico de dispersión de simulaciones
    scatter = plt.scatter(
        simulacion['Volatilidad'], 
        simulacion['Retorno'],
        c=simulacion['Sharpe'],
        cmap='viridis',
        alpha=0.6,
        s=20
    )
    
    plt.colorbar(scatter, label='Sharpe Ratio')
    
    # Frontera eficiente
    if frontera is not None:
        plt.plot(frontera['Volatilidad'], frontera['Retorno'], 
                'r-', linewidth=3, label='Frontera Eficiente')
    
    # Portfolios especiales
    if portfolios_especiales:
        for nombre, portfolio in portfolios_especiales.items():
            if portfolio.get('exito', False):
                plt.scatter(portfolio['volatilidad'], portfolio['retorno_neto'],
                          marker='*', s=200, label=nombre, zorder=5)
    
    plt.xlabel('Volatilidad (Riesgo)')
    plt.ylabel('Retorno Esperado')
    plt.title(titulo)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # TODO: Los estudiantes deben marcar su portfolio elegido
    # plt.scatter(vol_elegido, ret_elegido, color='red', s=100, marker='*', label='Mi Elección')
    
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    print("🧪 Testing módulo portfolio_utils...")
    
    # Crear datos de ejemplo
    np.random.seed(42)
    fechas = pd.date_range('2020-01-01', periods=1000, freq='D')
    
    # Simular retornos correlacionados
    retornos_ejemplo = pd.DataFrame({
        'AAPL': np.random.normal(0.001, 0.02, 1000),
        'GOOGL': np.random.normal(0.0008, 0.025, 1000),
        'MSFT': np.random.normal(0.0012, 0.018, 1000)
    }, index=fechas)
    
    # Test funciones
    metricas = calcular_metricas_riesgo(retornos_ejemplo)
    simulacion = simular_portfolios(retornos_ejemplo, num_simulaciones=1000)
    
    print("✅ Tests completados exitosamente")