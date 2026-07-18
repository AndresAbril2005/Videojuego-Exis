import socket
import threading
import json


HOST = "0.0.0.0"
PUERTO = 12345


clientes = []

ranking = {}


# =========================
# ENVIAR RANKING
# =========================

def enviar_ranking():

    datos = []

    for nombre, info in ranking.items():

        datos.append({

            "nombre": nombre,
            "nivel": info["nivel"],
            "tiempo": info["tiempo"]

        })

    # Ordenar:
    # 1. Mayor nivel
    # 2. Menor tiempo

    datos.sort(
        key=lambda x: (-x["nivel"], x["tiempo"])
    )

    mensaje = json.dumps(datos) + "\n"

    for cliente in clientes[:]:

        try:

            cliente.send(
                mensaje.encode("utf-8")
            )

        except:

            if cliente in clientes:
                clientes.remove(cliente)


# =========================
# CLIENTE
# =========================

def manejar_cliente(cliente):

    clientes.append(cliente)

    while True:

        try:

            datos = cliente.recv(4096)

            if not datos:
                break

            mensaje = json.loads(
                datos.decode("utf-8")
            )

            nombre = mensaje["nombre"]
            nivel = mensaje["nivel"]
            tiempo = mensaje["tiempo"]

            ranking[nombre] = {

                "nivel": nivel,
                "tiempo": tiempo

            }

            print(ranking)

            enviar_ranking()

        except Exception as e:

            print(e)
            break

    cliente.close()

    if cliente in clientes:
        clientes.remove(cliente)


# =========================
# SERVIDOR
# =========================

servidor = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

servidor.bind((HOST, PUERTO))

servidor.listen()

print("Servidor iniciado")

while True:

    cliente, direccion = servidor.accept()

    print("Conectado:", direccion)

    threading.Thread(
        target=manejar_cliente,
        args=(cliente,),
        daemon=True
    ).start()