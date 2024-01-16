import cv2

harcascade = "model/plate_number.xml"

cap = cv2.VideoCapture(0)

cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
count = 0

# Cargar el clasificador fuera del bucle
plate_cascade = cv2.CascadeClassifier(harcascade)

while True:
    success, img = cap.read()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "PLACA", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y + h, x:x + w]
            cv2.imshow("ROI", img_roi)

    cv2.imshow("RESULTADO", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        cv2.imwrite("plates/scaned_img_" + str(count) + ".jpg", img_roi)
        print("PLACA GUARDADA")
        count += 1
    elif key == 27:  # Cerrar con la tecla 'Esc' (código ASCII 27)
        break

cap.release()
cv2.destroyAllWindows()