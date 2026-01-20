import csv
from pathlib import Path
from rich.console import Console
from rich.table import Table
import os
import sys
#from paquetes.AgustinVeron.Menu import limpiar_pantalla
import paquetes.LisandroRojas.funcionesLisandro_prolijo as FL
""" opcional para eyectar la terminal
import subprocess
subprocess.run(["cmd", "/k", "python", "main.py"])
 """
#import paquetes.AgustinVeron.Menu as MenuAgus
##################################
#lisandro
#mucha pelea con como manejar los archivos y las rutas
def elegir_archivo():
    from pathlib import Path
    from rich.console import Console
    console = Console()

    estaCarpeta = Path(__file__).resolve().parent
    exe_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else None
    try:
        script_dir = Path(sys.argv[0]).resolve().parent
    except Exception:
        script_dir = Path.cwd()

    search_dirs = [d for d in (exe_dir, script_dir, Path.cwd(), estaCarpeta) if d is not None]

    # recolectar .csv (sin duplicados)
    seen = set()
    archCSV = []
    for d in search_dirs:
        for p in sorted(Path(d).glob("*.csv")):
            rp = str(p.resolve())
            if rp not in seen:
                seen.add(rp)
                archCSV.append(p)

    while True:
        console.print("\n📂 Archivos CSV encontrados:", style="bold cyan")
        if archCSV:
            for i, a in enumerate(archCSV, 1):
                console.print(f"  {i}. {a.name}")
            console.print("  0. Introducir ruta completa")
            console.print("  S. Salir")
            opt = input("Seleccione una opción: ").strip()
            if opt.lower() == "s":
                exit()
            if opt == "0":
                ruta = input("Ruta completa del CSV: ").strip().strip('"')
                p = Path(ruta)
                if p.exists() and p.suffix.lower() == ".csv":
                    return p
                console.print("Archivo no válido o no existe.", style="red")
                continue
            if opt.isdigit():
                idx = int(opt)
                if 1 <= idx <= len(archCSV):
                    return archCSV[idx - 1]
            console.print("Opción inválida.", style="red")
        else:
            console.print("  No se encontraron .csv en las ubicaciones inspeccionadas.", style="yellow")
            ruta = input("Ingrese ruta completa del CSV (o S para salir): ").strip()
            if ruta.lower() == "s":
                exit()
            p = Path(ruta.strip('"'))
            if p.exists() and p.suffix.lower() == ".csv":
                return p
            console.print("Archivo no válido. Intente nuevamente.", style="red")

#LIMITE DE EJECUCION:  10 PROCESOS [PROCESADOS] , entrar todo. necesitamos los rotos para el informe
def leer_procesos(csv_path: Path):
    """ lee el csv y devuelve una lista de objetos Proceso """
    (listaProcesos) = [] #lista
    valid_count = 0
    with csv_path.open(mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        for row_number, row in enumerate(reader,start=1):#
            if not row:
                continue
            if len(row)!=4:
                raise ValueError(
                    f"Error en fila {row_number}, campos insuficientes para simulador"
                )
            if valid_count >= 10:
                print("No se admiten mas de 10 procesos para este simulador.")
                break#
            #=============== EN ESTE ORDEN SE USAN LOS CAMPOS DE VALORES DE LOS ARCHIVOS CSV ================
            id_proceso,t_arribo,tamaño,t_irrupcion = row
            #=============== EN ESTE ORDEN SE USAN LOS CAMPOS DE VALORES DE LOS ARCHIVOS CSV ================
            try: #todo va bien
                proceso = {
                "id": id_proceso,
                "t_arribo": int(t_arribo),
                "tamaño": int(tamaño),
                "t_irrupcion": int(t_irrupcion),
                "bandera_baja_logica": False
                }
            except ValueError as e: #todo fue horrible
                raise ValueError(f"Fallo en linea {row_number} del archivo") from e
            print("Proceso ingresado:")
            print(f"ID={proceso['id']} | arribo={proceso['t_arribo']} | tamaño={proceso['tamaño']} | irrupcion={proceso['t_irrupcion']}")
            if (proceso.get("tamaño")<=250): #agrega (listaProcesos) nuevos solo si alcanzan a entrar en como minimo en la particion mas grande
                print("A sido cargado")
                (listaProcesos).append(proceso) 
                valid_count+=1
            else:
                print("A sido rechazado por tamaño de proceso por encima del tamaño mas grande de particiones del simulador de 250k")
            
        if (len(listaProcesos))<1:
            return False

    (listaProcesos).sort(key=lambda p: p["t_arribo"])
    return (listaProcesos)

def mostrar_tabla(procesos):
    console = Console()
      #renderizar la tablita hermosa con rich, ciclando los objetos en Procesos
    table = Table(title="Procesos Cargados", show_lines=True)
    table.add_column("ID Proceso", justify="right", style="yellow", no_wrap=True)
    table.add_column("Tiempo Arribo", justify="right")
    table.add_column("Tamaño",justify="right" )
    table.add_column("Tiempo Irrupcion", justify="right")
    table.add_column("ESTADO", justify="right")
    for p in procesos:
        estadoActual=FL.actualizar_estado_Proceso(p)
        table.add_row( #medio tipo:  array[0] pero con los key del diccionario
            str(p["id"]),
            str(p["t_arribo"]),
            str(p["tamaño"]),
            str(p["t_irrupcion"]),
            #str(p["bandera_baja_logica"])
            estadoActual
        )
    console.print(table)


########################################################################################################################################################
#viejo_isabel
#
#def elegir_archivo_csv():
#    carpeta_simulador = Path(__file__).resolve().parent  # carpeta donde está funcionesconlistas_otro.py
#    archivos_csv = list(carpeta_simulador.glob("*.csv"))
#
#    print("\n📂 Archivos CSV disponibles en la carpeta del simulador:")
#    for i, archivo in enumerate(archivos_csv, start=1):
#        print(f"{i}. {archivo.name}")
#
#    print("========= OTRAS OPCIONES=========")
#    print("0. Elegir archivo externo (fuera de la carpeta del simulador)")
#    print("S. Cancelar y salir del simulador")
#    
#    opcion = str(input("\nSeleccione una opcion: "))
#
#    if opcion.lower() == "s":
#        print("SALIENDO.....")
#        exit()
#    
#    if opcion.isdigit():
#        opcion = int(opcion)
#        if opcion == 0:
#            ruta = input("Ingrese la ruta completa del archivo externo: ")
#            return Path(ruta)
#        else:
#            return archivos_csv[opcion - 1]
#    else:
#        return Path(opcion)
#
##LIMITE DE EJECUCION:  10 PROCESOS [PROCESADOS] , entrar todo. necesitamos los rotos para el informe
#def leer_procesos(csv_path: Path):
#    """ lee el csv y devuelve una lista de objetos Proceso """
#    #csv_path = csv_path = Path.cwd() / csv_filename
#    (listaProcesos) = [] #lista
#    valid_count = 0
#    with csv_path.open(mode="r", newline="", encoding="utf-8") as f:
#        reader = csv.reader(f, delimiter=',')
#        for row_number, row in enumerate(reader,start=1):#
#            if not row:
#                continue
#            if len(row)!=4:
#                raise ValueError(
#                    f"Error en fila {row_number}, campos insuficientes para simulador"
#                )
#            if valid_count >= 10:
#                print("No se admiten mas de 10 (listaProcesos) para este simulador.")          #### mmmm revisar esto
#                #print("Hasta acá llegaste papu")
#                break#
#            id_proceso,t_arribo,tamaño,t_irrupcion = row#
#            try: #todo va bien
#                proceso={ # formato diccionario
#                    "id": str(id_proceso),
#                    "t_arribo": int(t_arribo),
#                    "tamaño": int(tamaño),
#                    "t_irrupcion" : int(t_irrupcion),
#                    "bandera_baja_logica": False
#                }
#            except ValueError as e: #todo fue horrible
#                raise ValueError(f"Fallo en linea {row_number} del archivo") from e
#            print("Proceso ingresado:")
#            print(f"ID={proceso['id']} | arribo={proceso['t_arribo']} | tamaño={proceso['tamaño']} | irrupcion={proceso['t_irrupcion']}")
#            if (proceso.get("tamaño")<=250): #agrega (listaProcesos) nuevos solo si alcanzan a entrar en como minimo en la particion mas grande
#                print("A sido cargado")
#                (listaProcesos).append(proceso) 
#                valid_count+=1#
#            else:
#                print("A sido rechazado por tamaño por encima del tamaño mas grande de particiones del simulador de 250k")
#            
#        if (len((listaProcesos)))<1:
#            return False
#
#    (listaProcesos).sort(key=lambda p: p["t_arribo"])
#    return (listaProcesos)
#

# 
#test
#estado_global_copy.listaProcesos=leer_procesos('procesos.csv')
#mostrar_tabla(estado_global_copy.listaProcesos)
######################################################






##############################################################
#for debug: esto se tiene que hacer en el main despues

#procesos=leer_procesos('procesos.csv')
#mostrar_tabla(procesos)
#

""" 

Se exporta leer_procesos()  y mostrar_tabla()  para el MENU (Agustin)>>

'from testcsv import leer_procesos, mostrar_tabla, mover_proceso'

"""
