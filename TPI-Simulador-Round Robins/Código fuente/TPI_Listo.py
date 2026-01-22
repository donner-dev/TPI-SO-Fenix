###################################### IMPORTS ######################################
import csv
from pathlib import Path
from typing import Dict
from rich.console import Console
from rich.table import Table
import msvcrt
import time
import sys
import os
sys.path.append('..')


""" Importé las funciones de SIMULADOR.py  para tenerlo modulado como se habia discutido (vamos viendo si queda bien o no) """
import paquetes.LisandroRojas.funcionesLisandro_prolijo as Lis
import paquetes.AgustinVeron.Menu as MA
import paquetes.estado_global as vGlobal
import paquetes.LisandroRojas.funcionesconlistas_isabel_arregladoLisandro as FunArchivos




###################################### VARIABLES GLOBALES ######################################
listaNuevos=[]
listaSuspendidos=[]
listaListos=[]
listaMP=[
    {
        "Particion": 1,
        "TamañoTotal": 250,
        "Dueño": "usuario",
        "Proceso_alojado": {}, #MemoriaPrincipal[puntero]["Proceso_alojado"]= asigna VARIABLE_proceso_actual, asigna el diccionario completo del proceso
        "Fragmentacion Interna":0,
        "dirComienzo": 151,
        "Ocupado": False
    },
    {
        "Particion": 2,
        "TamañoTotal": 150,
        "Dueño": "usuario",
        "Proceso_alojado": {},
        "Fragmentacion Interna":0,
        "dirComienzo": 51,
        "Ocupado": False
    },
    {
        "Particion": 3,
        "TamañoTotal": 50,
        "Dueño": "usuario",
        "Proceso_alojado": {},
        "Fragmentacion Interna":0,
        "dirComienzo": 0,
        "Ocupado": False
    },
]
listaTerminados=[]

T_Simulacion=0
cantProcesosRestantes=0
multiprogramacion=0

#variables de cálculo:
Sumatoria_TRetorno= 0
Sumatoria_TEspera= 0

paso1=None
paso2=None

###################################### MENÚ ######################################
""" Podemos revisar en donde van las funciones del menú, si acá o en otro archivo aparte?  mas que nada lo del render de logo- Donner """
#Dimensiones de pantalla
xMaxPantalla = 90
yMaxPantalla = 34
#Posicion vertical de las opciones
pos_opciones = (yMaxPantalla//2)+12
pos_opciones2 = (yMaxPantalla//2)+6
#Colores para strings
NEGRITA = "\033[1m"
AZUL="\033[44m" 
ROJO="\033[41m" 
VERDE="\033[42m"
AMARILLO="\033[43m"
NEGRO="\033[30m"
BLANCO="\033[47m"
RESET = "\033[0m"
#Teclas
TECLA_ENTER    = '\r'
TECLA_ARRIBA   = '\xe0H'
TECLA_ABAJO    = '\xe0P'

#Clean Screen (Limpiar pantalla)
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

#Gotoxy (se posiciona en un punto específico de la pantalla)
def gotoxy(x, y):
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()

#Lee un caracter ingresado desde el teclado directamente desde el buffer de entrada
def read_single_key_windows():
    tecla_bytes = msvcrt.getch()
    if tecla_bytes == b'\xe0' or tecla_bytes == b'\x00':
        return tecla_bytes.decode('latin-1') + msvcrt.getch().decode('latin-1')  
    return tecla_bytes.decode('latin-1')

#Limpia el buffer de entrada del teclado
def limpiar_buffer_entrada():
    while msvcrt.kbhit():
        msvcrt.getch()

#Logo del engranaje
def mostrar_logo():
    '''
    ---por cada linea---
    Asigno string
    Me posiciono; imprimo
    '''
    mensajeOp = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)-1,3); print(mensajeOp)
    mensajeOp = f"░{ROJO}++++++++++++++++++++{RESET}{NEGRO}%#{RESET}{VERDE}++++++++++++++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+13,4); print(mensajeOp)
    mensajeOp = f"░{ROJO}++++++++++++++++++++{RESET}{NEGRO}%#{RESET}{VERDE}++++++++++++++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+13,5); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++++++++++++++++{RESET}{NEGRO}%*:{RESET}{BLANCO}..{RESET}{NEGRO}-%#{RESET}{VERDE}+++++++++++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,6); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++++++++{RESET}{NEGRO}%%%#+++*%{RESET}{BLANCO}.....{RESET}{NEGRO}*%++++%%%*{RESET}{VERDE}+++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,7); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++++++{RESET}{NEGRO}%%:{RESET}{BLANCO}...{RESET}{NEGRO}%%={RESET}{BLANCO}..........{RESET}{NEGRO}%%*{RESET}{BLANCO}...{RESET}{NEGRO}#%*{RESET}{VERDE}+++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,8); print(mensajeOp)
    mensajeOp = f"░{ROJO}++++++{RESET}{NEGRO}%%{RESET}{BLANCO}.........................{RESET}{NEGRO}*%{RESET}{VERDE}+++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,9); print(mensajeOp)
    mensajeOp = f"░{ROJO}++++++++{RESET}{NEGRO}%#{RESET}{BLANCO}......{RESET}{NEGRO}:%%%%%%%+{RESET}{BLANCO}.......{RESET}{NEGRO}%#{RESET}{VERDE}++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+31,10); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++++++{RESET}{NEGRO}%%{RESET}{BLANCO}.....{RESET}{NEGRO}#%*{RESET}{AZUL}++++++++{RESET}{NEGRO}%%:{RESET}{BLANCO}....{RESET}{NEGRO}=%{RESET}{VERDE}++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,11); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++{RESET}{NEGRO}%%%*={RESET}{BLANCO}.....{RESET}{NEGRO}%%{RESET}{AZUL}++++++++++++{RESET}{NEGRO}%:{RESET}{BLANCO}....{RESET}{NEGRO}:=#%%{RESET}{VERDE}++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,12); print(mensajeOp)
    mensajeOp = f"░{NEGRO}%%%%#{RESET}{BLANCO}.......{RESET}{NEGRO}:%{RESET}{AZUL}+++++++++++++{RESET}{NEGRO}%%{RESET}{BLANCO}........{RESET}{NEGRO}%%%%%{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+31,13); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++{RESET}{NEGRO}%%{RESET}{BLANCO}........{RESET}{NEGRO}%*{RESET}{AZUL}++++++++++++{RESET}{NEGRO}%#{RESET}{BLANCO}........{RESET}{NEGRO}%{RESET}{AMARILLO}+---{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,14); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++++{RESET}{NEGRO}*#%#{RESET}{BLANCO}....{RESET}{NEGRO}:%#{RESET}{AZUL}++++++++++{RESET}{NEGRO}%%{RESET}{BLANCO}.....{RESET}{NEGRO}%%#{RESET}{AMARILLO}+-----{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,15); print(mensajeOp)
    mensajeOp = f"░{AZUL}++++++++{RESET}{NEGRO}%%{RESET}{BLANCO}.....{RESET}{NEGRO}-%%#+++*%%#{RESET}{BLANCO}.....{RESET}{NEGRO}:%{RESET}{AMARILLO}+--------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+31,16); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++++++{RESET}{NEGRO}%#{RESET}{BLANCO}.......................{RESET}{NEGRO}:%%{RESET}{AMARILLO}-------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,17); print(mensajeOp)
    mensajeOp = f"░{AZUL}++++++{RESET}{NEGRO}*%#{RESET}{BLANCO}....{RESET}{NEGRO}-:{RESET}{BLANCO}...........{RESET}{NEGRO}.+{RESET}{BLANCO}....{RESET}{NEGRO}:%%{RESET}{AMARILLO}-------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,18); print(mensajeOp)
    mensajeOp = f"░{AZUL}++++++++{RESET}{NEGRO}*%%%%*+%%%{RESET}{BLANCO}.....={RESET}{NEGRO}%%*=%%#%%{RESET}{AMARILLO}---------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,19); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++++++++++++++++{RESET}{NEGRO}%-{RESET}{BLANCO}....{RESET}{NEGRO}%%{RESET}{AMARILLO}-----------------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,20); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++++++++++++++++{RESET}{NEGRO}*%%%%%%{RESET}{AMARILLO}------------------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+13,21); print(mensajeOp)
    mensajeOp = f"░{AZUL}++++++++++++++++++++{RESET}{NEGRO}%*{RESET}{AMARILLO}--------------------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+13,22); print(mensajeOp)
    mensajeOp = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)-1,23); print(mensajeOp)

#Logo de la carpeta
def mostrar_logo2():
    # El dibujo tiene aproximadamente 42 caracteres de ancho.
    mensajeOp = "        ............                                " 
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),5); print(mensajeOp)
    mensajeOp = "       .=-        .%.                               " 
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),6); print(mensajeOp)
    mensajeOp = "       .=:         %.......................         "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),7); print(mensajeOp)
    mensajeOp = "       .=:         .......................==.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),8); print(mensajeOp)
    mensajeOp = "       .+*================================++.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),9); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),10); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),11); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),12); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),13); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),14); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),15); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),16); print(mensajeOp)
    mensajeOp = "       .=-                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),17); print(mensajeOp)
    mensajeOp = "        ..:::::::::::::::::::::::::::::::::.        "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),18); print(mensajeOp)


def mostrar_menu():
    mostrar_logo()
    mensajeOp = f"{NEGRITA}SIMULADOR DE GESTIÓN Y PLANIFICACIÓN DE PROCESOS{RESET}"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+4,(yMaxPantalla//2)+8)
    print(mensajeOp)
    mensajeOp = "Presione una tecla para iniciar la simulación:"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),(yMaxPantalla//2)+10)
    print(mensajeOp)
    mensajeOp = "Iniciar Simulacion"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),pos_opciones)
    print("\033[1;4;36m" + mensajeOp + "\033[0m")
    gotoxy(3,yMaxPantalla-2)
    print("V1.0 - ROUND ROBINS",end="")
    gotoxy(xMaxPantalla-12,yMaxPantalla-2)
    print("U.T.N FRRe",end="")
    #posicion del puntero en la posicion maxima en x e y para dibujar toda la pantalla
    gotoxy(xMaxPantalla,yMaxPantalla+2)

#Desplazamiento y selección en el menú principal
def selec_opcion_menu1():
    # Siempre devuelve la primera opción (0 + 1 = 1)
    X_PUNTERO = ((xMaxPantalla // 2) - 11)  

    # Dibujar directamente el puntero en la primera opción
    gotoxy(X_PUNTERO, pos_opciones)
    print("▶")

    # Esperar a que se presione Enter
    while True:
        tecla = read_single_key_windows()
        if tecla == TECLA_ENTER:
            break

    # Devuelve siempre 1
    return 1


#Desplazamiento y selección del menú para cargar procesos
def selec_opcion_menu2():
    limpiar_pantalla()
    mostrar_logo2()
    for y in range(1, yMaxPantalla):
        for x in range(1, xMaxPantalla):
            if (x == 1) or (x == xMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
            if (y == 1) or (y == yMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
    
    mensajeOp = "Use las flechas (⬆︎ ⬇︎) y presione (Enter)"
    gotoxy((xMaxPantalla-len(mensajeOp))//2+2,yMaxPantalla//2+4)
    print(mensajeOp)
    mensajeOp = "(1)-Cargar procesos mediante archivo (.csv)"
    gotoxy((xMaxPantalla-len(mensajeOp))//2,yMaxPantalla//2+6)
    print(mensajeOp)
    mensajeOp = "(2)-Carga manual de procesos"
    gotoxy((xMaxPantalla-len(mensajeOp))//2,yMaxPantalla//2+7)
    print(mensajeOp)
    # El índice de la opción seleccionada (0: Archivo, 1: Manual)
    pos_puntero = 0
    tecla = ''
    NUM_OPCIONES = 2 
    X_PUNTERO = (xMaxPantalla // 2) - 24 
    while True:
        # 1) Borrar el puntero de la posición anterior
        pos_puntero_ant = pos_puntero
        # 2) Lectura de tecla (Espera activa por un input)
        tecla = read_single_key_windows()
        # 3) Lógica de movimiento (Solo se ejecuta si se presionó una tecla válida)
        if tecla == TECLA_ARRIBA:
            pos_puntero = (pos_puntero - 1) % NUM_OPCIONES
        elif tecla == TECLA_ABAJO:
            pos_puntero = (pos_puntero + 1) % NUM_OPCIONES
        elif tecla == TECLA_ENTER:
            # Sale del bucle cuando se presiona Enter
            break 
        # 4. Redibujar Puntero (Solo si la posición cambió o si se leyó una tecla)
        if tecla:
            # Borrar puntero antiguo: Imprimir un espacio ' ' en la posición vertical anterior.
            gotoxy(X_PUNTERO, pos_opciones2 + pos_puntero_ant)
            print(" ", end="", flush=True) 
            # Dibujar puntero nuevo: Imprimir la flecha '▶' en la nueva posición.
            gotoxy(X_PUNTERO, pos_opciones2 + pos_puntero)
            print("▶", end="", flush=True)
        # importante: Mover el cursor al final de la pantalla después de redibujar
        # para que el próximo "print" del sistema operativo no arruine el menú.
        gotoxy(xMaxPantalla, yMaxPantalla + 2)

       
    return pos_puntero + 1 # Devuelve 1, 2, o 3 (el número de opción)

""" REVISAR si no cambiamos por la otra funcion.  - Donner """
def carga_manual_procesos(): 
    limpiar_pantalla()
    global cantProcesosRestantes
    """ carga procesos manualmente y devuelve una lista de objetos Proceso """
    procesos = []
    valid_count = 0
    ids_usados=set() #para evitar repetidos
    print("Se aceptarán hasta 10 procesos. Ingrese los datos solicitados.")
    while valid_count < 10:
        print(f"\n---Ingrese datos del proceso {valid_count+1}: ---")
        id_proceso = input("ID Proceso: ")
        if not id_proceso:
            print("El ID del proceso no puede estar vacío.")
            continue
        if id_proceso in ids_usados:
            print(f"Error: El ID '{id_proceso}' ya ha sido ingresado. Intente con otro.")
            continue
        
        try:
            tamaño = int(input("Tamaño (en KB, max 250): "))
            t_arribo = int(input("Tiempo de Arribo (entero no negativo): "))
            t_irrupcion = int(input("Tiempo de Irrupción (entero positivo): "))

            if tamaño <= 0 or t_arribo < 0 or t_irrupcion <= 0:
                 print("Error: El tamaño y la irrupción deben ser positivos. El arribo no debe ser negativo.")
                 continue
            

            if tamaño > 250:
                print("El tamaño del proceso excede la capacidad máxima permitida (250 KB). Intente nuevamente.")
                continue

        except ValueError:
            print("Error: Se esperaba un número entero para tamaño, arribo o irrupción.")
            continue

        
        proceso={ # formato diccionario
                "id": str(id_proceso),
                "tamaño": int(tamaño),
                "t_arribo": int(t_arribo),
                "t_irrupcion" : int(t_irrupcion),
                "tiempo_restante":0, 
                "t_finalizacion":0,
                "t_retorno": 0,
                "t_espera": 0,
                "admitido": False
            }
        procesos.append(proceso)
        ids_usados.add(id_proceso) # Añadir el ID al conjunto de usados
        valid_count += 1

    procesos.sort(key=lambda p: p["t_arribo"])

    cantProcesosRestantes=valid_count
    
    return procesos


def ejecutarMenu():
    global paso1
    global paso2
    limpiar_pantalla()
    mostrar_menu()
    limpiar_buffer_entrada()
    paso1 = selec_opcion_menu1()
    if paso1 == 1:
        paso2 = selec_opcion_menu2()
    elif paso1 == 2:
        paso2 = selec_opcion_menu2()
    elif paso1 == 3:
        limpiar_pantalla()
        sys.exit()
    


def leer_procesos(csv_filename: str):
    """Lee el CSV y devuelve una LISTA de procesos (diccionarios) ordenados por t_arribo"""
    
    #csv_path = Path(__file__).resolve().parent / csv_filename
    csv_path = Path.cwd() / csv_filename
    nuevos = []  # lista de procesos
    valid_count = 0

    # Verificar si el archivo existe
    if not csv_path.exists():
        return []  # devolvemos lista vacía para que el simulador no rompa

    with csv_path.open(mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')

        for row_number, row in enumerate(reader, start=1):
            if not row:
                continue
            if len(row) != 4:
                raise ValueError(
                    f"Error en fila {row_number}, campos insuficientes para simulador"
                )
            if valid_count >= 10:
                print("No se admiten más de 10 procesos para este simulador.")
                break

            id_proceso, tamaño, t_arribo, t_irrupcion = row
            try:
                tamaño_int = int(tamaño)
                if tamaño_int > 250:
                    print(f"Proceso {id_proceso} descartado: tamaño {tamaño_int} excede el máximo permitido (250).")
                    continue  # salta este proceso y no lo agrega

                proceso = {
                    "id": id_proceso,
                    "tamaño": tamaño_int,
                    "t_arribo": int(t_arribo),
                    "t_arribo_MP": None, # <-- campo adicional para calculo de tiempos de retorno
                    "t_irrupcion": int(t_irrupcion),
                    "tiempo_restante": int(t_irrupcion),
                    "t_finalizacion": 0,
                    "t_retorno": 0,
                    "t_espera": 0,
                    "admitido": False
                }
            except ValueError as e:
                raise ValueError(
                    f"Fallo en línea {row_number} del archivo"
                ) from e

            nuevos.append(proceso)
            valid_count += 1

    # Ordenar la lista por t_arribo
    lista_procesos_ordenados = sorted(
        nuevos,
        key=lambda proceso: proceso['t_arribo']
    )

    return lista_procesos_ordenados




#################################### FUNCIONES DE LA EJECUCIÓN ###################################

#def MPllena():
#    for p in range(len(listaMP)):
#        if listaMP[p]["Ocupado"] == False:
#            return False
#    return True


#
def AsignPartBestFit(procActual):
    global T_Simulacion
    menorDifTamaño = 10**10
    pos = -1
    for p in range(len(listaMP)):
        difTamaño= listaMP[p]["TamañoTotal"] - procActual["tamaño"]
        if ((difTamaño >= 0) and (difTamaño <= menorDifTamaño) and (listaMP[p]["Ocupado"] == False) and (not MPllena())):
            menorDifTamaño = difTamaño
            pos = p
    
    if pos != -1:
        listaMP[pos]["Fragmentacion Interna"]= listaMP[pos]["TamañoTotal"] - procActual["tamaño"]
        #Alojamiento para posterior cálculo de tiempos correspondientes
        listaMP[pos]["Proceso_alojado"]= procActual
        listaMP[pos]["Proceso_alojado"]["t_retorno"]= 0
        listaMP[pos]["Proceso_alojado"]["t_espera"]= T_Simulacion 
        listaMP[pos]["Ocupado"]= True

#
#def asignListaSuspendidos(procActual):
#    listaSuspendidos.append(procActual)
#
def mandarTerminados(procActual,indiceMP):
    # Marcar finalización
    procActual["t_finalizacion"] = T_simulador
    # Calcular tiempo de retorno
    procActual["t_retorno"] = procActual["t_finalizacion"] - procActual["t_arribo_MP"]
    #Hace que la partición esté disponible
    listaMP[indiceMP]["Ocupado"]= False
    #Lo lleva a la lista de terminados
    listaTerminados.append(procActual)
    for p in listaListos():
        if p["id"] == procActual["id"]:
            listaListos.pop(procActual)
            break

#

def BuscarSRTF() -> Optional[int]:
    """
    Busca el proceso con menor tiempo restante (SRTF) entre los listos que tengan
    t_RestanteCPU > 0. Retorna el índice de la partición donde está alojado ese
    proceso o None.

    ════════════════════════════════════════════════════════════════════════
    IMPORTANCIA: Comparamos por 'id' (campo del proceso) en lugar de usar 'is'
    (identidad de objeto).
    ════════════════════════════════════════════════════════════════════════
    Esto es más robusto porque:
    - Si se hace una copia del dict en algún punto, seguirá teniendo el mismo 'id'
    - 'is' solo funciona si es exactamente la misma referencia en memoria
    - Al comparar por 'id', toleramos copias involuntarias y mantenemos consistencia

    ════════════════════════════════════════════════════════════════════════
    RELACIÓN CON FIFO Y MEMORIA PRINCIPAL
    ════════════════════════════════════════════════════════════════════════
    
    Flujo esperado (referencias):
    1. mover_aColaListo(proceso) → vGlobal.aux = proceso_listo (referencia a
       dict en listaListos)
    2. cargarProcesoAlojado(MP, puntero, vGlobal.aux) → MP[puntero]["Proceso_alojado"]
       = vGlobal.aux (MISMA REFERENCIA)
    3. En ejecutarTodo(): proceso_actual["t_RestanteCPU"] -= 1 (modifica ambos:
       listaListos Y MemoriaPrincipal simultáneamente porque son la misma referencia)
    4. BuscarSRTF() busca por 'id' en listaListos, encuentra el proceso con menor
       t_RestanteCPU, y retorna el índice de su partición en MemoriaPrincipal.
    
    Esto es el puente entre:
    - FIFO (cola de admisión en listaListos)
    - SRTF (selección de quién entra a CPU)
    - Referencias compartidas (sincronización automática entre listas)
    """
    if len(vGlobal.listaListos) <1:
        return None

    menorTR = float("inf")
    procesoElegido = None
    for proc in vGlobal.listaListos:
        tr = proc.get("t_RestanteCPU", 0)
        if tr > 0 and tr < menorTR:
            menorTR = tr
            procesoElegido = proc

    if procesoElegido is None:
        return None

    # Comparar por 'id' en lugar de 'is' (identidad)
    proceso_id = procesoElegido.get("id")
    for i, particion in enumerate(vGlobal.MemoriaPrincipal):
        proc_alojado = particion.get("Proceso_alojado")
        if proc_alojado and proc_alojado.get("id") == proceso_id:
            return i
    return None

### tenemos que adaptar los nombres de funciones y de campos de valores de los diccionarios de procesos

""" Funciones que usa CARGAR_MPconMS (Agustin e Isabel)"""
#cabeEnAlgunaParticionLIBRE(proceso)
#mover_aColaListo(proceso)
#BestFitCICLO_ADMICION(vGlobal.aux)
#cargarProcesoAlojado(vGlobal.MemoriaPrincipal, puntero, vGlobal.aux)

def actualizar_proceso_enMemoriaPrincipal(lista: List, particion_actualizada: Dict) -> bool:
    """Actualiza los campos de una partición en MemoriaPrincipal (por Particion).
    ════════════════════════════════════════════════════════════════════════
    FIFO + MEMORIA PRINCIPAL
    ════════════════════════════════════════════════════════════════════════
    - Esta función actualiza una partición completa de MP.
    - Lo que muta aquí son los campos de la partición (Ocupado, Fragmentacion_Interna, etc.)
      Y el dict "Proceso_alojado" que es una REFERENCIA a un proceso en listaListos.

    - Si modificas particion_actualizada["Proceso_alojado"]["t_RestanteCPU"],
      eso afecta a AMBOS:
      a) El proceso en listaListos (que es la misma referencia)
      b) El dict en MP[i]["Proceso_alojado"]
    
    - Esto garantiza que la cola FIFO (listaListos) y la Memoria Principal
      están siempre sincronizadas.
    """
    for p in lista:
        if p.get("Particion") == particion_actualizada.get("Particion"):
            p.update(particion_actualizada)
            return True
    return False

def cargarProcesoAlojado(memoria: List, puntero: int, proceso_actual: Dict):
    """
    Asigna por referencia el dict del proceso a la partición seleccionada.
    """
    particion = memoria[puntero]
    particion["Proceso_alojado"] = proceso_actual
    particion["Fragmentacion_Interna"] = int(particion["TamañoTotal"] - proceso_actual.get("tamaño", 0))
    particion["Ocupado"] = True
    actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal, particion)

#SuspendidosYListos() ????

def CARGAR_MPconMS():
    """
    Carga MP con procesos desde suspendidos hasta tener 3 en listos.
    Elimina de suspendidos los procesos que ya están en la lista de listos.
    Usa slice assignment [:] para mantener la referencia al objeto lista original,
    evitando que otras referencias externas pierdan sincronía.

    ════════════════════════════════════════════════════════════════════════
    FIFO EN PROMOCIÓN DE MEMORIA SECUNDARIA A PRINCIPAL
    ════════════════════════════════════════════════════════════════════════
    - listaSuspendidos es una cola FIFO de procesos que no caben en MP.
    - Cuando libera espacio en MP (un proceso termina), esta función trae
      procesos de listaSuspendidos hacia listaListos.
    - Lo hace RECORRIENDO EN ORDEN (FIFO): los primeros suspendidos son los
      primeros en entrar a MP.
    - Esto mantiene coherencia: los primeros que llegaron, primeros entran a MP,
      primeros se ejecutan.
    - La relación con MemoriaPrincipal es directa: mover_aColaListo() crea una
      referencia que cargarProcesoAlojado() coloca en una partición de MP.
    """
    while len(vGlobal.listaListos) < 3:
        cambios = False
        for ingresa in list(vGlobal.listaSuspendidos):
            if cabeEnAlgunaParticionLIBRE(ingresa):
                mover_aColaListo(ingresa)
                puntero = BestFitCICLO_ADMICION(vGlobal.aux)
                if puntero is not None:
                    cargarProcesoAlojado(vGlobal.MemoriaPrincipal, puntero, vGlobal.aux)
                cambios = True
        SuspendidosYListos()
        if not cambios:
            break

#Funciones adaptadas que usa ADMICION_MULTI_5 (Agustin e Isabel)
def  marcar_procesoNuevo_Ingresado(procesoNuevo: Dict):
    #Marca en listaProcesos que el proceso ya fue ingresado (bandera_baja_logica)
    for p in vGlobal.listaProcesos:
        if p.get("id") == procesoNuevo.get("id") and p.get("bandera_baja_logica") is False:
            p["bandera_baja_logica"] = True
            break  #return True?

def actualizar_proceso_enLista(lista: List, proceso_actualizado: Dict) -> bool:
    """ 
    Actualiza el dicc de un proceso dentro de una lista por ID
    TRUE = Lo actualizo, FALSE = No lo encontré
    (!) Si el proceso tambien esta en MP como referencia, la mutacion se propaga automaticamente

    Ejemplo de sincronización automática:
    - p_listo = listaListos[i] (misma referencia que MP[j]["Proceso_alojado"])
    - actualizar_proceso_enLista(listaListos, {"id": p_listo["id"], "t_RestanteCPU": 5})
    - Ahora MP[j]["Proceso_alojado"]["t_RestanteCPU"] también es 5
    
    Este es el corazón de cómo FIFO + MemoriaPrincipal se sincronizan sin
    copias redundantes.
    """
    for p in lista:
        if p.get("id") == proceso_actualizado.get("id"):
            p.update(proceso_actualizado)
            return True
    return False

def mover_aColaSuspendido(proceso_actual:Dict):
    """
    Construye el dict necesario y mueve el proceso a la lista de suspendidos.
    Mantiene referencias correctas usando actualizar_proceso_enLista cuando corresponde.
    """
    marcar_procesoNuevo_Ingresado(proceso_actual)

    cargarTiempoRespuesta = int(vGlobal.T_simulador - proceso_actual.get("t_arribo", vGlobal.T_simulador))
    cargarTiempoIngreso = int(proceso_actual.get("t_ingreso", vGlobal.T_simulador))
    t_Restante = int(proceso_actual.get("t_RestanteCPU", proceso_actual.get("t_irrupcion", 0)))

    proceso_suspendido = {
        "id": proceso_actual.get("id"),
        "t_arribo": proceso_actual.get("t_arribo"),
        "tamaño": proceso_actual.get("tamaño"),
        "t_irrupcion": proceso_actual.get("t_irrupcion"),
        "t_Respuesta": cargarTiempoRespuesta,
        "t_ingreso": cargarTiempoIngreso,
        "t_RestanteCPU": t_Restante,
    }
    if not actualizar_proceso_enLista(vGlobal.listaSuspendidos, proceso_suspendido):
        vGlobal.listaSuspendidos.append(proceso_suspendido)
    

def ADMICION_MULTI_5():
    """
    Admite procesos manteniendo multiprogramacion <= 5 y hasta 3 procesos en
    MP simultáneamente.

    ════════════════════════════════════════════════════════════════════════
    ALGORITMO DE ADMISIÓN (FIFO + Planificador a Largo Plazo)
    ════════════════════════════════════════════════════════════════════════
    
    Restricciones:
    - multiprogramacion <= 5: máximo 5 procesos entre listos y suspendidos
    - listaListos <= 3: máximo 3 procesos en Memoria Principal
    - Si no caben en MP, van a listaSuspendidos (Memoria Secundaria)
    
    Orden de admisión (FIFO):
    1. Primero, trae procesos de listaSuspendidos a listaListos (CARGAR_MPconMS)
       usando BestFit hasta tener 3 en MP. Esto respeta FIFO: los primeros
       suspendidos entran primero a MP.
    
    2. Luego, recorre listaProcesos en orden (FIFO):
       - Si t_arribo <= T_simulador y bandera_baja_logica == False:
         a) Si cabe en MP: mover_aColaListo(proceso) + cargarProcesoAlojado()
         b) Si NO cabe: mover_aColaSuspendido(proceso)
       - Se detiene cuando multiprogramacion >= 5
    
    Relación con MemoriaPrincipal:
    - Los procesos en listaListos están ALOJADOS en particiones de MP.
    - Cada vGlobal.aux que entra es referencia en MP[i]["Proceso_alojado"].
    - Modificar listaListos afecta automáticamente a MemoriaPrincipal porque
      es la MISMA REFERENCIA.
    """
    vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)
    if vGlobal.multiprogramacion >= 5:
        return

    if len(vGlobal.listaListos) < 3 and vGlobal.listaSuspendidos:
        CARGAR_MPconMS()

    while vGlobal.multiprogramacion < 5:
        cambios = False
        for proceso in vGlobal.listaProcesos:
            if proceso.get("bandera_baja_logica") is False and proceso.get("t_arribo") <= vGlobal.T_simulador:
                if len(vGlobal.listaListos) < 3 and cabeEnAlgunaParticionLIBRE(proceso):
                    mover_aColaListo(proceso)
                    puntero = BestFitCICLO_ADMICION(vGlobal.aux)
                    if puntero is not None:
                        cargarProcesoAlojado(vGlobal.MemoriaPrincipal, puntero, vGlobal.aux)
                    cambios = True
                else:
                    mover_aColaSuspendido(proceso)
                    cambios = True
                vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)
                if vGlobal.multiprogramacion >= 5:
                    return
        if not cambios:
            break #sale del while si no hubo cambios
        else:
            banderaMostrarTablas = True # actualizar tablas en caso de cambios
    vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)



def cabeEnAlgunaParticion(listaMP,proc):
    for p in range(len(listaMP)):
        difTamaño= listaMP[p]["TamañoTotal"] - proc["tamaño"]
        if ((difTamaño >= 0) and (listaMP[p]["Ocupado"] == False)):
            return True
    return False


# aca agregamos las funciones de ciclos osiosos y la control de multiprogramacion == 0 para adelantar tiempo de simulacion a los intantes de arribos

def CiclosOciosos(proceso_siguiente: Dict):
    """
    Si no hay procesos listos avanza el tiempo del simulador hasta el próximo arribo
    y acumula el tiempo de CPU ocioso.
    """
    # recalcular multiprogramacion
    vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)

    # si hay procesos listos no hay ciclado ocioso
    if len(vGlobal.listaListos) > 0:
        return 

    if not proceso_siguiente:
        return

    t_arribo = proceso_siguiente.get("t_arribo")
    if t_arribo is None:
        return

    if t_arribo >= vGlobal.T_simulador:
        vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)
        avanzar = t_arribo - vGlobal.T_simulador
        vGlobal.T_CPU_ocioso += avanzar
        vGlobal.T_simulador = t_arribo
        vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)

def buscarSiguiente():
    """
    Busca y retorna el siguiente proceso pendiente de admisión o el próximo
    arribo futuro.

    ════════════════════════════════════════════════════════════════════════
    ORDEN DE BÚSQUEDA (FIFO en listaProcesos)
    ════════════════════════════════════════════════════════════════════════
    1. Procesos con `bandera_baja_logica` == False y `t_arribo` <= tiempo
       actual (procesos ya arribados y no ingresados).
    2. Procesos cuyo `t_arribo` coincide con el instante actual.
    3. Si no hay ninguno, retorna el primer proceso futuro (próximo arribo).

    ════════════════════════════════════════════════════════════════════════
    CONCEPTO FIFO AQUÍ
    ════════════════════════════════════════════════════════════════════════
    - Recorre listaProcesos secuencialmente (como en un archivo CSV FIFO).
    - Los primeros procesos que se encuentran con t_arribo <= T_simulador
      son retornados para admisión.
    - buscarSiguiente() actúa como "visor FIFO": devuelve el próximo proceso
      que necesita atención de admisión.
    - El SO (en ADMICION_MULTI_5()) luego decide si lo coloca en listaListos
      (si cabe en MP) o en listaSuspendidos (si no cabe).
    - La admisión respeta FIFO: los primeros procesos que caben van a MP,
      los demás van a MS y esperan su turno.

    Devuelve el dict del proceso o `None` si no hay procesos pendientes.
    """
    # primero pendientes ya arribados pero sin ingresar o el proceso que arribo en este ciclo
    pendiente=None
    #banderaEncontrado=False
    for p in vGlobal.listaProcesos:
        if (p.get("bandera_baja_logica") is False) and (p.get("t_arribo") <= vGlobal.T_simulador):
            #banderaEncontrado=True
            pendiente=p
            #break
            return pendiente
        if (p.get("t_arribo") == vGlobal.T_simulador):
            pendiente=p
            return pendiente
    #if banderaEncontrado==True:
    #    #print(f"Busqueda del siguiente PROCESO encontro un proceso esperando ingresar |ID: {pendiente["id"]} || T.ARRIBO: {pendiente["t_arribo"]} || TAMAÑO: {pendiente["tamaño"]} || T.IRRUPCION: {pendiente["t_irrupcion"]} |")
    #    return pendiente
    # próximo arribo futuro
    for p in vGlobal.listaProcesos:
        if (p.get("t_arribo") > vGlobal.T_simulador) and (p.get("bandera_baja_logica") is False):
            #print(f"Busqueda del siguiente encontró un proceso del futuro {p}")
            return p
    return None

def detectar_terminacion(proceso, indice_procesoEjecucion) -> bool:
    if proceso["tiempo_restante"] == 0:
        banderaMostrarTablas = True
        print(f"El proceso {proceso['id']} ha finalizado su ejecución.")
        # Manda a terminados
        mandarTerminados(proceso, indice_procesoEjecucion) # esta funcion tiene que copiar este proceso en la lista de terminados y removerlo de listos
        # Disminuye multiprogramación y se activa planificador de memoria
        ADMICION_MULTI_5()# Recalcula multiprogramación después de mandar a terminados
        return True

####################################### FUNCIONES GRÁFICAS ######################################
#
#def tablaNuevos():
#    console = Console()
#
#    # Crear tabla
#    table = Table(title="Procesos en estado de Nuevo", show_lines=True)
#
#    # Agregar columnas
#    table.add_column("Posición", justify="center", style="yellow", no_wrap=True)
#    table.add_column("ID  ", justify="center", style="yellow", no_wrap=True)
#    table.add_column("Tiempo de Arribo", justify="center" ,style="yellow")
#    table.add_column("Tiempo de Irrupcion", justify="center", style="yellow")
#
#    # Agregar filas de ejemplo
#    for i in range(len(listaNuevos)):
#        table.add_row(str(i+1), str(listaNuevos[i]["id"]), str(listaNuevos[i]["t_arribo"]), str(listaNuevos[i]["t_irrupcion"]))
#
#    # Mostrar tabla
#    console.print(table)
#
#
#
#def tablaMemoriaPrincipal():
#    console = Console()
#
#    # Crear tabla
#    table = Table(title="Procesos en estado de Listo (En Memoria Principal)", show_lines=True)
#
#    # Agregar columnas
#    table.add_column("Partición", justify="right", style="yellow")
#    table.add_column("Tamaño Total", justify="right", style="yellow")
#    table.add_column("Dir. comienzo", justify="right", style="yellow")
#    table.add_column("Frag. Interna", justify="right", style="yellow")
#    table.add_column("ID Proceso", justify="center", style="yellow", no_wrap=True)
#    table.add_column("T. de Arribo", justify="center", style="yellow")
#    table.add_column("T. de Irrupcion", justify="center", style="yellow")
#    table.add_column("Dueño", justify="center", style="yellow")
#
#
#    # Primero agregamos la fila del SO
#    table.add_row(
#        str(0),          # número de partición del SO (puede ser fijo)
#        str(251),          # número de partición del SO (puede ser fijo)
#        "-",
#        str(100),        # tamaño reservado al SO
#        "-",             # no tiene id
#        "-",             # no hay proceso
#        "-",             # no hay arribo
#        "SO"             # dueño = sistema operativo
#    )
#
#    # Luego recorremos las particiones de usuario
#    for i in range(len(listaMP)):
#        proc = listaMP[i]["Proceso_alojado"]
#        table.add_row(
#            str(listaMP[i]["Particion"]),
#            str(listaMP[i]["TamañoTotal"]),
#            str(listaMP[i]["dirComienzo"]),
#            str(listaMP[i]["Fragmentacion Interna"]),
#            str(proc.get("id", "-")),
#            str(proc.get("t_arribo", "-")),
#            str(proc.get("t_irrupcion", "-")),
#            str(listaMP[i]["Dueño"])
#        )
#
#    # Mostrar tabla
#    gotoxy(1,14)
#    console.print(table)
#
#
#def listosYSuspendidos():
#    console = Console()
#
#    # Crear tabla
#    table = Table(title="Procesos en estado de Listo y Suspendido (L/S)", show_lines=True)
#
#    # Agregar columnas
#    table.add_column("Posición", justify="center", style="yellow", no_wrap=True)
#    table.add_column("ID Proceso", justify="center", style="yellow", no_wrap=True)
#    table.add_column("TamañoTotal", justify="center", style="yellow")
#    table.add_column("Tiempo de Arribo", justify="center", style="yellow")
#    table.add_column("Tiempo de Irrupcion", justify="center", style="yellow")
#
#    # Recorrer lista de suspendidos
#    for i in range(len(listaSuspendidos)):
#        proc = listaSuspendidos[i]  # proc es un diccionario
#        table.add_row(
#            str(i+1),
#            str(proc.get("id", "-")),
#            str(proc.get("tamaño", "-")),
#            str(proc.get("t_arribo", "-")),
#            str(proc.get("t_irrupcion", "-"))
#        )
#
#    # Mostrar tabla
#    console.print(table)
#
#
#def mostrarProcesoCPU(proc):
#    console = Console()
#    table = Table(title="Proceso en ejecución (CPU)", show_lines=True)
#
#    table.add_column(" ID  ", justify="center", style="yellow")
#    table.add_column("Tiempo de Arribo", justify="center", style="yellow")
#    table.add_column("Tiempo de Irrupción", justify="center", style="yellow")
#    table.add_column("Tiempo Restante", justify="center", style="yellow")
#
#    table.add_row(
#        str(proc.get("id", "-")),
#        str(proc.get("t_arribo", "-")),
#        str(proc.get("t_irrupcion", "-")),
#        str(proc.get("tiempo_restante", "-"))
#    )
#
#    console.print(table)
#
#
#def tablaTerminados():
#    global Sumatoria_TRetorno
#    global Sumatoria_TEspera
#    global T_Simulacion
#
#    for i in range(len(listaTerminados)):
#        Sumatoria_TEspera= listaTerminados[i]["t_espera"] + Sumatoria_TEspera
#        Sumatoria_TRetorno= listaTerminados[i]["t_retorno"] + Sumatoria_TRetorno
#    
#
#    console = Console()
#
#    gotoxy(1,1)
#    console.print("[bold underline grey70]Informe estadístico[/bold underline grey70]")
#    gotoxy(1,2)
#    print("Tiempo de Espera promedio:", Sumatoria_TEspera / len(listaTerminados), "(ut)")
#    gotoxy(1,3)
#    print("Tiempo de Retorno promedio:", Sumatoria_TRetorno / len(listaTerminados), "(ut)")
#    gotoxy(1,4)
#    rendimientoSistema = len(listaTerminados) / T_Simulacion
#    print("Rendimiento del sistema:", round(rendimientoSistema, 3), "(procesos/ut)")
#    print()
#
#    # Crear tabla
#    table = Table(title="Procesos en estado de Terminados", show_lines=True)
#
#    # Agregar columnas
#    table.add_column("Posición", justify="center", style="yellow", no_wrap=True)
#    table.add_column("ID  ", justify="center", style="yellow", no_wrap=True)
#    table.add_column("Tiempo de Arribo", justify="center" ,style="yellow")
#    table.add_column("Tiempo de Irrupcion", justify="center", style="yellow")
#    table.add_column("Tiempo de Espera", justify="center", style="yellow")
#    table.add_column("Tiempo de Retorno", justify="center", style="yellow")
#
#    # Agregar filas de ejemplo
#    for i in range(len(listaTerminados)):
#        table.add_row(
#            str(i+1),
#            str(listaTerminados[i]["id"]),
#            str(listaTerminados[i]["t_arribo"]),
#            str(listaTerminados[i]["t_irrupcion"]),
#            str(listaTerminados[i]["t_espera"]),
#            str(listaTerminados[i]["t_retorno"])),
#
#    # Mostrar tabla
#    console.print(table)
#    print()
#    console.print(f"[italic grey70]Simulación terminada...[/italic grey70]")
#
#def informacionEjecucion():
#    console = Console()
#    gotoxy(80,27)
#    console.print("[bold underline grey70]Estado de simulacion[/bold underline grey70]")
#    gotoxy(80,29)
#    console.print(f"[italic grey70]Tiempo simulación: {T_Simulacion}[/italic grey70]")
#    gotoxy(80,30)
#    console.print(f"[italic grey70]Multiprogramación: {multiprogramacion}[/italic grey70]")
#    gotoxy(80,31)
#    console.print(f"[italic grey70]Procesos restantes: {cantProcesosRestantes}[/italic grey70]")
#
#
#def mostrarPosCPU(posCpu):
#    if posCpu == 0:
#        posCpu= -1
#    elif posCpu==2:
#        posCpu= 3
#    gotoxy(120,21+posCpu)
#    print("\033[1m\033[30m\033[47m 🡄 CPU \033[0m")
#
#
#
####################################### ACÁ EMPIEZA EL CÓDIGO ######################################
#=========================== COLUMNA VERTEBRAL DEL SIMULADOR
#ejecutarMenu()
#
##CARGA DE ARCHIVO EN NUEVOS#
#############(0)#############
#if paso2 != 2:
#    while listaNuevos == []:
#        listaNuevos = leer_procesos("LOTE_3.csv")
#        if listaNuevos == []:
#            limpiar_pantalla()
#            gotoxy(xMaxPantalla//2+17,yMaxPantalla//2)
#            print("No se cargó el archivo .csv")
#            gotoxy(xMaxPantalla//2,yMaxPantalla//2+1)
#            print("Asegurate de que esté en la misma carpeta que el ejecutable")
#            gotoxy(xMaxPantalla//2-6,yMaxPantalla//2+2)
#            print("Cerrá el simulador y colocá el .CSV en la misma carpeta que el ejecutable!")
#            msvcrt.getch()
#            limpiar_pantalla()
#
#    cantProcesosRestantes= len(listaNuevos)
#else:
#    listaNuevos= carga_manual_procesos()
#    

#############(1)#############
##Admisión principal
ADMICION_MULTI_5()

############# BUCLE DE EJECUCIÓN #############
while len(listaTerminados) < len(listaNuevos):
    #CICLOS OCIOSOS SI NO HAY PROCESOS EN LISTOS
    proceso_siguiente = buscarSiguiente() #esta parte revisa los ciclos osiosos antes de tratar cualquier proceso
    CiclosOciosos(proceso_siguiente)
    # PRIMERO ciclos ociosos para hacer admision de procesos
    # tiempo del simulador parejo con los procesos que van llegando para hacer la admision de ese instante
    ADMICION_MULTI_5()
    ########## EJECUCION #########
    #SEGUNDO buscar el proceso SRTF
    indice_procesoEjecucion = BuscarSRTF() # retorna el indice de la particion en memoria principal que contiene el proceso con menor tiempo restante
    procesoEjecucion = listaMP[indice_procesoEjecucion]["Proceso_alojado"]
    if procesoEjecucion is None:
        continue # vuelve al while mayor para un ciclo ocioso
    while (procesoEjecucion is not None) and (procesoEjecucion["tiempo_restante"] > 0):
        # Ejecutar un ciclo de CPU
        procesoEjecucion["tiempo_restante"] -= 1
        T_simulador += 1
        # Sumar tiempo de espera a los demas procesos en listaListos ya cargados para este ciclo
        for otrosProcesos in listaListos:
            if otrosProcesos["id"] != procesoEjecucion["id"]:
                otrosProcesos["t_espera"] += 1
        # Verificar si llegó un nuevo proceso para admisión
        ADMICION_MULTI_5() #acomoda memoria si es necesario y luego termina de admitir
        indice_procMasPrioridad = BuscarSRTF()
        procMasPrioridad = listaMP[indice_procMasPrioridad]["Proceso_alojado"]
        
        #revisa si el proceso en ejecucion ha terminado
        if detectar_terminacion(procesoEjecucion, indice_procesoEjecucion):#la termianacion del proceso en ejecucion ya usa ADMICION_MULTI_5()
            procesoEjecucion = None
                
        # Manejo de cambio de contexto
        if (len(listaListos) > 0) and (procesoEjecucion is None):
            print(f"Cambio de contexto al siguiente proceso SRTF.")
            indice_procesoEjecucion = BuscarSRTF()
            procesoEjecucion = listaMP[indice_procesoEjecucion]["Proceso_alojado"]
            print(f"Cambio de contexto: {procesoEjecucion['id']} ingresa a CPU")
        
        # control de APROPIACION de CPU para la admision de nuevos procesos causado por ADMICION_MULTI_5() en la linea 970
        if procMasPrioridad is not None:      
            if procMasPrioridad["id"] != procesoEjecucion["id"]:
                print(f"Cambio de contexto: {procesoEjecucion['id']} sale -> {procMasPrioridad['id']} APROPIA CPU")
                procesoEjecucion = procMasPrioridad
                indice_procesoEjecucion = indice_procMasPrioridad
                # la tabla de CPU se actualiza en la siguiente sección gráfica
        
        if banderaMostrarTablas == True:#mostrar por pantalla el estado actual del simulador
            banderaMostrarTablas = False # resetear bandera para otro ciclo
            #Funciones gráficas de pantalla
        
    ########## FIN EJECUCION #########


#
#====== ETAPA PARA REPORTE FINAL ===============
#    #Cálculos de tiempo de espera y de retorno
#    resPosSRTF = BuscarSRTF()
#    resProceso = listaMP[resPosSRTF]["Proceso_alojado"]
#
#    # Marcar inicio de ejecución
#    resProceso["t_inicio"] = T_Simulacion
#
#    # Calcular tiempo de espera
#    resProceso["t_espera"] = resProceso["t_inicio"] - resProceso["t_arribo"]
#
#    # Avanzar tiempo de simulación hasta que termine
#    T_Simulacion += resProceso["tiempo_restante"]
#
#    # Marcar finalización
#    resProceso["t_finalizacion"] = T_Simulacion
#
#    # Calcular tiempo de retorno
#    resProceso["t_retorno"] = resProceso["t_finalizacion"] - resProceso["t_arribo"]
#
#    # Ejecutar y terminar
#    resProceso["tiempo_restante"] = 0
#
#    #Manda a terminados
#    mandarTerminados(resProceso, resPosSRTF)
#    ##Disminuye multiprogramación y procesos restantes
#    multiprogramacion -= 1
#    cantProcesosRestantes -= 1
#
#
#    #Mostrar pantalla
#    limpiar_pantalla()
#    listosYSuspendidos()
#    tablaMemoriaPrincipal()
#    mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
#    mostrarPosCPU(BuscarSRTF())
#    informacionEjecucion()
#    print("Presione una tecla para continuar...")
#    msvcrt.getch()
#    limpiar_pantalla()
#
#    #Prepara proceso por SRTF pero no lo ejecuta
#    posPreparadoSRTF= BuscarSRTF()
#
#    #Mostrar pantalla
#    limpiar_pantalla()
#    listosYSuspendidos()
#    tablaMemoriaPrincipal()
#    mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
#    mostrarPosCPU(BuscarSRTF())
#    informacionEjecucion()
#    print("Presione una tecla para continuar...")
#    msvcrt.getch()
#    limpiar_pantalla()
#
#
#
#limpiar_pantalla()
#tablaTerminados()
#msvcrt.getch()
#
#