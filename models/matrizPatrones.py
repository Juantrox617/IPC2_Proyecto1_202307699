from models.matriz import EstacionLista
import os
from graphviz import Digraph

class SensorIdNodo:
    def __init__(self, id_sensor):
        self.id_sensor = id_sensor
        self.siguiente = None

class EstacionDictNodo:
    def __init__(self, id_est, nodo_est):
        self.id_est = id_est
        self.nodo_est = nodo_est
        self.siguiente = None

def buscar_estacion(estaciones_head, id_est):
    actual = estaciones_head
    while actual:
        if actual.id_est == id_est:
            return actual.nodo_est
        actual = actual.siguiente
    return None

def cargar_matriz_suelo_sin_print(ruta_xml, estaciones_suelo):
    import xml.etree.ElementTree as ET
    tree = ET.parse(ruta_xml)
    root = tree.getroot()
    sensores_head = None
    sensores_last = None
    sensores_ids_set = set()
    for campo in root.findall('campo'):
        sensores_suelo = campo.find('sensoresSuelo')
        if sensores_suelo is not None:
            for sensor in sensores_suelo.findall('sensorS'):
                id_sensor = sensor.get('id')
                if id_sensor not in sensores_ids_set:
                    nodo = SensorIdNodo(id_sensor)
                    if sensores_head is None:
                        sensores_head = nodo
                    else:
                        sensores_last.siguiente = nodo
                    sensores_last = nodo
                    sensores_ids_set.add(id_sensor)
    sensores_head = ordenar_sensores_enlazados(sensores_head)
    for campo in root.findall('campo'):
        estaciones_base = campo.find('estacionesBase')
        sensores_suelo = campo.find('sensoresSuelo')
        estaciones_dict_head = None
        estaciones_dict_last = None
        for est in estaciones_base.findall('estacion'):
            id_est = est.get('id')
            nodo_est = estaciones_suelo.agregar_estacion(id_est)
            dict_nodo = EstacionDictNodo(id_est, nodo_est)
            if estaciones_dict_head is None:
                estaciones_dict_head = dict_nodo
            else:
                estaciones_dict_last.siguiente = dict_nodo
            estaciones_dict_last = dict_nodo
        actual_dict = estaciones_dict_head
        while actual_dict:
            agregar_sensores_faltantes_enlazados(actual_dict.nodo_est.sensores, sensores_head)
            actual_dict = actual_dict.siguiente
        if sensores_suelo is not None:
            for sensor in sensores_suelo.findall('sensorS'):
                id_sensor = sensor.get('id')
                for freq in sensor.findall('frecuencia'):
                    id_estacion = freq.get('idEstacion')
                    valor = int(freq.text)
                    nodo_est = buscar_estacion(estaciones_dict_head, id_estacion)
                    if nodo_est:
                        nodo_est.sensores.agregar_sensor(id_sensor, valor)
    return sensores_head

def cargar_matriz_cultivo_sin_print(ruta_xml, estaciones_cultivo):
    import xml.etree.ElementTree as ET
    tree = ET.parse(ruta_xml)
    root = tree.getroot()
    sensores_head = None
    sensores_last = None
    sensores_ids_set = set()
    for campo in root.findall('campo'):
        sensores_cultivo = campo.find('sensoresCultivo')
        if sensores_cultivo is not None:
            for sensor in sensores_cultivo.findall('sensorT'):
                id_sensor = sensor.get('id')
                if id_sensor not in sensores_ids_set:
                    nodo = SensorIdNodo(id_sensor)
                    if sensores_head is None:
                        sensores_head = nodo
                    else:
                        sensores_last.siguiente = nodo
                    sensores_last = nodo
                    sensores_ids_set.add(id_sensor)
    sensores_head = ordenar_sensores_enlazados(sensores_head)
    for campo in root.findall('campo'):
        estaciones_base = campo.find('estacionesBase')
        sensores_cultivo = campo.find('sensoresCultivo')
        estaciones_dict_head = None
        estaciones_dict_last = None
        for est in estaciones_base.findall('estacion'):
            id_est = est.get('id')
            nodo_est = estaciones_cultivo.agregar_estacion(id_est)
            dict_nodo = EstacionDictNodo(id_est, nodo_est)
            if estaciones_dict_head is None:
                estaciones_dict_head = dict_nodo
            else:
                estaciones_dict_last.siguiente = dict_nodo
            estaciones_dict_last = dict_nodo
        actual_dict = estaciones_dict_head
        while actual_dict:
            agregar_sensores_faltantes_enlazados(actual_dict.nodo_est.sensores, sensores_head)
            actual_dict = actual_dict.siguiente
        if sensores_cultivo is not None:
            for sensor in sensores_cultivo.findall('sensorT'):
                id_sensor = sensor.get('id')
                for freq in sensor.findall('frecuencia'):
                    id_estacion = freq.get('idEstacion')
                    valor = int(freq.text)
                    nodo_est = buscar_estacion(estaciones_dict_head, id_estacion)
                    if nodo_est:
                        nodo_est.sensores.agregar_sensor(id_sensor, valor)
    return sensores_head

def ordenar_sensores_enlazados(head):
    def insertar_ordenado(head, nodo):
        if head is None or nodo.id_sensor < head.id_sensor:
            nodo.siguiente = head
            return nodo
        actual = head
        while actual.siguiente and actual.siguiente.id_sensor < nodo.id_sensor:
            actual = actual.siguiente
        nodo.siguiente = actual.siguiente
        actual.siguiente = nodo
        return head

    nuevo_head = None
    actual = head
    while actual:
        siguiente = actual.siguiente
        actual.siguiente = None
        nuevo_head = insertar_ordenado(nuevo_head, actual)
        actual = siguiente
    return nuevo_head

def agregar_sensores_faltantes_enlazados(sensor_lista, sensores_head):
    actual = sensores_head
    while actual:
        sensor_lista.agregar_sensor(actual.id_sensor, 0)
        actual = actual.siguiente

def graficar_matriz_patron(estaciones, sensores_head, nombre="matriz_patron"):
    dot = Digraph(comment=nombre)
    tabla = '<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">'
    tabla += '<TR><TD><B>Estación/Sensor</B></TD>'
    actual_sensor = sensores_head
    while actual_sensor:
        tabla += f'<TD><B>s{actual_sensor.id_sensor}</B></TD>'
        actual_sensor = actual_sensor.siguiente
    tabla += '</TR>'
    actual_est = estaciones.head
    while actual_est:
        tabla += f'<TR><TD><B>n{actual_est.id_estacion}</B></TD>'
        actual_sensor = sensores_head
        while actual_sensor:
            valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
            tabla += f'<TD>{1 if valor != 0 else 0}</TD>'
            actual_sensor = actual_sensor.siguiente
        tabla += '</TR>'
        actual_est = actual_est.siguiente
    tabla += '</TABLE>'
    dot.node("matriz", f'<{tabla}>', shape="plaintext")
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    output_path = os.path.join(data_dir, f"{nombre}.dot")
    dot.render(output_path, view=False, format="png")

def matriz_patron(estaciones, sensores_head):
    actual_sensor = sensores_head
    print("      ", end="")
    while actual_sensor:
        print(f"s{actual_sensor.id_sensor}".ljust(8), end="")
        actual_sensor = actual_sensor.siguiente
    print()
    actual_est = estaciones.head
    while actual_est:
        print(f"n{actual_est.id_estacion}".ljust(6), end="")
        actual_sensor = sensores_head
        while actual_sensor:
            valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
            print(str(1 if valor != 0 else 0).ljust(8), end="")
            actual_sensor = actual_sensor.siguiente
        print()
        actual_est = actual_est.siguiente

def procesar_patrones_suelo(ruta_xml):
    estaciones_suelo = EstacionLista()
    sensores_head = cargar_matriz_suelo_sin_print(ruta_xml, estaciones_suelo)
    matriz_patron(estaciones_suelo, sensores_head)
    graficar_matriz_patron(estaciones_suelo, sensores_head, nombre="matriz_patron_suelo")

def procesar_patrones_cultivo(ruta_xml):
    estaciones_cultivo = EstacionLista()
    sensores_head = cargar_matriz_cultivo_sin_print(ruta_xml, estaciones_cultivo)
    matriz_patron(estaciones_cultivo, sensores_head)
    graficar_matriz_patron(estaciones_cultivo, sensores_head, nombre="matriz_patron_cultivo")


