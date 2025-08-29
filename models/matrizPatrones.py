from models.matriz import EstacionLista
import os
from graphviz import Digraph

def cargar_matriz_suelo_sin_print(ruta_xml, estaciones_suelo):
    import xml.etree.ElementTree as ET
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
    return sensores_ids

def cargar_matriz_cultivo_sin_print(ruta_xml, estaciones_cultivo):
    import xml.etree.ElementTree as ET
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
    return sensores_ids

def graficar_matriz_patron(estaciones, sensores_ids, nombre="matriz_patron"):
    dot = Digraph(comment=nombre)
    tabla = '<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">'
    tabla += '<TR><TD><B>Estación/Sensor</B></TD>'
    for id_sensor in sensores_ids:
        tabla += f'<TD><B>s{id_sensor}</B></TD>'
    tabla += '</TR>'
    actual_est = estaciones.head
    while actual_est:
        tabla += f'<TR><TD><B>n{actual_est.id_estacion}</B></TD>'
        for id_sensor in sensores_ids:
            valor = actual_est.sensores.obtener_valor(id_sensor)
            tabla += f'<TD>{1 if valor != 0 else 0}</TD>'
        tabla += '</TR>'
        actual_est = actual_est.siguiente
    tabla += '</TABLE>'
    dot.node("matriz", f'<{tabla}>', shape="plaintext")
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    output_path = os.path.join(data_dir, f"{nombre}.gv")
    dot.render(output_path, view=True, format="png")

def matriz_patron(estaciones, sensores_ids):
    actual_est = estaciones.head
    print("      ", end="")
    for id_sensor in sensores_ids:
        print(f"s{id_sensor}".ljust(8), end="")
    print()
    while actual_est:
        print(f"n{actual_est.id_estacion}".ljust(6), end="")
        for id_sensor in sensores_ids:
            valor = actual_est.sensores.obtener_valor(id_sensor)
            print(str(1 if valor != 0 else 0).ljust(8), end="")
        print()
        actual_est = actual_est.siguiente

def procesar_patrones_suelo(ruta_xml):
    estaciones_suelo = EstacionLista()
    sensores_ids = cargar_matriz_suelo_sin_print(ruta_xml, estaciones_suelo)
    matriz_patron(estaciones_suelo, sensores_ids)
    graficar_matriz_patron(estaciones_suelo, sensores_ids, nombre="matriz_patron_suelo")

def procesar_patrones_cultivo(ruta_xml):
    estaciones_cultivo = EstacionLista()
    sensores_ids = cargar_matriz_cultivo_sin_print(ruta_xml, estaciones_cultivo)
    matriz_patron(estaciones_cultivo, sensores_ids)
    graficar_matriz_patron(estaciones_cultivo, sensores_ids, nombre="matriz_patron_cultivo")
def procesar_patrones_cultivo(ruta_xml):
    estaciones_cultivo = EstacionLista()
    sensores_ids = cargar_matriz_cultivo_sin_print(ruta_xml, estaciones_cultivo)
    matriz_patron(estaciones_cultivo, sensores_ids)
    graficar_matriz_patron(estaciones_cultivo, sensores_ids, nombre="matriz_patron_cultivo")


