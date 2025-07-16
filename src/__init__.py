"""
Trabajo Práctico - Análisis Integral de Inversiones
Universidad Tecnológica Nacional - Facultad Regional La Plata
Finanzas para Control Empresario

Módulo principal con funciones auxiliares para análisis financiero.

Autor: Cátedra Finanzas para Control Empresario
Año: 2025
"""

__version__ = "1.0.0"
__author__ = "Cátedra Finanzas UTN-FRLP"
__email__ = "finanzas@frlp.utn.edu.ar"

# Importaciones principales
from .data_utils import (
    obtener_datos_historicos,
    limpiar_datos,
    calcular_retornos
)

from .portfolio_utils import (
    calcular_metricas_riesgo,
    optimizar_portfolio,
    simular_portfolios,
    graficar_frontera_eficiente
)

from .technical_analysis import (
    calcular_medias_moviles,
    calcular_rsi,
    calcular_macd,
    calcular_bollinger_bands,
    backtest_estrategia
)

from .fundamental_analysis import (
    obtener_datos_fundamentales,
    calcular_ratios_sector,
    analizar_empresa
)

# Configuración por defecto
CONFIG = {
    'periodo_defecto': '5y',
    'ventana_volatilidad': 252,
    'nivel_confianza_var': 0.05,
    'costos_transaccion': 0.005,
    'restriccion_peso_max': 0.40,
    'restriccion_peso_min': 0.05
}

# Empresas asignadas
EMPRESAS_ASIGNADAS = {
    'Shortreder': {
        'empresa_principal': 'BYMA.BA',
        'sector': 'Servicios Financieros',
        'mercado': 'Argentina'
    },
    'Malacalza': {
        'empresa_principal': 'MELI',
        'sector': 'E-commerce/Fintech',
        'mercado': 'LATAM'
    },
    'Griffo': {
        'empresa_principal': 'TX',
        'sector': 'Siderúrgico',
        'mercado': 'Internacional'
    },
    'Moya': {
        'empresa_principal': 'KO',
        'sector': 'Bebidas',
        'mercado': 'Internacional'
    },
    'Villaverde': {
        'empresa_principal': 'AAPL',
        'sector': 'Tecnología',
        'mercado': 'Internacional'
    },
    'Serrano': {
        'empresa_principal': 'YPF.BA',
        'sector': 'Energía',
        'mercado': 'Argentina'
    },
    'Sack': {
        'empresa_principal': 'LOMA.BA',
        'sector': 'Materiales',
        'mercado': 'Argentina'
    }
}

# Índices de referencia
INDICES_REFERENCIA = {
    'Argentina': '^MERV',
    'Internacional': '^GSPC',  # S&P 500
    'LATAM': '^GSPC'  # S&P 500 como proxy
}

def obtener_config_alumno(apellido):
    """
    Obtiene la configuración específica para un alumno
    
    Parámetros:
    -----------
    apellido : str
        Apellido del alumno
    
    Retorna:
    --------
    dict : Configuración del alumno
    """
    if apellido not in EMPRESAS_ASIGNADAS:
        raise ValueError(f"Alumno '{apellido}' no encontrado. Alumnos disponibles: {list(EMPRESAS_ASIGNADAS.keys())}")
    
    config = EMPRESAS_ASIGNADAS[apellido].copy()
    config['indice_referencia'] = INDICES_REFERENCIA[config['mercado']]
    
    return config

print(f"📊 Módulo de Análisis Financiero UTN-FRLP v{__version__} cargado exitosamente")
print(f"🎯 {len(EMPRESAS_ASIGNADAS)} empresas asignadas para análisis")
print(f"📚 Módulos disponibles: data_utils, portfolio_utils, technical_analysis, fundamental_analysis")