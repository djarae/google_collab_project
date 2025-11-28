"""
CSV Analysis Algorithm - Duplicate Detection and Pattern Analysis
Punto 0: Algoritmo para analizar cada CSV de manera efectiva
Objetivo: Identificar datos duplicados y patrones extraños en archivos NAC (1990-2017)
"""

import pandas as pd
import os
from pathlib import Path
import json
from datetime import datetime
import hashlib

class CSVAnalyzer:
    """Analizador completo de archivos CSV para detectar duplicados y anomalías"""
    
    def __init__(self, data_directory):
        self.data_directory = Path(data_directory)
        self.analysis_results = {}
        self.global_duplicates = []
        
    def analyze_single_csv(self, file_path):
        """
        Analiza un archivo CSV individual
        
        Returns:
            dict: Diccionario con métricas y hallazgos del archivo
        """
        file_name = file_path.name
        print(f"\n{'='*80}")
        print(f"Analizando: {file_name}")
        print(f"{'='*80}")
        
        analysis = {
            'file_name': file_name,
            'file_size_mb': file_path.stat().st_size / (1024 * 1024),
            'analysis_timestamp': datetime.now().isoformat(),
            'errors': [],
            'warnings': [],
            'metrics': {},
            'duplicates': {},
            'anomalies': []
        }
        
        try:
            # Intentar leer con diferentes delimitadores y encodings
            df = self._read_csv_flexible(file_path, analysis)
            
            if df is None:
                return analysis
            
            # Métricas básicas
            analysis['metrics']['total_rows'] = len(df)
            analysis['metrics']['total_columns'] = len(df.columns)
            analysis['metrics']['column_names'] = list(df.columns)
            analysis['metrics']['memory_usage_mb'] = df.memory_usage(deep=True).sum() / (1024 * 1024)
            
            # Análisis de duplicados
            self._analyze_duplicates(df, analysis)
            
            # Análisis de valores nulos
            self._analyze_null_values(df, analysis)
            
            # Análisis de tipos de datos
            self._analyze_data_types(df, analysis)
            
            # Análisis de patrones anómalos
            self._detect_anomalies(df, analysis, file_name)
            
            # Análisis de consistencia de datos
            self._analyze_data_consistency(df, analysis)
            
            # Crear hash de filas para comparación global
            self._create_row_hashes(df, analysis, file_name)
            
            print(f"✓ Análisis completado: {len(df)} filas, {len(df.columns)} columnas")
            
        except Exception as e:
            analysis['errors'].append(f"Error crítico: {str(e)}")
            print(f"✗ Error al analizar {file_name}: {str(e)}")
        
        return analysis
    
    def _read_csv_flexible(self, file_path, analysis):
        """Intenta leer el CSV con diferentes configuraciones"""
        
        # Configuraciones a probar
        configs = [
            {'sep': ';', 'encoding': 'utf-8', 'quotechar': '"'},
            {'sep': ';', 'encoding': 'latin-1', 'quotechar': '"'},
            {'sep': ';', 'encoding': 'iso-8859-1', 'quotechar': '"'},
            {'sep': ',', 'encoding': 'utf-8', 'quotechar': '"'},
            {'sep': ';', 'encoding': 'utf-8', 'quoting': 3},  # QUOTE_NONE
        ]
        
        for config in configs:
            try:
                df = pd.read_csv(file_path, **config, low_memory=False)
                analysis['read_config'] = config
                return df
            except Exception as e:
                continue
        
        analysis['errors'].append("No se pudo leer el archivo con ninguna configuración")
        return None
    
    def _analyze_duplicates(self, df, analysis):
        """Analiza duplicados en el DataFrame"""
        
        # Duplicados exactos (todas las columnas)
        duplicate_rows = df.duplicated()
        num_duplicates = duplicate_rows.sum()
        
        analysis['duplicates']['exact_duplicates'] = {
            'count': int(num_duplicates),
            'percentage': round((num_duplicates / len(df)) * 100, 2)
        }
        
        if num_duplicates > 0:
            analysis['warnings'].append(
                f"Se encontraron {num_duplicates} filas duplicadas exactas ({analysis['duplicates']['exact_duplicates']['percentage']}%)"
            )
        
        # Duplicados por subconjunto de columnas clave
        # Asumiendo que estas columnas identifican un registro único
        key_columns = []
        for col in ['SEXO', 'DIA_NAC', 'MES_NAC', 'ANO_NAC', 'TIPO_PARTO']:
            if col in df.columns:
                key_columns.append(col)
        
        if key_columns:
            subset_duplicates = df.duplicated(subset=key_columns)
            num_subset_duplicates = subset_duplicates.sum()
            
            analysis['duplicates']['key_column_duplicates'] = {
                'columns': key_columns,
                'count': int(num_subset_duplicates),
                'percentage': round((num_subset_duplicates / len(df)) * 100, 2)
            }
            
            if num_subset_duplicates > 0:
                analysis['warnings'].append(
                    f"Se encontraron {num_subset_duplicates} duplicados en columnas clave ({analysis['duplicates']['key_column_duplicates']['percentage']}%)"
                )
    
    def _analyze_null_values(self, df, analysis):
        """Analiza valores nulos en el DataFrame"""
        
        null_counts = df.isnull().sum()
        null_percentages = (null_counts / len(df)) * 100
        
        columns_with_nulls = null_counts[null_counts > 0].to_dict()
        
        analysis['metrics']['null_values'] = {
            'total_nulls': int(null_counts.sum()),
            'columns_with_nulls': {
                col: {
                    'count': int(count),
                    'percentage': round(null_percentages[col], 2)
                }
                for col, count in columns_with_nulls.items()
            }
        }
        
        # Advertir sobre columnas con muchos nulos
        for col, count in columns_with_nulls.items():
            if null_percentages[col] > 50:
                analysis['warnings'].append(
                    f"Columna '{col}' tiene {null_percentages[col]:.2f}% de valores nulos"
                )
    
    def _analyze_data_types(self, df, analysis):
        """Analiza los tipos de datos de las columnas"""
        
        dtypes_summary = df.dtypes.value_counts().to_dict()
        
        analysis['metrics']['data_types'] = {
            str(dtype): int(count) for dtype, count in dtypes_summary.items()
        }
    
    def _detect_anomalies(self, df, analysis, file_name):
        """Detecta patrones anómalos en los datos"""
        
        # Extraer año del nombre del archivo
        year = file_name.split('_')[1].split('.')[0]
        
        # Anomalía 1: Verificar que ANO_NAC coincida con el año del archivo
        if 'ANO_NAC' in df.columns:
            wrong_year = df[df['ANO_NAC'].astype(str) != year]
            if len(wrong_year) > 0:
                analysis['anomalies'].append({
                    'type': 'year_mismatch',
                    'description': f"Registros con ANO_NAC diferente a {year}",
                    'count': int(len(wrong_year)),
                    'percentage': round((len(wrong_year) / len(df)) * 100, 2)
                })
        
        # Anomalía 2: Valores fuera de rango en columnas numéricas
        if 'DIA_NAC' in df.columns:
            invalid_days = df[(df['DIA_NAC'] < 1) | (df['DIA_NAC'] > 31)]
            if len(invalid_days) > 0:
                analysis['anomalies'].append({
                    'type': 'invalid_day',
                    'description': 'Días de nacimiento inválidos (< 1 o > 31)',
                    'count': int(len(invalid_days))
                })
        
        if 'MES_NAC' in df.columns:
            invalid_months = df[(df['MES_NAC'] < 1) | (df['MES_NAC'] > 12)]
            if len(invalid_months) > 0:
                analysis['anomalies'].append({
                    'type': 'invalid_month',
                    'description': 'Meses de nacimiento inválidos (< 1 o > 12)',
                    'count': int(len(invalid_months))
                })
        
        # Anomalía 3: Filas completamente vacías
        empty_rows = df.isnull().all(axis=1).sum()
        if empty_rows > 0:
            analysis['anomalies'].append({
                'type': 'empty_rows',
                'description': 'Filas completamente vacías',
                'count': int(empty_rows)
            })
        
        # Anomalía 4: Columnas completamente vacías
        empty_cols = df.columns[df.isnull().all()].tolist()
        if empty_cols:
            analysis['anomalies'].append({
                'type': 'empty_columns',
                'description': 'Columnas completamente vacías',
                'columns': empty_cols
            })
    
    def _analyze_data_consistency(self, df, analysis):
        """Analiza la consistencia de los datos"""
        
        consistency_issues = []
        
        # Verificar valores únicos en columnas categóricas
        categorical_cols = ['SEXO', 'TIPO_PARTO', 'TIPO_ATENC', 'ATENC_PART']
        
        for col in categorical_cols:
            if col in df.columns:
                unique_values = df[col].nunique()
                value_counts = df[col].value_counts().to_dict()
                
                # Convertir keys a strings para JSON serialization
                value_counts_str = {str(k): int(v) for k, v in value_counts.items()}
                
                consistency_issues.append({
                    'column': col,
                    'unique_values': int(unique_values),
                    'top_5_values': value_counts_str
                })
        
        analysis['metrics']['consistency'] = consistency_issues
    
    def _create_row_hashes(self, df, analysis, file_name):
        """Crea hashes de filas para detectar duplicados entre archivos"""
        
        # Crear hash de cada fila para comparación global
        row_hashes = []
        for idx, row in df.iterrows():
            row_str = '|'.join([str(v) for v in row.values])
            row_hash = hashlib.md5(row_str.encode()).hexdigest()
            row_hashes.append({
                'file': file_name,
                'row_index': idx,
                'hash': row_hash
            })
        
        self.global_duplicates.extend(row_hashes)
        analysis['metrics']['row_hashes_created'] = len(row_hashes)
    
    def analyze_all_files(self):
        """Analiza todos los archivos CSV en el directorio"""
        
        csv_files = sorted(self.data_directory.glob('NAC_*.csv'))
        
        print(f"\n{'#'*80}")
        print(f"INICIANDO ANÁLISIS DE {len(csv_files)} ARCHIVOS CSV")
        print(f"{'#'*80}\n")
        
        for csv_file in csv_files:
            analysis = self.analyze_single_csv(csv_file)
            self.analysis_results[csv_file.name] = analysis
        
        # Detectar duplicados entre archivos
        self._detect_cross_file_duplicates()
        
        return self.analysis_results
    
    def _detect_cross_file_duplicates(self):
        """Detecta duplicados entre diferentes archivos"""
        
        print(f"\n{'='*80}")
        print("ANALIZANDO DUPLICADOS ENTRE ARCHIVOS")
        print(f"{'='*80}")
        
        # Crear diccionario de hashes
        hash_dict = {}
        for entry in self.global_duplicates:
            hash_val = entry['hash']
            if hash_val not in hash_dict:
                hash_dict[hash_val] = []
            hash_dict[hash_val].append({
                'file': entry['file'],
                'row': entry['row_index']
            })
        
        # Encontrar hashes que aparecen en múltiples archivos
        cross_file_dups = {
            hash_val: locations 
            for hash_val, locations in hash_dict.items() 
            if len(locations) > 1 and len(set(loc['file'] for loc in locations)) > 1
        }
        
        self.cross_file_duplicates = cross_file_dups
        
        print(f"✓ Se encontraron {len(cross_file_dups)} registros duplicados entre archivos")
    
    def generate_report(self, output_file='analysis_report.json'):
        """Genera un reporte completo del análisis"""
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'total_files_analyzed': len(self.analysis_results),
            'individual_file_analysis': self.analysis_results,
            'cross_file_duplicates': {
                'total_duplicate_groups': len(self.cross_file_duplicates),
                'sample_duplicates': dict(list(self.cross_file_duplicates.items())[:10])  # Primeros 10 ejemplos
            },
            'summary': self._generate_summary()
        }
        
        output_path = self.data_directory.parent / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'#'*80}")
        print(f"REPORTE GUARDADO EN: {output_path}")
        print(f"{'#'*80}\n")
        
        return output_path
    
    def _generate_summary(self):
        """Genera un resumen ejecutivo del análisis"""
        
        total_rows = sum(
            result['metrics'].get('total_rows', 0) 
            for result in self.analysis_results.values()
        )
        
        total_duplicates = sum(
            result['duplicates'].get('exact_duplicates', {}).get('count', 0)
            for result in self.analysis_results.values()
        )
        
        files_with_anomalies = sum(
            1 for result in self.analysis_results.values()
            if result.get('anomalies', [])
        )
        
        files_with_errors = sum(
            1 for result in self.analysis_results.values()
            if result.get('errors', [])
        )
        
        # Archivos sospechosos (más grandes de lo normal)
        avg_size = sum(
            result['file_size_mb'] 
            for result in self.analysis_results.values()
        ) / len(self.analysis_results)
        
        suspicious_files = [
            {
                'file': name,
                'size_mb': round(result['file_size_mb'], 2),
                'rows': result['metrics'].get('total_rows', 0)
            }
            for name, result in self.analysis_results.items()
            if result['file_size_mb'] > avg_size * 1.3  # 30% más grande que el promedio
        ]
        
        return {
            'total_records_analyzed': total_rows,
            'total_exact_duplicates': total_duplicates,
            'files_with_anomalies': files_with_anomalies,
            'files_with_errors': files_with_errors,
            'suspicious_files': suspicious_files,
            'average_file_size_mb': round(avg_size, 2)
        }
    
    def print_summary(self):
        """Imprime un resumen en consola"""
        
        summary = self._generate_summary()
        
        print(f"\n{'#'*80}")
        print("RESUMEN EJECUTIVO DEL ANÁLISIS")
        print(f"{'#'*80}\n")
        
        print(f"📊 Total de registros analizados: {summary['total_records_analyzed']:,}")
        print(f"🔄 Total de duplicados exactos: {summary['total_exact_duplicates']:,}")
        print(f"⚠️  Archivos con anomalías: {summary['files_with_anomalies']}")
        print(f"❌ Archivos con errores: {summary['files_with_errors']}")
        print(f"📁 Tamaño promedio de archivo: {summary['average_file_size_mb']:.2f} MB")
        
        if summary['suspicious_files']:
            print(f"\n🚨 ARCHIVOS SOSPECHOSOS (más grandes de lo normal):")
            for file_info in summary['suspicious_files']:
                print(f"   - {file_info['file']}: {file_info['size_mb']} MB ({file_info['rows']:,} filas)")
        
        print(f"\n{'#'*80}\n")


def main():
    """Función principal para ejecutar el análisis"""
    
    # Configurar el directorio de datos
    data_dir = Path(r"c:\Users\nidok\OneDrive\Documentos\REPOSITORIOS\google_collab_project\resources\03_BI")
    
    # Crear el analizador
    analyzer = CSVAnalyzer(data_dir)
    
    # Analizar todos los archivos
    results = analyzer.analyze_all_files()
    
    # Imprimir resumen
    analyzer.print_summary()
    
    # Generar reporte completo
    report_path = analyzer.generate_report('csv_analysis_report.json')
    
    print(f"✅ Análisis completado exitosamente!")
    print(f"📄 Reporte detallado: {report_path}")


if __name__ == "__main__":
    main()
