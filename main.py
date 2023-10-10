import cv2
import numpy as np
import os

# Ruta de la carpeta con las imágenes originales
carpeta_entrada = 'C:/Users/dilan/Desktop/trabajos pendientes/PASANTIA/CODIGOS/Aislamiento en paint de imagenes/103FPLAN/'

# Ruta de la carpeta con los recortes
carpeta_salida = 'C:/Users/dilan/Desktop/trabajos pendientes/PASANTIA/CODIGOS/Aislamiento en paint de imagenes/103PLAN/Recortes_103plan/'

# verificar que la carpeta de salida exista, sino se crea
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Listamos los archivos en la carpeta de imagenes
archivos = os.listdir(carpeta_entrada)

# Definimos los valores de umbral para detectar el rojo brillante y no todo el espectro de rojos
lower_red = np.array([0, 0, 175]) # bajos 
upper_red = np.array([100, 100, 255]) # altos

# Recorremos los archivos en la carpeta de imagenes 
for archivo in archivos:
    if archivo.endswith('.JPG') or archivo.endswith('.png'):  # Validar el formato en JPG o png
        # Cargamos la imagen
        imagen = cv2.imread(os.path.join(carpeta_entrada, archivo))

        # Convertimos la imagen a formato BGR 
        if len(imagen.shape) == 2:
            imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)

        # Creamos una máscara para el color rojo
        mascara = cv2.inRange(imagen, lower_red, upper_red)

        # Encontramos los contornos en la máscara
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Si se detectan contornos rojos
        if contornos:
            for i, contorno in enumerate(contornos):
                # Encontramos las coordenadas del rectángulo que rodea el contorno del marco rojo
                x, y, w, h = cv2.boundingRect(contorno)

                # Recortamos la región dentro del marco rojo de la imagen original
                region_recortada = imagen[y:y + h, x:x + w]

                # Guardamos la región recortada en la carpeta de salida
                nombre_archivo_salida = os.path.splitext(archivo)[0] + f'_recorte_{i}.jpg'
                cv2.imwrite(os.path.join(carpeta_salida, nombre_archivo_salida), region_recortada)
        else:
            print(f'No se encontraron marcos rojos en {archivo}')
