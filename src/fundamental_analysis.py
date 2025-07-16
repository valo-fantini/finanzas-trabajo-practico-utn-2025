"""
Módulo de Análisis Fundamental
Trabajo Práctico - Análisis Integral de Inversiones

Implementa análisis fundamental y valuación de empresas

Funciones principales:
- obtener_datos_fundamentales(): Ratios financieros vía yfinance
- calcular_ratios_sector(): Comparación sectorial
- analizar_empresa(): Análisis FODA y ventajas competitivas
- valuar_empresa_dcf(): Valuación por DCF simplificado
"""

import pandas as pd
import numpy as np
import yfinance as yf
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

def obtener_datos_fundamentales(ticker):
    """
    Obtiene ratios fundamentales de Yahoo Finance
    
    TAREA CRÍTICA: Validar datos y complementar con fuentes locales
    para empresas argentinas
    
    Parámetros:
    -----------
    ticker : str
        Símbolo de la empresa
    
    Retorna:
    --------
    dict : Diccionario con ratios fundamentales
    """
    
    print(f"📊 Obteniendo datos fundamentales para {ticker}...")
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Información básica de la empresa
        empresa_info = {
            'ticker': ticker,
            'nombre': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'industria': info.get('industry', 'N/A'),
            'pais': info.get('country', 'N/A'),
            'moneda': info.get('currency', 'USD'),
            'employees': info.get('fullTimeEmployees', 'N/A'),
            'descripcion': info.get('longBusinessSummary', 'N/A')
        }
        
        # Ratios de Valuación
        ratios_valuacion = {
            'Market_Cap': info.get('marketCap'),
            'Enterprise_Value': info.get('enterpriseValue'),
            'Forward_PE': info.get('forwardPE'),
            'Trailing_PE': info.get('trailingPE'),
            'PEG_Ratio': info.get('pegRatio'),
            'Price_Book': info.get('priceToBook'),
            'Price_Sales': info.get('priceToSalesTrailing12Months'),
            'EV_EBITDA': info.get('enterpriseToEbitda'),
            'EV_Revenue': info.get('enterpriseToRevenue')
        }
        
        # Ratios de Rentabilidad
        ratios_rentabilidad = {
            'ROE': info.get('returnOnEquity'),
            'ROA': info.get('returnOnAssets'),
            'Operating_Margin': info.get('operatingMargins'),
            'Profit_Margin': info.get('profitMargins'),
            'Gross_Margin': info.get('grossMargins'),
            'EBITDA_Margin': info.get('ebitdaMargins')
        }
        
        # Ratios de Solvencia
        ratios_solvencia = {
            'Debt_Equity': info.get('debtToEquity'),
            'Current_Ratio': info.get('currentRatio'),
            'Quick_Ratio': info.get('quickRatio'),
            'Total_Cash': info.get('totalCash'),
            'Total_Debt': info.get('totalDebt'),
            'Free_Cashflow': info.get('freeCashflow')
        }
        
        # Ratios de Mercado
        ratios_mercado = {
            'Beta': info.get('beta'),
            '52_Week_High': info.get('fiftyTwoWeekHigh'),
            '52_Week_Low': info.get('fiftyTwoWeekLow'),
            '52_Week_Change': info.get('52WeekChange'),
            '200_Day_MA': info.get('twoHundredDayAverage'),
            '50_Day_MA': info.get('fiftyDayAverage'),
            'Dividend_Yield': info.get('dividendYield'),
            '5_Year_Avg_Dividend_Yield': info.get('fiveYearAvgDividendYield')
        }
        
        # Información financiera adicional
        info_financiera = {
            'Revenue': info.get('totalRevenue'),
            'EBITDA': info.get('ebitda'),
            'Net_Income': info.get('netIncomeToCommon'),
            'Book_Value': info.get('bookValue'),
            'Price_Earnings_Growth': info.get('earningsGrowth'),
            'Revenue_Growth': info.get('revenueGrowth'),
            'Earnings_Per_Share': info.get('trailingEps'),
            'Forward_EPS': info.get('forwardEps')
        }
        
        # Consolidar todos los datos
        datos_completos = {
            'info_empresa': empresa_info,
            'ratios_valuacion': ratios_valuacion,
            'ratios_rentabilidad': ratios_rentabilidad,
            'ratios_solvencia': ratios_solvencia,
            'ratios_mercado': ratios_mercado,
            'info_financiera': info_financiera,
            'fecha_actualizacion': datetime.now()
        }
        
        print(f"✅ Datos obtenidos para {empresa_info['nombre']}")
        print(f"   🏢 Sector: {empresa_info['sector']}")
        print(f"   🌍 País: {empresa_info['pais']}")
        print(f"   💰 Market Cap: ${ratios_valuacion['Market_Cap']:,}" if ratios_valuacion['Market_Cap'] else "   💰 Market Cap: N/A")
        
        return datos_completos
        
    except Exception as e:
        print(f"❌ Error obteniendo datos para {ticker}: {str(e)}")
        return {
            'error': str(e),
            'ticker': ticker,
            'fecha_error': datetime.now()
        }

def calcular_ratios_sector(tickers_sector, nombre_sector="Sector"):
    """
    Calcula y compara ratios fundamentales para un sector
    
    Parámetros:
    -----------
    tickers_sector : list
        Lista de tickers del sector a analizar
    nombre_sector : str, opcional
        Nombre del sector para reportes
    
    Retorna:
    --------
    pandas.DataFrame : Comparación sectorial de ratios
    """
    
    print(f"📊 Analizando sector: {nombre_sector}")
    print(f"🏢 Empresas: {tickers_sector}")
    
    datos_sector = {}
    
    for ticker in tickers_sector:
        print(f"\n📈 Procesando {ticker}...")
        datos = obtener_datos_fundamentales(ticker)
        
        if 'error' not in datos:
            # Extraer ratios clave para comparación
            datos_sector[ticker] = {
                # Información básica
                'Nombre': datos['info_empresa']['nombre'],
                'Sector': datos['info_empresa']['sector'],
                'País': datos['info_empresa']['pais'],
                
                # Valuación
                'Market_Cap': datos['ratios_valuacion']['Market_Cap'],
                'Enterprise_Value': datos['ratios_valuacion']['Enterprise_Value'],
                'P/E_Forward': datos['ratios_valuacion']['Forward_PE'],
                'P/E_Trailing': datos['ratios_valuacion']['Trailing_PE'],
                'PEG_Ratio': datos['ratios_valuacion']['PEG_Ratio'],
                'Price/Book': datos['ratios_valuacion']['Price_Book'],
                'Price/Sales': datos['ratios_valuacion']['Price_Sales'],
                'EV/EBITDA': datos['ratios_valuacion']['EV_EBITDA'],
                'EV/Revenue': datos['ratios_valuacion']['EV_Revenue'],
                
                # Rentabilidad
                'ROE': datos['ratios_rentabilidad']['ROE'],
                'ROA': datos['ratios_rentabilidad']['ROA'],
                'Operating_Margin': datos['ratios_rentabilidad']['Operating_Margin'],
                'Profit_Margin': datos['ratios_rentabilidad']['Profit_Margin'],
                'Gross_Margin': datos['ratios_rentabilidad']['Gross_Margin'],
                
                # Solvencia
                'Debt/Equity': datos['ratios_solvencia']['Debt_Equity'],
                'Current_Ratio': datos['ratios_solvencia']['Current_Ratio'],
                'Quick_Ratio': datos['ratios_solvencia']['Quick_Ratio'],
                
                # Mercado
                'Beta': datos['ratios_mercado']['Beta'],
                '52W_Change': datos['ratios_mercado']['52_Week_Change'],
                'Dividend_Yield': datos['ratios_mercado']['Dividend_Yield'],
                
                # Crecimiento
                'Revenue_Growth': datos['info_financiera']['Revenue_Growth'],
                'Earnings_Growth': datos['info_financiera']['Price_Earnings_Growth']
            }
        else:
            print(f"⚠️  No se pudieron obtener datos para {ticker}")
    
    if not datos_sector:
        print("❌ No se pudieron obtener datos para ninguna empresa del sector")
        return None
    
    # Convertir a DataFrame
    df_sector = pd.DataFrame(datos_sector).T
    
    # Calcular estadísticas sectoriales
    print(f"\n📊 === RESUMEN SECTORIAL: {nombre_sector} ===")
    print(f"🏢 Empresas analizadas: {len(df_sector)}")
    
    # Convertir columnas numéricas
    columnas_numericas = ['Market_Cap', 'P/E_Forward', 'P/E_Trailing', 'Price/Book', 
                         'ROE', 'ROA', 'Operating_Margin', 'Profit_Margin', 'Beta']
    
    for col in columnas_numericas:
        if col in df_sector.columns:
            df_sector[col] = pd.to_numeric(df_sector[col], errors='coerce')
    
    # Estadísticas descriptivas
    if 'P/E_Forward' in df_sector.columns:
        pe_promedio = df_sector['P/E_Forward'].mean()
        print(f"📈 P/E Forward promedio: {pe_promedio:.1f}" if not pd.isna(pe_promedio) else "📈 P/E Forward promedio: N/A")
    
    if 'ROE' in df_sector.columns:
        roe_promedio = df_sector['ROE'].mean()
        print(f"💰 ROE promedio: {roe_promedio:.1%}" if not pd.isna(roe_promedio) else "💰 ROE promedio: N/A")
    
    if 'Operating_Margin' in df_sector.columns:
        margin_promedio = df_sector['Operating_Margin'].mean()
        print(f"📊 Margen operativo promedio: {margin_promedio:.1%}" if not pd.isna(margin_promedio) else "📊 Margen operativo promedio: N/A")
    
    return df_sector

def identificar_lideres_rezagados(df_sector, metricas_clave=['P/E_Forward', 'ROE', 'Operating_Margin']):
    """
    Identifica líderes y rezagados del sector basado en métricas clave
    
    Parámetros:
    -----------
    df_sector : pandas.DataFrame
        DataFrame con datos sectoriales
    metricas_clave : list, opcional
        Lista de métricas para evaluar
    
    Retorna:
    --------
    dict : Análisis de líderes y rezagados
    """
    
    print("🏆 Identificando líderes y rezagados del sector...")
    
    if df_sector is None or df_sector.empty:
        return None
    
    analisis = {
        'lideres': {},
        'rezagados': {},
        'ranking': {}
    }
    
    for metrica in metricas_clave:
        if metrica in df_sector.columns:
            # Limpiar datos
            datos_metrica = df_sector[metrica].dropna()
            
            if len(datos_metrica) > 0:
                # Para P/E, menor es mejor; para ROE y márgenes, mayor es mejor
                if 'P/E' in metrica or 'Price' in metrica:
                    # Menor es mejor (valuación más atractiva)
                    lider = datos_metrica.idxmin()
                    rezagado = datos_metrica.idxmax()
                    ranking = datos_metrica.sort_values()
                else:
                    # Mayor es mejor (rentabilidad, márgenes)
                    lider = datos_metrica.idxmax()
                    rezagado = datos_metrica.idxmin()
                    ranking = datos_metrica.sort_values(ascending=False)
                
                analisis['lideres'][metrica] = {
                    'empresa': lider,
                    'valor': datos_metrica[lider]
                }
                
                analisis['rezagados'][metrica] = {
                    'empresa': rezagado,
                    'valor': datos_metrica[rezagado]
                }
                
                analisis['ranking'][metrica] = ranking
                
                print(f"📊 {metrica}:")
                print(f"   🥇 Líder: {lider} ({datos_metrica[lider]:.2f})")
                print(f"   🔻 Rezagado: {rezagado} ({datos_metrica[rezagado]:.2f})")
    
    return analisis

def analizar_empresa(ticker, incluir_competidores=True, competidores=None):
    """
    Análisis integral de una empresa específica
    
    Parámetros:
    -----------
    ticker : str
        Ticker de la empresa a analizar
    incluir_competidores : bool, opcional
        Si incluir análisis de competidores
    competidores : list, opcional
        Lista de competidores a incluir
    
    Retorna:
    --------
    dict : Análisis completo de la empresa
    """
    
    print(f"🔍 === ANÁLISIS INTEGRAL: {ticker} ===")
    
    # 1. Datos fundamentales de la empresa
    datos_empresa = obtener_datos_fundamentales(ticker)
    
    if 'error' in datos_empresa:
        return datos_empresa
    
    # 2. Análisis FODA básico basado en ratios
    foda = generar_foda_basico(datos_empresa)
    
    # 3. Análisis de competidores si se solicita
    analisis_competitivo = None
    if incluir_competidores and competidores:
        print(f"\n🏢 Analizando competidores: {competidores}")
        todas_empresas = [ticker] + competidores
        analisis_competitivo = calcular_ratios_sector(todas_empresas, "Análisis Competitivo")
    
    # 4. Evaluación de ventajas competitivas
    ventajas_competitivas = evaluar_ventajas_competitivas(datos_empresa)
    
    # 5. Análisis de riesgos
    riesgos = identificar_riesgos(datos_empresa)
    
    # 6. Consolidar análisis
    analisis_completo = {
        'ticker': ticker,
        'datos_fundamentales': datos_empresa,
        'analisis_foda': foda,
        'ventajas_competitivas': ventajas_competitivas,
        'riesgos_identificados': riesgos,
        'analisis_competitivo': analisis_competitivo,
        'fecha_analisis': datetime.now()
    }
    
    return analisis_completo

def generar_foda_basico(datos_empresa):
    """
    Genera un análisis FODA básico basado en ratios financieros
    
    Parámetros:
    -----------
    datos_empresa : dict
        Datos fundamentales de la empresa
    
    Retorna:
    --------
    dict : Análisis FODA
    """
    
    fortalezas = []
    oportunidades = []
    debilidades = []
    amenazas = []
    
    ratios_val = datos_empresa['ratios_valuacion']
    ratios_rent = datos_empresa['ratios_rentabilidad']
    ratios_solv = datos_empresa['ratios_solvencia']
    ratios_merc = datos_empresa['ratios_mercado']
    
    # Análisis de fortalezas
    if ratios_rent['ROE'] and ratios_rent['ROE'] > 0.15:
        fortalezas.append(f"ROE alto ({ratios_rent['ROE']:.1%}) - Buena rentabilidad sobre el patrimonio")
    
    if ratios_rent['Operating_Margin'] and ratios_rent['Operating_Margin'] > 0.15:
        fortalezas.append(f"Margen operativo alto ({ratios_rent['Operating_Margin']:.1%}) - Eficiencia operativa")
    
    if ratios_solv['Current_Ratio'] and ratios_solv['Current_Ratio'] > 2:
        fortalezas.append(f"Liquidez sólida (Ratio corriente: {ratios_solv['Current_Ratio']:.1f})")
    
    # Análisis de debilidades
    if ratios_rent['ROE'] and ratios_rent['ROE'] < 0.08:
        debilidades.append(f"ROE bajo ({ratios_rent['ROE']:.1%}) - Rentabilidad limitada")
    
    if ratios_solv['Debt_Equity'] and ratios_solv['Debt_Equity'] > 100:
        debilidades.append(f"Alto apalancamiento (D/E: {ratios_solv['Debt_Equity']:.0f}%) - Riesgo financiero")
    
    if ratios_rent['Operating_Margin'] and ratios_rent['Operating_Margin'] < 0.05:
        debilidades.append(f"Margen operativo bajo ({ratios_rent['Operating_Margin']:.1%}) - Presión en rentabilidad")
    
    # Análisis de oportunidades (basado en valuación)
    if ratios_val['Forward_PE'] and ratios_val['Forward_PE'] < 15:
        oportunidades.append(f"Valuación atractiva (P/E Forward: {ratios_val['Forward_PE']:.1f})")
    
    if ratios_val['Price_Book'] and ratios_val['Price_Book'] < 1.5:
        oportunidades.append(f"Cotiza cerca del valor libro (P/B: {ratios_val['Price_Book']:.1f})")
    
    # Análisis de amenazas
    if ratios_merc['Beta'] and ratios_merc['Beta'] > 1.5:
        amenazas.append(f"Alta volatilidad (Beta: {ratios_merc['Beta']:.1f}) - Mayor riesgo de mercado")
    
    if ratios_val['Forward_PE'] and ratios_val['Forward_PE'] > 30:
        amenazas.append(f"Valuación elevada (P/E Forward: {ratios_val['Forward_PE']:.1f}) - Riesgo de corrección")
    
    return {
        'Fortalezas': fortalezas,
        'Oportunidades': oportunidades,
        'Debilidades': debilidades,
        'Amenazas': amenazas
    }

def evaluar_ventajas_competitivas(datos_empresa):
    """
    Evalúa las posibles ventajas competitivas (economic moats)
    
    Parámetros:
    -----------
    datos_empresa : dict
        Datos fundamentales de la empresa
    
    Retorna:
    --------
    dict : Evaluación de ventajas competitivas
    """
    
    ventajas = {
        'moat_score': 0,  # Puntuación de 0-10
        'indicadores_positivos': [],
        'areas_preocupacion': [],
        'recomendaciones': []
    }
    
    ratios_rent = datos_empresa['ratios_rentabilidad']
    ratios_val = datos_empresa['ratios_valuacion']
    info_empresa = datos_empresa['info_empresa']
    
    # Indicadores de ventaja competitiva
    
    # 1. ROE consistentemente alto
    if ratios_rent['ROE'] and ratios_rent['ROE'] > 0.15:
        ventajas['moat_score'] += 2
        ventajas['indicadores_positivos'].append("ROE alto - Posible ventaja competitiva")
    
    # 2. Márgenes operativos elevados
    if ratios_rent['Operating_Margin'] and ratios_rent['Operating_Margin'] > 0.20:
        ventajas['moat_score'] += 2
        ventajas['indicadores_positivos'].append("Márgenes operativos elevados - Poder de pricing")
    
    # 3. Market cap grande (economías de escala)
    if ratios_val['Market_Cap'] and ratios_val['Market_Cap'] > 50_000_000_000:  # >$50B
        ventajas['moat_score'] += 1
        ventajas['indicadores_positivos'].append("Gran capitalización - Posibles economías de escala")
    
    # 4. Sector defensivo
    sectores_defensivos = ['Utilities', 'Consumer Staples', 'Healthcare']
    if info_empresa['sector'] in sectores_defensivos:
        ventajas['moat_score'] += 1
        ventajas['indicadores_positivos'].append(f"Sector defensivo ({info_empresa['sector']})")
    
    # Áreas de preocupación
    if ratios_rent['ROE'] and ratios_rent['ROE'] < 0.10:
        ventajas['areas_preocupacion'].append("ROE bajo - Ventaja competitiva limitada")
    
    if ratios_rent['Operating_Margin'] and ratios_rent['Operating_Margin'] < 0.10:
        ventajas['areas_preocupacion'].append("Márgenes operativos bajos - Presión competitiva")
    
    # Recomendaciones
    if ventajas['moat_score'] >= 5:
        ventajas['recomendaciones'].append("Empresa con ventajas competitivas sólidas")
    elif ventajas['moat_score'] >= 3:
        ventajas['recomendaciones'].append("Ventajas competitivas moderadas - Monitorear evolución")
    else:
        ventajas['recomendaciones'].append("Ventajas competitivas limitadas - Mayor riesgo competitivo")
    
    return ventajas

def identificar_riesgos(datos_empresa):
    """
    Identifica riesgos específicos de la empresa
    
    Parámetros:
    -----------
    datos_empresa : dict
        Datos fundamentales de la empresa
    
    Retorna:
    --------
    dict : Análisis de riesgos
    """
    
    riesgos = {
        'riesgos_financieros': [],
        'riesgos_operativos': [],
        'riesgos_mercado': [],
        'riesgos_especificos': [],
        'nivel_riesgo': 'Bajo'  # Bajo, Medio, Alto
    }
    
    ratios_solv = datos_empresa['ratios_solvencia']
    ratios_rent = datos_empresa['ratios_rentabilidad']
    ratios_merc = datos_empresa['ratios_mercado']
    info_empresa = datos_empresa['info_empresa']
    
    puntuacion_riesgo = 0
    
    # Riesgos financieros
    if ratios_solv['Debt_Equity'] and ratios_solv['Debt_Equity'] > 100:
        riesgos['riesgos_financieros'].append(f"Alto apalancamiento (D/E: {ratios_solv['Debt_Equity']:.0f}%)")
        puntuacion_riesgo += 2
    
    if ratios_solv['Current_Ratio'] and ratios_solv['Current_Ratio'] < 1:
        riesgos['riesgos_financieros'].append(f"Liquidez comprometida (Ratio corriente: {ratios_solv['Current_Ratio']:.1f})")
        puntuacion_riesgo += 2
    
    # Riesgos operativos
    if ratios_rent['Operating_Margin'] and ratios_rent['Operating_Margin'] < 0:
        riesgos['riesgos_operativos'].append("Márgenes operativos negativos")
        puntuacion_riesgo += 3
    
    if ratios_rent['ROE'] and ratios_rent['ROE'] < 0:
        riesgos['riesgos_operativos'].append("ROE negativo - Destrucción de valor")
        puntuacion_riesgo += 2
    
    # Riesgos de mercado
    if ratios_merc['Beta'] and ratios_merc['Beta'] > 1.5:
        riesgos['riesgos_mercado'].append(f"Alta volatilidad (Beta: {ratios_merc['Beta']:.1f})")
        puntuacion_riesgo += 1
    
    # Riesgos específicos por país
    if info_empresa['pais'] == 'Argentina':
        riesgos['riesgos_especificos'].extend([
            "Riesgo país - Inestabilidad macroeconómica",
            "Riesgo cambiario - Volatilidad del peso argentino",
            "Riesgo regulatorio - Posibles cambios en políticas"
        ])
        puntuacion_riesgo += 2
    
    # Determinar nivel de riesgo
    if puntuacion_riesgo >= 6:
        riesgos['nivel_riesgo'] = 'Alto'
    elif puntuacion_riesgo >= 3:
        riesgos['nivel_riesgo'] = 'Medio'
    else:
        riesgos['nivel_riesgo'] = 'Bajo'
    
    return riesgos

def valuar_empresa_dcf(ticker, tasa_crecimiento=0.05, tasa_descuento=0.10, años_proyeccion=5):
    """
    Valuación simplificada por DCF (Discounted Cash Flow)
    
    TAREA CRÍTICA: Los estudiantes deben entender y justificar los supuestos
    
    Parámetros:
    -----------
    ticker : str
        Ticker de la empresa
    tasa_crecimiento : float, opcional
        Tasa de crecimiento perpetuo (default: 5%)
    tasa_descuento : float, opcional
        WACC estimado (default: 10%)
    años_proyeccion : int, opcional
        Años de proyección explícita (default: 5)
    
    Retorna:
    --------
    dict : Resultados de la valuación DCF
    """
    
    print(f"💰 Valuando {ticker} por DCF...")
    print(f"   📈 Tasa crecimiento perpetuo: {tasa_crecimiento:.1%}")
    print(f"   💸 Tasa descuento (WACC): {tasa_descuento:.1%}")
    print(f"   📅 Años proyección: {años_proyeccion}")
    
    # Obtener datos de la empresa
    datos = obtener_datos_fundamentales(ticker)
    
    if 'error' in datos:
        return {'error': 'No se pudieron obtener datos para DCF'}
    
    # Extraer información financiera
    fcf_actual = datos['ratios_solvencia']['Free_Cashflow']
    total_debt = datos['ratios_solvencia']['Total_Debt']
    total_cash = datos['ratios_solvencia']['Total_Cash']
    market_cap = datos['ratios_valuacion']['Market_Cap']
    
    if not fcf_actual:
        return {'error': 'Free Cash Flow no disponible para DCF'}
    
    # Proyección de Free Cash Flows
    fcf_proyectado = []
    fcf_base = fcf_actual
    
    for año in range(1, años_proyeccion + 1):
        # Crecimiento decreciente: alto inicial, convergiendo a tasa perpetua
        tasa_año = tasa_crecimiento + (0.10 - tasa_crecimiento) * np.exp(-año/2)
        fcf_año = fcf_base * (1 + tasa_año)
        fcf_proyectado.append(fcf_año)
        fcf_base = fcf_año
    
    # Valor terminal
    fcf_terminal = fcf_proyectado[-1] * (1 + tasa_crecimiento)
    valor_terminal = fcf_terminal / (tasa_descuento - tasa_crecimiento)
    
    # Descontar flujos a valor presente
    vp_fcf = []
    for i, fcf in enumerate(fcf_proyectado, 1):
        vp = fcf / (1 + tasa_descuento) ** i
        vp_fcf.append(vp)
    
    # Valor presente del valor terminal
    vp_terminal = valor_terminal / (1 + tasa_descuento) ** años_proyeccion
    
    # Valor total de la empresa
    valor_empresa = sum(vp_fcf) + vp_terminal
    
    # Valor del equity (valor empresa - deuda neta)
    deuda_neta = (total_debt or 0) - (total_cash or 0)
    valor_equity = valor_empresa - deuda_neta
    
    # Obtener número de acciones (aproximado por market cap / precio actual)
    try:
        stock = yf.Ticker(ticker)
        precio_actual = stock.history(period='1d')['Close'].iloc[-1]
        acciones_circulacion = market_cap / precio_actual if market_cap and precio_actual else None
        precio_objetivo = valor_equity / acciones_circulacion if acciones_circulacion else None
    except:
        precio_actual = None
        precio_objetivo = None
        acciones_circulacion = None
    
    resultados_dcf = {
        'ticker': ticker,
        'supuestos': {
            'fcf_base': fcf_actual,
            'tasa_crecimiento': tasa_crecimiento,
            'tasa_descuento': tasa_descuento,
            'años_proyeccion': años_proyeccion
        },
        'proyecciones': {
            'fcf_proyectado': fcf_proyectado,
            'valor_terminal': valor_terminal,
            'vp_fcf': vp_fcf,
            'vp_terminal': vp_terminal
        },
        'valuacion': {
            'valor_empresa': valor_empresa,
            'deuda_neta': deuda_neta,
            'valor_equity': valor_equity,
            'precio_actual': precio_actual,
            'precio_objetivo': precio_objetivo,
            'upside_downside': (precio_objetivo / precio_actual - 1) if precio_objetivo and precio_actual else None
        },
        'fecha_valuacion': datetime.now()
    }
    
    # Mostrar resultados
    print(f"✅ Valuación DCF completada:")
    print(f"   🏢 Valor empresa: ${valor_empresa:,.0f}")
    print(f"   💰 Valor equity: ${valor_equity:,.0f}")
    if precio_objetivo and precio_actual:
        print(f"   🎯 Precio objetivo: ${precio_objetivo:.2f}")
        print(f"   📊 Precio actual: ${precio_actual:.2f}")
        print(f"   📈 Upside/Downside: {(precio_objetivo/precio_actual-1):.1%}")
    
    return resultados_dcf

# Ejemplo de uso
if __name__ == "__main__":
    print("🧪 Testing módulo fundamental_analysis...")
    
    # Test con Apple
    try:
        print("Testing análisis fundamental de Apple...")
        analisis_aapl = analizar_empresa('AAPL', incluir_competidores=True, 
                                       competidores=['MSFT', 'GOOGL'])
        
        print("Testing valuación DCF...")
        dcf_aapl = valuar_empresa_dcf('AAPL')
        
        print("✅ Tests completados exitosamente")
        
    except Exception as e:
        print(f"❌ Error en tests: {e}")
