import cv2
import requests

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
        cv2.imwrite(filename, frame)  # Guarda la imagen

        # Endpoint de Laravel al que enviarás la imagen
        url = "http://3.147.187.80/api/estacion/673a970b8548904611656030/actuadores/camara/guardar"

        # Prepara los datos para enviar
        with open(filename, 'rb') as file:
            files = {'imagen': file}  # Cambia 'imagen' por el nombre esperado en el request del backend
            response = requests.post(url, files=files)

        # Muestra la respuesta del servidor
        if response.status_code == 200:
            print("Imagen enviada correctamente:", response.json())
            return response.json()["path"]
        else:
            print("Error al enviar la imagen:", response.status_code, response.text)
    else:
        print("No se pudo capturar la foto.")

    # Libera la cámara
    cap.release()
    cv2.destroyAllWindows()





if __name__ == "__main__":
    x = tomarFotoYEnviar()
    print(x)