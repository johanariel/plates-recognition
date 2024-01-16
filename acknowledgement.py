import easyocr

count = 0

def reconocer_texto_en_imagen(ruta_imagen):
    # Crea un objeto Reader de easyocr con el modelo 'es' para español
    reader = easyocr.Reader(['es'])

    # Lee la imagen y realiza el reconocimiento de texto
    resultados = reader.readtext(ruta_imagen)

    # Extrae el texto reconocido de los resultados
    texto_reconocido = ' '.join([resultado[1] for resultado in resultados])

    return texto_reconocido

""" if __name__ == "__main__":
    # Ruta de la última imagen guardada
    ruta_imagen = 'plates/scaned_img_' + str(count) + '.jpg'

    # Llama a la función para reconocer texto en la última imagen
    texto_extraido = reconocer_texto_en_imagen(ruta_imagen)

    # Quita el guión ("-") del texto extraído
    texto_sin_guion = texto_extraido.replace('-', '')

    # Imprime el texto sin guión
    print(texto_sin_guion) """