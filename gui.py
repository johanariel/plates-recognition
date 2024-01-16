import tkinter as tk
from tkinter import Label, PhotoImage
from PIL import Image, ImageTk
import mysql.connector
from acknowledgement import reconocer_texto_en_imagen

count = 0

# Conectar a la base de datos (reemplaza 'tudb', 'tuusuario', 'tupassword' con tus credenciales reales)
conexion = mysql.connector.connect(host='localhost', user='root', password='', database='tudb')
cursor = conexion.cursor()

def obtener_informacion_placa(placa):
    # Consulta a la base de datos para obtener la información asociada a la placa
    query = f"SELECT nombre, apellido, marca, modelo FROM informacion WHERE placa = '{placa}'"
    cursor.execute(query)
    resultado = cursor.fetchone()
    return resultado

class GUI(tk.Tk):
    def __init__(self, placa_inicial):
        tk.Tk.__init__(self)
        self.title('Información de la Placa')

        # Crear elementos de la interfaz gráfica
        self.label_placa = Label(self, text='Placa: ')
        self.label_nombre = Label(self, text='Nombre: ')
        self.label_apellido = Label(self, text='Apellido: ')
        self.label_marca = Label(self, text='Marca: ')
        self.label_modelo = Label(self, text='Modelo: ')
        self.label_imagen = Label(self)

        # Posicionar elementos en la interfaz gráfica
        self.label_placa.pack()
        self.label_nombre.pack()
        self.label_apellido.pack()
        self.label_marca.pack()
        self.label_modelo.pack()
        self.label_imagen.pack()

        # Actualizar la interfaz gráfica con la información de la placa
        self.actualizar_interfaz(placa_inicial)

    def actualizar_interfaz(self, placa):
        # Obtener información de la base de datos
        informacion_placa = obtener_informacion_placa(placa)

        # Actualizar etiquetas con la información
        self.label_placa.config(text=f'Placa: {placa}')
        self.label_nombre.config(text=f'Nombre: {informacion_placa[0]}')
        self.label_apellido.config(text=f'Apellido: {informacion_placa[1]}')
        self.label_marca.config(text=f'Marca: {informacion_placa[2]}')
        self.label_modelo.config(text=f'Modelo: {informacion_placa[3]}')

        # Mostrar la imagen asociada a la placa (reemplaza 'ruta_imagen' con la ruta real)
        imagen = Image.open('plates/scaned_img_0.jpg')
        imagen = imagen.resize((300, 200), Image.ANTIALIAS)
        imagen = ImageTk.PhotoImage(imagen)
        self.label_imagen.config(image=imagen)
        self.label_imagen.image = imagen

if __name__ == "__main__":
    # Ruta de la última imagen guardada
    ruta_imagen = 'plates/scaned_img_' + str(count) + '.jpg'

    # Llama a la función para reconocer texto en la última imagen
    texto_extraido = reconocer_texto_en_imagen(ruta_imagen)

    # Quita el guión ("-") del texto extraído
    texto_sin_guion = texto_extraido.replace('-', '')

    # Imprime el texto sin guión
    print(texto_sin_guion)

    # Crear y mostrar la interfaz gráfica con la información de la placa
    app = GUI(texto_sin_guion)
    app.mainloop()