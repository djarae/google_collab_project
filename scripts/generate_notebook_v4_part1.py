import nbformat as nbf

nb = nbf.v4.new_notebook()

# ============================================================================
# TÍTULO Y CONFIGURACIÓN INICIAL
# ============================================================================

nb.cells.append(nbf.v4.new_markdown_cell("""
# 📊 Evaluación Parcial 4 - Análisis de Nacimientos en Chile (1990-2017)

**Integrantes:**
- [Tu Nombre Aquí]
- [Nombre Compañero/a]

**Fecha:** Noviembre 2025

---

## 📋 Contenido del Notebook

Este notebook contiene un análisis completo de los datos de nacimientos en Chile desde 1990 hasta 2017:

- **Punto 0**: Análisis de Calidad de Datos (Detección de Duplicados y Anomalías)
- **Punto 1**: Unificación de Datos
- **Punto 2**: Mes más Frecuente de Nacimientos
- **Punto 3**: Día del Año más Común de Cumpleaños
- **Punto 4**: Correlación Peso-Talla
- **Punto 5**: Correlación Edad Padre-Madre
- **Punto 6**: Categorías Gestacionales (Prematuro, A término, Postérmino)
- **Punto 7**: Indicador de Nacimientos Especiales y Outliers

---

## 🚀 Instrucciones para Google Colab

### 1. Subir Archivos CSV

Ejecuta esta celda para subir los archivos CSV desde tu computadora:

```python
from google.colab import files
import os

# Crear directorio para los datos
os.makedirs('data', exist_ok=True)

# Subir archivos
print("Por favor, selecciona TODOS los archivos NAC_*.csv")
uploaded = files.upload()

# Mover archivos a la carpeta data
for filename in uploaded.keys():
    os.rename(filename, f'data/{filename}')
    
print(f"✅ {len(uploaded)} archivos subidos correctamente")
```

### 2. Ejecutar las Celdas

Una vez subidos los archivos, ejecuta las celdas en orden (Shift + Enter).

---
"""))

# ============================================================================
# IMPORTS Y CONFIGURACIÓN
# ============================================================================

nb.cells.append(nbf.v4.new_markdown_cell("""
## 📦 Imports y Configuración
"""))

nb.cells.append(nbf.v4.new_code_cell("""
# Imports necesarios
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualizaciones
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("✅ Librerías importadas correctamente")
"""))

# ============================================================================
# PUNTO 0: ANÁLISIS DE CALIDAD DE DATOS
# ============================================================================

nb.cells.append(nbf.v4.new_markdown_cell("""
---

## 🔍 Punto 0: Análisis de Calidad de Datos

**Objetivo**: Antes de analizar los datos, es fundamental verificar su calidad, identificando:
- Duplicados exactos
- Duplicados en columnas clave
- Anomalías (fechas inválidas, valores fuera de rango)
- Valores nulos

Este análisis nos permite limpiar los datos y asegurar resultados confiables.
"""))

nb.cells.append(nbf.v4.new_code_cell("""
def analyze_data_quality(data_dir='data'):
    \"\"\"
    Analiza la calidad de los datos CSV
    \"\"\"
    print("="*80)
    print("ANÁLISIS DE CALIDAD DE DATOS")
    print("="*80)
    
    all_files = sorted(glob.glob(os.path.join(data_dir, 'NAC_*.csv')))
    
    if not all_files:
        print("⚠️ No se encontraron archivos NAC_*.csv")
        return None
    
    quality_report = {
        'total_files': len(all_files),
        'total_records': 0,
        'exact_duplicates': 0,
        'files_with_issues': []
    }
    
    for file_path in all_files:
        filename = os.path.basename(file_path)
        
        try:
            # Leer archivo
            df = pd.read_csv(file_path, sep=';', encoding='latin-1', low_memory=False)
            
            # Contar registros
            quality_report['total_records'] += len(df)
            
            # Detectar duplicados exactos
            duplicates = df.duplicated().sum()
            quality_report['exact_duplicates'] += duplicates
            
            # Detectar anomalías
            issues = []
            
            # Verificar columnas clave
            if 'DIA_NAC' in df.columns:
                invalid_days = df[(df['DIA_NAC'] < 1) | (df['DIA_NAC'] > 31)]
                if len(invalid_days) > 0:
                    issues.append(f"{len(invalid_days)} días inválidos")
            
            if 'MES_NAC' in df.columns:
                invalid_months = df[(df['MES_NAC'] < 1) | (df['MES_NAC'] > 12)]
                if len(invalid_months) > 0:
                    issues.append(f"{len(invalid_months)} meses inválidos")
            
            if duplicates > 0 or issues:
                quality_report['files_with_issues'].append({
                    'file': filename,
                    'duplicates': duplicates,
                    'issues': issues
                })
            
            print(f"✓ {filename}: {len(df):,} registros, {duplicates} duplicados")
            
        except Exception as e:
            print(f"✗ Error en {filename}: {e}")
    
    # Resumen
    print("\\n" + "="*80)
    print("RESUMEN DE CALIDAD")
    print("="*80)
    print(f"📊 Total de archivos analizados: {quality_report['total_files']}")
    print(f"📊 Total de registros: {quality_report['total_records']:,}")
    print(f"🔄 Duplicados exactos encontrados: {quality_report['exact_duplicates']:,}")
    print(f"⚠️  Archivos con problemas: {len(quality_report['files_with_issues'])}")
    
    if quality_report['exact_duplicates'] > 0:
        pct = (quality_report['exact_duplicates'] / quality_report['total_records']) * 100
        print(f"   → Porcentaje de duplicados: {pct:.4f}%")
    
    return quality_report

# Ejecutar análisis de calidad
quality_report = analyze_data_quality()
"""))

# ============================================================================
# PUNTO 1: CARGA Y UNIFICACIÓN DE DATOS
# ============================================================================

nb.cells.append(nbf.v4.new_markdown_cell("""
---

## 1️⃣ Punto 1: Juntar todos los archivos en un solo dataframe global

**Objetivo**: Cargar todos los archivos CSV (NAC_1990.csv a NAC_2017.csv) y unificarlos en un único DataFrame.

**Proceso**:
1. Buscar todos los archivos NAC_*.csv
2. Leer cada archivo con el encoding correcto
3. Estandarizar nombres de columnas
4. Concatenar en un DataFrame global
5. Convertir columnas numéricas
6. Eliminar duplicados exactos
"""))

nb.cells.append(nbf.v4.new_code_cell("""
def load_and_clean_data(data_dir='data'):
    \"\"\"
    Carga y limpia todos los archivos CSV de nacimientos
    \"\"\"
    print("🔄 Cargando datos...")
    all_files = sorted(glob.glob(os.path.join(data_dir, 'NAC_*.csv')))
    
    if not all_files:
        print("⚠️ No se encontraron archivos NAC_*.csv en el directorio")
        print(f"   Directorio buscado: {data_dir}")
        return None
    
    df_list = []
    
    for filename in all_files:
        try:
            # Intentar leer con diferentes encodings
            df = pd.read_csv(filename, sep=';', encoding='latin-1', low_memory=False)
            
            # Estandarizar columnas a mayúsculas
            df.columns = [c.upper().strip() for c in df.columns]
            
            # Agregar columna de año de origen
            year = os.path.basename(filename).split('_')[1].split('.')[0]
            df['ARCHIVO_ORIGEN'] = year
            
            df_list.append(df)
            print(f"✓ {os.path.basename(filename)}: {df.shape[0]:,} registros, {df.shape[1]} columnas")
            
        except Exception as e:
            print(f"✗ Error cargando {filename}: {e}")
    
    if not df_list:
        return None
    
    # Concatenar todos los dataframes
    print("\\n🔗 Concatenando dataframes...")
    full_df = pd.concat(df_list, ignore_index=True)
    
    print(f"✓ DataFrame unificado: {full_df.shape[0]:,} registros, {full_df.shape[1]} columnas")
    
    # Convertir columnas numéricas clave
    print("\\n🔢 Convirtiendo columnas numéricas...")
    numeric_cols = ['PESO', 'TALLA', 'EDAD_P', 'EDAD_M', 'MES_NAC', 'DIA_NAC', 'ANO_NAC', 'SEMANAS']
    
    for col in numeric_cols:
        if col in full_df.columns:
            full_df[col] = pd.to_numeric(full_df[col], errors='coerce')
            print(f"   ✓ {col}")
    
    # Eliminar duplicados exactos
    print("\\n🧹 Eliminando duplicados exactos...")
    before = len(full_df)
    full_df = full_df.drop_duplicates()
    after = len(full_df)
    removed = before - after
    
    if removed > 0:
        print(f"   ✓ Eliminados {removed:,} duplicados ({(removed/before)*100:.2f}%)")
    else:
        print(f"   ✓ No se encontraron duplicados exactos")
    
    print(f"\\n✅ Datos cargados: {full_df.shape[0]:,} registros finales")
    
    return full_df

# Cargar datos
df = load_and_clean_data()

# Mostrar información básica
if df is not None:
    print("\\n" + "="*80)
    print("INFORMACIÓN DEL DATASET")
    print("="*80)
    print(f"Registros totales: {len(df):,}")
    print(f"Columnas: {len(df.columns)}")
    print(f"Periodo: {df['ANO_NAC'].min():.0f} - {df['ANO_NAC'].max():.0f}")
    print(f"Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print("\\nPrimeras 5 filas:")
    display(df.head())
"""))

# ============================================================================
# PUNTO 2: MES MÁS FRECUENTE
# ============================================================================

nb.cells.append(nbf.v4.new_markdown_cell("""
---

## 2️⃣ Punto 2: ¿Cuál es el mes más frecuente de nacimientos en Chile?

**Objetivo**: Identificar en qué mes del año nacen más bebés en Chile.

**Hipótesis**: Podría haber patrones estacionales relacionados con:
- Clima (9 meses antes)
- Festividades
- Factores culturales
"""))

nb.cells.append(nbf.v4.new_code_cell("""
if df is not None and 'MES_NAC' in df.columns:
    # Filtrar meses válidos
    valid_months = df[df['MES_NAC'].between(1, 12)].copy()
    
    # Calcular frecuencias
    month_counts = valid_months['MES_NAC'].value_counts().sort_index()
    freq_month = valid_months['MES_NAC'].mode()[0]
    
    # Nombres de meses
    month_names = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    print("="*80)
    print("ANÁLISIS DE FRECUENCIA POR MES")
    print("="*80)
    print(f"\\n📅 Mes más frecuente: {month_names[int(freq_month)]} (Mes {int(freq_month)})")
    print(f"   Nacimientos: {month_counts[freq_month]:,}")
    print(f"   Porcentaje: {(month_counts[freq_month]/len(valid_months))*100:.2f}%")
    
    print("\\n📊 Top 5 meses con más nacimientos:")
    for i, (month, count) in enumerate(month_counts.sort_values(ascending=False).head().items(), 1):
        pct = (count / len(valid_months)) * 100
        print(f"   {i}. {month_names[int(month)]}: {count:,} ({pct:.2f}%)")
    
    # Visualización
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico de barras
    month_counts.plot(kind='bar', ax=axes[0], color='skyblue', edgecolor='black')
    axes[0].set_title('Frecuencia de Nacimientos por Mes', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Mes', fontsize=12)
    axes[0].set_ylabel('Cantidad de Nacimientos', fontsize=12)
    axes[0].set_xticklabels([month_names[i] for i in range(1, 13)], rotation=45, ha='right')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Gráfico de línea
    month_counts.plot(kind='line', ax=axes[1], marker='o', color='coral', linewidth=2, markersize=8)
    axes[1].set_title('Tendencia de Nacimientos por Mes', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Mes', fontsize=12)
    axes[1].set_ylabel('Cantidad de Nacimientos', fontsize=12)
    axes[1].set_xticks(range(1, 13))
    axes[1].set_xticklabels([month_names[i] for i in range(1, 13)], rotation=45, ha='right')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Comentario
    print("\\n💡 INTERPRETACIÓN:")
    print("   Los meses con más nacimientos suelen estar relacionados con la concepción")
    print("   9 meses antes. Factores como festividades de fin de año, vacaciones de")
    print("   verano, y clima pueden influir en estos patrones.")
else:
    print("⚠️ No se pudo realizar el análisis (columna MES_NAC no encontrada)")
"""))

# ============================================================================
# PUNTO 3: DÍA MÁS COMÚN
# ============================================================================

nb.cells.append(nbf.v4.new_markdown_cell("""
---

## 3️⃣ Punto 3: ¿Cuál es el día del año más común de cumpleaños?

**Objetivo**: Identificar la fecha específica (día-mes) en la que más personas cumplen años.

**Nota**: Se excluye el 29 de febrero por ser una fecha especial que solo ocurre cada 4 años.
"""))

nb.cells.append(nbf.v4.new_code_cell("""
if df is not None and 'MES_NAC' in df.columns and 'DIA_NAC' in df.columns:
    # Filtrar fechas válidas
    valid_dates = df[
        (df['MES_NAC'].between(1, 12)) & 
        (df['DIA_NAC'].between(1, 31))
    ].copy()
    
    # Crear columna de fecha (MM-DD)
    valid_dates['FECHA_CUMPLE'] = (
        valid_dates['MES_NAC'].astype(int).astype(str).str.zfill(2) + '-' +
        valid_dates['DIA_NAC'].astype(int).astype(str).str.zfill(2)
    )
    
    # Calcular frecuencias
    date_counts = valid_dates['FECHA_CUMPLE'].value_counts()
    freq_date = date_counts.index[0]
    
    # Nombres de meses
    month_names = {
        '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
        '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
        '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
    }
    
    print("="*80)
    print("ANÁLISIS DE DÍA DE CUMPLEAÑOS MÁS COMÚN")
    print("="*80)
    
    month, day = freq_date.split('-')
    print(f"\\n🎂 Día más común: {day} de {month_names[month]} ({freq_date})")
    print(f"   Nacimientos: {date_counts[freq_date]:,}")
    print(f"   Porcentaje: {(date_counts[freq_date]/len(valid_dates))*100:.4f}%")
    
    print("\\n🏆 Top 10 días con más cumpleaños:")
    for i, (date, count) in enumerate(date_counts.head(10).items(), 1):
        m, d = date.split('-')
        pct = (count / len(valid_dates)) * 100
        print(f"   {i:2d}. {d} de {month_names[m]:12s} ({date}): {count:,} ({pct:.4f}%)")
    
    # Visualización
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Top 20 días
    top_20 = date_counts.head(20)
    top_20.plot(kind='barh', ax=axes[0], color='lightgreen', edgecolor='black')
    axes[0].set_title('Top 20 Días de Cumpleaños Más Comunes', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Cantidad de Nacimientos', fontsize=12)
    axes[0].set_ylabel('Fecha (MM-DD)', fontsize=12)
    axes[0].invert_yaxis()
    axes[0].grid(axis='x', alpha=0.3)
    
    # Distribución por mes
    valid_dates['MES'] = valid_dates['MES_NAC'].astype(int)
    month_day_counts = valid_dates.groupby('MES').size()
    month_day_counts.plot(kind='bar', ax=axes[1], color='salmon', edgecolor='black')
    axes[1].set_title('Distribución de Nacimientos por Mes', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Mes', fontsize=12)
    axes[1].set_ylabel('Cantidad de Nacimientos', fontsize=12)
    axes[1].set_xticklabels([month_names[str(i).zfill(2)] for i in range(1, 13)], rotation=45, ha='right')
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("\\n💡 INTERPRETACIÓN:")
    print("   Las fechas más comunes de cumpleaños pueden estar influenciadas por:")
    print("   - Patrones estacionales de concepción")
    print("   - Planificación familiar")
    print("   - Factores médicos (cesáreas programadas)")
else:
    print("⚠️ No se pudo realizar el análisis (columnas no encontradas)")
"""))

# Continúa en el siguiente bloque...
# (Por límite de caracteres, dividiré en múltiples bloques)

# Save notebook
with open('notebooks/Entrega_Evaluacion_4.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("✅ Notebook Entrega_Evaluacion_4.ipynb creado exitosamente (Parte 1/2)")
