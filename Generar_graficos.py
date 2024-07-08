import os
import pandas as pd
import matplotlib.pyplot as plt

# Cambiar el directorio actual al directorio donde está guardado el script
os.chdir('ProyeccionCarteraBCP')

# Verificar el directorio actual
current_dir = os.getcwd()
print("Directorio actual:", current_dir)

# Ruta relativa dentro del repositorio clonado en GitHub
file_path = 'rebuilt.Copia de Informe_preliminarA.xlsx'

# Leer el archivo Excel
df = pd.read_excel(file_path, sheet_name='Base.gral', header=3)

# Crear una copia del DataFrame original
df_copia = df.copy()

# Cambiar el nombre de la primera columna a "Fecha"
df_copia.rename(columns={df_copia.columns[0]: 'Fecha',
                         df_copia.columns[13]: 'Mora_16_de_julio',
                         df_copia.columns[14]: 'Mora_Ceja',
                         df_copia.columns[15]: 'Total_Mora'}, inplace=True)

# Mostrar las primeras filas del nuevo DataFrame para verificar
print(df_copia.head())

# Eliminar "al " de la columna 'Fecha'
df_copia['Fecha'] = df_copia['Fecha'].str.replace('al ', '')

# Aplicar conversión a minúsculas a la columna 'Fecha'
df_copia['Fecha'] = df_copia['Fecha'].str.lower()

# Eliminar "de " de la columna 'Fecha'
df_copia['Fecha'] = df_copia['Fecha'].str.replace('de ', '')

# Reemplazar " " por "/"
df_copia['Fecha'] = df_copia['Fecha'].str.replace(' ', '/')

# Eliminar filas donde Mora_16 de julio sea NaN
df_copia = df_copia.dropna(subset=['Mora_16_de_julio'])

# Diccionario para mapear meses en español a números
meses_dict = {
    'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
    'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
    'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
}

# Aplicar el mapeo a la columna 'Fecha'
for mes, num in meses_dict.items():
    df_copia['Fecha'] = df_copia['Fecha'].str.replace(mes, num)

# Convertir a tipo datetime
df_copia['Fecha'] = pd.to_datetime(df_copia['Fecha'], format='%d/%m/%Y', errors='coerce')

# Formatear las fechas al formato 'dd-mm-yyyy'
df_copia['Fecha'] = df_copia['Fecha'].dt.strftime('%d-%m-%Y')

print(df_copia.dtypes)
print(df_copia.head())

# Crear DataFrame 'mora' con columnas específicas y ajuste de nombres
mora = df_copia.iloc[:, [0, 13, 14, 15]].copy()

mora['Mora_16_de_julio'] = mora['Mora_16_de_julio'] * 100
mora['Mora_Ceja'] = mora['Mora_Ceja'] * 100
mora['Total_Mora'] = mora['Total_Mora'] * 100

# Mostrar las primeras filas para verificar
print(mora.head())

# Eliminar filas donde Mora_16 de julio sea NaN
mora = mora.dropna(subset=['Mora_16_de_julio'])

# Mostrar las primeras filas para verificar
print(mora.head())

# Directorio de salida para los gráficos
output_dir = current_dir


# Directorio de salida para los gráficos
output_dir = current_dir

# Función para crear y guardar los gráficos
def crear_y_guardar_grafico(df, columna, color, titulo, nombre_archivo):
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Fecha'], df[columna], color=color, label=columna, marker='o')
    plt.plot(df['Fecha'], df[columna], color=color, linestyle='-', linewidth=1)
    plt.title(titulo)
    plt.xlabel('Fecha')
    plt.ylabel('Valor')
    plt.xticks(df['Fecha'], rotation=45, ha='right')  # Mostrar todas las fechas en el eje x
    plt.ylim(-1.1, 1.1)  # Limitar el rango del eje y
    plt.axhline(y=0, color='black', linestyle='--')  # Agregar línea horizontal en el eje x en 0
    plt.legend()
    plt.tight_layout()
    
    # Guardar el gráfico como una imagen
    plt.savefig(os.path.join(output_dir, nombre_archivo))
    
    plt.show()

# Crear y guardar gráficos
crear_y_guardar_grafico(mora, 'Mora_16_de_julio', 'blue', 'Mora_16_de_julio', 'Mora_16_de_julio.png')
crear_y_guardar_grafico(mora, 'Mora_Ceja', 'green', 'Mora_Ceja', 'Mora_Ceja.png')
crear_y_guardar_grafico(mora, 'Total_Mora', 'orange', 'Total_Mora', 'Total_Mora.png')

# Verificar la ruta del directorio actual después de guardar los gráficos
current_dir_after = os.getcwd()
print("Directorio actual después de guardar los gráficos:", current_dir_after)
