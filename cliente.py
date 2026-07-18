import socket
import threading
import json


class ClienteJuego:

    def __init__(self, host="10.167.149.16", puerto=12345):

        self.host = host
        self.puerto = puerto

        self.socket = None
        self.conectado = False

        self.ranking = []

    # ------------------------
    # Conectarse
    # ------------------------

    def conectar(self):

        try:

            self.socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.socket.connect(
                (self.host, self.puerto)
            )

            self.conectado = True

            print("Conectado al servidor")

            threading.Thread(
                target=self.recibir,
                daemon=True
            ).start()

            return True

        except Exception as e:

            print("No fue posible conectar:", e)
            return False

    # ------------------------
    # Enviar datos
    # ------------------------

    def enviar(self, datos):

        if not self.conectado:
            return

        try:

            mensaje = json.dumps(datos)

            self.socket.send(
                (mensaje + "\n").encode("utf-8")
            )

        except Exception as e:

            print("Error enviando:", e)

    # ------------------------
    # Escuchar servidor
    # ------------------------

    def recibir(self):

        while self.conectado:

            try:

                datos = self.socket.recv(4096)

                if not datos:
                    break

                mensaje = datos.decode("utf-8").strip()

                try:

                    self.ranking = json.loads(mensaje)

                    print("Ranking recibido:")
                    print(self.ranking)

                except:

                    print("Servidor:", mensaje)

            except:

                break

        self.conectado = False

    # ------------------------
    # Desconectar
    # ------------------------

    def cerrar(self):

        self.conectado = False

        try:

            self.socket.close()

        except:
            pass