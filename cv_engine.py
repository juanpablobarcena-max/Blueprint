import cv2
import numpy as np

def procesar_sombreado_civil(imagen_array, punto_x, punto_y, tolerancia=30):
    """
    Convierte un sombreado CAD (rayas/puntos) en una mancha sólida para calcular su área.
    """
    # 1. Obtener color del píxel clickeado
    color_objetivo = imagen_array[punto_y, punto_x]
    
    # 2. Crear máscara con rango de tolerancia
    lower_bound = np.clip(color_objetivo - tolerancia, 0, 255)
    upper_bound = np.clip(color_objetivo + tolerancia, 0, 255)
    mascara = cv2.inRange(imagen_array, lower_bound, upper_bound)
    
    # 3. Morfología Matemática (El truco para sombreados)
    # "Engorda" las líneas del tramado hasta que se fusionan en un área sólida
    kernel = np.ones((9,9), np.uint8)
    mascara_cerrada = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    
    # 4. Encontrar el contorno exterior de la nueva mancha
    contornos, _ = cv2.findContours(mascara_cerrada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrar y devolver el contorno más grande (el área detectada)
    if contornos:
        contorno_principal = max(contornos, key=cv2.contourArea)
        area_pixeles = cv2.contourArea(contorno_principal)
        perimetro_pixeles = cv2.arcLength(contorno_principal, True)
        return contorno_principal, area_pixeles, perimetro_pixeles
    return None, 0, 0

def procesar_linea_redes(imagen_array, mascara_color):
    """
    Toma una red de tuberías del mismo color y la reduce a 1 píxel de grosor 
    (esqueletización) para medir metros lineales exactos.
    """
    # Usar el algoritmo de esqueletización de OpenCV (ximgproc si está disponible, o adelgazamiento morfológico)
    esqueleto = cv2.ximgproc.thinning(mascara_color)
    
    # Contar píxeles blancos en el esqueleto da la longitud aproximada en píxeles
    longitud_pixeles = np.sum(esqueleto == 255)
    return esqueleto, longitud_pixeles