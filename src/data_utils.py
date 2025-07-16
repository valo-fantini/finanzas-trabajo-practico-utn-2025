"""
Módulo de Utilidades para Obtención y Limpieza de Datos
Trabajo Práctico - Análisis Integral de Inversiones

Funciones principales:
- obtener_datos_historicos(): Descarga datos de yfinance
- limpiar_datos(): Limpieza y validación de datos
- calcular_retornos(): Cálculo de retornos logarítmicos
- detectar_outliers(): Identificación de valores atípicos
- validar_datos(): Validación de calidad de datos
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
from scipy import stats

def obtener_datos_historicos(tickers, periodo="5y", inicio=None, fin=None):
    """
    Obtiene datos históricos para una lista de tickers usando yfinance
    
    Parámetros:
    -----------
    tickers : list o str
        Lista de símbolos de acciones o ticker individual
    periodo : str, opcional
        Período de datos ("5y", "2y", "1y", "6mo", etc.)
    inicio : str, opcional
        Fecha de inicio en formato 'YYYY-MM-DD'
    fin : str, opcional
        Fecha de fin en formato 'YYYY-MM-DD'
    
    Retorna:
    --------
    pandas.DataFrame : Precios de cierre ajustados
    """
    
    print(f"📥 Descargando datos históricos...")
    print(f"📊 Tickers: {tickers}")
    print(f"📅 Período: {periodo}")
    
    # Convertir a lista si es un string
    if isinstance(tickers, str):
        tickers = [tickers]
    
    try:
        # Descargar datos
        if inicio and fin:
            data = yf.download(tickers, start=inicio, end=fin, progress=False)
        else:
            data = yf.download(tickers, period=periodo, progress=False)
        
        # Extraer precios de cierre ajustados
        if 'Adj Close' in data.columns:
            precios = data['Adj Close']
        else:
            precios = data
        
        # Si es una sola acción, convertir a DataFrame
        if isinstance(precios, pd.Series):
            precios = precios.to_frame(name=tickers[0])
        
        # Validar datos obtenidos
        if precios.empty:
            raise ValueError("No se obtuvieron datos para los tickers especificados")
        
        print(f"✅ Datos obtenidos exitosamente:")
        print(f"   📈 {precios.shape[0]} observaciones")
        print(f"   🏢 {precios.shape[1]} activos")
        print(f"   📅 Período: {precios.index[0].date()} a {precios.index[-1].date()}")
        
        return precios
        
    except Exception as e:
        print(f"❌ Error obteniendo datos: {str(e)}")
        raise

def calcular_retornos(precios, metodo='logaritmico'):
    """
    Calcula retornos de los precios
    
    Parámetros:
    -----------
    precios : pandas.DataFrame
        DataFrame con precios de activos
    metodo : str, opcional
        Método de cálculo: 'logaritmico' (default) o 'simple'
    
    Retorna:
    --------
    pandas.DataFrame : Retornos calculados
    """
    
    print(f"📊 Calculando retornos {metodo}s...")
    
    if metodo == 'logaritmico':
        retornos = np.log(precios / precios.shift(1))
    elif metodo == 'simple':
        retornos = precios.pct_change()
    else:
        raise ValueError("Método debe ser 'logaritmico' o 'simple'")
    
    # Eliminar primera fila (NaN)
    retornos = retornos.dropna()
    
    print(f"✅ Retornos calculados: {retornos.shape[0]} observaciones")
    
    return retornos

def detectar_outliers(data, metodo='zscore', umbral=3):
    """
    Detecta outliers en los datos
    
    Parámetros:
    -----------
    data : pandas.DataFrame o pandas.Series
        Datos a analizar
    metodo : str, opcional
        Método de detección: 'zscore' (default) o 'iqr'
    umbral : float, opcional
        Umbral para considerar outlier (default: 3 para zscore, 1.5 para IQR)
    
    Retorna:
    --------
    pandas.DataFrame : Matriz booleana indicando outliers
    """
    
    print(f"🔍 Detectando outliers usando método: {metodo}")
    
    if isinstance(data, pd.Series):
        data = data.to_frame()
    
    outliers = pd.DataFrame(False, index=data.index, columns=data.columns)
    
    for col in data.columns:
        serie = data[col].dropna()
        
        if metodo == 'zscore':
            z_scores = np.abs(stats.zscore(serie))
            outliers.loc[serie.index, col] = z_scores > umbral
            
        elif metodo == 'iqr':
            Q1 = serie.quantile(0.25)
            Q3 = serie.quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - umbral * IQR
            limite_superior = Q3 + umbral * IQR
            outliers.loc[serie.index, col] = (serie < limite_inferior) | (serie > limite_superior)
    
    num_outliers = outliers.sum().sum()
    print(f"⚠️  Outliers detectados: {num_outliers}")
    
    return outliers

def limpiar_datos(df, metodo_faltantes='ffill', remover_outliers=False, umbral_outliers=3):
    """
    Limpia y prepara los datos para análisis
    
    TAREA CRÍTICA PARA ESTUDIANTES: 
    Deben justificar su metodología para manejar datos faltantes y outliers
    
    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame con datos a limpiar
    metodo_faltantes : str, opcional
        Método para datos faltantes: 'ffill', 'bfill', 'interpolate', 'drop'
    remover_outliers : bool, opcional
        Si remover outliers detectados
    umbral_outliers : float, opcional
        Umbral para detección de outliers
    
    Retorna:
    --------
    pandas.DataFrame : Datos limpios
    dict : Reporte de limpieza
    """
    
    print("🧹 === INICIANDO LIMPIEZA DE DATOS ===")
    
    # Crear copia para no modificar original
    df_limpio = df.copy()
    
    # Reporte inicial
    reporte = {
        'filas_originales': len(df),
        'columnas_originales': len(df.columns),
        'datos_faltantes_original': df.isnull().sum().to_dict(),
        'outliers_detectados': {},
        'metodo_faltantes': metodo_faltantes,
        'remover_outliers': remover_outliers
    }
    
    print(f"📊 Datos originales: {df.shape}")
    print(f"📉 Datos faltantes por columna:")
    for col, faltantes in reporte['datos_faltantes_original'].items():
        if faltantes > 0:
            print(f"   {col}: {faltantes} ({faltantes/len(df)*100:.1f}%)")
    
    # 1. Manejo de datos faltantes
    if df.isnull().any().any():
        print(f"🔧 Aplicando método '{metodo_faltantes}' para datos faltantes...")
        
        if metodo_faltantes == 'ffill':
            df_limpio = df_limpio.fillna(method='ffill')
        elif metodo_faltantes == 'bfill':
            df_limpio = df_limpio.fillna(method='bfill')
        elif metodo_faltantes == 'interpolate':
            df_limpio = df_limpio.interpolate()
        elif metodo_faltantes == 'drop':
            df_limpio = df_limpio.dropna()
        
        # Verificar si quedan datos faltantes
        faltantes_restantes = df_limpio.isnull().sum().sum()
        if faltantes_restantes > 0:
            print(f"⚠️  Aún quedan {faltantes_restantes} datos faltantes después de la limpieza")
    
    # 2. Detección y manejo de outliers
    if remover_outliers:
        print("🔍 Detectando outliers...")
        outliers = detectar_outliers(df_limpio, umbral=umbral_outliers)
        
        # Contar outliers por columna
        for col in outliers.columns:
            num_outliers = outliers[col].sum()
            reporte['outliers_detectados'][col] = num_outliers
            
            if num_outliers > 0:
                print(f"   {col}: {num_outliers} outliers")
                
                # TODO: Los estudiantes deben decidir cómo manejar outliers
                # Opciones: eliminar, winsorize, transformar, etc.
                # Por ahora solo reportamos
        
        print("📝 TAREA PARA ESTUDIANTES:")
        print("   - Analizar patrones en datos faltantes")
        print("   - Justificar método de imputación elegido")
        print("   - Decidir qué hacer con outliers detectados")
        print("   - Documentar todas las decisiones tomadas")
    
    # 3. Validaciones finales
    print("✅ Validaciones finales:")
    
    # Verificar fechas duplicadas
    fechas_duplicadas = df_limpio.index.duplicated().sum()
    if fechas_duplicadas > 0:
        print(f"⚠️  {fechas_duplicadas} fechas duplicadas encontradas")
        df_limpio = df_limpio[~df_limpio.index.duplicated(keep='first')]
    
    # Verificar orden cronológico
    if not df_limpio.index.is_monotonic_increasing:
        print("📅 Ordenando datos cronológicamente...")
        df_limpio = df_limpio.sort_index()
    
    # Estadísticas finales
    reporte.update({
        'filas_finales': len(df_limpio),
        'datos_faltantes_final': df_limpio.isnull().sum().to_dict(),
        'periodo_final': f"{df_limpio.index[0].date()} a {df_limpio.index[-1].date()}"
    })
    
    print(f"✅ Limpieza completada:")
    print(f"   📊 Datos finales: {df_limpio.shape}")
    print(f"   📅 Período: {reporte['periodo_final']}")
    
    return df_limpio, reporte

def validar_datos(df, nombre_activo="Activo"):
    """
    Valida la calidad de los datos financieros
    
    Parámetros:
    -----------
    df : pandas.DataFrame
        Datos a validar
    nombre_activo : str, opcional
        Nombre para identificar el activo en reportes
    
    Retorna:
    --------
    dict : Reporte de validación
    """
    
    print(f"🔍 === VALIDANDO CALIDAD DE DATOS: {nombre_activo} ===")
    
    validaciones = {
        'activo': nombre_activo,
        'periodo': f"{df.index[0].date()} a {df.index[-1].date()}",
        'observaciones': len(df),
        'problemas_detectados': [],
        'warnings': [],
        'stats_basicas': {}
    }
    
    for col in df.columns:
        serie = df[col]
        
        # Estadísticas básicas
        validaciones['stats_basicas'][col] = {
            'min': serie.min(),
            'max': serie.max(),
            'mean': serie.mean(),
            'std': serie.std(),
            'valores_cero': (serie == 0).sum(),
            'valores_negativos': (serie < 0).sum() if serie.min() < 0 else 0
        }
        
        # Validaciones específicas
        
        # 1. Valores negativos en precios (si es columna de precios)
        if 'price' in col.lower() or 'precio' in col.lower():
            if serie.min() <= 0:
                validaciones['problemas_detectados'].append(
                    f"{col}: Contiene precios negativos o cero"
                )
        
        # 2. Volatilidad extrema
        if len(serie) > 1:
            retornos = serie.pct_change().dropna()
            if retornos.std() > 0.1:  # 10% diario
                validaciones['warnings'].append(
                    f"{col}: Volatilidad muy alta ({retornos.std()*100:.1f}% diario)"
                )
        
        # 3. Valores constantes
        if serie.nunique() == 1:
            validaciones['problemas_detectados'].append(
                f"{col}: Todos los valores son iguales ({serie.iloc[0]})"
            )
        
        # 4. Saltos extremos
        if len(serie) > 1:
            cambios = serie.pct_change().dropna()
            cambios_extremos = (cambios.abs() > 0.5).sum()  # >50% en un día
            if cambios_extremos > 0:
                validaciones['warnings'].append(
                    f"{col}: {cambios_extremos} cambios diarios >50%"
                )
    
    # Mostrar resultados
    print(f"📊 Período analizado: {validaciones['periodo']}")
    print(f"📈 Observaciones: {validaciones['observaciones']}")
    
    if validaciones['problemas_detectados']:
        print("❌ Problemas detectados:")
        for problema in validaciones['problemas_detectados']:
            print(f"   • {problema}")
    
    if validaciones['warnings']:
        print("⚠️  Advertencias:")
        for warning in validaciones['warnings']:
            print(f"   • {warning}")
    
    if not validaciones['problemas_detectados'] and not validaciones['warnings']:
        print("✅ No se detectaron problemas en los datos")
    
    return validaciones

def obtener_info_mercado(ticker):
    """
    Obtiene información adicional sobre un ticker
    
    Parámetros:
    -----------
    ticker : str
        Símbolo del activo
    
    Retorna:
    --------
    dict : Información del ticker
    """
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            'nombre': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'industria': info.get('industry', 'N/A'),
            'pais': info.get('country', 'N/A'),
            'moneda': info.get('currency', 'N/A'),
            'market_cap': info.get('marketCap'),
            'descripcion': info.get('longBusinessSummary', 'N/A')[:200] + '...'
        }
    
    except Exception as e:
        print(f"⚠️  No se pudo obtener información para {ticker}: {e}")
        return {'nombre': ticker, 'error': str(e)}

# Ejemplo de uso y testing
if __name__ == "__main__":
    print("🧪 Ejecutando tests del módulo data_utils...")
    
    # Test básico
    try:
        # Obtener datos de Apple
        datos = obtener_datos_historicos(['AAPL'], periodo='1y')
        
        # Limpiar datos
        datos_limpios, reporte = limpiar_datos(datos)
        
        # Validar
        validacion = validar_datos(datos_limpios, "AAPL")
        
        # Calcular retornos
        retornos = calcular_retornos(datos_limpios)
        
        print("✅ Todos los tests pasaron correctamente")
        
    except Exception as e:
        print(f"❌ Error en tests: {e}")
