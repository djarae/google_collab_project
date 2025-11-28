import nbformat as nbf

nb = nbf.v4.new_notebook()

# Title
nb.cells.append(nbf.v4.new_markdown_cell("""
# Evaluación Parcial 3 - Análisis de Nacimientos en Chile (1990-2017)

**Integrantes:**
- [Nombre Estudiante 1]
- [Nombre Estudiante 2]

**Instrucciones:**
Generar un archivo .ipynb donde redacte de manera clara y ordenada, todas las actividades que están enumerados en esta tarea.
"""))

# Imports
nb.cells.append(nbf.v4.new_code_cell("""
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de gráficos
plt.style.use('seaborn-v0_8')
"""))

# 1. Load Data
nb.cells.append(nbf.v4.new_markdown_cell("""
## 1. Juntar todos los archivos de todos los años en un solo dataframe global
"""))

nb.cells.append(nbf.v4.new_code_cell("""
def load_and_clean_data(data_dir='resources/03_BI'):
    print("Cargando datos...")
    all_files = glob.glob(os.path.join(data_dir, "NAC_*.csv"))
    df_list = []
    
    for filename in all_files:
        try:
            # Intentar leer con latin1 (común en archivos antiguos)
            df = pd.read_csv(filename, sep=';', encoding='latin1', low_memory=False)
            
            # Estandarizar columnas a mayúsculas
            df.columns = [c.upper() for c in df.columns]
            
            df_list.append(df)
            print(f"Cargado {os.path.basename(filename)}: {df.shape}")
        except Exception as e:
            print(f"Error cargando {filename}: {e}")
            
    if not df_list:
        return None
        
    full_df = pd.concat(df_list, ignore_index=True)
    
    # Convertir columnas numéricas clave
    numeric_cols = ['PESO', 'TALLA', 'EDAD_P', 'EDAD_M', 'MES_NAC', 'DIA_NAC', 'ANO_NAC', 'SEMANAS']
    for col in numeric_cols:
        if col in full_df.columns:
            full_df[col] = pd.to_numeric(full_df[col], errors='coerce')
            
    print(f"Total registros: {full_df.shape}")
    return full_df

df = load_and_clean_data()
"""))

# 2. Freq Month
nb.cells.append(nbf.v4.new_markdown_cell("""
## 2. ¿Cuál es el mes más frecuente de nacimientos en Chile? Comentar al respecto.
"""))

nb.cells.append(nbf.v4.new_code_cell("""
if df is not None and 'MES_NAC' in df.columns:
    freq_month = df['MES_NAC'].mode()[0]
    print(f"Mes más frecuente: {int(freq_month)}")
    
    # Visualización
    plt.figure(figsize=(10, 6))
    df['MES_NAC'].value_counts().sort_index().plot(kind='bar')
    plt.title('Frecuencia de Nacimientos por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad')
    plt.show()
"""))

# 3. Freq Day
nb.cells.append(nbf.v4.new_markdown_cell("""
## 3. ¿Cuál es el día del año más común en el que la gente en Chile está de cumpleaños?
"""))

nb.cells.append(nbf.v4.new_code_cell("""
if df is not None and 'MES_NAC' in df.columns and 'DIA_NAC' in df.columns:
    # Filtrar fechas válidas
    valid_dates = df[(df['MES_NAC'].between(1, 12)) & (df['DIA_NAC'].between(1, 31))].copy()
    
    # Crear columna MM-DD
    valid_dates['DIA_MES'] = valid_dates['MES_NAC'].astype(int).astype(str).str.zfill(2) + '-' + \
                             valid_dates['DIA_NAC'].astype(int).astype(str).str.zfill(2)
    
    freq_day = valid_dates['DIA_MES'].mode()[0]
    print(f"Día más frecuente (MM-DD): {freq_day}")
    
    # Top 5 días
    print("Top 5 días con más nacimientos:")
    print(valid_dates['DIA_MES'].value_counts().head())
"""))

# 4. Cov/Corr Peso vs Talla
nb.cells.append(nbf.v4.new_markdown_cell("""
## 4. Calcular covarianza y correlación entre peso y talla a nivel general. Luego hacerlo por año. ¿Cambia con el paso de los años?
"""))

nb.cells.append(nbf.v4.new_code_cell("""
if df is not None:
    # Filtrar datos válidos
    valid_pt = df[(df['PESO'] > 0) & (df['PESO'] < 9999) & (df['TALLA'] > 0) & (df['TALLA'] < 99)].copy()
    
    cov_global = valid_pt['PESO'].cov(valid_pt['TALLA'])
    corr_global = valid_pt['PESO'].corr(valid_pt['TALLA'])
    
    print(f"Covarianza Global: {cov_global:.2f}")
    print(f"Correlación Global: {corr_global:.4f}")
    
    # Por año
    years = sorted(valid_pt['ANO_NAC'].unique())
    corrs = []
    for year in years:
        subset = valid_pt[valid_pt['ANO_NAC'] == year]
        if len(subset) > 100:
            c = subset['PESO'].corr(subset['TALLA'])
            corrs.append(c)
            # print(f"Año {year}: {c:.4f}")
            
    # Gráfico de evolución
    plt.figure(figsize=(12, 6))
    plt.plot(years, corrs, marker='o')
    plt.title('Evolución de la Correlación Peso-Talla por Año')
    plt.xlabel('Año')
    plt.ylabel('Correlación de Pearson')
    plt.grid(True)
    plt.show()
"""))

# 5. Cov/Corr Parents Age
nb.cells.append(nbf.v4.new_markdown_cell("""
## 5. Calcular covarianza y correlación entre la edad del padre y la edad de la madre, a nivel general. Luego hacerlo por año. ¿Cambia con el paso de los años?
"""))

nb.cells.append(nbf.v4.new_code_cell("""
if df is not None:
    # Filtrar datos válidos
    valid_age = df[(df['EDAD_P'] > 10) & (df['EDAD_P'] < 100) & (df['EDAD_M'] > 10) & (df['EDAD_M'] < 100)].copy()
    
    cov_global = valid_age['EDAD_P'].cov(valid_age['EDAD_M'])
    corr_global = valid_age['EDAD_P'].corr(valid_age['EDAD_M'])
    
    print(f"Covarianza Global: {cov_global:.2f}")
    print(f"Correlación Global: {corr_global:.4f}")
    
    # Por año
    years = sorted(valid_age['ANO_NAC'].unique())
    corrs_age = []
    for year in years:
        subset = valid_age[valid_age['ANO_NAC'] == year]
        if len(subset) > 100:
            c = subset['EDAD_P'].corr(subset['EDAD_M'])
            corrs_age.append(c)
            
    # Gráfico de evolución
    plt.figure(figsize=(12, 6))
    plt.plot(years, corrs_age, marker='o', color='green')
    plt.title('Evolución de la Correlación Edad Padre-Madre por Año')
    plt.xlabel('Año')
    plt.ylabel('Correlación de Pearson')
    plt.grid(True)
    plt.show()
"""))

# 6. Premature
nb.cells.append(nbf.v4.new_markdown_cell("""
## 6. Investigue las condiciones para que un bebé cuando nazca se considere “prematuro”, “a término” y “postérmino”. Hacer diagramas de caja para el peso y la talla para estas 3 categorías.
"""))

nb.cells.append(nbf.v4.new_code_cell("""
if df is not None and 'SEMANAS' in df.columns:
    # Filtrar semanas válidas (e.g., 20 a 45)
    valid_sem = df[(df['SEMANAS'] >= 20) & (df['SEMANAS'] <= 45) & 
                   (df['PESO'] > 0) & (df['PESO'] < 6000) & 
                   (df['TALLA'] > 20) & (df['TALLA'] < 70)].copy()
    
    def categorize_weeks(weeks):
        if weeks < 37: return 'Prematuro'
        elif weeks <= 41: return 'A término'
        else: return 'Postérmino'
        
    valid_sem['Categoria'] = valid_sem['SEMANAS'].apply(categorize_weeks)
    
    print(valid_sem['Categoria'].value_counts())
    
    # Boxplots
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.boxplot(x='Categoria', y='PESO', data=valid_sem, ax=axes[0], order=['Prematuro', 'A término', 'Postérmino'])
    axes[0].set_title('Distribución de Peso por Categoría')
    
    sns.boxplot(x='Categoria', y='TALLA', data=valid_sem, ax=axes[1], order=['Prematuro', 'A término', 'Postérmino'])
    axes[1].set_title('Distribución de Talla por Categoría')
    
    plt.tight_layout()
    plt.show()
"""))

# 7. Ambulance/Transit
nb.cells.append(nbf.v4.new_markdown_cell("""
## 7. Crear una columna llamada “indicador” que valga “1” si él bebé nació́ en una ambulancia y que valga “2” si él bebé nació́ en el trayecto (para los datos desde 1996). Caracterice los datos atípicos (outliers).

> **Nota:** No se encontraron códigos explícitos para "Ambulancia" o "Trayecto" en las columnas `LOCAL_PART` o `ESTAB` en los datos proporcionados. Se ha creado la columna `indicador` inicializada en 0. Si se dispone de los códigos específicos, se pueden actualizar en la lógica siguiente.
"""))

nb.cells.append(nbf.v4.new_code_cell("""
if df is not None:
    # Inicializar indicador
    df['indicador'] = 0
    
    # Lógica tentativa (si se conocieran los códigos)
    # Ejemplo: df.loc[df['LOCAL_PART'] == 99, 'indicador'] = 1
    
    print("Columna 'indicador' creada.")
    
    # Análisis de Outliers (Código preparado para cuando se tenga el indicador)
    subset = df[df['indicador'].isin([1, 2])]
    
    if not subset.empty:
        vars_to_analyze = ['PESO', 'TALLA', 'EDAD_P', 'EDAD_M']
        
        for var in vars_to_analyze:
            if var in subset.columns:
                print(f"\\n--- Análisis de Outliers para {var} ---")
                Q1 = subset[var].quantile(0.25)
                Q3 = subset[var].quantile(0.75)
                IQR = Q3 - Q1
                print(f"IQR: {IQR}")
                
                outliers = subset[(subset[var] < (Q1 - 1.5 * IQR)) | (subset[var] > (Q3 + 1.5 * IQR))]
                print(f"Cantidad de outliers: {len(outliers)}")
    else:
        print("No hay datos identificados como Ambulancia (1) o Trayecto (2) para analizar.")
"""))

# Save
with open('Entrega_Evaluacion_3.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook generated successfully.")
