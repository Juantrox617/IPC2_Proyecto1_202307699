import os
import xml.etree.ElementTree as ET
from graphviz import Digraph

class SensorNodo:
    def __init__(self, id_sensor, valor=0):
        self.id_sensor = id_sensor
        self.valor = valor
        self.siguiente = None
        self.anterior = None

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

    def agregar_sensores_faltantes(self, sensores_ids):
        for id_sensor in sensores_ids:
            actual = self.head
            existe = False
            while actual:
                if actual.id_sensor == id_sensor:
                    existe = True
                    break
                actual = actual.siguiente
            if not existe:
                self.agregar_sensor(id_sensor, 0)

    def graficar(self, nombre="matriz"):
        dot = Digraph(comment=nombre)
        dot.attr(rankdir='LR', shape='box')
<<<<<<< HEAD
        dot.node("Estaciones/Sensores", shape="plaintext")
=======
        # Nodo cabecera
        dot.node("Estaciones/Sensores", shape="plaintext")
        # Nodos de sensores
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42
        actual = self.head
        while actual:
            dot.node(f"s{actual.id_sensor}", f"s{actual.id_sensor}", shape="box")
            dot.edge("Estaciones/Sensores", f"s{actual.id_sensor}")
            actual = actual.siguiente
<<<<<<< HEAD
=======
        # Nodos de estaciones y valores
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42
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
<<<<<<< HEAD
=======
        # Guardar en carpeta data
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42
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

    def mostrar(self, sensores_ids):
        print("      ", end="")
        for id_sensor in sensores_ids:
            print(f"s{id_sensor}".ljust(8), end="")
        print()
        actual_est = self.head
        while actual_est:
            print(f"n{actual_est.id_estacion}".ljust(6), end="")
            for id_sensor in sensores_ids:
                valor = actual_est.sensores.obtener_valor(id_sensor)
                print(str(valor).ljust(8), end="")
            print()
            actual_est = actual_est.siguiente

    def graficar(self, sensores_ids, nombre="matriz"):
        dot = Digraph(comment=nombre)
<<<<<<< HEAD
        tabla = '<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">'
=======
        # Construir la tabla en HTML
        tabla = '<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">'
        # Encabezado
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42
        tabla += '<TR><TD><B>Estación/Sensor</B></TD>'
        for id_sensor in sensores_ids:
            tabla += f'<TD><B>s{id_sensor}</B></TD>'
        tabla += '</TR>'
<<<<<<< HEAD
=======
        # Filas de estaciones y valores
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42
        actual_est = self.head
        while actual_est:
            tabla += f'<TR><TD><B>n{actual_est.id_estacion}</B></TD>'
            for id_sensor in sensores_ids:
                valor = actual_est.sensores.obtener_valor(id_sensor)
                tabla += f'<TD>{valor}</TD>'
            tabla += '</TR>'
            actual_est = actual_est.siguiente
        tabla += '</TABLE>'
<<<<<<< HEAD
        dot.node("matriz", f'<{tabla}>', shape="plaintext")
=======
        # Nodo único con la tabla
        dot.node("matriz", f'<{tabla}>', shape="plaintext")
        # Guardar en carpeta data
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        output_path = os.path.join(data_dir, f"{nombre}.gv")
        dot.render(output_path, view=True, format="png")

def cargar_matriz_suelo(ruta_xml, estaciones_suelo):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()
    sensores_ids = set()
    for campo in root.findall('campo'):
        sensores_suelo = campo.find('sensoresSuelo')
        if sensores_suelo is not None:
            for sensor in sensores_suelo.findall('sensorS'):
                id_sensor = sensor.get('id')
                sensores_ids.add(id_sensor)
    sensores_ids = sorted(list(sensores_ids))
    for campo in root.findall('campo'):
        estaciones_base = campo.find('estacionesBase')
        sensores_suelo = campo.find('sensoresSuelo')
        estaciones_dict = {}
        for est in estaciones_base.findall('estacion'):
            id_est = est.get('id')
            print(f"cargando sensor de suelo de la estacion {id_est}")
            nodo_est = estaciones_suelo.agregar_estacion(id_est)
            estaciones_dict[id_est] = nodo_est
        for est in estaciones_dict.values():
            est.sensores.agregar_sensores_faltantes(sensores_ids)
        if sensores_suelo is not None:
            for sensor in sensores_suelo.findall('sensorS'):
                id_sensor = sensor.get('id')
                for freq in sensor.findall('frecuencia'):
                    id_estacion = freq.get('idEstacion')
                    valor = int(freq.text)
                    if id_estacion in estaciones_dict:
                        estaciones_dict[id_estacion].sensores.agregar_sensor(id_sensor, valor)
<<<<<<< HEAD
    estaciones_suelo.graficar(sensores_ids, nombre="matriz_suelo")
    return sensores_ids
=======
    
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42

def cargar_matriz_cultivo(ruta_xml, estaciones_cultivo):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()
    sensores_ids = set()
    for campo in root.findall('campo'):
        sensores_cultivo = campo.find('sensoresCultivo')
        if sensores_cultivo is not None:
            for sensor in sensores_cultivo.findall('sensorT'):
                id_sensor = sensor.get('id')
                sensores_ids.add(id_sensor)
    sensores_ids = sorted(list(sensores_ids))
    for campo in root.findall('campo'):
        estaciones_base = campo.find('estacionesBase')
        sensores_cultivo = campo.find('sensoresCultivo')
        estaciones_dict = {}
        for est in estaciones_base.findall('estacion'):
            id_est = est.get('id')
            print(f"cargando sensor de cultivo de la estacion {id_est}")
            nodo_est = estaciones_cultivo.agregar_estacion(id_est)
            estaciones_dict[id_est] = nodo_est
        for est in estaciones_dict.values():
            est.sensores.agregar_sensores_faltantes(sensores_ids)
        if sensores_cultivo is not None:
            for sensor in sensores_cultivo.findall('sensorT'):
                id_sensor = sensor.get('id')
                for freq in sensor.findall('frecuencia'):
                    id_estacion = freq.get('idEstacion')
                    valor = int(freq.text)
                    if id_estacion in estaciones_dict:
                        estaciones_dict[id_estacion].sensores.agregar_sensor(id_sensor, valor)
<<<<<<< HEAD
    estaciones_cultivo.graficar(sensores_ids, nombre="matriz_cultivo")
    return sensores_ids
        
=======
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42
   



