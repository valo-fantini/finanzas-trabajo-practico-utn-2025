# 📊 Trabajo Práctico: Análisis Integral de Inversiones

**Universidad Tecnológica Nacional - Facultad Regional La Plata**  
**Materia:** Finanzas para Control Empresario  
**Carrera:** Ingeniería Industrial  
**Año:** 2025  

## 🎯 Descripción

Este repositorio contiene el material base para el Trabajo Práctico Integral de la materia Finanzas para Control Empresario. Los estudiantes desarrollarán un análisis completo que incluye:

- **Análisis de Cartera de Acciones** (Teoría Moderna de Portfolios)
- **Análisis Técnico** (Indicadores y estrategias de trading)
- **Análisis Fundamental** (Valuación de empresas)

## 📋 Empresas Asignadas

| Empresa | Alumno | Ticker | Sector |
|---------|--------|--------|--------|
| BYMA | Shortreder | BYMA.BA | Servicios Financieros |
| MercadoLibre | Malacalza | MELI | E-commerce/Fintech |
| Ternium | Griffo | TX | Siderúrgico |
| Coca Cola | Moya | KO | Bebidas |
| Apple | Villaverde | AAPL | Tecnología |
| YPF | Serrano | YPF.BA | Energía |
| Loma Negra | Sack | LOMA.BA | Materiales |

## 🗂️ Estructura del Proyecto

```
finanzas-trabajo-practico-utn-2025/
│
├── 📄 README.md                     # Este archivo
├── 📋 CONSIGNAS.md                  # Consignas detalladas del TP
├── 📦 requirements.txt              # Dependencias Python
├── 🚫 .gitignore                   # Archivos a ignorar
│
├── 📊 notebooks/                   # Jupyter Notebooks por sección
│   ├── 01_obtencion_datos.ipynb
│   ├── 02_analisis_cartera.ipynb
│   ├── 03_analisis_tecnico.ipynb
│   ├── 04_analisis_fundamental.ipynb
│   └── 05_integracion_final.ipynb
│
├── 🐍 src/                        # Código Python auxiliar
│   ├── __init__.py
│   ├── data_utils.py
│   ├── portfolio_utils.py
│   ├── technical_analysis.py
│   └── fundamental_analysis.py
│
├── 📈 empresas/                    # Trabajos por empresa
│   ├── BYMA/
│   ├── MELI/
│   ├── TERNIUM/
│   └── ...
│
└── 📝 docs/                       # Documentación adicional
    ├── metodologia.md
    └── recursos.md
```

## 🚀 Instrucciones de Inicio

### 1. Fork del Repositorio
```bash
# 1. Hacer FORK de este repositorio a tu cuenta
# 2. Clonar tu fork
git clone https://github.com/TU_USUARIO/finanzas-trabajo-practico-utn-2025.git
cd finanzas-trabajo-practico-utn-2025
```

### 2. Configuración del Entorno
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Mac/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración Personal
```python
# En notebooks/config.py, modificar:
ALUMNO = "TU_APELLIDO"  # Ejemplo: "Malacalza"
EMPRESA_PRINCIPAL = "TU_TICKER"  # Ejemplo: "MELI"
```

### 4. Iniciar Jupyter
```bash
jupyter notebook
```

## 📊 Notebooks Disponibles

1. **01_obtencion_datos.ipynb** - Descarga y limpieza de datos
2. **02_analisis_cartera.ipynb** - Optimización de portfolios
3. **03_analisis_tecnico.ipynb** - Indicadores y señales
4. **04_analisis_fundamental.ipynb** - Ratios y valuación
5. **05_integracion_final.ipynb** - Síntesis y recomendación

## 🔄 Workflow de Trabajo

1. **Trabajo local** en tu fork
2. **Commits frecuentes** con mensajes descriptivos
3. **Push** a tu repositorio
4. **Pull Request** al finalizar para revisión

## 📝 Entregables

- ✅ Notebooks completados y documentados
- ✅ Informe ejecutivo (máximo 10 páginas)
- ✅ Código limpio y comentado
- ✅ Conclusiones y recomendaciones fundamentadas

## ⚖️ Criterios de Evaluación

| Aspecto | Peso | Descripción |
|---------|------|-------------|
| Metodología | 25% | Rigurosidad en análisis |
| Análisis Crítico | 30% | Interpretación y síntesis |
| Implementación | 25% | Calidad del código |
| Presentación | 20% | Claridad en comunicación |

## 🎓 Objetivos de Aprendizaje

Al completar este TP, habrás desarrollado:

- ✅ Competencias en análisis cuantitativo de inversiones
- ✅ Capacidad de integración de múltiples enfoques
- ✅ Criterio propio para toma de decisiones financieras
- ✅ Habilidades de programación en Python para finanzas
- ✅ Competencias de presentación y comunicación técnica

---

**¡Éxitos en el desarrollo del trabajo práctico!** 🚀

*Última actualización: Julio 2025*