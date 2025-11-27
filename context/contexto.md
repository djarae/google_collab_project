Mira ,lee el pdf contiene informacion a anaziar. Lee tambien los csv , contienen informacion a analizar . Pues es bastante simple realmente. El requerimiento es hacerlo en google collab. La idea no es que lo haga la ia , pero si podria aprender a hacerlo con ella El profe tiende a pedir codigo de barras, de puntos , variabilidad etc Yo soy dev. asi que pensaba crear un algoritmo en python que analice los archivos uno por uno , un programa Pero nunca he usado google collab Si hago ese algoritmo en python en mi local ¿Puedo luego pasarlo a google collab? Pensaba dividir el algoritmo en dos partes 1 Analisis y limpiado de datos(por medio de un algoritmo creado) 2 Analisis de esos datos (creacion de diagramas etc.) Tambien una parte 0 , que seria un algoritmo o analisis para crear el algoritmo (analisador de patrone s repetitivos de algna forma optima ) En resumen, que harias? Revisa principalmente la pauta de evaluacion ,una vez obtenida la data es facil responder esas preguntas Pero debes analizar dos cosas: 1 Principalmente que se cumplan los puntos de la pauta de evaluacion 2 Un breve resumen de como responder las preguntas con la pauta analizada




🟦 CELDA 1 — Markdown
# Análisis Compacto de Datos de Nacimientos  
**Versión de aprendizaje: código limpio + explicaciones esenciales**

Este notebook realiza:

1. Carga automática de todos los archivos `NAC_*.csv`
2. Limpieza básica y estandarización
3. Unificación en un único dataframe
4. Estadísticas y análisis descriptivo
5. Frecuencias importantes
6. Correlación peso–talla
7. Detección de outliers (IQR)
8. Boxplots por categoría gestacional

🟦 CELDA 2 — Markdown
## 1. Cargar archivos CSV

Esta celda busca automáticamente todos los archivos CSV cuyo nombre comience con `NAC_`.

- Los concatena en un único dataframe
- Agrega una columna indicando el archivo origen

🟩 CELDA 3 — Código
import pandas as pd
import glob

# Busca archivos NAC_*.csv en el entorno
files = glob.glob("NAC_*.csv")

if not files:
    print("⚠️ No se encontraron archivos NAC_*.csv en el entorno.")
else:
    print("Archivos encontrados:", files)

dfs = []
for f in files:
    print("Cargando:", f)
    d = pd.read_csv(f, engine="python")
    d["archivo_origen"] = f
    dfs.append(d)

df = pd.concat(dfs, ignore_index=True)
df.head()

🟦 CELDA 4 — Markdown
## 2. Limpieza básica

En esta etapa:

- Convertimos columnas relevantes a tipo numérico
- Eliminamos valores imposibles (si corresponde)
- Confirmamos estructura del dataframe

🟩 CELDA 5 — Código
# Columnas que típicamente deben ser numéricas
num_cols = ['peso', 'talla', 'sem_gest', 'mes_nac', 'dia_nac', 'anio']

for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

df.describe(include='all').T

🟦 CELDA 6 — Markdown
## 3. Frecuencias y distribución temporal

Ejemplo: ¿Cuál es el mes con más nacimientos?

🟩 CELDA 7 — Código
if "mes_nac" in df.columns:
    print("Mes con mayor cantidad de nacimientos:")
    print(df["mes_nac"].value_counts().sort_index().idxmax())
else:
    print("No existe la columna mes_nac")

🟦 CELDA 8 — Markdown
## 4. Correlación entre peso y talla

Este análisis evalúa si existe relación lineal entre ambas variables.

Valores:
- **1.0** → correlación perfecta positiva  
- **0.0** → sin correlación  
- **-1.0** → correlación perfecta negativa  

🟩 CELDA 9 — Código
if set(["peso", "talla"]).issubset(df.columns):
    print(df[["peso", "talla"]].corr())
else:
    print("Faltan columnas peso o talla.")

🟦 CELDA 10 — Markdown
## 5. Detección de Outliers (IQR)

Regla estándar:  
Un valor es outlier si:

- `valor < Q1 - 1.5 * IQR`
- `valor > Q3 + 1.5 * IQR`

🟩 CELDA 11 — Código
def outliers_iqr(s):
    s = s.dropna()
    Q1 = s.quantile(0.25)
    Q3 = s.quantile(0.75)
    IQR = Q3 - Q1
    low = Q1 - 1.5 * IQR
    high = Q3 + 1.5 * IQR
    return s[(s < low) | (s > high)]

if "peso" in df.columns:
    print("Cantidad de outliers en peso:", len(outliers_iqr(df["peso"])))
else:
    print("No existe columna peso.")

🟦 CELDA 12 — Markdown
## 6. Boxplot de peso por categoría gestacional

Clasificación:

- Prematuro: < 37 semanas  
- Término: 37–41 semanas  
- Postérmino: ≥ 42 semanas  


🟩 CELDA 13 — Código
import matplotlib.pyplot as plt

def cat_gest(x):
    if pd.isna(x): return None
    if x < 37: return "prematuro"
    if x >= 42: return "postermino"
    return "termino"

if "sem_gest" in df.columns:
    df["categoria"] = df["sem_gest"].apply(cat_gest)

    groups = [
        df[df["categoria"] == "prematuro"]["peso"].dropna(),
        df[df["categoria"] == "termino"]["peso"].dropna(),
        df[df["categoria"] == "postermino"]["peso"].dropna(),
    ]

    plt.boxplot(groups, labels=["prematuro", "termino", "postermino"])
    plt.title("Boxplot de Peso por Categoría Gestacional")
    plt.ylabel("Peso (g)")
    plt.show()
else:
    print("No existe la columna sem_gest.")

🟦 CELDA 14 — Markdown
# Fin del Notebook

Este notebook:

- Limpia datos
- Combina múltiples CSV
- Calcula estadísticas clave
- Genera correlaciones
- Detecta outliers
- Produce boxplots gestacionales

Puedes extenderlo con:
- Gráficos adicionales
- Indicadores especiales
- Resumen PDF final para entregar