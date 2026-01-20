import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
#import copy

import msvcrt
import paquetes.estado_global as vGlobal
#from pathlib import Path
from rich.console import Console
from rich.table import Table
from paquetes.AgustinVeron.Menu import gotoxy as desplazarTabla, limpiar_pantalla
import paquetes.LisandroRojas.funcionesconlistas_isabel_arregladoLisandro as FunArchivosListasOtro
import paquetes.AgustinVeron.funcionesAgustin as FAgus



#esta funcion es para sumar  tiempo ocioso y tambien para desplazarse al primer arribo si estos no llegan al instante cero
def CiclosOciosos(proceso_siguiente:dict):
    #solo si no tiene procesos pendientes en listos puede ejecutarse un ciclo ocioso
    vGlobal.multiprogramacion = (len(vGlobal.listaListos))+(len(vGlobal.listaSuspendidos))
    if len(vGlobal.listaListos)<=1:
            if (proceso_siguiente.get("t_arribo"))<=(vGlobal.T_simulador):
                #demas lapsos de tiempo ociosos y si hay procesos pendientes despues de iniciar
                print("========================================================================================================================================\n")
                print(f"Sin arribos en instante {vGlobal.T_simulador}, el procesador se encuentra en estado ocioso.\n")
                #print("Presione una tecla para continuar al siguiente instante...")
                avanzar=(vGlobal.T_simulador) - (proceso_siguiente.get("t_arribo"))
                vGlobal.T_CPU_ocioso += avanzar
                vGlobal.T_simulador += avanzar
                ADMICION_MULTI_5() 
                print("========================================================================================================================================\n")
                print(f"Proceso arribo en instante {proceso_siguiente.get("t_arribo")}, el procesador deja de estar ocioso.\n")
                print(f"Presione una tecla para continuar...")
                vGlobal.multiprogramacion = ((len(vGlobal.listaListos))+(len(vGlobal.listaSuspendidos)))
                msvcrt.getch()  # espera cualquier tecla
    ADMICION_MULTI_5()
    solo_mostrarTablas()#ingresaron. hay que mostrar
    print(f"Presione una tecla para continuar...")
    msvcrt.getch()  # espera cualquier tecla
    limpiar_pantalla()
        


#muestra una columna adicional de la tabla de procesos cargados
def actualizar_estado_Proceso(proceso:dict)-> str:
    proceso_ID=proceso.get("id")
    if any((p.get("id")==proceso_ID and (p.get("CPU"))) for p in vGlobal.listaListos):
        return "EN EJECUCION"
    if any(p.get("id")==proceso_ID for p in vGlobal.listaListos):
        return "LISTO"
    if any(p.get("id")==proceso_ID for p in vGlobal.listaSuspendidos):
        return "LISTO/SUSPENDIDO"
    if any(p.get("id")==proceso_ID for p in vGlobal.listaTerminados):
        return "TERMINADO"
    if any(p.get("id")==proceso_ID for p in vGlobal.listaProcesos):
        return "NUEVO"


#para insertar elementos nuevos en las otras listas, les hay que generear otros campos y actualizarlos para terminar de actualizar la lista en general
def actualizar_proceso_enLista(lista: list, proceso_actualizado: dict) -> bool:
    for p in lista: #recorre la lista buscando el proceso
        if p.get("id") == proceso_actualizado.get("id"):
            p.update(proceso_actualizado)#en el mismo lugar del proceso actualiza el diccionario alojado en la lista y no rompe referencias
            return True # se encontro el proceso y se actualizo de forma correcta
    return False # No se encontro el proceso y no se pudo actualizar de forma correcta

def actualizar_proceso_enMemoriaPrincipal(lista: list, proceso_actualizado: dict) -> bool:
    for p in lista: #recorre la lista buscando la particion   
        if p.get("Particion") == proceso_actualizado.get("Particion"):
            p.update(proceso_actualizado) #en el mismo lugar de la particion actualiza el diccionario alojado en la lista y no rompe referencias
            return True # se encontro el proceso y se actualizo de forma correcta            
    return False # No se encontro el proceso y no se pudo actualizar de forma correcta

def marcar_procesoNuevo_Ingresado(procesoNuevo):
    for p in vGlobal.listaProcesos: #recorre la lista buscando el proceso
        if (p.get("id") == procesoNuevo.get("id")): #al proceso que estamos cargando a la cola de memoria, lo marcamos como ingresado en la lista de procesos
            p["bandera_baja_logica"]=True 
            #print(f"Proceso: {p["id"]}, marcado como ingresado")
            break

#copia datos de un proceso para acomodarlos en los campos de otra lista y completar los demas campos
def mover_aColaSuspendido(proceso_actual:dict):
    #marca ingresado el proceso nuevo. adentro de la funcion se revisa si no se ingreso antes
    marcar_procesoNuevo_Ingresado(proceso_actual)
    #obtener los datos del proceso actual
    #if "campo" not in proceso_actual:
    cargarTiempoRespuesta=int(vGlobal.T_simulador - proceso_actual.get("t_arribo"))
    if "t_ingreso" not in proceso_actual:
        cargarTiempoIngreso=int(vGlobal.T_simulador)
    else:cargarTiempoIngreso=proceso_actual.get("t_ingreso")
    if "t_RestanteCPU" not in proceso_actual:
        t_Restante=int(proceso_actual.get("t_irrupcion"))#inicializa si viene directo de procesos nuevos(listaProcesos)
    else:t_Restante=int(proceso_actual.get("t_RestanteCPU"))#actualiza si es necesario
    
    proceso_suspendido={
        "id": proceso_actual.get("id"),
        "t_arribo": proceso_actual.get("t_arribo"),
        "tamaño": proceso_actual.get("tamaño"),
        "t_irrupcion": proceso_actual.get("t_irrupcion"),
        "t_Respuesta": (cargarTiempoRespuesta), #aca se tiene que guardar el tiempo que el simulador tardo en atender la solicitud
        "t_ingreso": (cargarTiempoIngreso), #aca se tiene que guardar el tiempo en el que entra el proceso a memoria secundaria
        "t_RestanteCPU": (t_Restante), #actualizar segun una funcion que devuelva un entero. estamos en lista de suspendidos, solo se incicializa el campo porque entro a memoria secundaria, no puede ejecutarse hasta entrar a Memoria Principal
    }
    if actualizar_proceso_enLista(vGlobal.listaSuspendidos, proceso_suspendido):#actualiza el diccionario del proceso en la lista sin cambiar la cantidad  de elementos de la lista 
        print(f"\n")
    else: #agrega a la lista
        vGlobal.listaSuspendidos.append(proceso_suspendido)
        #print(f"proceso agregado a lista de suspendidos")
        
    
def mover_aColaListo(proceso_actual:dict):
    #marca ingresado el proceso nuevo. adentro de la funcion se revisa si no se ingreso antes desde suspendido
    marcar_procesoNuevo_Ingresado(proceso_actual)
    tiempoArriboMemPrincipal=vGlobal.T_simulador
    #revisar si el campo exite porque viene desde suspendido y solo se vuelve a copiar, no existe= viene de lista de nuevo
    if "t_Respuesta" not in proceso_actual:
        cargarTiempoRespuesta=int(vGlobal.T_simulador - proceso_actual.get("t_arribo"))
    else:
        cargarTiempoRespuesta=proceso_actual.get("t_Respuesta")
    if "t_ingreso" not in proceso_actual:#copia o carga el tiempo en el que entra el proceso al simulador
        cargarTiempoIngreso=int(vGlobal.T_simulador)
    else: cargarTiempoIngreso=proceso_actual.get("t_ingreso")
    if "t_RestanteCPU" not in proceso_actual:
        t_Restante=int(proceso_actual.get("t_irrupcion")) #inicializa si viene directo de procesos nuevos(listaProcesos)
    else: t_Restante=int(proceso_actual.get("t_RestanteCPU")) #copia el tiempo restante si ya existe
    if "tiempoTotal_enColaDeListo" not in proceso_actual:
        tiempoTotal_enColaDeListo=0 #recien entra a listo
    else:
        tiempoTotal_enColaDeListo=proceso_actual.get("tiempoTotal_enColaDeListo")#actualiza el tiempo ante cualquier interrupcion con un nuevo valor cargado desde la variable en el argumento

    proceso_listo={#cargamos el registro que agregamos a la lista
        "id": proceso_actual.get("id"),
        "t_arribo": proceso_actual.get("t_arribo"),
        "tamaño": proceso_actual.get("tamaño"),
        "t_arribo_MP": int(tiempoArriboMemPrincipal), #instante de tiempo en el que el proceso es cargado a memoria principal
        "t_irrupcion": proceso_actual.get("t_irrupcion"),
        "t_Respuesta": (cargarTiempoRespuesta), #aca se tiene que guardar el tiempo que el simulador tardo en atender la solicitud
        "t_ingreso": (cargarTiempoIngreso), #aca se tiene que guardar el tiempo en el que entra el proceso al simulador
        "t_RestanteCPU": int(t_Restante), #actualizar segun una funcion que devuelva un entero. estamos en lista de listos
        "tiempoTotal_enColaDeListo": int(tiempoTotal_enColaDeListo), #este tiene que actualizarse al momento de salir de listo para entrar a ejecucion
        "CPU": False #bandera para no mostrar en la tabla de listos pero si para la tabla de en ejecucion
    }
    if actualizar_proceso_enLista(vGlobal.listaListos,proceso_listo):#actualiza el diccionario del proceso en la lista sin cambiar la cantidad  de elementos de la lista. es para actualizar procesos cuando estos tienen algun cambio en algun campo
        print(f"proceso agregado a lista de listos")
        print("\n")
    else: #agrega a la lista
        vGlobal.listaListos.append(proceso_listo)
        #print(f"proceso agregado a lista de listos")
    vGlobal.aux=proceso_listo #resguarda el proceso para manejo del BestFitCICLO_ADMICION

#tablas de datos
#tabla cola de listos
def mostrarColaListos():
    console = Console()
    #renderizar la tablita hermosa con rich, ciclando los objetos en vGlobal.listaListos
    table = Table(title="Procesos en memoria Principal --> Estado: 'Listo'", show_lines=True)
    table.add_column("ID Proceso", justify="right", style="yellow", no_wrap=True)
    table.add_column("Tiempo Arribo", justify="right")
    table.add_column("Tamaño",justify="right" )
    table.add_column("Tiempo Arribo a MP", justify="right")
    table.add_column("Tiempo Irrupcion", justify="right")
    table.add_column("Tiempo de Respuesta", justify="right")
    table.add_column("Tiempo de Ingreso", justify="right")
    table.add_column("Tiempo Restante de CPU", justify="right")
    table.add_column("Tiempo de Total en Cola de Listos", justify="right")
    if vGlobal.listaListos != []:
        for p in vGlobal.listaListos:
            if (len(vGlobal.listaListos)>=0) and p["CPU"] == False: #es la marca proceso en CPU ejecutandoce o no, falso se muestra en tabla de listos
                table.add_row( #medio tipo:  array[0] pero con los key del diccionario
                    str(p["id"]),
                    str(p["t_arribo"]),
                    str(p["tamaño"]),
                    str(p["t_arribo_MP"]),
                    str(p["t_irrupcion"]),
                    str(p["t_Respuesta"]),
                    str(p["t_ingreso"]),
                    str(p["t_RestanteCPU"]),
                    str(p["tiempoTotal_enColaDeListo"])                    
                    )
            if (len(vGlobal.listaListos)==1) and (p["CPU"]==True):
                table.add_row(str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"))
    else:#lista vacia
        table.add_row(str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"))
    console.print(table)

#tabla cola de Listo/Suspendido
def mostrarColaSuspendido():
    console = Console()
      #renderizar la tablita hermosa con rich, ciclando los objetos en vGlobal.listaSuspendidos
    table = Table(title="Procesos en memoria Secundaria --> Estado: 'Listo y Suspendido'", show_lines=True)
    table.add_column("ID Proceso", justify="right", style="yellow", no_wrap=True)
    table.add_column("Tiempo Arribo", justify="right")
    table.add_column("Tamaño",justify="right" )
    table.add_column("Tiempo Irrupcion", justify="right")
    table.add_column("Tiempo de Respuesta", justify="right")
    table.add_column("Tiempo de Ingreso", justify="right")
    table.add_column("Tiempo Restante de CPU", justify="right")

    if vGlobal.listaSuspendidos:
        for p in vGlobal.listaSuspendidos:
            table.add_row(
               str(p["id"]),
               str(p["t_arribo"]),
               str(p["tamaño"]),
               str(p["t_irrupcion"]),
               str(p["t_Respuesta"]),
               str(p["t_ingreso"]),
               str(p["t_RestanteCPU"])
            )
    else:#lista vacia
        table.add_row(str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"))
    console.print(table)

def mover_aColaTerminados(proceso_actual:dict):
    total_Retorno= (vGlobal.T_simulador - proceso_actual.get("t_arribo_MP"))#tiempo que tardo en salir del simulador una vez empezo a ejecutarse
    instante_Retorno= vGlobal.T_simulador
    proceso_Terminado={
        "id": proceso_actual.get("id"),
        "t_arribo": proceso_actual.get("t_arribo"),
        "tamaño": proceso_actual.get("tamaño"),
        "t_arribo_MP": proceso_actual.get("t_arribo_MP"),
        "t_irrupcion": proceso_actual.get("t_irrupcion"),
        "t_Respuesta": proceso_actual.get("t_Respuesta"), #aca se tiene que guardar el tiempo que el simulador tardo en atender la solicitud
        "t_Retorno": (instante_Retorno), #tiempo que tarda en salir del cpu y volver a la cola de listos, sirve para medir el tiempo de CPU utilizado hasta un evento de apropiacion
        "total_Retorno":(total_Retorno),
        "t_ingreso": proceso_actual.get("t_ingreso"), #aca se tiene que guardar el tiempo en el que entra el proceso a memoria
        "tiempoTotal_enColaDeListo": (proceso_actual.get("tiempoTotal_enColaDeListo")), #este tiene que actualizarse al momento de salir de listo para entrar a ejecucion
        "tiempoFinalizacion": (vGlobal.T_simulador) #se guarda el instante de tiempo en el que finaliza, el mismo instante en el que se llama a esta funcion
    }
    #agragamos el proceso terminado a la lista de termindos
    if actualizar_proceso_enLista(vGlobal.listaTerminados,proceso_Terminado):
        print(f"\n")
    else:vGlobal.listaTerminados.append(proceso_Terminado)
    print(f"Proceso agregado a lista de Terminados\n")
    eliminarDeLista(vGlobal.listaListos,proceso_Terminado)
    mostrarTablaTerminados()

# tabla de informacion para procesos en estado Terminado
def mostrarTablaTerminados():
    console = Console()
      #renderizar la tablita hermosa con rich, ciclando los objetos en vGlobal.listaTerminados
    table = Table(title="Procesos Terminados --> Estado: 'Terminado'", show_lines=True)
    table.add_column("ID Proceso", justify="right", style="yellow", no_wrap=True)
    table.add_column("Tiempo Arribo", justify="right")
    table.add_column("Tamaño",justify="right" )
    table.add_column("Tiempo Arribo a MP", justify="right")
    table.add_column("Tiempo Irrupcion", justify="right")
    table.add_column("Tiempo de Ingreso", justify="right")
    table.add_column("Tiempo de Respuesta", justify="right")    
    table.add_column("Instante de Retorno", justify="right")
    table.add_column("Tiempo transcurrido hasta el Retorno", justify="right")
    table.add_column("Tiempo Total en Cola de Listos", justify="right")
    table.add_column("Tiempo de Finalizacion", justify="right")

    if vGlobal.listaTerminados:
        for p in vGlobal.listaTerminados:
            table.add_row( #medio tipo:  array[0] pero con los key del diccionario
                str(p["id"]),
                str(p["t_arribo"]),
                str(p["tamaño"]),
                str(p["t_arribo_MP"]),
                str(p["t_irrupcion"]),
                str(p["t_ingreso"]),
                str(p["t_Respuesta"]),
                str(p["t_Retorno"]),
                str(p["total_Retorno"]),
                str(p["tiempoTotal_enColaDeListo"]),
                str(p["tiempoFinalizacion"])
                )
    else:#lista vacia
        table.add_row(str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"),str("xxx"))
    console.print(table)

#=================================================================================================================
##estas funciones son para usar en la logica del SRTF y cargar los procesos a memoria principal
def cargarProcesoAlojado(memoria: list, puntero:int, proceso_actual:dict):
    particion=memoria[puntero]
    particion["Proceso_alojado"]=proceso_actual # ESTO ES UNA REFERENCIA AL DICCIONARIO DE LA COLA DE LISTOS, lo que se modifique desde el proceso en listo tambien se refleja en el diccionario dentro de proceso alojado
    particion["Fragmentacion_Interna"]=(int(particion["TamañoTotal"] - proceso_actual.get("tamaño")))
    particion["Ocupado"]=True
    actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal,particion)

def activarProceso_en_CPU(memoria: list, puntero:int):
    #print(f"==============================================|EJECUTANDO...activar proceso|==============================================")
    proceso=memoria[puntero]["Proceso_alojado"]#como el proceso esta referenciado al cargarlo a proceso alojado, el modificar CPU en MP tambien se modifica en cola de listos
    particion=memoria[puntero]
    proceso["CPU"]=True
    for p in vGlobal.listaListos:
        p["CPU"] = (p["id"] == proceso["id"])
    print("activa el CPU")
    actualizar_proceso_enLista(vGlobal.listaListos,proceso)
    actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal,particion)
    #print(f"==============================================|FIN EJECUCION...activar proceso|==============================================\n")

def desactivarProceso_en_CPU(memoria: list, puntero:int):
    #print(f"==============================================|EJECUTANDO...desactivar proceso|==============================================")
    proceso=memoria[puntero]["Proceso_alojado"]#como el proceso esta referenciado al cargarlo a proceso alojado, el modificar CPU en MP tambien se modifica en cola de listos
    particion=memoria[puntero]
    proceso["CPU"]=False
    for p in vGlobal.listaListos:
        p["CPU"] = (p["id"] == proceso["id"])
    print("desactiva el CPU")
    particion["Ocupado"]=True #sigue ocupada la particion

    #aseguramos que las listas se actualizan
    actualizar_proceso_enLista(vGlobal.listaListos,proceso)    
    actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal,particion)
    #print(f"==============================================|FIN EJECUCION...desactivar proceso|==============================================\n")

#Necesario para actualizar el estado de los procesos en memoria para mostrar las tablas de memoria principal
def terminarProcesoAlojado(memoria: list, puntero:int):
    #print(f"==============================================|EJECUTANDO...TERMINAR EL PROCESO|==============================================")
    particion=memoria[puntero]
    particion["Ocupado"]=False #libera la particion, no borramos el proceso asi sobreescribimos luego
    actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal,particion)
    #print(f"Proceso {particion["Proceso_alojado"]["id"]}, a finalizado")
    #print(f"==============================================|FIN EJECUCION...TERMINAR EL PROCESO|==============================================\n")

#tabla de informacion de particiones de memoria principal
def mostrarMemoriaPrincipal():
    console = Console()
    table = Table(title="Memoria Principal", show_lines=True)
    table.add_column("Particion", justify="right", style="green", no_wrap=True)
    table.add_column("Tamaño Total",justify="right")
    table.add_column("Direccion inicio",justify="right")    
    table.add_column("Tipo particion", justify="right")
    table.add_column("Proceso alojado", justify="right", style="yellow", no_wrap=True)
    table.add_column("Fragmentacion_Interna", justify="right")
    table.add_column("Ocupado", justify="right", style="yellow", no_wrap=True)
    
    
    particion_SO=vGlobal.MemoriaPrincipal[3]#ultimo Elemento
    table.add_row(
        str(particion_SO["Particion"]),
        str(particion_SO["TamañoTotal"]),
        str(particion_SO["Dir_Comienzo"]),
        str(particion_SO["Dueño"]),#Tipo particion
        str("SO"),
        str(particion_SO["Fragmentacion_Interna"]),
        "NO DISPONIBLE"      
    )
            
    for p in vGlobal.MemoriaPrincipal[:3]:
        if p.get("Ocupado"):
            espacio="NO DISPONIBLE"
        else:
            espacio="DISPONIBLE"
        if(p["Proceso_alojado"]!={}) and (p["Proceso_alojado"]!=None):
            #proceso_id_display = p["Proceso_alojado"]["id"] if isinstance(p["Proceso_alojado"], dict) else "Ninguno"
            if p["Proceso_alojado"]!={}:
                proceso=p["Proceso_alojado"]
            else: proceso="Ninguno"
            if proceso!="Ninguno":
                table.add_row(
                    str(p["Particion"]),
                    str(p["TamañoTotal"]),
                    str(p["Dir_Comienzo"]),
                    str(p["Dueño"]),
                    str(proceso["id"]),
                    str(p["Fragmentacion_Interna"]),
                    espacio
                )
        else:#particion sin procesos cargados
            table.add_row(
                str(p["Particion"]),
                str(p["TamañoTotal"]),
                str(p["Dir_Comienzo"]),
                str(p["Dueño"]),
                str("LIBRE"),
                str(p["Fragmentacion_Interna"]),
                espacio
                )
    console.print(table)

def mostrarProcesoCPU():
    console = Console()
    table = Table(title="Proceso utilizando CPU --> Estado: 'En Ejecucion'", show_lines=True)
    table.add_column("ID Proceso", justify="right", style="yellow", no_wrap=True)
    table.add_column("Tamaño",justify="right")
    table.add_column("Particion",justify="right", style="green", no_wrap=True)
    table.add_column("Tiempo Restante de CPU", justify="right")
    
    procesoEncontrado=False
    for p in vGlobal.MemoriaPrincipal[:3]: 
        if (p["Proceso_alojado"]) and ((p["Proceso_alojado"]).get("CPU")):
            procesoEncontrado=True
            laParticion=p
            break
    if vGlobal.listaListos:
        for procesito in vGlobal.listaListos:
            if (procesito.get("CPU"))==True:
                print(f"Particion {laParticion['Particion']} está ocupada con el proceso {procesito['id']} que esta usando la CPU")
                table.add_row(
                    str(procesito["id"]),
                    str(procesito["tamaño"]),
                    str(laParticion["Particion"]),
                    str(procesito["t_RestanteCPU"])
                )
    if not procesoEncontrado:
        table.add_row(str("xxx"),str("xxx"),str("xxx"),str("xxx"))
    console.print(table)


def solo_mostrarTablas():
    print(F"INSTANTE ACTUAL DEL SIMULADOR>>>>>>>>>>>>>>>>>   {vGlobal.T_simulador}")
    print(f"MULTIPROGRAMACION>>>>>>>>>>>>>>>>>   {vGlobal.multiprogramacion}")
    print(F"================================================================================================================\n")
    FunArchivosListasOtro.mostrar_tabla(vGlobal.listaProcesos) #muestra la tabla de procesos nuevos
    print(F"================================================================================================================\n")
    mostrarMemoriaPrincipal() #muestra la tabla de memoria principal
    print(F"================================================================================================================\n")
    mostrarProcesoCPU()#muestra la tabla de estado de cpu
    print(F"================================================================================================================\n")
    mostrarColaListos()#muestra la tabla de cola de listos
    print(F"================================================================================================================\n")
    mostrarColaSuspendido()#muestra la tabla de cola de suspendidos
    print(F"================================================================================================================\n")
    mostrarTablaTerminados()
    print(F"INSTANTE ACTUAL DEL SIMULADOR>>>>>>>>>>>>>>>>>   {vGlobal.T_simulador}")
    print(f"MULTIPROGRAMACION>>>>>>>>>>>>>>>>>   {vGlobal.multiprogramacion}")
    
def informe_final():
    console = Console()
    if vGlobal.T_simulador > 0:
        rendimiento = (len(vGlobal.listaTerminados)/vGlobal.T_simulador)*100
    else: rendimiento =0
    if vGlobal.T_simulador > 0:
        CPUociso_porcentaje=(vGlobal.T_CPU_ocioso/vGlobal.T_simulador)*100
    else: CPUociso_porcentaje =0
    if vGlobal.T_simulador > 0:
        usoCPU_porcentaje=(vGlobal.T_usoCPU_TotalGeneral/vGlobal.T_simulador)*100
    else: usoCPU_porcentaje =0
    promedioT_Espera=0
    promRetorno=0
    for p in vGlobal.listaTerminados:
        promedioT_Espera+=p.get("tiempoTotal_enColaDeListo")
        promRetorno+=p.get("total_Retorno")
    promRetorno=promRetorno/vGlobal.cantTotalProcesos
    promedioT_Espera=(promedioT_Espera)/vGlobal.cantTotalProcesos
    table = Table(title="Informe de Rendimiento del simulador", show_lines=True)
    table.add_column("Tiempo total de CPU ocioso", justify="right")
    table.add_column("Porcentaje CPU ocioso", justify="right")
    table.add_column("Tiempo de simulador", justify="right")    
    table.add_column("Tiempo total de CPU utilizado",justify="right")
    table.add_column("uso de CPU%", justify="right")
    table.add_column("Rendimiento", justify="right")
    table.add_column("T.Espera Promedio", justify="right")
    table.add_column("T.Retorno Promedio", justify="right")
    table.add_row(
                str(vGlobal.T_CPU_ocioso),
                f"{CPUociso_porcentaje:.2f} %",
                str(vGlobal.T_simulador),
                str(vGlobal.T_usoCPU_TotalGeneral),
                f"{usoCPU_porcentaje:.2f} %",
                f"{rendimiento:.2f} %",
                f"{promedioT_Espera:.2f}",
                f"{promRetorno:.2f}"
                )
    console.print(table)
    mostrarTablaTerminados()

def cabeEnAlgunaParticionLIBRE(procesoAct:dict) -> bool:
    #Determina si el proceso cabe en al menos una partición para si quiera pensar en admitirlo en MP
    bandera=False
    for l in vGlobal.MemoriaPrincipal:
        if (l.get("Ocupado")==False) and (l.get("TamañoTotal")-(procesoAct.get("tamaño"))>=0)and(l.get("Dueño")!="SO"):
            bandera=True
    return bandera

def BestFitCICLO_ADMICION(ProcActual:dict):
    #Determina la partición del proceso por la menor fragmentación interna
    menorFragmentacionInt = float("inf")
    posicionAsignada = None
    mejorEncontrado=False
    for i,particion in enumerate(vGlobal.MemoriaPrincipal):
        if (particion.get("Ocupado") == False)and(particion.get("Dueño")!="SO"):
            fragContraProceso=(particion.get("TamañoTotal") - ProcActual.get("tamaño"))
            if (fragContraProceso>=0) and (fragContraProceso< menorFragmentacionInt):
                menorFragmentacionInt = particion.get("TamañoTotal") - ProcActual.get("tamaño")
                posicionAsignada = i
                mejorEncontrado=True
            else: continue
    if mejorEncontrado==True:
        return posicionAsignada
    return None

def SuspendidosYListos():#eliminia procesos alojados en suspendidos porque ya estan en la cola de listos
    for j in vGlobal.listaListos:
        for p in (vGlobal.listaSuspendidos):
            if (j["id"]==p["id"]):
                eliminarDeLista(vGlobal.listaSuspendidos,p)

 
def eliminarDeLista(lista: list, proceso: dict):
    # elimina por id, una sola vez
    for i, p in enumerate(lista):#recorre la lista buscando el proceso
        if p.get("id") == proceso.get("id"):#si el proceso estaba cargado en la lista, lo elimina
            #print(lista)
            lista.pop(i)
            #print(f"Proceso: {proceso.get('id')}, fue ELIMINADO de la lista...")
            #print(lista)
            return True
    #print(f"No existe el proceso: {proceso.get('id')}, no puede eliminarse algo que no existe")
    return False


def BuscarSRTF():
    #print("\n====|EJECUCION DEL BUSCADOR SRTF|====\n")
    menorTR = float("inf")
    indiceDeLaParticion = None
    procesoElegido = None

    #si no hay listos, nada que elegir
    if (len(vGlobal.listaListos))<1:
        #print("⚠️ No hay procesos ejecutables en memoria principal")
        #volver y tiempo ocioso usa el none
        return None

    for procesosListos in vGlobal.listaListos:
        tr = procesosListos.get("t_RestanteCPU")
        if (tr > 0) and (tr < menorTR):
            menorTR = tr
            procesoElegido = procesosListos

    # localizar la partición del proceso elegido
    if procesoElegido is not None:
        for i, particion in enumerate(vGlobal.MemoriaPrincipal):
            if particion.get("Proceso_alojado") is procesoElegido:
                indiceDeLaParticion = i
                break

    if indiceDeLaParticion is not None:
        return indiceDeLaParticion

    #print("⚠️ No hay procesos ejecutables en memoria principal")
    #volver y tiempo ocioso usa el none
    return None


def CARGAR_MPconMS():#esta funcion es llamada porque la lista de suspendido es diferente de vacio
    bandera=True 
    #queremos cargar todos los procesos de los suspendidos hasta completar los 3 espacios de listos o vaciar la lista de suspendidos, segun lo que pase primero se activa la vandera y salimos del bucle while
    while (len(vGlobal.listaListos) < 3) and bandera:
        bandera_cambios= False
        for ingresaMemSec in list(vGlobal.listaSuspendidos):
            #print(f"Intentando admitir proceso suspendido: {ingresaMemSec['id']}")
            #if len(vGlobal.listaListos)>=3:
            #    break
            if cabeEnAlgunaParticionLIBRE(ingresaMemSec):# si hay una particion libre y al mismo tiempo que el proceso nuevo pueda entrar, se mueve a listo y se carga a MP
                mover_aColaListo(ingresaMemSec)#carga el proceso nuevo a Listo
                puntero=BestFitCICLO_ADMICION(vGlobal.aux)#buscamos la particion en la que coincidio que podia entrar antes de que otro proceso lo ocupe
                cargarProcesoAlojado(vGlobal.MemoriaPrincipal,puntero,vGlobal.aux)#cargamos en la particion que mejor entra
                bandera_cambios=True
                #print(f"PROCESO SUSPENDIDO: {ingresaMemSec['id']}, ADMITIDO A MEMORIA PRINCIPAL")
                #print(f"Proceso {ingresaMemSec['id']} cargado en partición {vGlobal.MemoriaPrincipal[puntero]["Particion"]}")
            #no entra, pasa al siguiente suspendido para revisar si puede entrar a MP, el proceso iterado de suspendido se queda en la lista de suspendidos
        #Se termino de ingresar procesos a listo o se termino de recorrer la lista de suspendidos
        SuspendidosYListos()#eliminamos los procesos de la cola de suspendidos
        #otro control de salida
        if (len(vGlobal.listaListos)>=3) or (vGlobal.listaSuspendidos==[]):# se completo la MP o se terminaron los procesos suspendidos
            bandera=False# salimos de la funcion de cargar MP con MS
        elif not bandera_cambios:
            bandera=False

#llamar esta funcion en cada instante de arribo de un proceso y en cada instante de que termina un proceso
def ADMICION_MULTI_5():#if (vGlobal.multiprogramacion < 5)and(vGlobal.listaProcesos[-1]["bandera_baja_logica"]==False):
    vGlobal.multiprogramacion = ((len(vGlobal.listaListos))+(len(vGlobal.listaSuspendidos)))
    
    if (vGlobal.multiprogramacion >= 5):
        print("Limite de multiprogramacion 5 alcanzado\nNo se admiten mas procesos")
        return
    if len(vGlobal.listaListos)<3 and ((len(vGlobal.listaSuspendidos))>=0):#acomodar procesos entre MP y MS. Completar MP desde MS
        CARGAR_MPconMS()#SOLO VA A CARGAR CON LO DISPONIBLE EN MS
        #Una vez completada la memoria Principal, movemos procesos nuevos a Suspendidos para completar la multiprogramacion
        
    #SI al terminar de cargar la MP se terminaron los suspendidos y tambien no se completo la MP, tenemos que ingresar procesos desde nuevos a MP y a MS luego
    bandera=True
    while (vGlobal.multiprogramacion < 5)and bandera:
        vGlobal.multiprogramacion = ((len(vGlobal.listaListos))+(len(vGlobal.listaSuspendidos)))
        bandera_cambios=False # siempre que hay cambios, actualizar multiprogramacion
        for procesoIngresa in vGlobal.listaProcesos:#revisar los procesos sin arribar
            #print(f"Intentando admitir proceso nuevo: {procesoIngresa['id']} con arribo {procesoIngresa['t_arribo']}")
            if procesoIngresa.get("bandera_baja_logica") is False and (procesoIngresa["t_arribo"]<=vGlobal.T_simulador):
            #controlar si hay espacio en MP o MS y tratamos procesos dentro del tiempo del simulador
                if (len(vGlobal.listaListos)<3) and cabeEnAlgunaParticionLIBRE(procesoIngresa):#primero revisar si hay espacio en memoria principal
                    #espacio en listos
                    mover_aColaListo(procesoIngresa)#carga el proceso nuevo a Listo
                    puntero=BestFitCICLO_ADMICION(vGlobal.aux)#buscamos la particion en la que coincidio que podia entrar antes de que otro proceso lo ocupe
                    cargarProcesoAlojado(vGlobal.MemoriaPrincipal,puntero,vGlobal.aux)#cargamos en la particion que mejor entra
                    bandera_cambios= True # siempre que hay cambios, actualizar multiprogramacion
                    vGlobal.banderaADMICION_Nuevos=True
                    vGlobal.multiprogramacion = ((len(vGlobal.listaListos))+(len(vGlobal.listaSuspendidos)))
                    #vGlobal.multiprogramacion+=1
                else:#no entraba en ninguna particion libre, se mueve a suspendido, tiene que esperar a que se libere un proceso que termina para entrar a MP
                    mover_aColaSuspendido(procesoIngresa)
                    bandera_cambios= True # siempre que hay cambios, actualizar multiprogramacion
                    vGlobal.banderaADMICION_Nuevos=True
                    vGlobal.multiprogramacion = ((len(vGlobal.listaListos))+(len(vGlobal.listaSuspendidos)))
                    #vGlobal.multiprogramacion+=1
                    #nuevo proceso fue ingresado a MP o a la MS, la multiprogramacion aumenta
                 
            vGlobal.multiprogramacion = ((len(vGlobal.listaListos))+(len(vGlobal.listaSuspendidos)))       
            #volver a controlar multiprogramacion
            if vGlobal.multiprogramacion>=5: 
                #print("Limite de multiprogramacion 5 alcanzado\nNo se admiten mas procesos")
                return
    
        if not bandera_cambios:#ya sea por multiprogramacion o por que llego a un arribo mayor al tiempo del simulador, salimos del while para no volver a recorrer con el for 
            bandera=False # siempre que hay cambios, actualizar multiprogramacion
            vGlobal.multiprogramacion = ((len(vGlobal.listaListos))+(len(vGlobal.listaSuspendidos)))
        
    #termina de ejecutar la funcion
    vGlobal.multiprogramacion = ((len(vGlobal.listaListos))+(len(vGlobal.listaSuspendidos)))
    