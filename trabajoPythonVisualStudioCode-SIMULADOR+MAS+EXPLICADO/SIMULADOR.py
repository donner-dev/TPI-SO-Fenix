
from re import I
import paquetes.LisandroRojas.funcionesLisandro_prolijo as Lis
import paquetes.AgustinVeron.Menu as MA
#import AgustinVeron.funcionesAgustin as FA
import paquetes.estado_global as vGlobal
import paquetes.LisandroRojas.funcionesconlistas_isabel_arregladoLisandro as FunArchivos
import os
import sys

"""
Módulo: SIMULADOR

Este script orquesta la simulación de gestión de procesos y memoria. Su
objetivo principal es coordinar las funciones implementadas en los módulos
importados (principalmente `paquetes.LisandroRojas.funcionesLisandro_prolijo`)
para: 1) admitir procesos desde archivos CSV, 2) gestionar admisión a memoria
principal/secundaria (BestFit y colas), 3) planificar la CPU usando SRTF
(shortest remaining time first), 4) ejecutar procesos ciclo a ciclo y 5)
producir un informe final de rendimiento.

Orden lógico y uso secuencial de funciones:
- `FunArchivos.elegir_archivo()` y `FunArchivos.leer_procesos()` cargan los
    procesos iniciales desde CSV.
- `Lis.ADMICION_MULTI_5()` controla la admisión de procesos en cada instante
    (manteniendo multiprogramación y llenando MP desde MSecundaria si aplica).
- `Lis.BuscarSRTF()` se utiliza para seleccionar el siguiente proceso en CPU
    (retorna índice de partición en MP o `None`).
- `Lis.activarProceso_en_CPU` / `Lis.desactivarProceso_en_CPU` y
    `Lis.terminarProcesoAlojado` manejan el estado de la CPU y la memoria.
- `ejecutarTodo(puntero)` ejecuta el ciclo de CPU del proceso alojado en la
    partición `puntero`, consumiendo CPU por ciclo, detectando arribos,
    apropiaciones SRTF y finalizaciones.
- `solo_mostrarTablas()` y funciones de `Lis` imprimen el estado cuando hay
    interrupciones para facilitar seguimiento y depuración.

Este archivo coordina el loop principal (`main`) y mantiene variables de
estado en `paquetes.estado_global` (`vGlobal`).

========================================================================
CONCEPTO FIFO (First In-First Out) EN ESTE SIMULADOR
========================================================================

Aunque el simulador usa SRTF para PLANIFICACIÓN (seleccionar quién entra en CPU),
usa una estrategia FIFO-like para ADMISIÓN de procesos:

1. LISTAPROCESOS (origen): Procesos llegan en orden (FIFO) del archivo CSV
   y se recorren secuencialmente en ADMICION_MULTI_5().

2. LISTALISTOS (cola FIFO en memoria principal):
   - Es una lista que mantiene procesos en orden de llegada a memoria.
   - Cuando un proceso no cabe en MP, se mueve a listaSuspendidos (MS).
   - ADMICION_MULTI_5() recorre listaProcesos en orden y admite los primeros
     que caben ("primeros llegan, primeros se admiten").

3. RELACIÓN FIFO → MemoriaPrincipal → Particiones:
   - listaListos[i] contiene REFERENCIAS a procesos en memoria.
   - Cada proceso en listaListos está alojado en una partición de MemoriaPrincipal.
   - El dict MemoriaPrincipal[j]["Proceso_alojado"] APUNTA al MISMO OBJETO que
     listaListos[i] (no es una copia, es la misma referencia en memoria).
   - Esto significa: modificar listaListos[i]["t_RestanteCPU"] también actualiza
     MemoriaPrincipal[j]["Proceso_alojado"]["t_RestanteCPU"] automáticamente.

4. FLUJO DE ADMISIÓN (FIFO-like):
   a) Se recorre listaProcesos en orden (FIFO del archivo).
   b) Para cada proceso que llega en el tiempo actual:
      - Se valida si cabe en alguna partición libre usando BestFit.
      - Si cabe en MP: mover_aColaListo(proceso) + cargarProcesoAlojado(MP, puntero, vGlobal.aux).
      - Si NO cabe: mover_aColaSuspendido(proceso) → se almacena en MS.
   c) Cuando libera espacio en MP, CARGAR_MPconMS() trae suspendidos hacia listos
      (manteniendo FIFO: los primeros suspendidos son los primeros en entrar a MP).

5. RELACIÓN CON SRTF (Planificador Corto Plazo):
   - FIFO controla CUÁNDO y EN QUÉ ORDEN ingresan procesos a memoria.
   - SRTF controla CUÁL proceso entra a CPU entre los que ya están en listaListos.
   - BuscarSRTF() busca en listaListos el proceso con menor t_RestanteCPU.
   - Este proceso SÍ puede no ser FIFO porque SRTF es una política de preemción.
"""



def ejecutarTodo(puntero_actual: int):
    """
    Ejecuta la simulación del proceso alojado en la partición indicada por
    `puntero_actual` hasta que termine o sea preemptado.

    Comportamiento principal:
    - Asegura que solo un proceso tenga la bandera `CPU` activa.
    - Consume 1 unidad de CPU por iteración, actualiza tiempos globales y
        decrementa `t_RestanteCPU` del proceso.
    - Maneja arribos en tiempo real: si llega un nuevo proceso se invoca
        `Lis.ADMICION_MULTI_5()` para admitirlo y se evalúa apropiación SRTF.
    - Si el proceso finaliza, libera la partición y mueve el proceso a la
        lista de terminados mediante funciones de `Lis`.

    Retorna el nuevo `puntero_actual` si sigue habiendo un proceso activo en
    esa partición, o `None` si el proceso terminó.

    ========================================================================
    RELACIÓN CON FIFO Y REFERENCIAS EN MEMORIA PRINCIPAL
    ========================================================================
    - El proceso ejecutado está alojado en:
      MemoriaPrincipal[puntero_actual]["Proceso_alojado"]
    - Esta es la MISMA referencia (apunta al mismo objeto diccionario) que está
      en listaListos (no es una copia).
    - Cuando modificamos t_RestanteCPU del proceso aquí en ejecutarTodo(),
      ambas listas (listaListos Y MemoriaPrincipal) se actualizan automáticamente.
    - Los cambios se propagan porque es la misma referencia de objeto en memoria.
    - Esto es el corazón de la sincronización: FIFO en admisión, pero referencias
      compartidas para evitar copias inconsistentes.
    """
    banderaMostrarTablas=False
    if puntero_actual is None:
        return None

    proceso = vGlobal.MemoriaPrincipal[puntero_actual]["Proceso_alojado"]
    
    # asegurar unico CPU=True
    for p in vGlobal.listaListos:
        p["CPU"] = (p["id"] == proceso["id"])#si son iguales se pone en true
        Lis.actualizar_proceso_enLista(vGlobal.listaListos,p)
    Lis.actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal,vGlobal.MemoriaPrincipal[puntero_actual])

    while proceso.get("t_RestanteCPU") > 0:

        # ════════════════════════════════════════════════════════════════════════
        # ACTUALIZACIÓN AUTOMÁTICA POR REFERENCIA (FIFO + Memoria Principal)
        # ════════════════════════════════════════════════════════════════════════
        # - proceso apunta a la MISMA referencia en MemoriaPrincipal y listaListos
        # - Re-obtener proceso aquí mantiene sincronía por si hubo modificaciones
        # - Las funciones actualizar_proceso_en* son operaciones defensivas:
        #   aunque muten el mismo objeto, se llaman para asegurar consistencia
        #   y facilitar debugging
        proceso = vGlobal.MemoriaPrincipal[puntero_actual]["Proceso_alojado"]#actualiza el proceso por si hubo cambios volviendo a iterar el while
        Lis.actualizar_proceso_enLista(vGlobal.listaListos,proceso)
        Lis.actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal,vGlobal.MemoriaPrincipal[puntero_actual])

        
        # ════════════════════════════════════════════════════════════════════════
        # CONSUMIR CPU 1 CICLO (FIFO + Planificador Corto Plazo SRTF)
        # ════════════════════════════════════════════════════════════════════════
        # - Decrementamos t_RestanteCPU del proceso actual en CPU.
        # - Esta modificación afecta a AMBAS listas (listaListos Y MemoriaPrincipal)
        #   porque son referencias al mismo diccionario de Python.
        # - En la siguiente iteración del main(), BuscarSRTF() buscará el siguiente
        #   proceso con menor t_RestanteCPU, potencialmente causando preemción SRTF.
        # - Aunque usamos FIFO para admisión, la ejecución es SRTF (no FIFO).
        #print(f"TIEMPO RESTANTE DE EJECUCION sin modificar.....{proceso["t_RestanteCPU"]}")
        proceso["t_RestanteCPU"] -= 1
        #print(f"TIEMPO RESTANTE DE EJECUCION modificado.....{proceso["t_RestanteCPU"]}")
        
        # avanzar tiempo
        vGlobal.T_simulador += 1 
        vGlobal.T_usoCPU_TotalGeneral+= 1 
        
        siguiente = buscarSiguiente()        
        if (siguiente is not None)and(vGlobal.multiprogramacion < 5)and(siguiente.get("t_arribo") == vGlobal.T_simulador):
            banderaMostrarTablas=True
            Lis.ADMICION_MULTI_5()#inrgresar nuevos procesos que arriban en este ciclo antes de mostrar tablas

        # ════════════════════════════════════════════════════════════════════════
        # SUMAR TIEMPO DE ESPERA A LISTOS NO ACTIVOS (FIFO en cola de Listos)
        # ════════════════════════════════════════════════════════════════════════
        # - Recorremos la cola de listos (listaListos) secuencialmente.
        # - Para cada proceso en la cola que NO está en CPU, incrementamos su
        #   tiempo de espera (tiempoTotal_enColaDeListo).
        # - Esto es el núcleo del concepto FIFO: los procesos esperan su turno
        #   en la cola, viendo pasar el tiempo mientras otros procesan.
        # - Aunque SRTF elige el siguiente en CPU (no FIFO), el tiempo de espera
        #   acumula para todos los procesos en listaListos.
        # - Al final, el informe mostrará cuánto tiempo esperó cada proceso en
        #   la cola de listos antes de obtener su turno en CPU.
        for p in vGlobal.listaListos:
            if p["id"] != proceso["id"]:
                p["tiempoTotal_enColaDeListo"] += 1
                Lis.actualizar_proceso_enLista(vGlobal.listaListos,p)
        
        Lis.actualizar_proceso_enLista(vGlobal.listaListos,proceso)#actualizo proceso en lista para mostrar que tiempo restante tiene en las tablas cuando hay una interrupcion
        Lis.actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal,vGlobal.MemoriaPrincipal[puntero_actual])
        if proceso.get("t_RestanteCPU") <1:
            banderaMostrarTablas=True #si el proceso termina en este ciclo, mostrar tablas para ver el cambio de estado a terminado y el siguiente proceso se manda a la CPU
            #MP-->CPU===>Planificador Corto plazo
            Lis.ADMICION_MULTI_5() #por si hay procesos esperando en MSecundaria, ingresarlos a MP
            #SRTF para cambiar al siguiente en prioridad de ejecucion
            nuevo_puntero = Lis.BuscarSRTF()
            
            Lis.desactivarProceso_en_CPU(vGlobal.MemoriaPrincipal, puntero_actual) #desactivamos el proceso QUE TERMINO
            #paranoias de actualizacion
            Lis.actualizar_proceso_enLista(vGlobal.listaListos,proceso)
            #solo sacar al proceso que termino
            print(f"EJECUCION DEL PROCESO  {proceso.get("id")}  TERMINADO EN INSTANTE....{vGlobal.T_simulador}")
            Lis.terminarProcesoAlojado(vGlobal.MemoriaPrincipal,puntero_actual)#desocupar particion en MP
            Lis.mover_aColaTerminados(proceso)# remover de listos para que salga de la memoria principal
            
            if (nuevo_puntero is not None):#procesos esperando para tomar turno
                #si termino en este instante actual, a otro proceso alojado en MP le toca usar el cpu
                proc_nuevo = vGlobal.MemoriaPrincipal[nuevo_puntero]["Proceso_alojado"]
                puntero_actual = nuevo_puntero #actualizo puntero al nuevo proceso a ejecutar 
                print("PLANIFICADOR CORTO PLAZO ACTIVA EL CAMBIO DE CONTEXTO CON SIGUIENTE PROCESO EN PRIORIRDAD DE CPU")
                #paranoias de actualizacion
                Lis.activarProceso_en_CPU(vGlobal.MemoriaPrincipal, puntero_actual)
                Lis.actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal,vGlobal.MemoriaPrincipal[puntero_actual])
                proceso = vGlobal.MemoriaPrincipal[puntero_actual]["Proceso_alojado"]#nuevo proceso a ejecutar en el resto del while
                Lis.actualizar_proceso_enLista(vGlobal.listaListos,proceso)
                # vuelvo a asegurar unico CPU=True
                for p in vGlobal.listaListos:
                    p["CPU"] = (p["id"] == proceso["id"])
                    Lis.actualizar_proceso_enLista(vGlobal.listaListos,p)
            Lis.ADMICION_MULTI_5() #por si hay procesos esperando en MSecundaria, ingresarlos a MP y tambien los procesos nuevos que arriben en este ciclo para mostrar tablas de las 2 cosas al mismo tiempo


        # ════════════════════════════════════════════════════════════════════════
        # ARRIBO CON ADMISIÓN (FIFO de listaProcesos, SRTF para preemción)
        # ════════════════════════════════════════════════════════════════════════
        # - Cuando un nuevo proceso llega (t_arribo <= T_simulador), se invoca
        #   ADMICION_MULTI_5().
        # - ADMICION_MULTI_5() recorre listaProcesos en orden (FIFO del archivo CSV).
        # - Admite procesos en orden: los primeros que caben en MP se van a listaListos,
        #   los que no caben se van a listaSuspendidos (Memory Secundaria).
        # - Después de admitir, se evalúa si hay preemción SRTF:
        #   si un proceso nuevo tiene menor t_RestanteCPU que el actual, lo desplaza.
        #si hay arribo exacto en este ciclo, admitir donde corresponda, acomodar procesos entre MP y MSecundaria y evaluar apropiación
        if (siguiente is not None)and(vGlobal.multiprogramacion < 5)and(siguiente.get("t_arribo") <= vGlobal.T_simulador):
            print(f"INTERRUPCION DE EJECUCION, SO INICIA ADMISION DE PROCESOS NUEVOS")
            banderaMostrarTablas=True
            #MSec >>>> MP >>>>> Planificador Mediano Plazo (CARGAR_MPconMS: traer de suspendidos a listos)
            #nuevos >>>>> MP >>>>> Planificador Largo Plazo (ADMICION_MULTI_5: ingresar nuevos procesos)
            Lis.ADMICION_MULTI_5()           
            nuevo_puntero = Lis.BuscarSRTF() #busco un proceso que cause apropiacion luego de la admision
            if (nuevo_puntero is not None):
                #despues de la admision por interrupcion de arribos, otros procesos habran ocupado los espacios libres, validar apropiacion
                proc_nuevo = vGlobal.MemoriaPrincipal[nuevo_puntero]["Proceso_alojado"]
                if (proc_nuevo.get("id") != proceso.get("id")):
                    # apropiación SRTF solo si TR nuevo < TR actual
                    if proc_nuevo.get("t_RestanteCPU") < proceso.get("t_RestanteCPU"):
                        print(f"=================APROPIACION DE CPU==================")
                        Lis.desactivarProceso_en_CPU(vGlobal.MemoriaPrincipal, puntero_actual) #desactivamos el proceso al que estan apropiando
                        Lis.actualizar_proceso_enLista(vGlobal.listaListos,proceso)
                        puntero_actual = nuevo_puntero
                        print(f"PLANIFICADOR CORTO PLAZO ACTIVA EL PROCESO {proc_nuevo.get("id")} EN CPU POR APROPIACION")
                        Lis.activarProceso_en_CPU(vGlobal.MemoriaPrincipal, puntero_actual)
                        proceso = vGlobal.MemoriaPrincipal[puntero_actual]["Proceso_alojado"]
                        Lis.actualizar_proceso_enLista(vGlobal.listaListos,proceso)
            #si hubo apropiacion o no, asegurar actualizar CPU en listos
            for p in vGlobal.listaListos:
                p["CPU"] = (p["id"] == proceso["id"])
                Lis.actualizar_proceso_enLista(vGlobal.listaListos,p)

        if banderaMostrarTablas==True:
            banderaMostrarTablas=False
            Lis.solo_mostrarTablas() #muestra la admision y posible apropiacion
            print(f"INTERRUPCION DE EJECUCION, SO FINALIZA ADMISION DE PROCESOS NUEVOS")
            print(f"Presione una tecla para continuar...")
            Lis.msvcrt.getch()  # espera cualquier tecla
            MA.limpiar_pantalla()
        

        proceso = vGlobal.MemoriaPrincipal[puntero_actual]["Proceso_alojado"]
        Lis.actualizar_proceso_enLista(vGlobal.listaListos,proceso)
    #el proceso no se borra de la particion si termina, solo se sobreescribe cuando otro proceso lo ocupa
    if (proceso.get("t_RestanteCPU") > 0):
        # siguen las ejecuciones
        return puntero_actual
    else:
        # termino y no hay proceso activo en esa partición
        return None
        

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

def main():
    """
    Loop principal del simulador:

    - Repite hasta que la cantidad de procesos terminados iguale la cantidad
        total de procesos cargados.
    - En cada iteración usa `buscarSiguiente()` para detectar arribos futuros
        o procesos pendientes.
    - Controla ciclos ociosos (`Lis.CiclosOciosos`), admisiones
        (`Lis.ADMICION_MULTI_5`) y selección del proceso a ejecutar (`Lis.BuscarSRTF`).
    - Activa el proceso seleccionado en CPU y delega la ejecución a
        `ejecutarTodo()`.
    """
    while len(vGlobal.listaTerminados) < len(vGlobal.listaProcesos):
        siguiente = buscarSiguiente()
        if siguiente is not None:
            Lis.CiclosOciosos(siguiente)
            if (vGlobal.T_simulador == siguiente["t_arribo"]):#hay que mostrar tablas
                #print(f"INTERRUPCION DE EJECUCION, SO INICIA ADMISION DE PROCESOS NUEVOS")
                Lis.ADMICION_MULTI_5()#control de multiprogramacion y manejo de admisiones
                Lis.solo_mostrarTablas() #muestra la admision
                print(f"INTERRUPCION DE EJECUCION, SO FINALIZA ADMISION DE PROCESOS NUEVOS")
                print(f"Presione una tecla para continuar ... ")
                Lis.msvcrt.getch() # espera cualquier tecla
                MA.limpiar_pantalla()     
        
        # Buscar proceso a ejecutar
        puntero = Lis.BuscarSRTF()
        
        # Si no hay proceso en CPU
        if puntero is None:
            siguiente = buscarSiguiente()
            # Si hay procesos pendientes/futuros pero sin listos
            if siguiente is not None:
                continue  # ← REINICIA EL LOOP para buscar ingresar mas programas
            else:
                # No hay más procesos -> salir
                break
        
        # Activar proceso en CPU
        print("PLANIFICADOR CORTO PLAZO ACTIVA EL PROCESO EN CPU")
        Lis.activarProceso_en_CPU(vGlobal.MemoriaPrincipal, puntero)
        
        # Ejecutar proceso
        puntero_ejecutado = ejecutarTodo(puntero)
        if puntero_ejecutado is None:
            # Proceso termino, reiniciar bucle para buscar otro proceso
            continue

            
            


#Inicializamos variables

sys.path.append('..')
vGlobal.T_simulador=0
vGlobal.T_usoCPU_TotalGeneral=0
vGlobal.T_CPU_ocioso=0
vGlobal.multiprogramacion=0
vGlobal.aux=None
archivo = FunArchivos.elegir_archivo()
vGlobal.listaProcesos=FunArchivos.leer_procesos(archivo)

while vGlobal.listaProcesos==False:
    archivo=None
    vGlobal.listaProcesos=None
    print("POR FAVOR ELIJA CARGAR OTRO ARCHIVO .CSV. EL INGRESADO NO CONTIENE PROCESOS VALIDOS PARA ESTE SIMULADOR ")
    print(f"Presione una tecla para continuar...")
    Lis.msvcrt.getch()  # espera cualquier tecla
    MA.limpiar_pantalla()
    archivo = FunArchivos.elegir_archivo()
    vGlobal.listaProcesos=FunArchivos.leer_procesos(archivo)
vGlobal.cantTotalProcesos= (len(vGlobal.listaProcesos))
#ejecuta el simulador
print("=========EL SIMULADOR INICIA=========")
main()
MA.limpiar_pantalla()
Lis.informe_final()
print(f"Simulación finalizada usando el archivo: {archivo.resolve()}")
print("cierre el simulador para volver a ejecutar otro archivo")
input("Presione ENTER para cerrar...")