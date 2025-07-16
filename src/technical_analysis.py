"""
Módulo de Análisis Técnico
Trabajo Práctico - Análisis Integral de Inversiones

Implementa indicadores técnicos principales para trading

Funciones principales:
- calcular_medias_moviles(): SMA, EMA, cruces
- calcular_rsi(): Relative Strength Index
- calcular_macd(): Moving Average Convergence Divergence
- calcular_bollinger_bands(): Bandas de Bollinger
- calcular_adx(): Average Directional Index
- backtest_estrategia(): Backtesting de estrategias
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

def calcular_medias_moviles(precios, ventanas=[20, 50, 200], tipo='SMA'):
    """
    Calcula medias móviles simples (SMA) o exponenciales (EMA)
    
    Parámetros:
    -----------
    precios : pandas.Series o pandas.DataFrame
        Precios del activo
    ventanas : list, opcional
        Lista de períodos para las medias móviles (default: [20, 50, 200])
    tipo : str, opcional
        Tipo de media: 'SMA' (simple) o 'EMA' (exponencial)
    
    Retorna:
    --------
    pandas.DataFrame : Precios originales con medias móviles
    """
    
    print(f"📊 Calculando medias móviles {tipo} con ventanas: {ventanas}")
    
    # Convertir a DataFrame si es Series
    if isinstance(precios, pd.Series):
        df = precios.to_frame('Precio')
    else:
        df = precios.copy()
    
    resultado = df.copy()
    
    for ventana in ventanas:
        if tipo == 'SMA':
            nombre_col = f'SMA_{ventana}'
            resultado[nombre_col] = df.iloc[:, 0].rolling(window=ventana).mean()
        elif tipo == 'EMA':
            nombre_col = f'EMA_{ventana}'
            resultado[nombre_col] = df.iloc[:, 0].ewm(span=ventana).mean()
        else:
            raise ValueError("Tipo debe ser 'SMA' o 'EMA'")
    
    print(f"✅ Medias móviles calculadas para {len(ventanas)} períodos")
    
    return resultado

def detectar_cruces_medias(datos, ma_corta, ma_larga):
    """
    Detecta cruces entre medias móviles (señales de compra/venta)
    
    Parámetros:
    -----------
    datos : pandas.DataFrame
        DataFrame con las medias móviles
    ma_corta : str
        Nombre de la columna de media móvil corta
    ma_larga : str
        Nombre de la columna de media móvil larga
    
    Retorna:
    --------
    pandas.DataFrame : Datos originales con señales de cruce
    """
    
    print(f"🔍 Detectando cruces entre {ma_corta} y {ma_larga}")
    
    resultado = datos.copy()
    
    # Calcular diferencia entre medias
    resultado['Diferencia'] = resultado[ma_corta] - resultado[ma_larga]
    
    # Detectar cruces
    resultado['Cruce'] = 0
    resultado['Señal'] = 'Hold'
    
    # Golden Cross (cruce alcista): MA corta cruza por encima de MA larga
    cruces_alcistas = (
        (resultado['Diferencia'] > 0) & 
        (resultado['Diferencia'].shift(1) <= 0)
    )
    
    # Death Cross (cruce bajista): MA corta cruza por debajo de MA larga
    cruces_bajistas = (
        (resultado['Diferencia'] < 0) & 
        (resultado['Diferencia'].shift(1) >= 0)
    )
    
    resultado.loc[cruces_alcistas, 'Cruce'] = 1
    resultado.loc[cruces_alcistas, 'Señal'] = 'Buy'
    
    resultado.loc[cruces_bajistas, 'Cruce'] = -1
    resultado.loc[cruces_bajistas, 'Señal'] = 'Sell'
    
    num_golden_cross = (resultado['Cruce'] == 1).sum()
    num_death_cross = (resultado['Cruce'] == -1).sum()
    
    print(f"📈 Golden Cross detectados: {num_golden_cross}")
    print(f"📉 Death Cross detectados: {num_death_cross}")
    
    return resultado

def calcular_rsi(precios, periodo=14):
    """
    Calcula el Relative Strength Index (RSI)
    
    TAREA CRÍTICA: Determinar parámetros óptimos para mercado argentino
    
    Parámetros:
    -----------
    precios : pandas.Series
        Serie de precios
    periodo : int, opcional
        Período para el cálculo del RSI (default: 14)
    
    Retorna:
    --------
    pandas.Series : Valores del RSI
    """
    
    print(f"📊 Calculando RSI con período {periodo}")
    
    # Calcular cambios diarios
    delta = precios.diff()
    
    # Separar ganancias y pérdidas
    ganancias = delta.where(delta > 0, 0)
    perdidas = -delta.where(delta < 0, 0)
    
    # Calcular promedios móviles de ganancias y pérdidas
    avg_ganancias = ganancias.rolling(window=periodo).mean()
    avg_perdidas = perdidas.rolling(window=periodo).mean()
    
    # Calcular RS y RSI
    rs = avg_ganancias / avg_perdidas
    rsi = 100 - (100 / (1 + rs))
    
    # Estadísticas del RSI
    rsi_stats = {
        'RSI_promedio': rsi.mean(),
        'RSI_min': rsi.min(),
        'RSI_max': rsi.max(),
        'Sobrecompra_70': (rsi > 70).sum(),
        'Sobreventa_30': (rsi < 30).sum()
    }
    
    print(f"📊 RSI calculado:")
    print(f"   Promedio: {rsi_stats['RSI_promedio']:.1f}")
    print(f"   Señales sobrecompra (>70): {rsi_stats['Sobrecompra_70']}")
    print(f"   Señales sobreventa (<30): {rsi_stats['Sobreventa_30']}")
    
    return rsi

def generar_señales_rsi(rsi, umbral_sobrecompra=70, umbral_sobreventa=30):
    """
    Genera señales de trading basadas en RSI
    
    Parámetros:
    -----------
    rsi : pandas.Series
        Valores del RSI
    umbral_sobrecompra : float, opcional
        Umbral de sobrecompra (default: 70)
    umbral_sobreventa : float, opcional
        Umbral de sobreventa (default: 30)
    
    Retorna:
    --------
    pandas.DataFrame : RSI con señales de trading
    """
    
    resultado = pd.DataFrame({'RSI': rsi})
    resultado['Señal'] = 'Hold'
    resultado['Posicion'] = 0
    
    # Señales de venta (sobrecompra)
    sobreventa_a_neutral = (rsi < umbral_sobreventa) & (rsi.shift(1) >= umbral_sobreventa)
    resultado.loc[sobreventa_a_neutral, 'Señal'] = 'Buy'
    resultado.loc[sobreventa_a_neutral, 'Posicion'] = 1
    
    # Señales de compra (sobreventa)
    sobrecompra_a_neutral = (rsi > umbral_sobrecompra) & (rsi.shift(1) <= umbral_sobrecompra)
    resultado.loc[sobrecompra_a_neutral, 'Señal'] = 'Sell'
    resultado.loc[sobrecompra_a_neutral, 'Posicion'] = -1
    
    return resultado

def calcular_macd(precios, periodo_rapido=12, periodo_lento=26, periodo_señal=9):
    """
    Calcula el MACD (Moving Average Convergence Divergence)
    
    Parámetros:
    -----------
    precios : pandas.Series
        Serie de precios
    periodo_rapido : int, opcional
        Período de la EMA rápida (default: 12)
    periodo_lento : int, opcional
        Período de la EMA lenta (default: 26)
    periodo_señal : int, opcional
        Período de la línea de señal (default: 9)
    
    Retorna:
    --------
    pandas.DataFrame : MACD, línea de señal e histograma
    """
    
    print(f"📊 Calculando MACD ({periodo_rapido}, {periodo_lento}, {periodo_señal})")
    
    # Calcular EMAs
    ema_rapida = precios.ewm(span=periodo_rapido).mean()
    ema_lenta = precios.ewm(span=periodo_lento).mean()
    
    # Calcular MACD
    macd = ema_rapida - ema_lenta
    
    # Línea de señal (EMA del MACD)
    señal = macd.ewm(span=periodo_señal).mean()
    
    # Histograma
    histograma = macd - señal
    
    resultado = pd.DataFrame({
        'MACD': macd,
        'Señal': señal,
        'Histograma': histograma
    }, index=precios.index)
    
    # Detectar cruces
    resultado['Cruce_MACD'] = 0
    resultado['Señal_Trading'] = 'Hold'
    
    # Cruce alcista: MACD cruza por encima de la línea de señal
    cruces_alcistas = (resultado['MACD'] > resultado['Señal']) & (resultado['MACD'].shift(1) <= resultado['Señal'].shift(1))
    resultado.loc[cruces_alcistas, 'Cruce_MACD'] = 1
    resultado.loc[cruces_alcistas, 'Señal_Trading'] = 'Buy'
    
    # Cruce bajista: MACD cruza por debajo de la línea de señal
    cruces_bajistas = (resultado['MACD'] < resultado['Señal']) & (resultado['MACD'].shift(1) >= resultado['Señal'].shift(1))
    resultado.loc[cruces_bajistas, 'Cruce_MACD'] = -1
    resultado.loc[cruces_bajistas, 'Señal_Trading'] = 'Sell'
    
    print(f"✅ MACD calculado con {(resultado['Cruce_MACD'] == 1).sum()} señales de compra y {(resultado['Cruce_MACD'] == -1).sum()} de venta")
    
    return resultado

def calcular_bollinger_bands(precios, periodo=20, std_dev=2):
    """
    Calcula las Bandas de Bollinger
    
    Parámetros:
    -----------
    precios : pandas.Series
        Serie de precios
    periodo : int, opcional
        Período de la media móvil (default: 20)
    std_dev : float, opcional
        Número de desviaciones estándar (default: 2)
    
    Retorna:
    --------
    pandas.DataFrame : Bandas de Bollinger y señales
    """
    
    print(f"📊 Calculando Bandas de Bollinger ({periodo} períodos, {std_dev} std)")
    
    # Media móvil y desviación estándar
    sma = precios.rolling(window=periodo).mean()
    std = precios.rolling(window=periodo).std()
    
    # Bandas superior e inferior
    banda_superior = sma + (std * std_dev)
    banda_inferior = sma - (std * std_dev)
    
    resultado = pd.DataFrame({
        'Precio': precios,
        'SMA': sma,
        'Banda_Superior': banda_superior,
        'Banda_Inferior': banda_inferior,
        'Banda_Width': (banda_superior - banda_inferior) / sma * 100,
        '%B': (precios - banda_inferior) / (banda_superior - banda_inferior) * 100
    })
    
    # Señales de trading
    resultado['Señal'] = 'Hold'
    resultado['Posicion'] = 0
    
    # Compra cuando el precio toca la banda inferior
    compra = (precios <= banda_inferior) & (precios.shift(1) > banda_inferior.shift(1))
    resultado.loc[compra, 'Señal'] = 'Buy'
    resultado.loc[compra, 'Posicion'] = 1
    
    # Venta cuando el precio toca la banda superior
    venta = (precios >= banda_superior) & (precios.shift(1) < banda_superior.shift(1))
    resultado.loc[venta, 'Señal'] = 'Sell'
    resultado.loc[venta, 'Posicion'] = -1
    
    # Estadísticas
    fuera_bandas = ((precios > banda_superior) | (precios < banda_inferior)).sum()
    total_datos = len(precios.dropna())
    pct_fuera_bandas = fuera_bandas / total_datos * 100
    
    print(f"📊 Estadísticas Bollinger:")
    print(f"   Ancho promedio bandas: {resultado['Banda_Width'].mean():.2f}%")
    print(f"   Tiempo fuera de bandas: {pct_fuera_bandas:.1f}%")
    print(f"   Señales generadas: {(resultado['Posicion'] != 0).sum()}")
    
    return resultado

def calcular_adx(precios_high, precios_low, precios_close, periodo=14):
    """
    Calcula el Average Directional Index (ADX)
    
    Parámetros:
    -----------
    precios_high : pandas.Series
        Precios máximos
    precios_low : pandas.Series
        Precios mínimos
    precios_close : pandas.Series
        Precios de cierre
    periodo : int, opcional
        Período para el cálculo (default: 14)
    
    Retorna:
    --------
    pandas.DataFrame : ADX, +DI, -DI
    """
    
    print(f"📊 Calculando ADX con período {periodo}")
    
    # True Range
    tr1 = precios_high - precios_low
    tr2 = abs(precios_high - precios_close.shift(1))
    tr3 = abs(precios_low - precios_close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Directional Movement
    dm_plus = precios_high.diff()
    dm_minus = -precios_low.diff()
    
    dm_plus[dm_plus < 0] = 0
    dm_minus[dm_minus < 0] = 0
    dm_plus[(dm_plus - dm_minus) < 0] = 0
    dm_minus[(dm_minus - dm_plus) < 0] = 0
    
    # Smoothed TR y DM
    tr_smooth = tr.rolling(window=periodo).mean()
    dm_plus_smooth = dm_plus.rolling(window=periodo).mean()
    dm_minus_smooth = dm_minus.rolling(window=periodo).mean()
    
    # +DI y -DI
    di_plus = 100 * dm_plus_smooth / tr_smooth
    di_minus = 100 * dm_minus_smooth / tr_smooth
    
    # DX
    dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
    
    # ADX
    adx = dx.rolling(window=periodo).mean()
    
    resultado = pd.DataFrame({
        'ADX': adx,
        '+DI': di_plus,
        '-DI': di_minus,
        'DX': dx
    })
    
    # Interpretación de señales
    resultado['Tendencia'] = 'Débil'
    resultado.loc[adx > 25, 'Tendencia'] = 'Fuerte'
    resultado.loc[adx > 50, 'Tendencia'] = 'Muy Fuerte'
    
    resultado['Direccion'] = 'Neutral'
    resultado.loc[di_plus > di_minus, 'Direccion'] = 'Alcista'
    resultado.loc[di_minus > di_plus, 'Direccion'] = 'Bajista'
    
    print(f"✅ ADX calculado:")
    print(f"   ADX promedio: {adx.mean():.1f}")
    print(f"   Tendencias fuertes (ADX>25): {(adx > 25).sum()} días")
    
    return resultado

def backtest_estrategia(precios, señales, comision=0.001, capital_inicial=100000):
    """
    Realiza backtesting de una estrategia de trading
    
    TAREA CRÍTICA: Calcular métricas ajustadas por riesgo y comparar con benchmark
    
    Parámetros:
    -----------
    precios : pandas.Series
        Serie de precios del activo
    señales : pandas.Series
        Serie con señales de trading (1=compra, -1=venta, 0=hold)
    comision : float, opcional
        Comisión por transacción como % del valor (default: 0.1%)
    capital_inicial : float, opcional
        Capital inicial para el backtest (default: 100,000)
    
    Retorna:
    --------
    pandas.DataFrame : Resultados del backtesting
    dict : Métricas de performance
    """
    
    print(f"🔄 Ejecutando backtesting...")
    print(f"   💰 Capital inicial: ${capital_inicial:,.0f}")
    print(f"   💳 Comisión: {comision:.3%}")
    
    # Preparar datos
    datos = pd.DataFrame({
        'Precio': precios,
        'Señal': señales
    }).dropna()
    
    # Inicializar variables
    datos['Posicion'] = 0  # 0=fuera, 1=dentro del mercado
    datos['Retorno_Activo'] = datos['Precio'].pct_change()
    datos['Retorno_Estrategia'] = 0.0
    datos['Capital'] = capital_inicial
    datos['Acciones'] = 0
    datos['Comisiones'] = 0.0
    
    capital = capital_inicial
    acciones = 0
    posicion = 0
    
    for i, (fecha, fila) in enumerate(datos.iterrows()):
        if i == 0:
            continue
            
        precio_actual = fila['Precio']
        señal_actual = fila['Señal']
        
        # Determinar acción a tomar
        if señal_actual == 1 and posicion == 0:  # Señal de compra
            # Comprar
            comision_pago = capital * comision
            acciones = (capital - comision_pago) / precio_actual
            capital = 0
            posicion = 1
            datos.loc[fecha, 'Comisiones'] = comision_pago
            
        elif señal_actual == -1 and posicion == 1:  # Señal de venta
            # Vender
            capital = acciones * precio_actual
            comision_pago = capital * comision
            capital -= comision_pago
            acciones = 0
            posicion = 0
            datos.loc[fecha, 'Comisiones'] = comision_pago
        
        # Actualizar valores
        datos.loc[fecha, 'Posicion'] = posicion
        datos.loc[fecha, 'Acciones'] = acciones
        
        # Calcular capital total (efectivo + valor de acciones)
        valor_acciones = acciones * precio_actual if acciones > 0 else 0
        capital_total = capital + valor_acciones
        datos.loc[fecha, 'Capital'] = capital_total
        
        # Calcular retorno de la estrategia
        if i > 0:
            capital_anterior = datos.iloc[i-1]['Capital']
            retorno_estrategia = (capital_total - capital_anterior) / capital_anterior
            datos.loc[fecha, 'Retorno_Estrategia'] = retorno_estrategia
    
    # Calcular métricas de performance
    capital_final = datos['Capital'].iloc[-1]
    retorno_total = (capital_final - capital_inicial) / capital_inicial
    
    # Retornos anualizados
    dias_trading = len(datos)
    años = dias_trading / 252
    retorno_anualizado_estrategia = (1 + retorno_total) ** (1/años) - 1
    
    # Buy & Hold para comparación
    retorno_buy_hold = (datos['Precio'].iloc[-1] - datos['Precio'].iloc[0]) / datos['Precio'].iloc[0]
    retorno_anualizado_buy_hold = (1 + retorno_buy_hold) ** (1/años) - 1
    
    # Volatilidad
    vol_estrategia = datos['Retorno_Estrategia'].std() * np.sqrt(252)
    vol_buy_hold = datos['Retorno_Activo'].std() * np.sqrt(252)
    
    # Sharpe Ratio (asumiendo rf=0)
    sharpe_estrategia = retorno_anualizado_estrategia / vol_estrategia if vol_estrategia > 0 else 0
    sharpe_buy_hold = retorno_anualizado_buy_hold / vol_buy_hold if vol_buy_hold > 0 else 0
    
    # Drawdown máximo
    capital_peak = datos['Capital'].expanding().max()
    drawdown = (datos['Capital'] - capital_peak) / capital_peak
    max_drawdown = drawdown.min()
    
    # Calmar Ratio
    calmar_ratio = retorno_anualizado_estrategia / abs(max_drawdown) if max_drawdown != 0 else 0
    
    # Win Rate
    trades = datos[datos['Señal'] != 0]
    winning_trades = len(trades[trades['Retorno_Estrategia'] > 0])
    total_trades = len(trades)
    win_rate = winning_trades / total_trades if total_trades > 0 else 0
    
    # Comisiones totales
    comisiones_totales = datos['Comisiones'].sum()
    
    metricas = {
        'Capital_Inicial': capital_inicial,
        'Capital_Final': capital_final,
        'Retorno_Total': retorno_total,
        'Retorno_Anualizado_Estrategia': retorno_anualizado_estrategia,
        'Retorno_Anualizado_BuyHold': retorno_anualizado_buy_hold,
        'Volatilidad_Estrategia': vol_estrategia,
        'Volatilidad_BuyHold': vol_buy_hold,
        'Sharpe_Estrategia': sharpe_estrategia,
        'Sharpe_BuyHold': sharpe_buy_hold,
        'Max_Drawdown': max_drawdown,
        'Calmar_Ratio': calmar_ratio,
        'Win_Rate': win_rate,
        'Total_Trades': total_trades,
        'Comisiones_Totales': comisiones_totales,
        'Dias_Backtesting': dias_trading
    }
    
    # Mostrar resultados
    print(f"✅ Backtesting completado:")
    print(f"   📈 Retorno estrategia: {retorno_anualizado_estrategia:.2%} anual")
    print(f"   📊 Retorno buy & hold: {retorno_anualizado_buy_hold:.2%} anual")
    print(f"   ⚡ Sharpe estrategia: {sharpe_estrategia:.3f}")
    print(f"   📉 Drawdown máximo: {max_drawdown:.2%}")
    print(f"   🎯 Win rate: {win_rate:.1%}")
    print(f"   💰 Comisiones pagadas: ${comisiones_totales:,.0f}")
    
    return datos, metricas

def graficar_indicador_tecnico(datos, indicador, precio_col='Precio', titulo="Análisis Técnico"):
    """
    Gráfica un indicador técnico junto con los precios
    
    Parámetros:
    -----------
    datos : pandas.DataFrame
        Datos con precios e indicador
    indicador : str
        Nombre de la columna del indicador a graficar
    precio_col : str, opcional
        Nombre de la columna de precios
    titulo : str, opcional
        Título del gráfico
    """
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)
    
    # Gráfico de precios
    ax1.plot(datos.index, datos[precio_col], label='Precio', linewidth=2)
    
    # Agregar medias móviles si existen
    for col in datos.columns:
        if 'SMA' in col or 'EMA' in col or 'Banda' in col:
            ax1.plot(datos.index, datos[col], label=col, alpha=0.7)
    
    # Señales de compra/venta si existen
    if 'Señal' in datos.columns:
        compras = datos[datos['Señal'] == 'Buy']
        ventas = datos[datos['Señal'] == 'Sell']
        
        ax1.scatter(compras.index, compras[precio_col], 
                   color='green', marker='^', s=100, label='Compra', zorder=5)
        ax1.scatter(ventas.index, ventas[precio_col], 
                   color='red', marker='v', s=100, label='Venta', zorder=5)
    
    ax1.set_title(f'{titulo} - Precios y Señales')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Gráfico del indicador
    ax2.plot(datos.index, datos[indicador], label=indicador, linewidth=2)
    
    # Líneas de referencia para RSI
    if indicador == 'RSI':
        ax2.axhline(70, color='red', linestyle='--', alpha=0.7, label='Sobrecompra (70)')
        ax2.axhline(30, color='green', linestyle='--', alpha=0.7, label='Sobreventa (30)')
        ax2.set_ylim(0, 100)
    
    # Línea cero para MACD
    if 'MACD' in indicador:
        ax2.axhline(0, color='black', linestyle='-', alpha=0.5)
    
    ax2.set_title(f'{titulo} - {indicador}')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Ejemplo de uso y testing
if __name__ == "__main__":
    print("🧪 Testing módulo technical_analysis...")
    
    # Crear datos de ejemplo
    np.random.seed(42)
    fechas = pd.date_range('2023-01-01', periods=252, freq='D')
    
    # Simular precios con tendencia
    precios_base = 100
    cambios = np.random.normal(0.001, 0.02, 252)
    precios = [precios_base]
    
    for cambio in cambios:
        precios.append(precios[-1] * (1 + cambio))
    
    precios_serie = pd.Series(precios[1:], index=fechas)
    
    # Test indicadores
    print("Testing RSI...")
    rsi = calcular_rsi(precios_serie)
    
    print("Testing MACD...")
    macd = calcular_macd(precios_serie)
    
    print("Testing Bollinger Bands...")
    bollinger = calcular_bollinger_bands(precios_serie)
    
    print("✅ Todos los tests completados exitosamente")
