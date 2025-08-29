from models.matriz import EstacionLista, EstacionNodo, SensorLista, SensorNodo
from graphviz import Digraph
import os

class PatronNodo:
    def __init__(self, patron):
        self.patron = patron
        self.estaciones_head = None
        self.estaciones_last = None
        self.siguiente = None

class EstacionGrupoNodo:
    def __init__(self, estacion):
        self.estacion = estacion
        self.siguiente = None

class SumaNodo:
    def __init__(self, valor=0):
        self.valor = valor
        self.siguiente = None

def obtener_patron(estacion, sensores_head):
    patron = ""
    actual_sensor = sensores_head
    while actual_sensor:
        valor = estacion.sensores.obtener_valor(actual_sensor.id_sensor)
        patron += "1" if valor != 0 else "0"
        actual_sensor = actual_sensor.siguiente
    return patron

def buscar_patron(head, patron):
    actual = head
    while actual:
        if actual.patron == patron:
            return actual
        actual = actual.siguiente
    return None

def reducir_matriz(estaciones, sensores_head):
    patrones_head = None
    patrones_last = None
    actual_est = estaciones.head
    while actual_est:
        patron = obtener_patron(actual_est, sensores_head)
        patron_nodo = buscar_patron(patrones_head, patron)
        if patron_nodo is None:
            patron_nodo = PatronNodo(patron)
            if patrones_head is None:
                patrones_head = patron_nodo
            else:
                patrones_last.siguiente = patron_nodo
            patrones_last = patron_nodo
        grupo_nodo = EstacionGrupoNodo(actual_est)
        if patron_nodo.estaciones_head is None:
            patron_nodo.estaciones_head = grupo_nodo
        else:
            patron_nodo.estaciones_last.siguiente = grupo_nodo
        patron_nodo.estaciones_last = grupo_nodo
        actual_est = actual_est.siguiente

    matriz_reducida = EstacionLista()
    patron_actual = patrones_head
    while patron_actual:
        suma_head = None
        suma_last = None
        tiene_valor = False
        actual_sensor = sensores_head
        while actual_sensor:
            suma_nodo = SumaNodo()
            suma_nodo.valor = 0
            if suma_head is None:
                suma_head = suma_nodo
            else:
                suma_last.siguiente = suma_nodo
            suma_last = suma_nodo
            actual_sensor = actual_sensor.siguiente

        grupo_actual = patron_actual.estaciones_head
        while grupo_actual:
            actual_sensor = sensores_head
            suma_actual = suma_head
            while actual_sensor and suma_actual:
                valor = grupo_actual.estacion.sensores.obtener_valor(actual_sensor.id_sensor)
                suma_actual.valor += valor
                if valor != 0:
                    tiene_valor = True
                actual_sensor = actual_sensor.siguiente
                suma_actual = suma_actual.siguiente
            grupo_actual = grupo_actual.siguiente

        if not tiene_valor:
            patron_actual = patron_actual.siguiente
            continue

        id_estacion = "n"
        grupo_actual = patron_actual.estaciones_head
        while grupo_actual:
            id_estacion += f"_{grupo_actual.estacion.id_estacion}"
            grupo_actual = grupo_actual.siguiente

        nueva_est = matriz_reducida.agregar_estacion(id_estacion)
        actual_sensor = sensores_head
        suma_actual = suma_head
        while actual_sensor and suma_actual:
            nueva_est.sensores.agregar_sensor(actual_sensor.id_sensor, suma_actual.valor)
            actual_sensor = actual_sensor.siguiente
            suma_actual = suma_actual.siguiente

        patron_actual = patron_actual.siguiente
    return matriz_reducida

def mostrar_matriz_reducida(matriz_reducida, sensores_head):
    print("      ", end="")
    actual_sensor = sensores_head
    while actual_sensor:
        print(f"s{actual_sensor.id_sensor}".ljust(8), end="")
        actual_sensor = actual_sensor.siguiente
    print()
    actual_est = matriz_reducida.head
    while actual_est:
        valores_no_cero = False
        actual_sensor = sensores_head
        while actual_sensor:
            valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
            if valor != 0:
                valores_no_cero = True
                break
            actual_sensor = actual_sensor.siguiente
        if valores_no_cero:
            print(f"{actual_est.id_estacion}".ljust(6), end="")
            actual_sensor = sensores_head
            while actual_sensor:
                valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
                print(str(valor).ljust(8), end="")
                actual_sensor = actual_sensor.siguiente
            print()
        actual_est = actual_est.siguiente

def graficar_matriz_reducida(matriz_reducida, sensores_head, nombre):
    dot = Digraph(comment=nombre)
    tabla = '<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">'
    tabla += '<TR><TD><B>Estación/Sensor</B></TD>'
    actual_sensor = sensores_head
    while actual_sensor:
        tabla += f'<TD><B>s{actual_sensor.id_sensor}</B></TD>'
        actual_sensor = actual_sensor.siguiente
    tabla += '</TR>'
    actual_est = matriz_reducida.head
    while actual_est:
        valores_no_cero = False
        actual_sensor = sensores_head
        while actual_sensor:
            valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
            if valor != 0:
                valores_no_cero = True
                break
            actual_sensor = actual_sensor.siguiente
        if valores_no_cero:
            tabla += f'<TR><TD><B>{actual_est.id_estacion}</B></TD>'
            actual_sensor = sensores_head
            while actual_sensor:
                valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
                tabla += f'<TD>{valor}</TD>'
                actual_sensor = actual_sensor.siguiente
            tabla += '</TR>'
        actual_est = actual_est.siguiente
    tabla += '</TABLE>'
    dot.node("matriz", f'<{tabla}>', shape="plaintext")
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    output_path = os.path.join(data_dir, f"{nombre}.gv")
    dot.render(output_path, view=True, format="png")

def reducir_matriz_cultivo(estaciones, sensores_head):
    patrones_head = None
    patrones_last = None
    actual_est = estaciones.head
    while actual_est:
        patron = obtener_patron(actual_est, sensores_head)
        patron_nodo = buscar_patron(patrones_head, patron)
        if patron_nodo is None:
            patron_nodo = PatronNodo(patron)
            if patrones_head is None:
                patrones_head = patron_nodo
            else:
                patrones_last.siguiente = patron_nodo
            patrones_last = patron_nodo
        grupo_nodo = EstacionGrupoNodo(actual_est)
        if patron_nodo.estaciones_head is None:
            patron_nodo.estaciones_head = grupo_nodo
        else:
            patron_nodo.estaciones_last.siguiente = grupo_nodo
        patron_nodo.estaciones_last = grupo_nodo
        actual_est = actual_est.siguiente

    matriz_reducida = EstacionLista()
    patron_actual = patrones_head
    while patron_actual:
        suma_head = None
        suma_last = None
        tiene_valor = False
        actual_sensor = sensores_head
        while actual_sensor:
            suma_nodo = SumaNodo()
            suma_nodo.valor = 0
            if suma_head is None:
                suma_head = suma_nodo
            else:
                suma_last.siguiente = suma_nodo
            suma_last = suma_nodo
            actual_sensor = actual_sensor.siguiente

        grupo_actual = patron_actual.estaciones_head
        while grupo_actual:
            actual_sensor = sensores_head
            suma_actual = suma_head
            while actual_sensor and suma_actual:
                valor = grupo_actual.estacion.sensores.obtener_valor(actual_sensor.id_sensor)
                suma_actual.valor += valor
                if valor != 0:
                    tiene_valor = True
                actual_sensor = actual_sensor.siguiente
                suma_actual = suma_actual.siguiente
            grupo_actual = grupo_actual.siguiente

        if not tiene_valor:
            patron_actual = patron_actual.siguiente
            continue

        id_estacion = "n"
        grupo_actual = patron_actual.estaciones_head
        while grupo_actual:
            id_estacion += f"_{grupo_actual.estacion.id_estacion}"
            grupo_actual = grupo_actual.siguiente

        nueva_est = matriz_reducida.agregar_estacion(id_estacion)
        actual_sensor = sensores_head
        suma_actual = suma_head
        while actual_sensor and suma_actual:
            nueva_est.sensores.agregar_sensor(actual_sensor.id_sensor, suma_actual.valor)
            actual_sensor = actual_sensor.siguiente
            suma_actual = suma_actual.siguiente

        patron_actual = patron_actual.siguiente
    return matriz_reducida

def mostrar_matriz_reducida_cultivo(matriz_reducida, sensores_head):
    print("      ", end="")
    actual_sensor = sensores_head
    while actual_sensor:
        print(f"s{actual_sensor.id_sensor}".ljust(8), end="")
        actual_sensor = actual_sensor.siguiente
    print()
    actual_est = matriz_reducida.head
    while actual_est:
        valores_no_cero = False
        actual_sensor = sensores_head
        while actual_sensor:
            valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
            if valor != 0:
                valores_no_cero = True
                break
            actual_sensor = actual_sensor.siguiente
        if valores_no_cero:
            print(f"{actual_est.id_estacion}".ljust(6), end="")
            actual_sensor = sensores_head
            while actual_sensor:
                valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
                print(str(valor).ljust(8), end="")
                actual_sensor = actual_sensor.siguiente
            print()
        actual_est = actual_est.siguiente

def graficar_matriz_reducida_cultivo(matriz_reducida, sensores_head, nombre):
    dot = Digraph(comment=nombre)
    tabla = '<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">'
    tabla += '<TR><TD><B>Estación/Sensor</B></TD>'
    actual_sensor = sensores_head
    while actual_sensor:
        tabla += f'<TD><B>s{actual_sensor.id_sensor}</B></TD>'
        actual_sensor = actual_sensor.siguiente
    tabla += '</TR>'
    actual_est = matriz_reducida.head
    while actual_est:
        valores_no_cero = False
        actual_sensor = sensores_head
        while actual_sensor:
            valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
            if valor != 0:
                valores_no_cero = True
                break
            actual_sensor = actual_sensor.siguiente
        if valores_no_cero:
            tabla += f'<TR><TD><B>{actual_est.id_estacion}</B></TD>'
            actual_sensor = sensores_head
            while actual_sensor:
                valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
                tabla += f'<TD>{valor}</TD>'
                actual_sensor = actual_sensor.siguiente
            tabla += '</TR>'
        actual_est = actual_est.siguiente
    tabla += '</TABLE>'
    dot.node("matriz", f'<{tabla}>', shape="plaintext")
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    output_path = os.path.join(data_dir, f"{nombre}.gv")
    dot.render(output_path, view=True, format="png")



