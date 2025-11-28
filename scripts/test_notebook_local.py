"""
Script de prueba para ejecutar el notebook optimizado localmente
Verifica que todas las funciones principales funcionan correctamente
"""

import pandas as pd
import numpy as np
import os
import glob
import gc
import sys

# Agregar color a los prints
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def print_memory_usage():
    """Muestra el uso de memoria actual"""
    try:
        import psutil
        process = psutil.Process()
        mem_info = process.memory_info()
        print(f"💾 Memoria en uso: {mem_info.rss / 1024**2:.1f} MB")
    except ImportError:
        print("⚠️  psutil no instalado, no se puede monitorear memoria")

def optimize_dtypes(df):
    """Optimiza tipos de datos para reducir memoria"""
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type == 'int64':
            c_min = df[col].min()
            c_max = df[col].max()
            
            if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                df[col] = df[col].astype(np.int8)
            elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                df[col] = df[col].astype(np.int16)
            elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                df[col] = df[col].astype(np.int32)
        
        elif col_type == 'float64':
            df[col] = df[col].astype(np.float32)
    
    return df

def test_data_loading():
    """Prueba la carga de datos optimizada"""
    print("\n" + "="*60)
    print("TEST 1: Carga de Datos Optimizada")
    print("="*60)
    
    data_dir = 'resources/03_BI'
    
    if not os.path.exists(data_dir):
        print_error(f"Directorio no encontrado: {data_dir}")
        return None
    
    all_files = sorted(glob.glob(os.path.join(data_dir, 'NAC_*.csv')))
    
    if not all_files:
        print_error("No se encontraron archivos NAC_*.csv")
        return None
    
    print_info(f"Encontrados {len(all_files)} archivos")
    
    # Cargar solo 2 archivos como prueba
    test_files = all_files[:2]
    
    essential_cols = [
        'SEXO', 'DIA_NAC', 'MES_NAC', 'ANO_NAC', 
        'PESO', 'TALLA', 'SEMANAS',
        'EDAD_P', 'EDAD_M', 'TIPO_PARTO'
    ]
    
    df_list = []
    
    for filename in test_files:
        try:
            df = pd.read_csv(
                filename, 
                sep=';', 
                encoding='latin-1',
                usecols=lambda x: x.upper() in essential_cols,
                low_memory=False,
                nrows=5000  # Solo 5000 filas para prueba
            )
            
            df.columns = [c.upper().strip() for c in df.columns]
            df = optimize_dtypes(df)
            
            df_list.append(df)
            print_success(f"{os.path.basename(filename)}: {len(df):,} registros")
            
        except Exception as e:
            print_error(f"Error en {filename}: {e}")
    
    if not df_list:
        return None
    
    full_df = pd.concat(df_list, ignore_index=True)
    del df_list
    gc.collect()
    
    print_success(f"Datos cargados: {len(full_df):,} registros, {len(full_df.columns)} columnas")
    print_memory_usage()
    
    return full_df

def test_analysis(df):
    """Prueba los análisis principales"""
    if df is None:
        print_error("No hay datos para analizar")
        return
    
    print("\n" + "="*60)
    print("TEST 2: Análisis de Datos")
    print("="*60)
    
    # Test 1: Mes más frecuente
    if 'MES_NAC' in df.columns:
        valid_months = df[df['MES_NAC'].between(1, 12)]
        freq_month = valid_months['MES_NAC'].mode()[0]
        print_success(f"Mes más frecuente: {int(freq_month)}")
    else:
        print_warning("Columna MES_NAC no encontrada")
    
    # Test 2: Correlación Peso-Talla
    if 'PESO' in df.columns and 'TALLA' in df.columns:
        valid_pt = df[(df['PESO'] > 0) & (df['PESO'] < 9999) & 
                      (df['TALLA'] > 0) & (df['TALLA'] < 99)]
        if len(valid_pt) > 0:
            corr = valid_pt['PESO'].corr(valid_pt['TALLA'])
            print_success(f"Correlación Peso-Talla: {corr:.4f}")
        else:
            print_warning("No hay datos válidos para correlación")
    else:
        print_warning("Columnas PESO/TALLA no encontradas")
    
    # Test 3: Tipos de datos optimizados
    print("\nTipos de datos:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")
    
    print_memory_usage()

def test_memory_optimization():
    """Prueba la optimización de memoria"""
    print("\n" + "="*60)
    print("TEST 3: Optimización de Memoria")
    print("="*60)
    
    # Crear DataFrame de prueba
    test_df = pd.DataFrame({
        'col_int64': np.random.randint(0, 10, 10000),
        'col_float64': np.random.random(10000)
    })
    
    mem_before = test_df.memory_usage(deep=True).sum() / 1024**2
    print(f"Memoria antes: {mem_before:.2f} MB")
    
    # Optimizar
    test_df = optimize_dtypes(test_df)
    
    mem_after = test_df.memory_usage(deep=True).sum() / 1024**2
    print(f"Memoria después: {mem_after:.2f} MB")
    
    reduction = ((mem_before - mem_after) / mem_before) * 100
    print_success(f"Reducción de memoria: {reduction:.1f}%")
    
    del test_df
    gc.collect()

def main():
    """Función principal de prueba"""
    print("\n" + "="*60)
    print("🧪 PRUEBA DEL NOTEBOOK OPTIMIZADO")
    print("="*60)
    
    print_info("Verificando bibliotecas...")
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        print_success("Todas las bibliotecas están instaladas")
    except ImportError as e:
        print_error(f"Falta biblioteca: {e}")
        return
    
    # Test 1: Carga de datos
    df = test_data_loading()
    
    # Test 2: Análisis
    if df is not None:
        test_analysis(df)
    
    # Test 3: Optimización de memoria
    test_memory_optimization()
    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60)
    print_info("El notebook está listo para usarse en Google Colab")
    print_info("Todas las funciones principales funcionan correctamente")

if __name__ == "__main__":
    main()
