import cv2
import easyocr

def reconocer_texto_en_imagen(ruta_imagen):
    # Crea un objeto Reader de easyocr con el modelo 'es' para español
    reader = easyocr.Reader(['es'])

    # Lee la imagen y realiza el reconocimiento de texto
    resultados = reader.readtext(ruta_imagen)

    # Extrae el texto reconocido de los resultados
    texto_reconocido = ' '.join([resultado[1] for resultado in resultados])

    return texto_reconocido

harcascade = "model/haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0)

cap.set(3, 640) # width
cap.set(4, 480) # height

min_area = 500
count = 0

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x,y,w,h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y+h, x:x+w]
            cv2.imshow("ROI", img_roi)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("plates/scaned_img_" + str(count) + ".jpg", img_roi)
        
        # Llama a la función para reconocer texto en la imagen guardada
        ruta_imagen = 'plates/scaned_img_' + str(count) + '.jpg'
        texto_extraido = reconocer_texto_en_imagen(ruta_imagen)

        # Imprime el texto reconocido
        print(texto_extraido)

        cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("Results",img)
        cv2.waitKey(500)
        count += 1

# Libera la captura de video y cierra las ventanas al finalizar
cap.release()
cv2.destroyAllWindows()
