###################################### IMPORTS ######################################


import csv
from pathlib import Path
import sys
from rich.console import Console
from rich.table import Table


sys.path.append('..')
#import estado_global#no se esta usando, queda comentado, tira error esto cuando este modulo.py se importa en otros modulos

#ESTO USA TODO LISTAS PARA LA IMPLEMENTACION. TranQuilmes.
import msvcrt
import time
import sys
import os


######################################VARIABLES GLOBALES######################################
listaNuevos=[]
listaSuspendidos=[]
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
    while valid_count < 10: #ponganle a 3 para testing rapido
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
            

            #Esto no se si lo vamos a mantener, si igual tendria que permitirse, solo para la estadistica?
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

def MPllena():
    for p in range(len(listaMP)):
        if listaMP[p]["Ocupado"] == False:
            return False
    return True

def BuscarSRTF():
    menorTR = float('inf')
    mejorPosSRTF = -1

    for i, part in enumerate(listaMP):
        if part["Ocupado"] and part["Dueño"] == "usuario":
            # SRTF se basa en el tiempo restante de CPU
            tr = part["Proceso_alojado"]["tiempo_restante"]
            if tr < menorTR:
                menorTR = tr
                mejorPosSRTF = i

    return mejorPosSRTF

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


def asignListaSuspendidos(procActual):
    listaSuspendidos.append(procActual)

def mandarTerminados(procActual,posSRTF):
    #Quita proceso alojado de partición
    listaMP[posSRTF]["Proceso_alojado"]= {}
    #Hace que la partición esté disponible
    listaMP[posSRTF]["Ocupado"]= False
    #Lo lleva a la lista de terminados
    listaTerminados.append(procActual)


def planifLargoPlazo():
    global multiprogramacion
    for i in range(len(listaNuevos)):
        if T_Simulacion >= listaNuevos[i]["t_arribo"] and (listaNuevos[i]["admitido"]==False) and (multiprogramacion < 5):
            if not MPllena() and cabeEnAlgunaParticion(listaMP,listaNuevos[i]):
                AsignPartBestFit(listaNuevos[i])
                multiprogramacion= multiprogramacion + 1
            else:
                asignListaSuspendidos(listaNuevos[i])
                multiprogramacion= multiprogramacion + 1
            
            listaNuevos[i]["admitido"]=True
            


def cabeEnAlgunaParticion(listaMP,proc):
    for p in range(len(listaMP)):
        difTamaño= listaMP[p]["TamañoTotal"] - proc["tamaño"]
        if ((difTamaño >= 0) and (listaMP[p]["Ocupado"] == False) and (not MPllena())):
            return True
    return False



def planifMedioPlazo():
    i = 0
    while i < len(listaSuspendidos) and not MPllena():
        proc = listaSuspendidos[i]
        if cabeEnAlgunaParticion(listaMP, proc):
            proc = listaSuspendidos.pop(i)  # lo saco directamente
            
            AsignPartBestFit(proc)
            # no incremento i, porque ahora el siguiente proceso ocupa este índice
        else:
            i += 1  # paso al siguiente

def alcanzarTiempoOciosoInicio():
    #Si el tiempo de arribo del primer proceso es mayor a cero, el tiempo de simulación avanza hasta ese tiempo
    global T_Simulacion
    
    limpiar_pantalla()
    if len(listaNuevos) > 0 and (listaNuevos[0]["t_arribo"] > 0):
        print("Tiempo de simulación requiere ajuste. T_Sim Actual:", T_Simulacion)
        T_Simulacion = listaNuevos[0]["t_arribo"]
        print("Tiempo de simulación ajustado a:", T_Simulacion)
        msvcrt.getch()
        limpiar_pantalla()

def alcanzarTiempoOcioso(posicionP):
    #Si el tiempo de arribo del proceso es mayor al siguiente, el tiempo de simulación avanza hasta ese tiempo
    global T_Simulacion
    
    limpiar_pantalla()
    if len(listaNuevos) > 0 and (listaNuevos[posicionP+1]["t_arribo"] > (listaNuevos[posicionP]["t_arribo"])):
        print("Tiempo de simulación requiere ajuste. T_Sim Actual:", T_Simulacion)
        T_Simulacion = listaNuevos[posicionP+1]["t_arribo"]
        print("Tiempo de simulación ajustado a:", T_Simulacion)
        msvcrt.getch()
        limpiar_pantalla()


###################################### FUNCIONES GRÁFICAS ######################################

def tablaNuevos():
    console = Console()

    # Crear tabla
    table = Table(title="Procesos en estado de Nuevo", show_lines=True)

    # Agregar columnas
    table.add_column("Posición", justify="center", style="yellow", no_wrap=True)
    table.add_column("ID  ", justify="center", style="yellow", no_wrap=True)
    table.add_column("Tiempo de Arribo", justify="center" ,style="yellow")
    table.add_column("Tiempo de Irrupcion", justify="center", style="yellow")

    # Agregar filas de ejemplo
    for i in range(len(listaNuevos)):
        table.add_row(str(i+1), str(listaNuevos[i]["id"]), str(listaNuevos[i]["t_arribo"]), str(listaNuevos[i]["t_irrupcion"]))

    # Mostrar tabla
    console.print(table)



def tablaMemoriaPrincipal():
    console = Console()

    # Crear tabla
    table = Table(title="Procesos en estado de Listo (En Memoria Principal)", show_lines=True)

    # Agregar columnas
    table.add_column("Partición", justify="right", style="yellow")
    table.add_column("Tamaño Total", justify="right", style="yellow")
    table.add_column("Dir. comienzo", justify="right", style="yellow")
    table.add_column("Frag. Interna", justify="right", style="yellow")
    table.add_column("ID Proceso", justify="center", style="yellow", no_wrap=True)
    table.add_column("T. de Arribo", justify="center", style="yellow")
    table.add_column("T. de Irrupcion", justify="center", style="yellow")
    table.add_column("Dueño", justify="center", style="yellow")


    # Primero agregamos la fila del SO
    table.add_row(
        str(0),          # número de partición del SO (puede ser fijo)
        str(251),          # número de partición del SO (puede ser fijo)
        "-",
        str(100),        # tamaño reservado al SO
        "-",             # no tiene id
        "-",             # no hay proceso
        "-",             # no hay arribo
        "SO"             # dueño = sistema operativo
    )

    # Luego recorremos las particiones de usuario
    for i in range(len(listaMP)):
        proc = listaMP[i]["Proceso_alojado"]
        table.add_row(
            str(listaMP[i]["Particion"]),
            str(listaMP[i]["TamañoTotal"]),
            str(listaMP[i]["dirComienzo"]),
            str(listaMP[i]["Fragmentacion Interna"]),
            str(proc.get("id", "-")),
            str(proc.get("t_arribo", "-")),
            str(proc.get("t_irrupcion", "-")),
            str(listaMP[i]["Dueño"])
        )

    # Mostrar tabla
    gotoxy(1,14)
    console.print(table)


def listosYSuspendidos():
    console = Console()

    # Crear tabla
    table = Table(title="Procesos en estado de Listo y Suspendido (L/S)", show_lines=True)

    # Agregar columnas
    table.add_column("Posición", justify="center", style="yellow", no_wrap=True)
    table.add_column("ID Proceso", justify="center", style="yellow", no_wrap=True)
    table.add_column("TamañoTotal", justify="center", style="yellow")
    table.add_column("Tiempo de Arribo", justify="center", style="yellow")
    table.add_column("Tiempo de Irrupcion", justify="center", style="yellow")

    # Recorrer lista de suspendidos
    for i in range(len(listaSuspendidos)):
        proc = listaSuspendidos[i]  # proc es un diccionario
        table.add_row(
            str(i+1),
            str(proc.get("id", "-")),
            str(proc.get("tamaño", "-")),
            str(proc.get("t_arribo", "-")),
            str(proc.get("t_irrupcion", "-"))
        )

    # Mostrar tabla
    console.print(table)


def mostrarProcesoCPU(proc):
    console = Console()
    table = Table(title="Proceso en ejecución (CPU)", show_lines=True)

    table.add_column(" ID  ", justify="center", style="yellow")
    table.add_column("Tiempo de Arribo", justify="center", style="yellow")
    table.add_column("Tiempo de Irrupción", justify="center", style="yellow")
    table.add_column("Tiempo Restante", justify="center", style="yellow")

    table.add_row(
        str(proc.get("id", "-")),
        str(proc.get("t_arribo", "-")),
        str(proc.get("t_irrupcion", "-")),
        str(proc.get("tiempo_restante", "-"))
    )

    console.print(table)


def tablaTerminados():
    global Sumatoria_TRetorno
    global Sumatoria_TEspera
    global T_Simulacion

    for i in range(len(listaTerminados)):
        Sumatoria_TEspera= listaTerminados[i]["t_espera"] + Sumatoria_TEspera
        Sumatoria_TRetorno= listaTerminados[i]["t_retorno"] + Sumatoria_TRetorno
    

    console = Console()

    gotoxy(1,1)
    console.print("[bold underline grey70]Informe estadístico[/bold underline grey70]")
    gotoxy(1,2)
    print("Tiempo de Espera promedio:", Sumatoria_TEspera / len(listaTerminados), "(ut)")
    gotoxy(1,3)
    print("Tiempo de Retorno promedio:", Sumatoria_TRetorno / len(listaTerminados), "(ut)")
    gotoxy(1,4)
    rendimientoSistema = len(listaTerminados) / T_Simulacion
    print("Rendimiento del sistema:", round(rendimientoSistema, 3), "(procesos/ut)")
    print()

    # Crear tabla
    table = Table(title="Procesos en estado de Terminados", show_lines=True)

    # Agregar columnas
    table.add_column("Posición", justify="center", style="yellow", no_wrap=True)
    table.add_column("ID  ", justify="center", style="yellow", no_wrap=True)
    table.add_column("Tiempo de Arribo", justify="center" ,style="yellow")
    table.add_column("Tiempo de Irrupcion", justify="center", style="yellow")
    table.add_column("Tiempo de Espera", justify="center", style="yellow")
    table.add_column("Tiempo de Retorno", justify="center", style="yellow")

    # Agregar filas de ejemplo
    for i in range(len(listaTerminados)):
        table.add_row(
            str(i+1),
            str(listaTerminados[i]["id"]),
            str(listaTerminados[i]["t_arribo"]),
            str(listaTerminados[i]["t_irrupcion"]),
            str(listaTerminados[i]["t_espera"]),
            str(listaTerminados[i]["t_retorno"])),

    # Mostrar tabla
    console.print(table)
    print()
    console.print(f"[italic grey70]Simulación terminada...[/italic grey70]")

def informacionEjecucion():
    console = Console()
    gotoxy(80,27)
    console.print("[bold underline grey70]Estado de simulacion[/bold underline grey70]")
    gotoxy(80,29)
    console.print(f"[italic grey70]Tiempo simulación: {T_Simulacion}[/italic grey70]")
    gotoxy(80,30)
    console.print(f"[italic grey70]Multiprogramación: {multiprogramacion}[/italic grey70]")
    gotoxy(80,31)
    console.print(f"[italic grey70]Procesos restantes: {cantProcesosRestantes}[/italic grey70]")


def mostrarPosCPU(posCpu):
    if posCpu == 0:
        posCpu= -1
    elif posCpu==2:
        posCpu= 3
    gotoxy(120,21+posCpu)
    print("\033[1m\033[30m\033[47m 🡄 CPU \033[0m")

###################################### ACÁ EMPIEZA EL CÓDIGO ######################################

ejecutarMenu()

#CARGA DE ARCHIVO EN NUEVOS#
############(0)#############
if paso2 != 2:
    while listaNuevos == []:
        listaNuevos = leer_procesos("procesos.csv")
        if listaNuevos == []:
            limpiar_pantalla()
            gotoxy(xMaxPantalla//2+17,yMaxPantalla//2)
            print("No se cargó el archivo .csv")
            gotoxy(xMaxPantalla//2,yMaxPantalla//2+1)
            print("Asegurate de que esté en la misma carpeta que el ejecutable")
            gotoxy(xMaxPantalla//2-6,yMaxPantalla//2+2)
            print("Cerrá el simulador y colocá el .CSV en la misma carpeta que el ejecutable!")
            msvcrt.getch()
            limpiar_pantalla()

    cantProcesosRestantes= len(listaNuevos)
else:
    listaNuevos= carga_manual_procesos()
    

#Mostrar pantalla
limpiar_pantalla()
tablaNuevos()
print("Presione una tecla para continuar...")
informacionEjecucion()
msvcrt.getch()
limpiar_pantalla()

#esto casi nunca se va a ejecutar, está por las dudas:
alcanzarTiempoOciosoInicio()


########### PLP ############
############(1)#############
#Admisión principal
planifLargoPlazo()


#Mostrar pantalla
limpiar_pantalla()
listosYSuspendidos()
tablaMemoriaPrincipal()
mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
mostrarPosCPU(BuscarSRTF())
informacionEjecucion()
print("Presione una tecla para continuar...")
msvcrt.getch()
limpiar_pantalla()



########### SRTF ###########
############(2)#############
#Selección SRTF, suma Tsim y ejecución 
    #Selección SRTF
listaMP[BuscarSRTF()]
limpiar_pantalla()
    #Suma Tsim

listaMP[BuscarSRTF()]["Proceso_alojado"]["t_retorno"]= listaMP[BuscarSRTF()]["Proceso_alojado"]["t_irrupcion"]

T_Simulacion = T_Simulacion + listaMP[BuscarSRTF()]["Proceso_alojado"]["tiempo_restante"]

#Mostrar pantalla
limpiar_pantalla()
listosYSuspendidos()
tablaMemoriaPrincipal()
mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
mostrarPosCPU(BuscarSRTF())
informacionEjecucion()
print("Presione una tecla para continuar...")
msvcrt.getch()
limpiar_pantalla()


######## EJECUCION #########
############(3)#############
    #Ejecución SRTF

listaMP[BuscarSRTF()]["Proceso_alojado"]["tiempo_restante"] = 0


#Mostrar pantalla
limpiar_pantalla()
listosYSuspendidos()
tablaMemoriaPrincipal()
mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
mostrarPosCPU(BuscarSRTF())
informacionEjecucion()
print("Presione una tecla para continuar...")
msvcrt.getch()
limpiar_pantalla()


#Mandar a lista Terminados (sí o sí uno ejecuta)
mandarTerminados(listaMP[BuscarSRTF()]["Proceso_alojado"],BuscarSRTF())
multiprogramacion= multiprogramacion - 1
cantProcesosRestantes= cantProcesosRestantes - 1


###### SRTF PREPARADO ######
############(4)#############
#Selección SRTF sin ejecutar

#Parche: si solo entra a MP un proceso, una vez ejecutado el que estaba que no intente hacer SRTF de nuevo
#Se hace este control para que, si no hay procesos cargados en memoria, que no prepare el SRTF
HayProcesosCargados = False
for i in range(len(listaMP)):
    if listaMP[i]["Proceso_alojado"] == {}:
        HayProcesosCargados = False
    else:
        HayProcesosCargados = True

if HayProcesosCargados:
    posPreparadoSRTF= BuscarSRTF()


#Mostrar pantalla
limpiar_pantalla()
listosYSuspendidos()
tablaMemoriaPrincipal()
mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
mostrarPosCPU(BuscarSRTF())
informacionEjecucion()
print("Presione una tecla para continuar...")
msvcrt.getch()
limpiar_pantalla()


############ BUCLE DE EJECUCIÓN #############
while cantProcesosRestantes > 0:

    #Lleva procesos desde L/S a MP
    planifMedioPlazo()

    #Mostrar pantalla
    limpiar_pantalla()
    listosYSuspendidos()
    tablaMemoriaPrincipal()
    mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
    mostrarPosCPU(BuscarSRTF())
    informacionEjecucion()
    print("Presione una tecla para continuar...")
    msvcrt.getch()
    limpiar_pantalla()


    #Lleva procesos desde nuevos hacia MP y L/S
    planifLargoPlazo()

    #Ejecución del parche: Si no había antes procesos cargados, acá se debe preparar el SRTF
    if not HayProcesosCargados:
        posPreparadoSRTF= BuscarSRTF()
        #como resultado, entrará al caso de no apropiación

    #Mostrar pantalla
    limpiar_pantalla()
    listosYSuspendidos()
    tablaMemoriaPrincipal()
    mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
    mostrarPosCPU(BuscarSRTF())
    informacionEjecucion()
    print("Presione una tecla para continuar...")
    msvcrt.getch()
    limpiar_pantalla()

    posLuegoDeAdmisionSRTF= BuscarSRTF()

    if posLuegoDeAdmisionSRTF != posPreparadoSRTF:
        posSRTFterminado= posLuegoDeAdmisionSRTF
    else:
        posSRTFterminado= posLuegoDeAdmisionSRTF

    #Mostrar pantalla
    limpiar_pantalla()
    listosYSuspendidos()
    tablaMemoriaPrincipal()
    mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
    mostrarPosCPU(BuscarSRTF())
    informacionEjecucion()
    print("Presione una tecla para continuar...")
    msvcrt.getch()
    limpiar_pantalla()


    #Cálculos de tiempo de espera y de retorno
    resPosSRTF = BuscarSRTF()
    resProceso = listaMP[resPosSRTF]["Proceso_alojado"]

    # Marcar inicio de ejecución
    resProceso["t_inicio"] = T_Simulacion

    # Calcular tiempo de espera
    resProceso["t_espera"] = resProceso["t_inicio"] - resProceso["t_arribo"]

    # Avanzar tiempo de simulación hasta que termine
    T_Simulacion += resProceso["tiempo_restante"]

    # Marcar finalización
    resProceso["t_finalizacion"] = T_Simulacion

    # Calcular tiempo de retorno
    resProceso["t_retorno"] = resProceso["t_finalizacion"] - resProceso["t_arribo"]

    # Ejecutar y terminar
    resProceso["tiempo_restante"] = 0

    #Manda a terminados
    mandarTerminados(resProceso, resPosSRTF)
    ##Disminuye multiprogramación y procesos restantes
    multiprogramacion -= 1
    cantProcesosRestantes -= 1


    #Mostrar pantalla
    limpiar_pantalla()
    listosYSuspendidos()
    tablaMemoriaPrincipal()
    mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
    mostrarPosCPU(BuscarSRTF())
    informacionEjecucion()
    print("Presione una tecla para continuar...")
    msvcrt.getch()
    limpiar_pantalla()

    #Prepara proceso por SRTF pero no lo ejecuta
    posPreparadoSRTF= BuscarSRTF()

    #Mostrar pantalla
    limpiar_pantalla()
    listosYSuspendidos()
    tablaMemoriaPrincipal()
    mostrarProcesoCPU(listaMP[BuscarSRTF()]["Proceso_alojado"])
    mostrarPosCPU(BuscarSRTF())
    informacionEjecucion()
    print("Presione una tecla para continuar...")
    msvcrt.getch()
    limpiar_pantalla()



limpiar_pantalla()
tablaTerminados()
msvcrt.getch()
#limpiar_pantalla()
