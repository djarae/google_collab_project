# 🔍 Análisis Completo de CSV - Detección de Duplicados (1990-2017)

## 📊 Resumen Ejecutivo

Se analizaron **28 archivos CSV** (NAC_1990.csv a NAC_2017.csv) conteniendo datos de nacimientos en Chile.

### Métricas Globales

- **Total de registros analizados**: 7,034,428 nacimientos
- **Total de duplicados exactos**: 544 registros (0.008%)
- **Archivos con anomalías**: 7 archivos
- **Archivos con errores**: 0
- **Tamaño promedio de archivo**: 22.67 MB

---

## 🚨 HALLAZGOS CRÍTICOS

### 1. **Duplicados en Columnas Clave (PATRÓN EXTRAÑO DETECTADO)**

> [!WARNING]
> **Se detectó un patrón anómalo extremadamente preocupante**: Aproximadamente el **99.3%** de los registros en CADA archivo aparecen como duplicados cuando se consideran las columnas clave (SEXO, DIA_NAC, MES_NAC, ANO_NAC, TIPO_PARTO).

**Esto significa que:**
- En un archivo con 273,775 registros (NAC_1994.csv), hay **272,054 duplicados** en columnas clave
- En un archivo con 292,145 registros (NAC_1990.csv), hay **290,038 duplicados** en columnas clave

**Interpretación:**
- Esto NO es necesariamente un error de datos duplicados
- Es **NORMAL** que múltiples bebés nazcan el mismo día, del mismo sexo, con el mismo tipo de parto
- Las columnas adicionales (PESO, TALLA, COMUNA, etc.) diferencian cada nacimiento individual
- **Conclusión**: Los datos parecen ser legítimos, no hay duplicados reales masivos

### 2. **Archivos Sospechosos por Tamaño**

> [!CAUTION]
> Dos archivos son significativamente más grandes que el promedio (30% más):

| Archivo | Tamaño (MB) | Registros | Observación |
|---------|-------------|-----------|-------------|
| **NAC_2009.csv** | 29.91 MB | 252,240 | 32% más grande que promedio |
| **NAC_2014.csv** | 39.70 MB | 250,997 | 75% más grande que promedio |

**Análisis:**
- NAC_2014.csv tiene casi el doble de tamaño que el promedio
- Ambos archivos tienen un número de registros similar a otros años
- **Posible causa**: Columnas adicionales, datos más detallados, o formato diferente
- **Recomendación**: Revisar la estructura de estos archivos específicamente

### 3. **Duplicados Exactos (Filas Idénticas)**

> [!IMPORTANT]
> Se encontraron **544 filas completamente duplicadas** en total:

**Distribución por año:**
- NAC_1990.csv: 49 duplicados (0.02%)
- NAC_1992.csv: 65 duplicados (0.02%)
- NAC_1991.csv: 29 duplicados (0.01%)
- NAC_1994.csv: 9 duplicados (0.00%)
- Y así sucesivamente...

**Conclusión**: La cantidad de duplicados exactos es **mínima** (menos del 0.01% del total)

### 4. **Duplicados Entre Archivos**

> [!NOTE]
> **No se encontraron duplicados entre archivos diferentes**
> - Total de grupos de duplicados cross-file: **0**
> - Esto confirma que cada archivo contiene datos únicos de su año correspondiente

---

## ⚠️ Anomalías Detectadas

### Datos Inválidos por Tipo

Se detectaron **7 archivos con anomalías**:

#### **Días de Nacimiento Inválidos** (< 1 o > 31)
- NAC_1990.csv: 19 registros
- NAC_1995.csv: 28 registros
- NAC_1994.csv: 5 registros

#### **Meses de Nacimiento Inválidos** (< 1 o > 12)
- NAC_1995.csv: 27 registros
- NAC_1994.csv: 5 registros

#### **Columnas Completamente Vacías**
- NAC_1996.csv: Columna 'ESTAB' tiene **99.58% de valores nulos** (263,686 de 264,793 registros)

---

## 📈 Análisis de Consistencia de Datos

### Distribución por Sexo (Consistente en todos los años)
- Sexo 1 (Masculino): ~51-52%
- Sexo 2 (Femenino): ~48-49%

### Tipo de Parto (Consistente)
- Tipo 1 (Normal): ~96-98%
- Tipo 2 (Cesárea): ~1.5-2%
- Tipo 9 (Desconocido): <1%
- Otros: <0.1%

### Tipo de Atención
- Tipo 2 (Profesional): ~70-75%
- Tipo 1 (Institucional): ~25-30%
- Tipo 3 (Otro): <1%

---

## 🔧 Estructura de Datos

### Variación de Columnas por Año

Los archivos tienen entre **27 y 33 columnas**, con variaciones en:

**Columnas comunes en todos los archivos:**
- SEXO, DIA_NAC, MES_NAC, ANO_NAC
- TIPO_PARTO, PESO, TALLA, SEMANAS
- EDAD_M (edad madre), EDAD_P (edad padre)
- COMUNA, REG_RES (región residencia)
- HIJ_VIVOS, HIJ_FALL, HIJ_MORT, HIJ_TOTAL

**Columnas que varían:**
- Nombres de columnas de atención: TIPO_ATENC vs ATENC_PART
- Nombres de columnas de lugar: LUGAR_PART vs LOCAL_PART
- Columnas adicionales en años específicos (ej: ESTAB en 1996)

---

## 💾 Calidad de Datos

### Valores Nulos
- **Mayoría de archivos**: Sin valores nulos o muy pocos (<0.01%)
- **Excepción**: NAC_1996.csv con columna ESTAB casi completamente vacía

### Tipos de Datos
- **Predominantemente numéricos**: int64 (27-30 columnas)
- **Algunos campos de texto**: object (2-4 columnas)
- **Campos mixtos**: float64 (0-1 columnas)

---

## ✅ Conclusiones y Recomendaciones

### ✅ Datos Generalmente Limpios
1. **No hay duplicados masivos reales** - El 99.3% de "duplicados" en columnas clave es normal
2. **Duplicados exactos mínimos** - Solo 544 de 7+ millones (0.008%)
3. **Sin duplicados entre archivos** - Cada año es independiente
4. **Estructura consistente** - Columnas principales presentes en todos los años

### ⚠️ Áreas de Atención

1. **NAC_2014.csv y NAC_2009.csv**
   - Investigar por qué son significativamente más grandes
   - Verificar si contienen columnas adicionales o datos más detallados

2. **Datos Inválidos**
   - Limpiar 19-28 registros con días inválidos
   - Limpiar 5-27 registros con meses inválidos
   - Total afectado: <100 registros de 7+ millones (despreciable)

3. **Columna ESTAB en NAC_1996.csv**
   - Considerar eliminar esta columna (99.58% vacía)

### 📋 Próximos Pasos Sugeridos

1. **Limpieza de Datos**
   ```python
   # Eliminar duplicados exactos (544 registros)
   df = df.drop_duplicates()
   
   # Filtrar días y meses inválidos
   df = df[(df['DIA_NAC'] >= 1) & (df['DIA_NAC'] <= 31)]
   df = df[(df['MES_NAC'] >= 1) & (df['MES_NAC'] <= 12)]
   ```

2. **Investigación Adicional**
   - Analizar en detalle NAC_2014.csv y NAC_2009.csv
   - Verificar la estructura de columnas en estos archivos

3. **Validación de Negocio**
   - Confirmar con expertos del dominio si los patrones detectados son esperados
   - Validar que las tasas de nacimientos por año son coherentes

---

## 📄 Archivos Generados

- **Reporte JSON completo**: `csv_analysis_report.json` (83 KB)
- **Script de análisis**: `csv_analysis_algorithm.py`
- **Este resumen**: `csv_analysis_summary.md`

---

**Fecha de análisis**: 2025-11-27  
**Algoritmo**: CSVAnalyzer v1.0  
**Total de archivos procesados**: 28  
**Tiempo de procesamiento**: ~9 minutos
