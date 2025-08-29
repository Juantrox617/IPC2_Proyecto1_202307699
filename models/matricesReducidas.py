from models.matriz import EstacionLista, EstacionNodo, SensorLista, SensorNodo
import os

def obtener_patron(estacion, sensores_ids):
    patron = []
    for id_sensor in sensores_ids:
        valor = estacion.sensores.obtener_valor(id_sensor)
        patron.append(1 if valor != 0 else 0)
    return tuple(patron)

def reducir_matriz(estaciones, sensores_ids):
    patrones = {}
    actual_est = estaciones.head
    while actual_est:
        patron = obtener_patron(actual_est, sensores_ids)
        if patron not in patrones:
            patrones[patron] = []
        patrones[patron].append(actual_est)
        actual_est = actual_est.siguiente

    matriz_reducida = EstacionLista()
    for idx, (patron, estaciones_grupo) in enumerate(patrones.items(), 1):
        suma_sensores = [sum(est.sensores.obtener_valor(id_sensor) for est in estaciones_grupo) for id_sensor in sensores_ids]
        if all(valor == 0 for valor in suma_sensores):
            continue  # No agregar filas con todos ceros
        id_estacion = f"n{'_'.join([est.id_estacion for est in estaciones_grupo])}"
        nueva_est = matriz_reducida.agregar_estacion(id_estacion)
        for id_sensor, suma in zip(sensores_ids, suma_sensores):
            nueva_est.sensores.agregar_sensor(id_sensor, suma)
    return matriz_reducida

def mostrar_matriz_reducida(matriz_reducida, sensores_ids):
    actual_est = matriz_reducida.head
    print("      ", end="")
    for id_sensor in sensores_ids:
        print(f"s{id_sensor}".ljust(8), end="")
    print()
    while actual_est:
        valores = [actual_est.sensores.obtener_valor(id_sensor) for id_sensor in sensores_ids]
        if any(valores):  # Solo mostrar si hay algún valor distinto de 0
            print(f"{actual_est.id_estacion}".ljust(6), end="")
            for valor in valores:
                print(str(valor).ljust(8), end="")
            print()
        actual_est = actual_est.siguiente

def graficar_matriz_reducida(matriz_reducida, sensores_ids, nombre):
    from graphviz import Digraph
    dot = Digraph(comment=nombre)
    tabla = '<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">'
    tabla += '<TR><TD><B>Estación/Sensor</B></TD>'
    for id_sensor in sensores_ids:
        tabla += f'<TD><B>s{id_sensor}</B></TD>'
    tabla += '</TR>'
    actual_est = matriz_reducida.head
    while actual_est:
        valores = [actual_est.sensores.obtener_valor(id_sensor) for id_sensor in sensores_ids]
        if any(valores):  # Solo mostrar si hay algún valor distinto de 0
            tabla += f'<TR><TD><B>{actual_est.id_estacion}</B></TD>'
            for valor in valores:
                tabla += f'<TD>{valor}</TD>'
            tabla += '</TR>'
        actual_est = actual_est.siguiente
    tabla += '</TABLE>'
    dot.node("matriz", f'<{tabla}>', shape="plaintext")
    import os
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    output_path = os.path.join(data_dir, f"{nombre}.gv")
    dot.render(output_path, view=True, format="png")

def reducir_matriz_cultivo(estaciones, sensores_ids):
    patrones = {}
    actual_est = estaciones.head
    while actual_est:
        patron = obtener_patron(actual_est, sensores_ids)
        if patron not in patrones:
            patrones[patron] = []
        patrones[patron].append(actual_est)
        actual_est = actual_est.siguiente

    matriz_reducida = EstacionLista()
    for idx, (patron, estaciones_grupo) in enumerate(patrones.items(), 1):
        suma_sensores = [sum(est.sensores.obtener_valor(id_sensor) for est in estaciones_grupo) for id_sensor in sensores_ids]
        if all(valor == 0 for valor in suma_sensores):
            continue
        id_estacion = f"n{'_'.join([est.id_estacion for est in estaciones_grupo])}"
        nueva_est = matriz_reducida.agregar_estacion(id_estacion)
        for id_sensor, suma in zip(sensores_ids, suma_sensores):
            nueva_est.sensores.agregar_sensor(id_sensor, suma)
    return matriz_reducida

def mostrar_matriz_reducida_cultivo(matriz_reducida, sensores_ids):
    actual_est = matriz_reducida.head
    print("      ", end="")
    for id_sensor in sensores_ids:
        print(f"s{id_sensor}".ljust(8), end="")
    print()
    while actual_est:
        valores = [actual_est.sensores.obtener_valor(id_sensor) for id_sensor in sensores_ids]
        if any(valores):
            print(f"{actual_est.id_estacion}".ljust(6), end="")
            for valor in valores:
                print(str(valor).ljust(8), end="")
            print()
        actual_est = actual_est.siguiente

def graficar_matriz_reducida_cultivo(matriz_reducida, sensores_ids, nombre):
    from graphviz import Digraph
    dot = Digraph(comment=nombre)
    tabla = '<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">'
    tabla += '<TR><TD><B>Estación/Sensor</B></TD>'
    for id_sensor in sensores_ids:
        tabla += f'<TD><B>s{id_sensor}</B></TD>'
    tabla += '</TR>'
    actual_est = matriz_reducida.head
    while actual_est:
        valores = [actual_est.sensores.obtener_valor(id_sensor) for id_sensor in sensores_ids]
        if any(valores):
            tabla += f'<TR><TD><B>{actual_est.id_estacion}</B></TD>'
            for valor in valores:
                tabla += f'<TD>{valor}</TD>'
            tabla += '</TR>'
        actual_est = actual_est.siguiente
    tabla += '</TABLE>'
    dot.node("matriz", f'<{tabla}>', shape="plaintext")
   
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    output_path = os.path.join(data_dir, f"{nombre}.gv")
    dot.render(output_path, view=True, format="png")


