import os
import numpy as np
from skimage import io
from skimage.transform import resize
from sklearn.model_selection import train_test_split

def generar_dataset():
    X = []
    y = []
    imagen = []
    total = 0
    
    for ruta, subdirectorio, ficheros in os.walk('english/fnt/'):
        # Ordenar el contenido del subdirectorio
        subdirectorio.sort()

        # Se itera fichero a fichero por cada subdirectorio del dataset
        for nombreFichero in ficheros:
            # Extraemos el código de la clase del nombre del fichero
            clase = nombreFichero[3:nombreFichero.index('-')]
            y.append(float(clase))

            # Componer la ruta completa a la imagen
            rutaCompleta = os.path.join(ruta, nombreFichero)

            # Cargar la imagen y reducirla a 32x32 píxeles
            imagen = io.imread(rutaCompleta, as_gray=True)
            imagen_reducida = resize(imagen,(32,32))

            # Invertir imagen
            imagen_reducida = 1 - imagen_reducida

            # Guardar imagen en la matriz como vector de 1024 píxeles
            X.append(imagen_reducida.reshape(1024,1))

            print (nombreFichero)
            total = total + 1

    print (total)

    # Convertir matriz de imágenes en array numpy
    X = np.array(X)
    X = X.reshape(X.shape[:2])

    print (X.shape)

    # Codificar el vector de clases como "one-hot encoding"
    from sklearn import preprocessing
    lb = preprocessing.LabelBinarizer()
    lb.fit(y)

    # Convertir vector de clases en matriz numpy
    y = lb.transform(y)

    # Asegurarse de que las dimensiones de y sean correctas
    print(y.shape)

    # Guardar matrices como ficheros de texto
    np.savetxt('datos_x.txt', X)
    np.savetxt('datos_y.txt',y)

def cargar_dataset():
    # Comprobar si ya existen las matrices de datos
    if not(os.path.isfile('datos_x.txt')) or \
        not(os.path.isfile('datos_y.txt')):
        generar_dataset()

    X = np.loadtxt('datos_x.txt')
    y = np.loadtxt('datos_y.txt')

    print (X.shape)

    # Generamos los conjuntos de datos de entrenamiento y test
    X_tr, X_test, y_tr, y_test = train_test_split(X, y, test_size=0.10, random_state=42)
    
    # Dividimos el conjunto "Train" en subconjuntos de entrenamiento y validación
    X_train, X_val, y_train, y_val = train_test_split(X_tr, y_tr, test_size=0.10, random_state=42)

    return X_train, X_val, X_test, y_train, y_val, y_test

######## LLAMADA PARA DEPURAR EL MODULO #########
# X_train, X_val, X_test, y_train, y_val, y_test = cargar_dataset()
# Dimensiones de X = (34584, 1024)
# Dimensiones de y = (34584, 36)