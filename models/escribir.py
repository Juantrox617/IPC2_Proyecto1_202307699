import xml.etree.ElementTree as ET
import os

def escribir_xml(nombre_archivo, contenido_dict):
<<<<<<< HEAD
=======
  
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42
    root = ET.Element("camposAgricolas")
    for campo in contenido_dict.get("campos"):
        campo_elem = ET.SubElement(root, "campo", id=campo.get("id", ""), nombre=campo.get("nombre", ""))
        estaciones_base = ET.SubElement(campo_elem, "estacionesBase")
        for est in campo.get("estaciones"):
            ET.SubElement(estaciones_base, "estacion", id=est.get("id", ""), nombre=est.get("nombre", ""))
        sensores_suelo = ET.SubElement(campo_elem, "sensoresSuelo")
        for sensor in campo.get("sensoresSuelo"):
            sensor_elem = ET.SubElement(sensores_suelo, "sensorS", id=sensor.get("id", ""), nombre=sensor.get("nombre", ""))
            for freq in sensor.get("frecuencias"):
                ET.SubElement(sensor_elem, "frecuencia", idEstacion=freq.get("idEstacion", "")).text = str(freq.get("valor", ""))
        sensores_cultivo = ET.SubElement(campo_elem, "sensoresCultivo")
        for sensor in campo.get("sensoresCultivo"):
            sensor_elem = ET.SubElement(sensores_cultivo, "sensorT", id=sensor.get("id", ""), nombre=sensor.get("nombre", ""))
            for freq in sensor.get("frecuencias"):
                ET.SubElement(sensor_elem, "frecuencia", idEstacion=freq.get("idEstacion", "")).text = str(freq.get("valor", ""))
    tree = ET.ElementTree(root)
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    ruta = os.path.join(data_dir, f"{nombre_archivo}.xml")
    tree.write(ruta, encoding="utf-8", xml_declaration=True)
    print(f"Archivo XML creado en: {ruta}")
<<<<<<< HEAD
    print(f"Archivo XML creado en: {ruta}")
=======
>>>>>>> 155241e1a95a18d1151ada5545762801de6a6d42
