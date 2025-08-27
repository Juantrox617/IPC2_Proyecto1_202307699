import os

def cargarXML(tipo):
    nArchivo = input("Ingrese el nombre del archivo XML: ")
    if nArchivo == '':
        return ''
    nombre_archivo = f"{nArchivo}.xml"
    rutaArchivo = os.path.join('data', nombre_archivo)
    if os.path.exists(rutaArchivo):
        return rutaArchivo
    else:
        print(f"Archivo no encontrado: {rutaArchivo}")
        return ''
