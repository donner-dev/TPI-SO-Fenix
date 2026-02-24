import csv
import estado_global
import RojasLisandroPaquete.funcionesLisandro_isabel_old as FLI
import AgustinVeron.Menu as FM

#Variables Globales
HV = 10**10             #High Value
cantProcesos = 0        #Cant procesos admitidos
Tsim = 0                #Tiempo de la simulación
GMP = 0                 #Grado de multiprogramación           
listaNuevo = []         
listaLS = []
MemoriaPrincipal = []
listaTerminado = []

#Formatos de los procesos:

#En lista de "Nuevo" y "L/S"
#Proceso = Registro 
    #idProc: Int
    #tamProc: Int
    #ta: Int
    #ti: Int
    #estado: Str
#FinRegistro

#En lista de "MP"
#ProcesoMP = Registro
    #idPart: Int
    #dirComienzoPart: Int
    #TamañoTotal: Int
    #idProceso: Int
    #fragInt: Int
    #ti: Int
    #estado: Str este es de proceso
    #
    #
    #
#FinRegistro

def cargarProcesos(nombre_archivo, listaDestino):
    #Carga procesos desde el archivo csv hacia la lista de "Nuevo" de forma ordenada de menor a mayor por TA
    registros_temporales = [] #Lista auxiliar para la recolección y ordenación
    try:
        with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for registro in lector:
                #Conversión de tipos (idProc, tamProc, ta, ti) de string a int
                try:
                    registro['idProc'] = int(registro['idProc'])
                    registro['tamProc'] = int(registro['tamProc'])
                    registro['ta'] = int(registro['ta'])
                    registro['ti'] = int(registro['ti'])
                except (ValueError, KeyError) as e:
                    # MOSTRAR EN PANTALLA:
                    print(f"Aviso: Saltando registro. Error de formato o columna faltante en CSV: {e}")
                    continue
                registros_temporales.append(registro)
        #Ordenamiento de registros por TA de menor a mayor usando una lista auxiliar, luego se vacía la listaDestino y se colocan los registros ordenados
        registros_ordenados = sorted(registros_temporales, key=lambda x: x['ta'])
        listaDestino.clear() 
        listaDestino.extend(registros_ordenados)
        #MOSTRAR POR PANTALLA
        print(f"Carga Exitosa: Se cargaron {len(listaDestino)} procesos a la lista de Nuevos, ordenados por 'ta'.")
        return True
    except FileNotFoundError:
        # MOSTRAR EN PANTALLA:
        # Escribir que no se encontró el archivo en pantalla y volver al menú para leer el archivo.
        return False
    except Exception as e:
        # MOSTRAR EN PANTALLA:
        # Escribir que ocurrió un error inesperado al leer el archivo.csv por estar mal el formato, que pruebe con otro.
        return False
    
def inicializarMemoriaPrincipal():
    MemoriaPrincipal.clear()
    for i in range(4): #va desde 0 a 3
        MemoriaPrincipal.append({})
        MemoriaPrincipal[i]["idPart"]= i
        if (i == 0):
            #50K trabajos pequeños
            MemoriaPrincipal[i]["dirComienzoPart"]= 1         
            MemoriaPrincipal[i]["TamañoTotal"]= 50
        elif (i == 1):
            #150K trabajos medianos
            MemoriaPrincipal[i]["dirComienzoPart"]= 51        
            MemoriaPrincipal[i]["TamañoTotal"]= 150
        elif (i == 2):
            #250K trabajos más grandes
            MemoriaPrincipal[i]["dirComienzoPart"]= 201       
            MemoriaPrincipal[i]["TamañoTotal"]= 250
        elif (i == 3):
            #100k Sistema Operativo
            MemoriaPrincipal[i]["dirComienzoPart"]= 451   
            MemoriaPrincipal[i]["TamañoTotal"]= 100
        MemoriaPrincipal[i]["fragInt"]= ""
        MemoriaPrincipal[i]["idProceso"]= ""
        MemoriaPrincipal[i]["ti"]= ""
        MemoriaPrincipal[i]["estado"]= ""

#Versión vieja 1:
#def MPllena():
#    for k in range(3): #va desde 0 a 2 sin pasar por 3, ya que allí está el SO.
#       if (MemoriaPrincipal[k]["Ocupado"] == False):
#            return False
#    return True

#Versión vieja 2:
#def MPllena():
#    for k in MemoriaPrincipal[:-1]: #va desde 0 a 2 sin pasar por 3, ya que allí está el SO.
#        if (MemoriaPrincipal[k]["Ocupado"] == False):
#            return False
#    return True

#def MPllena() -> bool: 
#    if len(estado_global.listaListos) < 3:
#        return False 
#    else:
#        return True
    
def MPllena() -> bool:
    for m in range(len(estado_global.MemoriaPrincipal)-1):
        if estado_global.MemoriaPrincipal[m]["Ocupado"]==False:
            return False
    return True

def cabeEnAlgunaParticion(procesoAct) -> bool:
    #Determina si el proceso cabe en al menos una partición para si quiera pensar en admitirlo en MP
    for l in range(len(MemoriaPrincipal)-1):
        if (MemoriaPrincipal[l]["TamañoTotal"] >= procesoAct.get("tamaño")):
            return True
    return False


def BestFit(tamañoProcActual):
    #Determina la partición del proceso por la menor fragmentación interna
    menorFragmentacionInt = HV
    posicionAsignada = 0
    for j in range(3):
        if (MemoriaPrincipal[j]["Ocupado"] == False):
            if ((MemoriaPrincipal[j]["TamañoTotal"] - tamañoProcActual) < menorFragmentacionInt):
                menorFragmentacionInt = MemoriaPrincipal[j]["TamañoTotal"] - tamañoProcActual
                posicionAsignada = j
    return posicionAsignada

#def BestFitCICLO_ADMICION(tamañoProcActual):
#    #Determina la partición del proceso por la menor fragmentación interna
#    menorFragmentacionInt = HV
#    posicionAsignada = 0
#    for i,j in enumerate(estado_global.MemoriaPrincipal[:-1]):
#        if (j["Ocupado"] == False):
#            if ((j["TamañoTotal"] - tamañoProcActual) < menorFragmentacionInt):
#                menorFragmentacionInt = j["TamañoTotal"] - tamañoProcActual
#                posicionAsignada = i
#    return posicionAsignada

def trasladarProceso(listaOrigen,listaDestino,posorigen,posdestino):
    #listaOrigen: lista de origen del proceso
    #listaDestino: lista de destino del proceso
    #posorigen: posicion de la lista de origen
    #posdestino: posicion destino (para ubicar proceso en partición)

    #listaOrigen
    if (listaOrigen == listaNuevo) or (listaOrigen == listaLS):
        #Si el origen es Nuevo o LS, se hace "pop" y se traslada a otra lista
        registroAux = listaOrigen.pop(posorigen)
    elif (listaOrigen == MemoriaPrincipal):
        #Si el origen es MP, no se hace "pop" porque cada elemento es una partición
        #se guardan los datos del elemento para llevarlos a Terminados
        #el único caso en que la lista de origen sea la MP, es para trasladar proceso a Terminados
        registroAux = listaOrigen[posorigen]

    #listaDestino
    if listaDestino == MemoriaPrincipal:
        #Si el destino es la MP, los datos del proceso se copian a la partición 
        MemoriaPrincipal[posdestino]["idProceso"]= registroAux["idProc"]
        MemoriaPrincipal[posdestino]["fragInt"]= MemoriaPrincipal[posdestino]["TamañoTotal"] - registroAux["tamProc"]
        MemoriaPrincipal[posdestino]["ti"]= registroAux["ti"]
        MemoriaPrincipal[posdestino]["estado"]= "Listo"
    elif listaDestino == listaLS:
        #Si el destino es L/S se hace append del proceso desde Nuevos
        registroAux["estado"] = "Listo y suspendido"
        listaDestino.append(registroAux)
    elif listaDestino == listaTerminado:
        #Si el destino es Terminados se hace append del proceso desde MP
        registroAux["estado"] = "Terminado"
        listaDestino.append(registroAux)

def hayProcesosParaAdmision():
    #Analiza si hay al menos un proceso para admitir si su (TA<=Tsim)
    i=0
    while i < len(listaNuevo):
        if (listaNuevo[i]["ta"] <= Tsim):
            return True
        i+=1
    return False

def posicionProcesoListaNuevo():
    #Busca la posición del proceso para admitir
    i=0
    while i < len(listaNuevo):
        if (listaNuevo[i]["ta"] <= Tsim):
            return i
        i+=1

def ShortestRemainingTimeFirst():
    #Se fija en la MP el proceso con menor TI
    menorTI=HV
    posMenorTI = 0
    for i in range(len(MemoriaPrincipal)):
        if (MemoriaPrincipal[i]["ti"] <= menorTI):
            menorTI=MemoriaPrincipal[i]["ti"]
            posMenorTI=i
    return posMenorTI


def cargarProcesoAlojado(lista: list, MP:dict, proceso_actual):
    lista[MP]["Proceso_alojado"]= proceso_actual
    lista[MP]["Fragmentacion Interna"]=int(lista[MP].get("TamañoTotal")-proceso_actual.get("tamaño"))
    lista[MP]["Ocupado"]=True

def AsignPartBestFit(procActual):
    menorDifTamaño = 10**10
    for p in range(len(estado_global.MemoriaPrincipal)-1):
        difTamaño= estado_global.MemoriaPrincipal[p].get("TamañoTotal") - procActual.get("tamaño")
        if ((difTamaño >= 0) and (difTamaño <= menorDifTamaño) and (estado_global.MemoriaPrincipal[p]["Ocupado"] == False) and (not MPllena())):
            menorDifTamaño = estado_global.MemoriaPrincipal[p].get("TamañoTotal") - procActual.get("tamaño")
            pos = p
    cargarProcesoAlojado(estado_global.MemoriaPrincipal,pos,procActual)


def BuscarSRTF():
    #Busca en las particiones de MP(en el campo de proceso alojado) el que menor Tiempo restante (TR) tenga para ejecutarse
    menorTR = 10**10
    for p in range(len(estado_global.MemoriaPrincipal)-1):
        if (estado_global.MemoriaPrincipal[p]["Ocupado"] and estado_global.MemoriaPrincipal[p]["Dueño"] != "SO"):
            if((estado_global.MemoriaPrincipal[p]["Proceso_alojado"]["t_RestanteCPU"]) < menorTR):
                menorTR = p
    return menorTR


def eliminarSuspendidosEnListos():
    k=0
    while k <= len(estado_global.listaSuspendidos):
        for i in range(len(estado_global.listaSuspendidos)-1):
            for j in range(len(estado_global.listaListos)-1):
                if estado_global.listaSuspendidos[i]["id"] == estado_global.listaListos[j]["id"]:
                    estado_global.listaListos.remove(i)
        k=k+1


#T_simulador=0 #redimiento = Nprocesos/T_simulador
#T_CPU_ocioso=0 #este mide los lapsos de tiempo que no hay procesos para ejecutar
#T_usoCPU=None #este lo usamos para sumar a los acumuladores generales y restar a los campos de tiempos restantes
#T_usoCPU_TotalGeneral=None
#multiprogramacion=0
#variableBest_fit=None
#aux=None
#cantTotalProcesos=0



def MostrarTablasEjecucion():
    FM.gotoxy(1,1)
    FLI.mostrarColaSuspendido()
    FM.gotoxy(1,11)
    FLI.mostrarMemoriaPrincipal()
    FM.gotoxy(1,25)
    FLI.mostrarProcesoCPU()
    FM.gotoxy(78,25)
    print("Estado global")
    FM.gotoxy(78,27)
    print("T. de simulación (TSim):", estado_global.T_simulador)
    FM.gotoxy(78,28)
    print("T. uso de CPU:", estado_global.T_usoCPU)
    FM.gotoxy(78,29)
    print("T. de CPU ocioso:", estado_global.T_CPU_ocioso)
    FM.gotoxy(78,30)
    print("Procesos Restantes:", estado_global.cantTotalProcesos)

def MostrarInfoEnEjecucion():
    FM.gotoxy(78,1)
    print("T. de simulación (TSim):", estado_global.T_simulador)
    FM.gotoxy(78,2)
    print("T. uso de CPU:", estado_global.T_usoCPU)
    FM.gotoxy(78,3)
    print("T. de CPU ocioso:", estado_global.T_CPU_ocioso)
    FM.gotoxy(78,4)
    print("Grado Multiprogramación:", estado_global.multiprogramacion)
    FM.gotoxy(78,5)
    print("Procesos Restantes:", estado_global.cantTotalProcesos)




