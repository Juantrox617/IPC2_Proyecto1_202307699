import os
import xml.etree.ElementTree as ET

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
        # Si el sensor ya existe, actualiza el valor
        actual = self.head
        while actual:
            if actual.id_sensor == id_sensor:
                actual.valor = valor
                return
            actual = actual.siguiente
        # Si no existe, lo agrega al final
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
        return 0  # Si no existe, retorna 0

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
        # Si ya existe, retorna la existente
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
        # Encabezado
        print("      ", end="")
        for id_sensor in sensores_ids:
            print(f"s{id_sensor}".ljust(8), end="")
        print()
        # Filas con estaciones
        actual_est = self.head
        while actual_est:
            print(f"n{actual_est.id_estacion}".ljust(6), end="")
            for id_sensor in sensores_ids:
                valor = actual_est.sensores.obtener_valor(id_sensor)
                print(str(valor).ljust(8), end="")
            print()
            actual_est = actual_est.siguiente

def cargar_matriz_suelo(ruta_xml, estaciones_suelo):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()
    sensores_ids = set()
    # Primero, recopila todos los IDs de sensores de suelo
    for campo in root.findall('campo'):
        sensores_suelo = campo.find('sensoresSuelo')
        if sensores_suelo is not None:
            for sensor in sensores_suelo.findall('sensorS'):
                id_sensor = sensor.get('id')
                sensores_ids.add(id_sensor)
    sensores_ids = sorted(list(sensores_ids))
    # Ahora, agrega estaciones y sensores
    for campo in root.findall('campo'):
        estaciones_base = campo.find('estacionesBase')
        sensores_suelo = campo.find('sensoresSuelo')
        estaciones_dict = {}
        for est in estaciones_base.findall('estacion'):
            id_est = est.get('id')
            print(f"cargando sensor de suelo de la estacion {id_est}")
            nodo_est = estaciones_suelo.agregar_estacion(id_est)
            estaciones_dict[id_est] = nodo_est
        # Inicializa todos los sensores en cada estación con valor 0
        for est in estaciones_dict.values():
            est.sensores.agregar_sensores_faltantes(sensores_ids)
        # Ahora agrega los valores reales
        if sensores_suelo is not None:
            for sensor in sensores_suelo.findall('sensorS'):
                id_sensor = sensor.get('id')
                for freq in sensor.findall('frecuencia'):
                    id_estacion = freq.get('idEstacion')
                    valor = int(freq.text)
                    if id_estacion in estaciones_dict:
                        estaciones_dict[id_estacion].sensores.agregar_sensor(id_sensor, valor)
    return sensores_ids

def cargar_matriz_cultivo(ruta_xml, estaciones_cultivo):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()
    sensores_ids = set()
    # Recopila todos los IDs de sensores de cultivo
    for campo in root.findall('campo'):
        sensores_cultivo = campo.find('sensoresCultivo')
        if sensores_cultivo is not None:
            for sensor in sensores_cultivo.findall('sensorT'):
                id_sensor = sensor.get('id')
                sensores_ids.add(id_sensor)
    sensores_ids = sorted(list(sensores_ids))
    # Agrega estaciones y sensores
    for campo in root.findall('campo'):
        estaciones_base = campo.find('estacionesBase')
        sensores_cultivo = campo.find('sensoresCultivo')
        estaciones_dict = {}
        for est in estaciones_base.findall('estacion'):
            id_est = est.get('id')
            print(f"cargando sensor de cultivo de la estacion {id_est}")
            nodo_est = estaciones_cultivo.agregar_estacion(id_est)
            estaciones_dict[id_est] = nodo_est
        # Inicializa todos los sensores en cada estación con valor 0
        for est in estaciones_dict.values():
            est.sensores.agregar_sensores_faltantes(sensores_ids)
        # Agrega los valores reales
        if sensores_cultivo is not None:
            for sensor in sensores_cultivo.findall('sensorT'):
                id_sensor = sensor.get('id')
                for freq in sensor.findall('frecuencia'):
                    id_estacion = freq.get('idEstacion')
                    valor = int(freq.text)
                    if id_estacion in estaciones_dict:
                        estaciones_dict[id_estacion].sensores.agregar_sensor(id_sensor, valor)
    return sensores_ids



