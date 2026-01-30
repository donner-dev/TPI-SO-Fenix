############################################ IMPORTS ############################################
import csv
from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
import msvcrt
import time
import sys
import os
sys.path.append('..')

""" Importé las funciones de SIMULADOR.py  para tenerlo modulado como se habia discutido (vamos viendo si queda bien o no) """
#import paquetes.LisandroRojas.funcionesLisandro_prolijo as Lis
#import paquetes.AgustinVeron.Menu as MA
#import paquetes.LisandroRojas.funcionesconlistas_isabel_arregladoLisandro as FunArchivos
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
        "dirComienzo": 201,
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
T_Simulacion=-1         #Empieza en -1 para que siempre se haga un incremento en el primer ciclo.
T_CPU_ocioso=0         
cantProcesosRestantes=0
multiprogramacion=0
aux=None
banderaMostrarTablas=False

#variables de cálculo estadístico:
Sumatoria_TRetorno= 0
Sumatoria_TEspera= 0

############################### FUNCIONES PARA EL MENÚ ######################################
#Algunas de las funciones de esta sección también se usan durante la ejecución del simulador.

""" Podemos revisar en donde van las funciones del menú, si acá o en otro archivo aparte?  mas que nada lo del render de logo- Donner """
#Dimensiones de pantalla
xMaxPantalla = 90
yMaxPantalla = 34
#Posicion vertical de las opciones
pos_opciones = (yMaxPantalla//2)+12
pos_opciones2 = (yMaxPantalla//2)+6
#Colores para strings
NEGRITA = "\033[1m"
AZUL="\033[34m"
ROJO="\033[41m" 
VERDE="\033[42m"
AMARILLO="\033[33m"
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


def seleccionarCSV():
    global AZUL
    global AMARILLO
    global RESET
    
    #Obtiene los archivos CSV
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivos = os.listdir(directorio_actual)
    archivos_csv = [a for a in archivos if a.lower().endswith(".csv")]

    if not archivos_csv:
        gotoxy(20,22)
        print("No se encontraron archivos CSV en el directorio.")
        gotoxy(10,23)
        print("Coloque un archivo .csv en el directorio y vuelva a abrir el programa.")
        msvcrt.getch()
        return None

    console = Console()
    gotoxy(34,20)
    console.print(f"[bold italic grey70]Seleccione un archivo...[/bold italic grey70]")

    #Mostrar instrucciones
    mensajeOp = "Use las flechas (⬆︎ ⬇︎) y presione (Enter)"
    gotoxy((xMaxPantalla-len(mensajeOp))//2+1, yMaxPantalla//2+5)
    print(mensajeOp)

    #Mostrar lista de archivos CSV
    pos_opciones = yMaxPantalla//2+6
    for i, archivo in enumerate(archivos_csv, start=1):
        gotoxy(37, pos_opciones+i)
        print(f"{AZUL}{i}. {AMARILLO}{archivo}{RESET}")

    # Inicializar puntero
    pos_puntero = 0
    tecla = ''
    NUM_OPCIONES = len(archivos_csv)
    X_PUNTERO = (xMaxPantalla // 2) - 30  # Ajustá según tu diseño

    while True:
        pos_puntero_ant = pos_puntero
        tecla = read_single_key_windows()

        if tecla == TECLA_ARRIBA:
            pos_puntero = (pos_puntero - 1) % NUM_OPCIONES
        elif tecla == TECLA_ABAJO:
            pos_puntero = (pos_puntero + 1) % NUM_OPCIONES
        elif tecla == TECLA_ENTER:
            # Cuando se presiona Enter, se devuelve el nombre del archivo seleccionado
            return archivos_csv[pos_puntero]

        if tecla:
            # Borrar puntero anterior
            gotoxy(X_PUNTERO, pos_opciones + pos_puntero_ant + 1)
            print(" ", end="", flush=True)
            # Dibujar puntero nuevo
            gotoxy(X_PUNTERO, pos_opciones + pos_puntero + 1)
            print("▶", end="", flush=True)

        gotoxy(xMaxPantalla, yMaxPantalla + 2)


def leer_procesos(csv_filename: str):
    """Lee el CSV y devuelve una LISTA de procesos (diccionarios) ordenados por t_arribo"""
    
    csv_path = Path(__file__).resolve().parent / csv_filename
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
                    "t_RestanteCPU": int(t_irrupcion),
                    "t_finalizacion": None,
                    "total_retorno": None,
                    "t_ingreso": None,
                    "t_respuesta": None,
                    "t_totalenColaListo": 0,
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

def ejecutarMenu():
    global listaNuevos
    

    #Bordes y texto 
    limpiar_pantalla()
    for y in range(1, yMaxPantalla):
        for x in range(1, xMaxPantalla):
            if (x == 1) or (x == xMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
            if (y == 1) or (y == yMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
    mostrar_logo2()


    #Carga de archivo CSV
    nombreArchivoCSV = seleccionarCSV()
    listaNuevos = leer_procesos(nombreArchivoCSV)
    limpiar_pantalla()


################################ FUNCIONES PARA LA EJECUCIÓN ####################################

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
        listaMP[pos]["Fragmentacion Interna"] = listaMP[pos]["TamañoTotal"] - procActual["tamaño"]      
        listaMP[pos]["Proceso_alojado"] = procActual
        listaMP[pos]["Ocupado"] = True
        # Registrar instante real en que el proceso queda ALOJADO en MP (si no estaba ya fijado)
        if procActual.get("t_arribo_MP") is None:
            procActual["t_arribo_MP"] = T_Simulacion

def cabeEnAlgunaParticionLIBRE(proc):
    global listaMP

    for p in range(len(listaMP)):
        difTamaño= listaMP[p]["TamañoTotal"] - proc["tamaño"]
        if ((difTamaño >= 0) and (listaMP[p]["Ocupado"] == False)):
            return True
    return False

def mover_aColaListo(procActual):
    global T_Simulacion

    #Proceso entró en ámbito de multiprogramación
    procActual["admitido"] = True
    
    #Tiempo en que quedó esperando en la lista de nuevos.
    if procActual["t_respuesta"] is None:
        procActual["t_respuesta"] = T_Simulacion - procActual["t_arribo"]
    else: 
        procActual["t_respuesta"] = procActual.get("t_respuesta")

    if procActual["t_totalenColaListo"] is None:
        procActual["t_totalenColaListo"] = 0
    else: # Preservar el tiempo acumulado en la cola de listos (no reiniciarlo)
        procActual["t_totalenColaListo"] = procActual.get("t_totalenColaListo")

    # Mantener compatibilidad: asegurar que exista el campo `t_RestanteCPU`
    procActual.setdefault("t_RestanteCPU", procActual.get("t_irrupcion", 0))

    # preparar tiempo de ingreso: instante en que el sim. lo acomoda en memoria principal o secundaria
    if procActual["t_ingreso"] is None:
        procActual["t_ingreso"] = T_Simulacion
    else:
        procActual["t_ingreso"] = procActual.get("t_ingreso")

    #preparar tiempo de arribo: cuando llega a memoria principal
    if procActual["t_ingreso"] is None:
        procActual["t_arribo_MP"] = T_Simulacion
    else:
        procActual["t_arribo_MP"] = procActual.get("t_arribo_MP")
    #ingresa proceso a listaListos (cola de turnos)
    
    global aux
    aux = procActual
    listaListos.append(procActual)


def mover_aColaSuspendido(procActual):
    global T_Simulacion

    #Proceso entró en ámbito de multiprogramación
    procActual["admitido"] = True
    
    #Tiempo en que quedó esperando en la lista de nuevos.
    if procActual["t_respuesta"] is None:
        procActual["t_respuesta"] = T_Simulacion - procActual["t_arribo"]
    else: 
        procActual["t_respuesta"] = procActual.get("t_respuesta")

    #Guarda el instante en que ingresa al ámbito de la multiprogramación
    if procActual["t_ingreso"] is None:
        procActual["t_ingreso"] = T_Simulacion
    else:
        procActual["t_ingreso"] = procActual.get("t_ingreso")
    
    listaSuspendidos.append(procActual)


def mandarTerminados(procActual,indiceMP):
    global T_Simulacion
    
    #Marcar finalización (usar campo único `t_finalizacion`)
    procActual["t_finalizacion"] = T_Simulacion
    procActual["CPU"] = False  # marcar que ya no está en CPU
    procActual["t_respuesta"] = procActual.get("t_respuesta")
    procActual["t_totalenColaListo"] = procActual.get("t_totalenColaListo")
    #Hace que la partición esté disponible
    listaMP[indiceMP]["Ocupado"] = False


    # Normalizar/normalización defensiva de `t_arribo_MP` (cubrir casos donde la clave existe pero su valor es None)
    if procActual.get("t_arribo_MP") is None:
        procActual["t_arribo_MP"] = procActual.get("t_ingreso") if procActual.get("t_ingreso") is not None else procActual.get("t_arribo", T_Simulacion)

    # total_retorno: tiempo desde que ingresó a MP hasta finalización (calcular desde t_finalizacion)
    t_arribo_mp_val = procActual.get("t_arribo_MP", procActual.get("t_arribo", T_Simulacion))
    procActual["total_retorno"] = int(procActual.get("t_finalizacion", T_Simulacion) - t_arribo_mp_val)

    #agregar a la lista de terminados
    listaTerminados.append(procActual)

    #quitar de la listaListos el proceso
    listaListos[:] = [p for p in listaListos if p["id"] != procActual["id"]]


def BuscarSRTF() -> Optional[int]:
    """
    Busca el proceso con menor tiempo restante (SRTF) entre los listos que tengan
    `t_RestanteCPU` > 0. Retorna el índice de la partición donde está alojado ese
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
       listaListos y MemoriaPrincipal simultáneamente porque son la misma referencia)
    4. BuscarSRTF() busca por 'id' en listaListos, encuentra el proceso con menor
       `t_RestanteCPU`, a ese proceso lo marca como en CPU poniendo `CPU = True` y retorna el índice de su partición en MemoriaPrincipal.
    
    Esto es el puente entre:
    - FIFO (cola de admisión en listaListos)
    - SRTF (selección de quién entra a CPU)
    - Referencias compartidas (sincronización automática entre listas)
    """
    if len(listaListos) < 1:
        return None
    
    # Busca proceso en la cola de listos por menor tiempo restante (`t_RestanteCPU`)
    menorTR = float("inf")
    procesoElegido = None
    for proc in listaListos:
        tr = proc.get("t_RestanteCPU", 0)
        proc["CPU"] = False  # marcar que no está en CPU
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
       - Si t_arribo <= T_Simulacion y admitido == False:
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
            if (proceso.get("admitido") is False) and (proceso.get("t_arribo") <= T_Simulacion):
                if (len(listaListos) < 3) and cabeEnAlgunaParticionLIBRE(proceso):
                    mover_aColaListo(proceso)
                    AsignPartBestFit(aux)
                    cambios = True
                #elif not cabeEnAlgunaParticionLIBRE(proceso):
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
    global T_CPU_ocioso

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

    if t_arribo >= T_Simulacion:
        multiprogramacion = len(listaListos) + len(listaSuspendidos)
        avanzar = t_arribo - T_Simulacion
        T_CPU_ocioso += avanzar
        T_Simulacion = t_arribo
        multiprogramacion = len(listaListos) + len(listaSuspendidos)

def buscarSiguiente():
    """
    Busca y retorna el siguiente proceso pendiente de admisión o el próximo
    arribo futuro.

    ════════════════════════════════════════════════════════════════════════
    ORDEN DE BÚSQUEDA (FIFO en listaProcesos)
    ════════════════════════════════════════════════════════════════════════
    1. Procesos con `admitido` == False y `t_arribo` <= tiempo
       actual (procesos ya arribados y no ingresados).
    2. Procesos cuyo `t_arribo` coincide con el instante actual.
    3. Si no hay ninguno, retorna el primer proceso futuro (próximo arribo).

    ════════════════════════════════════════════════════════════════════════
    CONCEPTO FIFO AQUÍ
    ════════════════════════════════════════════════════════════════════════
    - Recorre listaProcesos secuencialmente (como en un archivo CSV FIFO).
    - Los primeros procesos que se encuentran con t_arribo <= T_Simulacion
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
        if (p.get("admitido") is False) and (p.get("t_arribo") <= T_Simulacion):
            pendiente=p
            return pendiente
 
    # próximo arribo futuro
    for p in listaNuevos:
        if (p.get("t_arribo") > T_Simulacion) and (p.get("admitido") is False):
            #print(f"Busqueda del siguiente encontró un proceso del futuro {p}")
            return p
    return None

def detectar_terminacion(proceso, indice_procesoEjecucion) -> bool:
    global banderaMostrarTablas
    if proceso.get("t_RestanteCPU", 0) == 0:
        banderaMostrarTablas = True
        print(f"El proceso {proceso['id']} ha finalizado su ejecución.")
        # Manda a terminados
        mandarTerminados(proceso, indice_procesoEjecucion) # esta funcion tiene que copiar este proceso en la lista de terminados y removerlo de listos
        return True

def actualizar_estado_Proceso(proceso: Dict) -> Optional[str]:
    """
    Devuelve una cadena con el estado actual del proceso según las listas.
    """
    global listaListos, listaSuspendidos, listaTerminados, listaNuevos

    pid = proceso.get("id")
    if any(p.get("id") == pid and p.get("CPU") for p in listaListos):
        return "EN EJECUCION"
    if any(p.get("id") == pid for p in listaListos):
        return "LISTO"
    if any(p.get("id") == pid for p in listaSuspendidos):
        return "LISTO/SUSPENDIDO"
    if any(p.get("id") == pid for p in listaTerminados):
        return "TERMINADO"
    if any(p.get("id") == pid for p in listaNuevos):
        return "NUEVO"
    return None

####################################### FUNCIONES "MOSTRAR_TABLAS" ##########################################
def mostrarNuevos():  #agustin
    console = Console()

    #Crear tabla
    table = Table(title="Procesos en estado de Nuevo", show_lines=True)

    #Columnas
    table.add_column("Posición", justify="center", style="yellow", no_wrap=True)
    table.add_column("ID  ", justify="center", style="yellow", no_wrap=True)
    table.add_column("Tamaño", justify="center" ,style="yellow")
    table.add_column("Tiempo de Arribo", justify="center" ,style="yellow")
    table.add_column("Tiempo de Irrupcion", justify="center", style="yellow")

    #Filas
    for i in range(len(listaNuevos)):
        table.add_row(str(i+1), str(listaNuevos[i]["id"]), str(listaNuevos[i]["tamaño"]), str(listaNuevos[i]["t_arribo"]), str(listaNuevos[i]["t_irrupcion"]))
    #Mostrar tabla
    console.print(table)
    console.print(f"[italic grey70]Archivo leído exitosamente![/italic grey70]")
    print()
    console.print(f"[italic grey70]Presione enter para continuar...[/italic grey70]")


def mostrarColaListos():  #ezequiel
    """ Muestra la tabla de procesos en lista de listos """
    console = Console()
    table = Table(title="Procesos en COLA de LISTOS --> Estado: 'Listo'", show_lines=True)
    cols = [
        ("Orden", None),
        ("ID Proceso", "yellow"),
        ("Tamaño", None),
        ("T. Arribo", None),
        ("T. Arribo a MP", None),
        ("T. Irrupcion", None),
        ("T. Respuesta", None),
        ("T. Ingreso", None),
        ("T. Restante de CPU", None),
        ("T. Total de espera por CPU", None),
    ]
    for name, style in cols:
        table.add_column(name, justify="center", style=style or "", no_wrap=False)

    if listaListos:
        for p in listaListos:
            if not p.get("CPU"): # mostrar solo los que no están en CPU
                table.add_row(
                    str(listaListos.index(p) + 1),
                    str(p.get("id", "xxx")),
                    str(p.get("tamaño", "xxx")),
                    str(p.get("t_arribo", "xxx")),                    
                    str(p.get("t_arribo_MP", "xxx")),
                    str(p.get("t_irrupcion", "xxx")),
                    str(p.get("t_respuesta", "xxx")),
                    str(p.get("t_ingreso", "xxx")),
                    str(p.get("t_RestanteCPU", "xxx")),
                    str(p.get("t_totalenColaListo", "xxx")),
                )
        # si la lista no esta vacia pero el unico proceso esta en CPU
        if all(p.get("CPU") for p in listaListos):
            table.add_row(*["xxx"] * len(cols))
    else:# lista vacia y sin procesos para elegir en CPU
        table.add_row(*["xxx"] * len(cols))
    console.print(table)


def mostrarCPU():  #ezequiel
    """ Muestra la tabla de procesos en CPU """
    console = Console()
    table = Table(title="Proceso utilizando CPU --> Estado: 'En Ejecución'", show_lines=True)
    for h, style in [("ID Proceso", "yellow"), ("Tamaño", None), ("Particion", None), ("T. Restante de CPU", None)]:
        table.add_column(h, justify="center", style=style or "", no_wrap=False)
    if listaListos:
        for proceso in listaListos:
            if proceso.get("CPU"):
                #buscar particion en memoria principal
                particion_asignada = None
                for i, particion in enumerate(listaMP):
                    proc_alojado = particion.get("Proceso_alojado")
                    if proc_alojado and proc_alojado.get("id") == proceso.get("id"):
                        particion_asignada = i 
                        break
                table.add_row(
                    str(proceso.get("id", "xxx")),
                    str(proceso.get("tamaño", "xxx")),
                    str(listaMP[particion_asignada]["Particion"] if particion_asignada is not None else "xxx"),
                    str(proceso.get("t_RestanteCPU", "xxx")),
                )
                break
    else:
        table.add_row(*["xxx"] * 4)
    console.print(table)


def mostrarMemoriaPrincipal():  #agustin
    """ Muestra la tabla de particiones de memoria principal """
    console = Console()

    #Anotaciones
    #{
    #Formato tabla mem principal.

    #id_particion (1,2,3)
    #id_proceso alojado 
    #tamaño part
    #frag
    #Estado (disponible/ocupado)

    #Agregar fila de sistema operativo (partición 0)
    #}

    #Tabla
    table = Table(title="Procesos en estado de Listo (En Memoria Principal)", show_lines=True)

    #Columnas
    table.add_column("Partición", justify="right")
    table.add_column("Tamaño Total", justify="right")
    table.add_column("Dir. comienzo", justify="right")
    table.add_column("Frag. Interna", justify="right")
    table.add_column("ID Proceso", justify="center", style="yellow", no_wrap=True)
    table.add_column("Dueño", justify="center")
    table.add_column("Estado Part.", justify="center", style="bright_magenta")

    #Filas
    #Primero la fila del Sistema Operativo
    table.add_row(
        "0",        #Partición del SO
        "100",
        "451",      #Dir Comienzo
        "-",
        "-",
        "SO",
        "Ocupado",
    )

    #Luego las particiones del usuario 
    for i in range(len(listaMP)):
        proc = listaMP[i]["Proceso_alojado"]
        if str(listaMP[i]["Ocupado"]) == "True":
            estadoPart = "Ocupado"
        else:
            estadoPart = "Libre" 
        table.add_row(
            str(listaMP[i]["Particion"]),
            str(listaMP[i]["TamañoTotal"]),
            str(listaMP[i]["dirComienzo"]),
            str(listaMP[i]["Fragmentacion Interna"]),
            str(proc.get("id", "-")),
            str(listaMP[i]["Dueño"]),
            str(estadoPart),
        )
    console.print(table)


def mostrarColaSuspendidos():  #isabel
    """ Muestra la tabla de procesos en estado de 'suspendido' """
    
    console = Console()
    table = Table(title="Procesos en Memoria Secundaria --> Estado: 'Listo y Suspendido'", show_lines=True)
    headers = ["ID Proceso", "Tiempo Arribo", "Tamaño", "Tiempo Irrupcion", "Tiempo de Respuesta", "Tiempo de Ingreso", "Tiempo Restante de CPU"]
    for h in headers:
        table.add_column(h, justify="right", style="yellow" if h == "ID Proceso" else "", no_wrap=False)
    if listaSuspendidos:
        for p in listaSuspendidos:
            table.add_row(*(str(p.get(k, "xxx")) for k in ["id", "t_arribo", "tamaño", "t_irrupcion", "t_respuesta", "t_ingreso", "t_RestanteCPU"]))
    else:
        table.add_row(*["xxx"] * len(headers))
    console.print(table)


def mostrarTerminados(): #agustin
    """ Muestra la tabla de procesos terminados """
    
    global T_Simulacion
    
    console = Console()
    table = Table(title="Procesos Terminados", show_lines=True)

    #Columnas
    table.add_column("Posicion", justify="center", no_wrap=True)
    table.add_column("ID", justify="center", style="yellow", no_wrap=True)
    table.add_column("Tamaño", justify="center", no_wrap=True)
    table.add_column("T. de arribo", justify="center", no_wrap=True)
    table.add_column("T. arribo a MP", justify="center", no_wrap=True)
    table.add_column("T. irrupcion", justify="center", no_wrap=True)
    table.add_column("T. finalizacion", justify="center", no_wrap=True)
    table.add_column("T. ingreso", justify="center", no_wrap=True)
    table.add_column("T. respuesta", justify="center", no_wrap=True)
    table.add_column("T. total de retorno", justify="center", no_wrap=True)
    table.add_column("T. total en listos", justify="center", no_wrap=True)
   
    #Filas
    if len(listaTerminados) != 0:
        for i in range(len(listaTerminados)):
            table.add_row(
                str(i+1),
                str(listaTerminados[i]["id"]),
                str(listaTerminados[i]["tamaño"]),
                str(listaTerminados[i]["t_arribo"]),
                str(listaTerminados[i]["t_arribo_MP"]),
                str(listaTerminados[i]["t_irrupcion"]),
                str(listaTerminados[i]["t_finalizacion"]),
                str(listaTerminados[i]["t_ingreso"]),
                str(listaTerminados[i]["t_respuesta"]),
                str(listaTerminados[i]["total_retorno"]),
                str(listaTerminados[i]["t_totalenColaListo"]),
            )
    else:
        table.add_row(*["xxx"] * 11)
    #Mostrar tabla
    console.print(table)

def mostrarInforme(): #agustin
    """ Muestra la tabla de procesos terminados con el informe final """
    global T_Simulacion
    global Sumatoria_TEspera
    global Sumatoria_TRetorno
    console = Console()
    table = Table(title="Procesos Terminados", show_lines=True)

    #Sumatorias de tiempos para el informe final. (usar duraciones, no instantes)
    Sumatoria_TEspera = sum(p.get("t_respuesta", 0) for p in listaTerminados)
    Sumatoria_TRetorno = sum(p.get("total_retorno", p.get("t_finalizacion", 0)) for p in listaTerminados)

    gotoxy(1,1)
    console.print("[bold underline grey70]Informe estadístico[/bold underline grey70]")
    gotoxy(1,2)
    print("Tiempo de Espera promedio:", Sumatoria_TEspera / len(listaTerminados), "(ut)")
    gotoxy(1,3)
    print("Tiempo de Retorno promedio:", Sumatoria_TRetorno / len(listaTerminados), "(ut)")
    gotoxy(1,4)
    rendimientoSistema = len(listaTerminados) / T_Simulacion
    print("Rendimiento del sistema:", round(rendimientoSistema, 3), "(procesos/ut)\n")#Saltar renglón
    mostrarTerminados()
    #Saltar renglón
    print("\n")  
    console.print(f"[italic grey70]Simulación terminada...[/italic grey70]")

def mostrarTablasActualizadas():
    global listaNuevos
    console = Console()
      #renderizar la tablita hermosa con rich, ciclando los objetos en Procesos
    table = Table(title="Procesos Cargados", show_lines=True)
    table.add_column("ID Proceso", justify="right", style="yellow", no_wrap=True)
    table.add_column("Tiempo Arribo", justify="right")
    table.add_column("Tamaño",justify="right" )
    table.add_column("Tiempo Irrupcion", justify="right")
    table.add_column("ESTADO", justify="right")
    for p in listaNuevos:
        estadoActual= actualizar_estado_Proceso(p)
        table.add_row( #medio tipo:  array[0] pero con los key del diccionario
            str(p["id"]),
            str(p["t_arribo"]),
            str(p["tamaño"]),
            str(p["t_irrupcion"]),
            estadoActual
        )
    console.print(table)

def MostrarTablas():
    """Muestra todas las tablas disponibles en el simulador"""
    limpiar_pantalla()
    mostrarTablasActualizadas()
    mostrarMemoriaPrincipal()
    mostrarColaListos()
    mostrarCPU()
    mostrarColaSuspendidos()
    mostrarTerminados()

####################################### MAIN PRINCIPAL ##########################################
ejecutarMenu()

mostrarNuevos()

msvcrt.getch()
limpiar_pantalla()

while len(listaTerminados) < len(listaNuevos):
    
    banderaMostrarTablas = False # bandera para mostrar tablas si hay cambios en admision o terminacion
    procesoEjecucion = None
    
    #CICLOS OCIOSOS SI NO HAY PROCESOS EN LISTOS
    proceso_siguiente = buscarSiguiente() #esta parte revisa los ciclos osiosos antes de tratar cualquier proceso
    CiclosOciosos(proceso_siguiente)
    
    # PRIMERO: ciclos ociosos para hacer admision de procesos
    # tiempo del simulador parejo con los procesos que van llegando para hacer la admision de ese instante
    
    ADMICION_MULTI_5()
    if banderaMostrarTablas == True:#mostrar por pantalla el estado actual del simulador
            #Mostrar pantalla poner todas las tablas.
            banderaMostrarTablas = False # resetear bandera para otro ciclo
            MostrarTablas()
            print(f"Tiempo de simulación actual: >>>>>>>>>>>>>>>> {T_Simulacion} (ut) <<<<<<<<<<<<<<<<")
            print(f"Multiprogramación actual: >>>>>>>>>>>>>>>> {multiprogramacion} procesos <<<<<<<<<<<<<<<<")
            print(f"presione cualquier tecla para continuar...")
            msvcrt.getch()  # espera cualquier tecla
            limpiar_pantalla()
    ########## EJECUCION #########
    #SEGUNDO buscar el proceso SRTF
    indice_procesoEjecucion = BuscarSRTF() # retorna el indice de la particion en memoria principal que contiene el proceso con menor tiempo restante
    
    if indice_procesoEjecucion is None:
        continue # vuelve al while mayor para un ciclo ocioso

    procesoEjecucion = listaMP[indice_procesoEjecucion]["Proceso_alojado"]

    while (procesoEjecucion is not None) and (procesoEjecucion.get("t_RestanteCPU", 0) > 0):
        
        banderaMostrarTablas = False # bandera para mostrar tablas si hay cambios en admision o terminacion
        
        # Ejecutar un ciclo de CPU (decrementar único contador estándar)
        procesoEjecucion["t_RestanteCPU"] -= 1
        T_Simulacion += 1
        
        # Sumar tiempo de espera a los demas procesos en listaListos ya cargados para este ciclo
        for otrosProcesos in listaListos:
            if otrosProcesos["id"] != procesoEjecucion["id"]:
                otrosProcesos["t_totalenColaListo"] = otrosProcesos.get("t_totalenColaListo", 0) + 1
        
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
            if indice_procesoEjecucion is None:
                continue # vuelve al while mayor para un ciclo ocioso
            procesoEjecucion = listaMP[indice_procesoEjecucion]["Proceso_alojado"]
            print(f"Cambio de contexto: {procesoEjecucion['id']} ingresa a CPU")

        if indice_procesoEjecucion is None:
            break #vuelve al while mayor para un ciclo ocioso

        ADMICION_MULTI_5() # revisar si hay admision de nuevos procesos después del cambio de contexto para ocupar el espacio liberado
        indice_procMasPrioridad = BuscarSRTF()
        
        # control de APROPIACION de CPU para la admision de nuevos procesos causado por ADMICION_MULTI_5
        if indice_procMasPrioridad is not None and procesoEjecucion is not None:     
            procMasPrioridad = listaMP[indice_procMasPrioridad]["Proceso_alojado"]
            
            # Validar que procMasPrioridad no sea dict vacío
            if procMasPrioridad and procMasPrioridad.get("id") is not None:
                if procMasPrioridad.get("id") != procesoEjecucion.get("id"):
                    print(f"Cambio de contexto: {procesoEjecucion['id']} sale -> {procMasPrioridad['id']} APROPIA CPU")
                    procesoEjecucion = procMasPrioridad
                    indice_procesoEjecucion = indice_procMasPrioridad
                    # la tabla de CPU se actualiza en la siguiente sección gráfica
        
        if banderaMostrarTablas == True:#mostrar por pantalla el estado actual del simulador
            #Mostrar pantalla poner todas las tablas.
            banderaMostrarTablas = False # resetear bandera para otro ciclo
            MostrarTablas()
            print(f"Tiempo de simulación actual: >>>>>>>>>>>>>>>> {T_Simulacion} (ut) <<<<<<<<<<<<<<<<")
            print(f"Multiprogramación actual: >>>>>>>>>>>>>>>> {multiprogramacion} procesos <<<<<<<<<<<<<<<<")
            print(f"presione cualquier tecla para continuar...")
            msvcrt.getch()  # espera cualquier tecla
            limpiar_pantalla()
    #Informe final al terminar la simulación
    mostrarInforme()