# 📊 Google Colab Project - Análisis de Datos de Nacimientos (1990-2017)

Proyecto de análisis de datos de nacimientos en Chile utilizando Python y Google Colab.

---

## 📁 Estructura del Proyecto

```
google_collab_project/
├── 📂 analysis/           # Algoritmos de análisis de datos
│   └── csv_analysis_algorithm.py
│
├── 📂 context/            # Contexto del problema y bibliotecas
│   ├── contexto.md
│   └── contexto_bibliotecas.md
│
├── 📂 docs/               # Documentación y reportes
│   ├── csv_analysis_summary.md
│   └── inspection_1996.txt
│
├── 📂 notebooks/          # Jupyter Notebooks
│   └── Entrega_Evaluacion_3.ipynb
│
├── 📂 resources/          # Datos y recursos
│   ├── 03_BI/            # Archivos CSV (NAC_1990.csv - NAC_2017.csv)
│   ├── csv_analysis_report.json
│   └── Evaluación Parcial 3 Instrucciones Encargo.pdf
│
└── 📂 scripts/            # Scripts de utilidad
    ├── analysis.py
    ├── deep_search_1996.py
    ├── deep_search_2017.py
    ├── extract_pdf.py
    ├── generate_notebook.py
    ├── inspect_1996.py
    ├── inspect_1996_full.py
    ├── inspect_data.py
    └── search_keywords.py
```

---

## 🎯 Descripción del Proyecto

Este proyecto analiza datos de nacimientos en Chile desde 1990 hasta 2017, con el objetivo de:

1. **Identificar duplicados** en los datos
2. **Detectar anomalías** y patrones extraños
3. **Analizar la calidad** de los datos
4. **Generar reportes** detallados

---

## 📊 Análisis Realizado

### Datos Analizados
- **28 archivos CSV** (NAC_1990.csv a NAC_2017.csv)
- **7,034,428 registros** de nacimientos
- **Periodo**: 1990-2017

### Hallazgos Principales
- ✅ **Duplicados exactos**: 544 registros (0.008%)
- ✅ **Sin duplicados entre archivos**
- ⚠️ **Anomalías menores**: ~100 registros con fechas inválidas
- 🔍 **Archivos sospechosos**: NAC_2014.csv y NAC_2009.csv (más grandes de lo normal)

Ver [`docs/csv_analysis_summary.md`](docs/csv_analysis_summary.md) para más detalles.

---

## 🚀 Uso

### Análisis de CSV

```bash
# Ejecutar el algoritmo de análisis completo
python analysis/csv_analysis_algorithm.py
```

Este script:
- Analiza todos los archivos CSV en `resources/03_BI/`
- Detecta duplicados exactos y en columnas clave
- Identifica anomalías (fechas inválidas, valores fuera de rango)
- Genera un reporte JSON completo

### Scripts de Utilidad

```bash
# Inspeccionar datos de un año específico
python scripts/inspect_data.py

# Búsqueda profunda en archivos específicos
python scripts/deep_search_1996.py
python scripts/deep_search_2017.py

# Generar notebook de Jupyter
python scripts/generate_notebook.py
```

---

## 📦 Dependencias

```bash
pip install pandas numpy jupyter
```

---

## 📄 Documentación

- **[Resumen de Análisis](docs/csv_analysis_summary.md)**: Hallazgos principales y recomendaciones
- **[Reporte Completo](resources/csv_analysis_report.json)**: Análisis detallado en formato JSON
- **[Contexto del Problema](context/contexto.md)**: Descripción del problema a resolver
- **[Contexto de Bibliotecas](context/contexto_bibliotecas.md)**: Información sobre bibliotecas utilizadas

---

## 🔧 Archivos Principales

### `analysis/csv_analysis_algorithm.py`
Algoritmo completo de análisis con clase `CSVAnalyzer`:
- Lectura flexible de CSV (múltiples encodings y delimitadores)
- Detección de duplicados (exactos, por columnas clave, cross-file)
- Detección de anomalías (valores inválidos, columnas vacías)
- Generación de reportes JSON

### `notebooks/Entrega_Evaluacion_3.ipynb`
Notebook principal para Google Colab con el análisis completo.

---

## 📈 Resultados

### Métricas Globales
- **Total de registros**: 7,034,428
- **Duplicados exactos**: 544 (0.008%)
- **Archivos con anomalías**: 7
- **Tamaño promedio**: 22.67 MB por archivo

### Distribución de Datos
- **Sexo**: ~51% Masculino, ~49% Femenino
- **Tipo de Parto**: ~96-98% Normal, ~1.5-2% Cesárea
- **Tipo de Atención**: ~70-75% Profesional, ~25-30% Institucional

---

## ⚠️ Notas Importantes

1. **Patrón de "duplicados"**: El 99.3% de registros aparecen como duplicados en columnas clave (SEXO, DIA_NAC, MES_NAC, ANO_NAC, TIPO_PARTO), pero esto es **normal** ya que múltiples bebés nacen el mismo día con las mismas características básicas.

2. **Archivos sospechosos**: NAC_2014.csv (39.7 MB) y NAC_2009.csv (29.9 MB) son significativamente más grandes que el promedio. Se recomienda investigar.

3. **Datos limpios**: En general, los datos están en excelente estado con menos del 0.01% de duplicados reales.

---

## 👥 Autor

Proyecto desarrollado para la Evaluación Parcial 3.

---

## 📝 Licencia

Este proyecto es parte de un trabajo académico.
