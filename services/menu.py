from services.cargar_archivos import cargarXML
from models.matriz import EstacionLista, cargar_matriz_suelo, cargar_matriz_cultivo
from models.matrizPatrones import procesar_patrones_suelo, procesar_patrones_cultivo

def menu():
    ruta_archivo = ''
    while True:
        print("\n--- Menú Principal ---")
        print("1. Cargar archivo XML")
        print("2. Procesar archivo (matrices de suelo y cultivo)")
        print("3. Mostrar matrices de patrones")
        print("4. Salir")
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
                cargar_matriz_suelo(ruta_archivo, estaciones_suelo)
                estaciones_cultivo = EstacionLista()
                cargar_matriz_cultivo(ruta_archivo, estaciones_cultivo)
        elif opcion == '3':
            if not ruta_archivo:
                print("Primero debe cargar un archivo XML.")
            else:
                procesar_patrones_suelo(ruta_archivo)
                procesar_patrones_cultivo(ruta_archivo)
        elif opcion == '4':
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()


