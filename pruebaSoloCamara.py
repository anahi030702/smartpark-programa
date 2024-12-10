import cv2

def tomarFotoYEnviar():
    # Cambia el índice de la cámara según sea necesario (1 para cámara externa)
    cap = cv2.VideoCapture(1)

    # Verifica si la cámara se ha abierto correctamente
    if not cap.isOpened():
        print("No se pudo acceder a la cámara.")
        exit()

    # Captura un solo frame
    ret, frame = cap.read()

    if ret:
        # Guarda temporalmente la imagen en disco
        filename = "foto_a_enviar.jpg"
        res = cv2.imwrite(filename, frame)  # Guarda la imagen
        if res:
            print("foto guardada exitosamente")
        else:
            print("no se pudo guardar la foto")

    else:
        print("No se pudo capturar la foto.")

    # Libera la cámara
    cap.release()
    cv2.destroyAllWindows()





if __name__ == "__main__":
    x = tomarFotoYEnviar()
    print(x)