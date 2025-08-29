from services.cargar_archivos import cargarXML
from models.matriz import EstacionLista, cargar_matriz_suelo, cargar_matriz_cultivo
from models.matrizPatrones import procesar_patrones_suelo, procesar_patrones_cultivo
from models.matricesReducidas import (
    reducir_matriz, mostrar_matriz_reducida, graficar_matriz_reducida,
    reducir_matriz_cultivo, mostrar_matriz_reducida_cultivo, graficar_matriz_reducida_cultivo
)

def menu():
    ruta_archivo = ''
    estaciones_suelo = None
    estaciones_cultivo = None
    sensores_suelo_head = None
    sensores_cultivo_head = None
    while True:
        print("\n--- Menú Principal ---")
        print("1. Cargar archivo XML")
        print("2. Procesar archivo (matrices de suelo y cultivo)")
        print("3. Mostrar matrices de patrones")
        print("4. Graficar matrices con Graphviz")
        print("5. Matrices reducidas")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            ruta_archivo = cargarXML('xml')
            if ruta_archivo:
                print("Archivo cargado correctamente.")
            else:
                print("No se pudo cargar el archivo.")
        elif opcion == '2':
            if not ruta_archivo:
                print("Primero debe cargar un archivo XML.")
            else:
                estaciones_suelo = EstacionLista()
                sensores_suelo_head = cargar_matriz_suelo(ruta_archivo, estaciones_suelo)
                estaciones_cultivo = EstacionLista()
                sensores_cultivo_head = cargar_matriz_cultivo(ruta_archivo, estaciones_cultivo)
        elif opcion == '3':
            if not ruta_archivo:
                print("Primero debe cargar un archivo XML.")
            else:
                procesar_patrones_suelo(ruta_archivo)
                procesar_patrones_cultivo(ruta_archivo)
        elif opcion == '4':
            if not ruta_archivo:
                print("Primero debe cargar un archivo XML.")
            else:
                print("Generando gráficos de matrices con Graphviz...")
                estaciones_suelo = EstacionLista()
                sensores_suelo_head = cargar_matriz_suelo(ruta_archivo, estaciones_suelo)
                estaciones_cultivo = EstacionLista()
                sensores_cultivo_head = cargar_matriz_cultivo(ruta_archivo, estaciones_cultivo)
                procesar_patrones_suelo(ruta_archivo)
                procesar_patrones_cultivo(ruta_archivo)
                print("Gráficos generados y abiertos.")
        elif opcion == '5':
            if not estaciones_suelo or not sensores_suelo_head or not estaciones_cultivo or not sensores_cultivo_head:
                print("Primero debe procesar el archivo para tener datos.")
            else:
                matriz_reducida_suelo = reducir_matriz(estaciones_suelo, sensores_suelo_head)
                print("Matriz reducida de estaciones con sensores (suelo):")
                mostrar_matriz_reducida(matriz_reducida_suelo, sensores_suelo_head)
                graficar_matriz_reducida(matriz_reducida_suelo, sensores_suelo_head, "matriz_suelo_reducida")
                matriz_reducida_cultivo = reducir_matriz_cultivo(estaciones_cultivo, sensores_cultivo_head)
                print("Matriz reducida de estaciones con sensores (cultivo):")
                mostrar_matriz_reducida_cultivo(matriz_reducida_cultivo, sensores_cultivo_head)
                graficar_matriz_reducida_cultivo(matriz_reducida_cultivo, sensores_cultivo_head, "matriz_cultivo_reducida")
                print("Gráficos de matrices reducidas generados en la carpeta data.")
        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()

