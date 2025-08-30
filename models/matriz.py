import os
import xml.etree.ElementTree as ET
from graphviz import Digraph

class SensorNodo:
    def __init__(self, id_sensor, valor=0):
        self.id_sensor = id_sensor
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class SensorIdNodo:
    def __init__(self, id_sensor):
        self.id_sensor = id_sensor
        self.siguiente = None

class SensorLista:
    def __init__(self):
        self.head = None

    def agregar_sensor(self, id_sensor, valor):
        actual = self.head
        while actual:
            if actual.id_sensor == id_sensor:
                actual.valor = valor
                return
            actual = actual.siguiente
        nuevo = SensorNodo(id_sensor, valor)
        if self.head is None:
            self.head = nuevo
        else:
            actual = self.head
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
            nuevo.anterior = actual

    def obtener_valor(self, id_sensor):
        actual = self.head
        while actual:
            if actual.id_sensor == id_sensor:
                return actual.valor
            actual = actual.siguiente
        return 0

    def agregar_sensores_faltantes(self, sensores_head):
        actual = sensores_head
        while actual:
            self.agregar_sensor(actual.id_sensor, 0)
            actual = actual.siguiente

    def graficar(self, nombre="matriz"):
        dot = Digraph(comment=nombre)
        dot.attr(rankdir='LR', shape='box')
        dot.node("Estaciones/Sensores", shape="plaintext")
        actual = self.head
        while actual:
            dot.node(f"s{actual.id_sensor}", f"s{actual.id_sensor}", shape="box")
            dot.edge("Estaciones/Sensores", f"s{actual.id_sensor}")
            actual = actual.siguiente
        actual_est = self.head
        while actual_est:
            dot.node(f"n{actual_est.id_estacion}", f"n{actual_est.id_estacion}", shape="box")
            dot.edge("Estaciones/Sensores", f"n{actual_est.id_estacion}")
            actual_sen = actual_est.sensores.head
            while actual_sen:
                valor_node = f"n{actual_est.id_estacion}_s{actual_sen.id_sensor}"
                dot.node(valor_node, str(actual_sen.valor), shape="ellipse")
                dot.edge(f"n{actual_est.id_estacion}", valor_node)
                dot.edge(f"s{actual_sen.id_sensor}", valor_node)
                actual_sen = actual_sen.siguiente
            actual_est = actual_est.siguiente
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        output_path = os.path.join(data_dir, f"{nombre}.gv")
        dot.render(output_path, view=True, format="png")

class EstacionNodo:
    def __init__(self, id_estacion):
        self.id_estacion = id_estacion
        self.sensores = SensorLista()
        self.siguiente = None
        self.anterior = None

class EstacionLista:
    def __init__(self):
        self.head = None

    def agregar_estacion(self, id_estacion):
        actual = self.head
        while actual:
            if actual.id_estacion == id_estacion:
                return actual
            actual = actual.siguiente
        nueva = EstacionNodo(id_estacion)
        if self.head is None:
            self.head = nueva
        else:
            actual = self.head
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nueva
            nueva.anterior = actual
        return nueva

    def mostrar(self, sensores_head):
        print("      ", end="")
        actual_sensor = sensores_head
        while actual_sensor:
            print(f"s{actual_sensor.id_sensor}".ljust(8), end="")
            actual_sensor = actual_sensor.siguiente
        print()
        actual_est = self.head
        while actual_est:
            print(f"n{actual_est.id_estacion}".ljust(6), end="")
            actual_sensor = sensores_head
            while actual_sensor:
                valor = actual_est.sensores.obtener_valor(actual_sensor.id_sensor)
                print(str(valor).ljust(8), end="")
                actual_sensor = actual_sensor.siguiente
            print()
            actual_est = actual_est.siguiente

    def graficar(self, sensores_head, nombre="matriz"):
        dot = Digraph(comment=nombre)
        tabla = '<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">'
        tabla += '<TR><TD><B>Estación/Sensor</B></TD>'
        actual_sensor = sensores_head
        while actual_sensor:
            tabla += f'<TD><B>s{actual_sensor.id_sensor}</B></TD>'
            actual_sensor = actual_sensor.siguiente
        tabla += '</TR>'
        actual_est = self.head
        while actual_est:
            tabla += f'<TR><TD><B>n{actual_est.id_estacion}</B></TD>'
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
        output_path = os.path.join(data_dir, f"{nombre}.dot")
        dot.render(output_path, view=False, format="png")

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

def cargar_matriz_suelo(ruta_xml, estaciones_suelo):
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
            print(f"cargando sensor de suelo de la estacion {id_est}")
            nodo_est = estaciones_suelo.agregar_estacion(id_est)
            dict_nodo = EstacionDictNodo(id_est, nodo_est)
            if estaciones_dict_head is None:
                estaciones_dict_head = dict_nodo
            else:
                estaciones_dict_last.siguiente = dict_nodo
            estaciones_dict_last = dict_nodo
        actual_dict = estaciones_dict_head
        while actual_dict:
            actual_dict.nodo_est.sensores.agregar_sensores_faltantes(sensores_head)
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
    estaciones_suelo.graficar(sensores_head, nombre="matriz_suelo")
    return sensores_head

def cargar_matriz_cultivo(ruta_xml, estaciones_cultivo):
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
            print(f"cargando sensor de cultivo de la estacion {id_est}")
            nodo_est = estaciones_cultivo.agregar_estacion(id_est)
            dict_nodo = EstacionDictNodo(id_est, nodo_est)
            if estaciones_dict_head is None:
                estaciones_dict_head = dict_nodo
            else:
                estaciones_dict_last.siguiente = dict_nodo
            estaciones_dict_last = dict_nodo
        actual_dict = estaciones_dict_head
        while actual_dict:
            actual_dict.nodo_est.sensores.agregar_sensores_faltantes(sensores_head)
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
    estaciones_cultivo.graficar(sensores_head, nombre="matriz_cultivo")
    return sensores_head





