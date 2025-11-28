# 🚀 Guía Completa: Cómo Ejecutar el Notebook en Google Colab

## 📋 Requisitos Previos

- Cuenta de Google (Gmail)
- Archivos CSV de nacimientos (NAC_1990.csv a NAC_2017.csv)
- Navegador web actualizado

---

## 🎯 Paso 1: Subir el Notebook a Google Colab

### Opción A: Desde Google Drive (Recomendado)

1. **Subir el notebook a Google Drive**:
   - Abre [Google Drive](https://drive.google.com)
   - Crea una carpeta llamada "Evaluacion_Parcial_4"
   - Arrastra el archivo `Entrega_Evaluacion_4.ipynb` a esa carpeta

2. **Abrir con Google Colab**:
   - Haz clic derecho en `Entrega_Evaluacion_4.ipynb`
   - Selecciona "Abrir con" → "Google Colaboratory"
   - Si no aparece Colaboratory, selecciona "Conectar más aplicaciones" y busca "Colaboratory"

### Opción B: Subida Directa

1. Ve a [Google Colab](https://colab.research.google.com/)
2. Haz clic en "Archivo" → "Subir notebook"
3. Selecciona `Entrega_Evaluacion_4.ipynb` desde tu computadora

---

## 📁 Paso 2: Subir los Archivos CSV

Hay **dos formas** de subir los datos:

### Método 1: Subida Manual (Más Fácil)

1. En Google Colab, haz clic en el ícono de **carpeta** 📁 en el panel izquierdo
2. Haz clic en el ícono de **nueva carpeta** y crea una carpeta llamada `data`
3. Haz clic en el ícono de **subir archivo** (flecha hacia arriba)
4. Selecciona **TODOS** los archivos CSV (NAC_1990.csv a NAC_2017.csv)
5. Espera a que se suban todos los archivos

> ⚠️ **Nota**: Los archivos se borrarán cuando cierres la sesión. Deberás subirlos nuevamente cada vez.

### Método 2: Desde Google Drive (Más Rápido para Reusar)

1. **Subir CSVs a Google Drive**:
   - Crea una carpeta en Google Drive llamada "datos_nacimientos"
   - Sube todos los archivos CSV a esa carpeta

2. **Montar Google Drive en Colab**:
   Ejecuta esta celda en el notebook:
   
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
   
   - Autoriza el acceso cuando se te solicite
   - Los archivos estarán en `/content/drive/MyDrive/datos_nacimientos/`

3. **Modificar la ruta en el código**:
   Cambia `data_dir='data'` por:
   ```python
   data_dir='/content/drive/MyDrive/datos_nacimientos'
   ```

---

## ▶️ Paso 3: Ejecutar el Notebook

### Ejecución Básica

1. **Ejecutar celda por celda**:
   - Haz clic en una celda
   - Presiona `Shift + Enter` para ejecutarla
   - Espera a que termine antes de ejecutar la siguiente

2. **Ejecutar todo el notebook**:
   - Ve a "Entorno de ejecución" → "Ejecutar todas"
   - Espera a que todas las celdas se ejecuten (puede tardar 5-10 minutos)

### Orden de Ejecución

```
1. Imports y Configuración ✅
2. Punto 0: Análisis de Calidad ✅
3. Punto 1: Carga de Datos ✅
4. Punto 2: Mes Más Frecuente ✅
5. Punto 3: Día Más Común ✅
6. Punto 4: Correlación Peso-Talla ✅
7. Punto 5: Correlación Edad Padre-Madre ✅
8. Punto 6: Categorías Gestacionales ✅
9. Punto 7: Outliers ✅
```

---

## 🎨 Paso 4: Visualizar Resultados

- **Gráficos**: Se mostrarán automáticamente debajo de cada celda
- **Tablas**: Usa `display(df.head())` para ver datos
- **Estadísticas**: Se imprimirán en la salida de cada celda

---

## 💾 Paso 5: Guardar y Descargar

### Guardar el Notebook

1. **En Google Drive**:
   - "Archivo" → "Guardar"
   - Se guarda automáticamente en Drive

2. **Descargar a tu PC**:
   - "Archivo" → "Descargar" → "Descargar .ipynb"

### Descargar Resultados

Para guardar gráficos o datos:

```python
# Guardar un gráfico
plt.savefig('grafico.png', dpi=300, bbox_inches='tight')

# Descargar archivo
from google.colab import files
files.download('grafico.png')

# Guardar DataFrame a CSV
df.to_csv('datos_procesados.csv', index=False)
files.download('datos_procesados.csv')
```

---

## 🔧 Solución de Problemas

### Problema 1: "No se encontraron archivos NAC_*.csv"

**Solución**:
- Verifica que los archivos estén en la carpeta `data`
- Asegúrate de que los nombres sean exactos: `NAC_1990.csv`, `NAC_1991.csv`, etc.
- Revisa que la ruta en el código sea correcta

### Problema 2: Error de Memoria

**Solución**:
- Ve a "Entorno de ejecución" → "Cambiar tipo de entorno de ejecución"
- Selecciona "GPU" o "TPU" (tienen más RAM)
- Reinicia el entorno

### Problema 3: Sesión Desconectada

**Solución**:
- Google Colab desconecta después de 90 minutos de inactividad
- Simplemente vuelve a ejecutar las celdas
- Los archivos subidos se habrán borrado, deberás subirlos nuevamente

### Problema 4: Gráficos No Se Muestran

**Solución**:
- Asegúrate de tener `%matplotlib inline` al inicio
- Ejecuta de nuevo la celda de configuración
- Verifica que matplotlib esté importado correctamente

---

## 📊 Consejos y Mejores Prácticas

### ✅ Antes de Ejecutar

1. Lee todas las instrucciones del notebook
2. Asegúrate de tener todos los archivos CSV
3. Verifica que tengas buena conexión a internet

### ✅ Durante la Ejecución

1. No cierres la pestaña mientras se ejecuta
2. Espera a que cada celda termine antes de continuar
3. Lee los mensajes de salida para detectar errores

### ✅ Después de Ejecutar

1. Revisa todos los gráficos generados
2. Verifica que los resultados tengan sentido
3. Guarda una copia del notebook con resultados

---

## 🎓 Recursos Adicionales

### Documentación

- [Google Colab - Guía Oficial](https://colab.research.google.com/notebooks/intro.ipynb)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)

### Atajos de Teclado en Colab

- `Ctrl + Enter`: Ejecutar celda actual
- `Shift + Enter`: Ejecutar celda y avanzar
- `Ctrl + M + B`: Insertar celda abajo
- `Ctrl + M + A`: Insertar celda arriba
- `Ctrl + M + D`: Eliminar celda

---

## ❓ Preguntas Frecuentes

**P: ¿Cuánto tiempo tarda en ejecutarse todo el notebook?**  
R: Entre 5-15 minutos dependiendo del tamaño de los datos y la velocidad de conexión.

**P: ¿Puedo ejecutar el notebook sin conexión?**  
R: No, Google Colab requiere conexión a internet.

**P: ¿Los datos quedan guardados en Google?**  
R: Los archivos temporales se borran al cerrar la sesión. Si usas Google Drive, permanecen ahí.

**P: ¿Puedo compartir el notebook con mi compañero/a?**  
R: Sí, usa "Compartir" en la esquina superior derecha y envía el enlace.

**P: ¿Cómo exporto el notebook a PDF?**  
R: "Archivo" → "Imprimir" → "Guardar como PDF"

---

## 📝 Checklist Final

Antes de entregar, verifica:

- [ ] Todos los archivos CSV fueron cargados correctamente
- [ ] Todas las celdas se ejecutaron sin errores
- [ ] Todos los gráficos se visualizan correctamente
- [ ] Los nombres de los integrantes están actualizados
- [ ] El notebook está guardado en Google Drive
- [ ] Tienes una copia de respaldo descargada

---

## 🎉 ¡Listo!

Ahora tienes todo lo necesario para ejecutar el análisis completo en Google Colab.

Si encuentras algún problema no documentado aquí, revisa:
1. Los mensajes de error en las celdas
2. La documentación oficial de Google Colab
3. Consulta con tu profesor/a

**¡Éxito con tu evaluación!** 🚀
