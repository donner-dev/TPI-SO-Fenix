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
import paquetes.LisandroRojas.funcionesconlistas_isabel_arregladoLisandro as FunArchivos
#import paquetes.estado_global as vGlobal

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
listaSuspendidos = []  ### * 
T_Simulacion=0
cantProcesosRestantes=0
multiprogramacion=0
aux=None
banderaMostrarTablas=False

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
                "t_arribo_MP": None,
                "t_irrupcion" : int(t_irrupcion),
                "tiempo_restante":0, 
                "t_finalizacion":0,
                "t_retorno": 0,
                "total_retorno": 0,
                "t_ingreso": 0,
                "t_respuesta": 0,           #Tiempo de espera en lista de nuevos.
                "t_totalenColaListo": 0,
                "bandera_baja_logica": False,
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
                    "total_retorno": None,
                    "t_ingreso": None,
                    "t_respuesta": None,
                    "t_totalenColaListo": 0,
                    "bandera_baja_logica": False,
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


def MPllena():
    for p in range(len(listaMP)):
        if listaMP[p]["Ocupado"] == False:
            return False
    return True

#Adaptar best Fit
def AsignPartBestFit(procActual):
    global T_Simulacion
    menorDifTamaño = 10**10
    pos = -1 
    for p in range(len(listaMP)):
        difTamaño= listaMP[p]["TamañoTotal"] - procActual["tamaño"]
        if ((difTamaño >= 0) and (difTamaño <= menorDifTamaño) and (listaMP[p]["Ocupado"] == False) and (not MPllena())):
            menorDifTamaño = difTamaño
            pos = p

    #si la posicion p es distinta de -1, se escogió una partición apta
    if pos != -1:
        listaMP[pos]["Fragmentacion Interna"]= listaMP[pos]["TamañoTotal"] - procActual["tamaño"]      
        listaMP[pos]["Proceso_alojado"]= procActual
        listaMP[pos]["Ocupado"]= True

def cabeEnAlgunaParticionLIBRE(listaMP,proc):
    for p in range(len(listaMP)):
        difTamaño= listaMP[p]["TamañoTotal"] - proc["tamaño"]
        if ((difTamaño >= 0) and (listaMP[p]["Ocupado"] == False)):
            return True
    return False


def mover_aColaListo(procActual):
    global T_Simulacion

    #Proceso entró en ámbito de multiprogramación
    procActual["bandera_baja_logica"] = True
    
    #Tiempo en que quedó esperando en la lista de nuevos.
    if procActual["t_respuesta"] == None:
        procActual["t_respuesta"] = T_Simulacion - procActual["t_arribo"]
    else: 
        procActual["t_respuesta"] = procActual.get("t_respuesta")

    procActual["t_totalenColaListo"]= 0    

    #preparar tiempo de ingreso: Instante en que el sim. lo acomoda en mem. secundaria
    if procActual["t_ingreso"] == None:
        procActual["t_ingreso"] = T_Simulacion
    else:
        procActual["t_ingreso"] = procActual.get("t_ingreso")

    #preparar tiempo de arribo: cuando llega a memoria principal
    procActual["t_arribo_MP"] = T_Simulacion
    #ingresa proceso a listaListos (cola de turnos)
    
    global aux
    aux = procActual
    listaListos.append(procActual)


def mover_aColaSuspendido(procActual):
    global T_Simulacion

    #Proceso entró en ámbito de multiprogramación
    procActual["bandera_baja_logica"] = True
    
    #Tiempo en que quedó esperando en la lista de nuevos.
    if procActual["t_respuesta"] == None:
        procActual["t_respuesta"] = T_Simulacion - procActual["t_arribo"]
    else: 
        procActual["t_respuesta"] = procActual.get("t_respuesta")

    #Guarda el instante en que ingresa al ámbito de la multiprogramación
    if procActual["t_ingreso"] == None:
        procActual["t_ingreso"] = T_Simulacion
    else:
        procActual["t_ingreso"] = procActual.get("t_ingreso")

    listaSuspendidos.append(procActual)


def mandarTerminados(procActual,indiceMP):
    global T_Simulacion
    
    #Marcar finalización
    procActual["t_finalizacion"] = T_Simulacion
    procActual["total_retorno"] = T_Simulacion - procActual["t_arribo_MP"] 

    #Hace que la partición esté disponible
    listaMP[indiceMP]["Ocupado"]= False
    
    #agregar a la lista de terminados
    listaTerminados.append(procActual)
    
    #quitar de la listaListos el proceso
    for p in listaListos():
        if p["id"] == procActual["id"]:
            listaListos.pop(procActual)
            break


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
    1. mover_aColaListo(proceso) → aux = proceso_listo (referencia a
       dict en listaListos)
    2. cargarProcesoAlojado(MP, puntero, aux) → MP[puntero]["Proceso_alojado"]
       = aux (MISMA REFERENCIA)
    3. En ejecutarTodo(): proceso_actual["t_RestanteCPU"] -= 1 (modifica ambos:
       listaListos Y MemoriaPrincipal simultáneamente porque son la misma referencia)
    4. BuscarSRTF() busca por 'id' en listaListos, encuentra el proceso con menor
       t_RestanteCPU, a ese proceso lo marca como en CPU colocando en TRUE el campo CPU que actua como bandera, y retorna el índice de su partición en MemoriaPrincipal.
    
    Esto es el puente entre:
    - FIFO (cola de admisión en listaListos)
    - SRTF (selección de quién entra a CPU)
    - Referencias compartidas (sincronización automática entre listas)
    """
    if len(listaListos) < 1:
        return None
    
    #Busca proceso en la cola de turnos (lista de listos)
    menorTR = float("inf")
    procesoElegido = None
    for proc in listaListos:
        tr = proc.get("t_RestanteCPU", 0)
        proc["CPU"] = False  #marcar que no está en CPU
        if tr > 0 and tr < menorTR:
            menorTR = tr
            procesoElegido = proc

    if procesoElegido is None:
        return None

    #El proceso encontrado en listaListos, ahora busca su índice en memoria
    procesoElegido["CPU"] = True  #marcar que está en CPU
    proceso_id = procesoElegido.get("id")
    for i, particion in enumerate(listaMP):
        proc_alojado = particion.get("Proceso_alojado")
        if proc_alojado and proc_alojado.get("id") == proceso_id:
            return i
    return None


def CARGAR_MPconMS():
    while len(listaListos) < 3:
        cambios = False
        for ingresa in list(listaSuspendidos):
            if cabeEnAlgunaParticionLIBRE(ingresa):
                mover_aColaListo(ingresa)
                AsignPartBestFit(aux)
                cambios = True
        #QuitarListosDeSuspendidos() lo voy a poner directamente aca xq es super especifico de esta funcion
        ids_listos = {p.get("id") for p in listaListos}
        listaSuspendidos[:] = [p for p in listaSuspendidos if p.get("id") not in ids_listos]

        if not cambios:
            break

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
    global multiprogramacion
    global banderaMostrarTablas
    #verif. si la suma de procesos en el ámbito de mpg es >=5
    multiprogramacion = len(listaListos) + len(listaSuspendidos)
    if multiprogramacion >= 5:
        return

    #si listaListos menor a 3 y listaSuspendidos no vacía 
    if len(listaListos) < 3 and listaSuspendidos:
        CARGAR_MPconMS()

    while multiprogramacion < 5:
        cambios = False
        for proceso in listaNuevos:
            if proceso.get("bandera_baja_logica") is False and proceso.get("t_arribo") <= T_simulador:
                if len(listaListos) < 3 and cabeEnAlgunaParticionLIBRE(proceso):
                    mover_aColaListo(proceso)
                    AsignPartBestFit(aux)
                    cambios = True
                else:
                    mover_aColaSuspendido(proceso)
                    cambios = True
                multiprogramacion = len(listaListos) + len(listaSuspendidos)
                if multiprogramacion >= 5:
                    return
        if not cambios:
            break #sale del while si no hubo cambios
        else:
            banderaMostrarTablas = True # actualizar tablas en caso de cambios (usar esta bandera)
    multiprogramacion = len(listaListos) + len(listaSuspendidos)


# aca agregamos las funciones de ciclos osiosos y la control de multiprogramacion == 0 para adelantar tiempo de simulacion a los intantes de arribos
def CiclosOciosos(proceso_siguiente: dict):
    """
    Si no hay procesos listos avanza el tiempo del simulador hasta el próximo arribo
    y acumula el tiempo de CPU ocioso.
    """
    global multiprogramacion
    global T_Simulacion

    # recalcular multiprogramacion
    multiprogramacion = len(listaListos) + len(listaSuspendidos)

    # si hay procesos listos no hay ciclado ocioso
    if len(listaListos) > 0:
        return 

    if not proceso_siguiente:
        return

    t_arribo = proceso_siguiente.get("t_arribo")
    if t_arribo is None:
        return

    if t_arribo >= T_simulador:
        multiprogramacion = len(listaListos) + len(listaSuspendidos)
        avanzar = t_arribo - T_simulador
        T_CPU_ocioso += avanzar
        T_simulador = t_arribo
        multiprogramacion = len(listaListos) + len(listaSuspendidos)

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
    for p in listaNuevos:
        if (p.get("bandera_baja_logica") is False) and (p.get("t_arribo") <= T_simulador):
            pendiente=p
            return pendiente
 
    # próximo arribo futuro
    for p in listaNuevos:
        if (p.get("t_arribo") > T_simulador) and (p.get("bandera_baja_logica") is False):
            #print(f"Busqueda del siguiente encontró un proceso del futuro {p}")
            return p
    return None

def detectar_terminacion(proceso, indice_procesoEjecucion) -> bool:
    global banderaMostrarTablas
    if proceso["tiempo_restante"] == 0:
        banderaMostrarTablas = True
        print(f"El proceso {proceso['id']} ha finalizado su ejecución.")
        # Manda a terminados
        mandarTerminados(proceso, indice_procesoEjecucion) # esta funcion tiene que copiar este proceso en la lista de terminados y removerlo de listos
        return True


################################# FUNCIONES MOSTRARTABLAS ################################
def mostrarColaListos():  #ezequiel
    """ Muestra la tabla de procesos en lista de listos """
    
def mostrarCPU():  #ezequiel
    """ Muestra la tabla de procesos en CPU """

def mostrarMemoriaPrincipal():  #isabel
    """ Muestra la tabla de particiones de memoria principal """

def mostrarColaSuspendidos():  #isabel
    console = Console()
    table = Table(title=" [ Procesos en Memoria Secundaria --> Estado: 'Listo y Suspendido' ]", show_lines=True)
    headers = ["ID Proceso", "Tiempo Arribo", "Tamaño", "Tiempo Irrupcion", "Tiempo de Respuesta", "Tiempo de Ingreso", "Tiempo Restante de CPU"]
    for h in headers:
        table.add_column(h, justify="right")
    if listaSuspendidos:
        for p in listaSuspendidos:
            table.add_row(*(str(p.get(k, "xxx")) for k in ["id", "t_arribo", "tamaño", "t_irrupcion", "t_Respuesta", "t_ingreso", "t_RestanteCPU"]))
    else:
        table.add_row(*["xxx"] * len(headers))
    console.print(table)

def mostrarTerminados(): #agustin
    """ Muestra la tabla de procesos terminados """



####################################### FUNCIONES GRÁFICAS ######################################
#        borradisimo









############# BUCLE DE EJECUCIÓN #############
while len(listaTerminados) < len(listaNuevos):
    
    banderaMostrarTablas = False # bandera para mostrar tablas si hay cambios en admision o terminacion
    procesoEjecucion = None
    
    #CICLOS OCIOSOS SI NO HAY PROCESOS EN LISTOS
    proceso_siguiente = buscarSiguiente() #esta parte revisa los ciclos osiosos antes de tratar cualquier proceso
    CiclosOciosos(proceso_siguiente)
    
    # PRIMERO: ciclos ociosos para hacer admision de procesos
    # tiempo del simulador parejo con los procesos que van llegando para hacer la admision de ese instante
    
    ADMICION_MULTI_5()

    ########## EJECUCION #########
    #SEGUNDO buscar el proceso SRTF
    indice_procesoEjecucion = BuscarSRTF() # retorna el indice de la particion en memoria principal que contiene el proceso con menor tiempo restante
    
    if indice_procesoEjecucion is None:
        continue # vuelve al while mayor para un ciclo ocioso

    procesoEjecucion = listaMP[indice_procesoEjecucion]["Proceso_alojado"]

    while (procesoEjecucion is not None) and (procesoEjecucion["tiempo_restante"] > 0):
        
        banderaMostrarTablas = False # bandera para mostrar tablas si hay cambios en admision o terminacion
        
        # Ejecutar un ciclo de CPU
        procesoEjecucion["tiempo_restante"] -= 1
        T_simulador += 1
        
        # Sumar tiempo de espera a los demas procesos en listaListos ya cargados para este ciclo
        for otrosProcesos in listaListos:
            if otrosProcesos["id"] != procesoEjecucion["id"]:
                otrosProcesos["t_totalenColaListo"] += 1
        
        # Verificar si llegó un nuevo proceso para admisión
        ADMICION_MULTI_5() #acomoda memoria si es necesario y luego termina de admitir

        #revisa si el proceso en ejecucion ha terminado
        if detectar_terminacion(procesoEjecucion, indice_procesoEjecucion):
            #detectar_terminacion manda el proceso a terminados, y quita de la cola de listos y libera la partición disponiendola (ocupado = falso)
            procesoEjecucion = None
                
        # Manejo de cambio de contexto (cuando termina un proceso, busca otro para ejecutar)
        if (len(listaListos) > 0) and (procesoEjecucion is None):
            print(f"Cambio de contexto al siguiente proceso SRTF.")
            indice_procesoEjecucion = BuscarSRTF()
            procesoEjecucion = listaMP[indice_procesoEjecucion]["Proceso_alojado"]
            print(f"Cambio de contexto: {procesoEjecucion['id']} ingresa a CPU")

        ADMICION_MULTI_5() # revisar si hay admision de nuevos procesos después del cambio de contexto para ocupar el espacio liberado
        indice_procMasPrioridad = BuscarSRTF()
        procMasPrioridad = listaMP[indice_procMasPrioridad]["Proceso_alojado"]
        
        # control de APROPIACION de CPU para la admision de nuevos procesos causado por ADMICION_MULTI_5
        if procMasPrioridad is not None:      
            if procMasPrioridad["id"] != procesoEjecucion["id"]:
                print(f"Cambio de contexto: {procesoEjecucion['id']} sale -> {procMasPrioridad['id']} APROPIA CPU")
                procesoEjecucion = procMasPrioridad
                indice_procesoEjecucion = indice_procMasPrioridad
                # la tabla de CPU se actualiza en la siguiente sección gráfica
        
        if banderaMostrarTablas == True:#mostrar por pantalla el estado actual del simulador
            #Mostrar pantalla
            banderaMostrarTablas = False # resetear bandera para otro ciclo
            

    #Más abajo mostrar el informe

def mostrar_listaTerminados():
    
