

import sys
import os
from tkinter.ttk import Style
from typing import List, Dict, Optional, Text
import msvcrt #para pausar pantalla
from rich.console import Console
from rich.table import Table

"""
Módulo: funcionesLisandro_prolijo

Este módulo contiene las funciones principales que actúan como columna vertebral
del simulador: gestión de listas de procesos (nuevos, listos, suspendidos, terminados),
admisión a memoria principal y secundaria, asignación de particiones (BestFit),
operaciones sobre la CPU (activar/desactivar/terminar procesos) y la impresión
de tablas de estado con la librería rich. Las funciones aquí modulan el flujo
de admisión, planificación a corto plazo (SRTF) y la recolección de métricas
de rendimiento al final de la simulación.

Notas:
- Las estructuras principales están en `paquetes.estado_global` (vGlobal).
- Muchas funciones actualizan objetos por referencia (dicts en listas y memoria),
  por lo que se compara por `id` cuando corresponde.
"""

# Asegurar que los imports locales funcionen
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# imports relativos
import paquetes.estado_global as vGlobal
from paquetes.AgustinVeron.Menu import gotoxy as desplazarTabla, limpiar_pantalla
import paquetes.LisandroRojas.funcionesconlistas_isabel_arregladoLisandro as FunArchivos

###############################
# este modulo fue reorganizado para mejorar la claridad y evitar confusiones con referencias
# las funciones ahora usan actualizaciones por referencia y helpers para mantener la integridad de los datos
# las funciones de mostrar tablas se agruparon al final para mejor lectura del flujo lógico 
# las funciones de manipulación de memoria y CPU también se agruparon al final
###############################



#este modulo fue reorganizado y mejor comentado con ayuda del chat con copilot de visual estudio code en base al modulo funcionesLisandro.py en el cual no se uso ninguna ia
'''Cambios y correcciones principales (resumen):

Correcciones de sintaxis: f-strings problemáticos (comillas anidadas) y condiciones lógicas erróneas (ej. len(lista) < 0 → se cambió a verificación adecuada).
Organización de imports: agrupados, tipado añadido y path handling seguro (añade parent_dir solo si hace falta).
Docstrings en todas las funciones principales para facilitar lectura y mantenimiento.
Eliminé código viejo comentado y ejemplos redundantes (mantengo solo lo esencial).
Mejor manejo de iteraciones que modifican listas: uso de list(...) al iterar cuando se modifica la lista y uso de comprehensions para filtrar.
Corrección lógica en BuscarSRTF: ahora retorna None cuando no hay listos y la comprobación de menor TR es correcta.
Mensajes y prints simplificados para no romper el flujo; se mantienen llamadas a funciones de UI (msvcrt.getch, limpiar_pantalla) tal como en original.
Breve explicación sobre referencias vs copias (para que lo tengas como guía):

Dicts y listas son mutables. Si haces d = lista[i] y después d['x']=1, lista[i]['x'] cambia también.
Para copiar: usar import copy; copy.copy(obj) (superficial) o copy.deepcopy(obj) (profunda).
Si quieres "mover" un diccionario de una lista a otra manteniendo la referencia (que las modificaciones sean visibles desde ambas listas), no lo copies; añade el mismo dict (ej. otra_lista.append(original_dict)).
Si necesitas un snapshot independiente para mostrar o procesar sin afectar el original, usa deepcopy.
Para actualizar un elemento en la lista de forma segura busca por id e usa lista[idx].update(nuevo_dict) en vez de reemplazar por copia accidental.
'''

# -------------------
# Helpers / documentación breve sobre referencias
# -------------------
# Nota rápida para el aprendizaje:
# - Las listas y diccionarios en Python son mutables y se pasan por referencia.
#   Si haces `a = lista[idx]` y modificas `a['campo'] = x`, la lista original cambia.
# - Para crear copias independientes usa copy.copy(obj) (copia superficial)
#   o copy.deepcopy(obj) (copia profunda) si hay estructuras anidadas.
# - Para actualizar un diccionario dentro de una lista, actualizar el diccionario
#   muta el elemento original; si quieres reemplazar el elemento en la lista,
#   usa lista[idx] = nuevo_dict o lista.pop(idx); lista.insert(idx, nuevo_dict).
# Esto evita confusiones entre "referencia" y "copia" al manejar procesos.
# -------------------


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
        avanzar = t_arribo - vGlobal.T_simulador
        vGlobal.T_CPU_ocioso += avanzar
        vGlobal.T_simulador = t_arribo


def actualizar_estado_Proceso(proceso: Dict) -> Optional[str]:
    """
    Devuelve una cadena con el estado actual del proceso según las listas.
    """
    pid = proceso.get("id")
    if any(p.get("id") == pid and p.get("CPU") for p in vGlobal.listaListos):
        return "EN EJECUCION"
    if any(p.get("id") == pid for p in vGlobal.listaListos):
        return "LISTO"
    if any(p.get("id") == pid for p in vGlobal.listaSuspendidos):
        return "LISTO/SUSPENDIDO"
    if any(p.get("id") == pid for p in vGlobal.listaTerminados):
        return "TERMINADO"
    if any(p.get("id") == pid for p in vGlobal.listaProcesos):
        return "NUEVO"
    return None


def actualizar_proceso_enLista(lista: List, proceso_actualizado: Dict) -> bool:
    """
    Actualiza el diccionario de un proceso dentro de una lista (por id).
    Retorna True si lo actualizó, False si no lo encontró.

    ════════════════════════════════════════════════════════════════════════
    RELACIÓN CON REFERENCIAS Y FIFO
    ════════════════════════════════════════════════════════════════════════
    - En Python, dicts y listas son mutables y se pasan por referencia.
    - Esta función busca un proceso por 'id' dentro de 'lista' (puede ser
      listaListos, listaSuspendidos, listaTerminados, etc.).
    - Usa .update() para mutar el dict existente, no para reemplazarlo.
    - Esto es importante: si ese proceso también está en MemoriaPrincipal
      (como referencia), la mutación se propaga automáticamente.
    
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


def actualizar_proceso_enMemoriaPrincipal(lista: List, particion_actualizada: Dict) -> bool:
    """
    Actualiza los campos de una partición en MemoriaPrincipal (por Particion).

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


def marcar_procesoNuevo_Ingresado(procesoNuevo: Dict):
    """
    Marca en listaProcesos que el proceso ya fue ingresado (bandera_baja_logica).
    """
    for p in vGlobal.listaProcesos:
        if p.get("id") == procesoNuevo.get("id") and p.get("bandera_baja_logica") is False:
            p["bandera_baja_logica"] = True
            break


def mover_aColaSuspendido(proceso_actual: Dict):
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


def mover_aColaListo(proceso_actual: Dict):
    """
    Construye el dict para la cola de listos y lo inserta (o actualiza si existe).
    Guarda una referencia temporal en vGlobal.aux para la admisión BestFit.

    ════════════════════════════════════════════════════════════════════════
    CONCEPTO FIFO EN ESTA FUNCIÓN
    ════════════════════════════════════════════════════════════════════════
    - Cuando un proceso es admitido a Memoria Principal, entra a listaListos.
    - listaListos es una cola FIFO de procesos que están listos para ejecutarse.
    - El nuevo proceso se AÑADE AL FINAL de listaListos (append).
    - Aunque SRTF seleccionará el siguiente en CPU (no necesariamente el primero),
      la orden FIFO garantiza que los procesos se admiten en el orden correcto.
    - vGlobal.aux guarda una referencia al proceso recién admitido para que
      cargarProcesoAlojado() lo coloque en una partición de MemoriaPrincipal.
    - Este dict en listaListos es la MISMA REFERENCIA que estará en
      MemoriaPrincipal[particion]["Proceso_alojado"], permitiendo actualizaciones
      automáticas cuando se modifiquen campos como t_RestanteCPU.
    """
    marcar_procesoNuevo_Ingresado(proceso_actual)
    tiempoArriboMemPrincipal = vGlobal.T_simulador
    cargarTiempoRespuesta = int(proceso_actual.get("t_Respuesta", vGlobal.T_simulador - proceso_actual.get("t_arribo", vGlobal.T_simulador)))
    cargarTiempoIngreso = int(proceso_actual.get("t_ingreso", vGlobal.T_simulador))
    t_Restante = int(proceso_actual.get("t_RestanteCPU", proceso_actual.get("t_irrupcion", 0)))
    if "tiempoTotal_enColaDeListo" not in proceso_actual:
        tiempoTotal_enColaDeListo=0 #recien entra a listo
    else:
        tiempoTotal_enColaDeListo=proceso_actual.get("tiempoTotal_enColaDeListo")#actualiza el tiempo ante cualquier interrupcion con un nuevo valor cargado desde la variable en el argumento
    proceso_listo = {
        "id": proceso_actual.get("id"),
        "t_arribo": proceso_actual.get("t_arribo"),
        "tamaño": proceso_actual.get("tamaño"),
        "t_arribo_MP": tiempoArriboMemPrincipal,
        "t_irrupcion": proceso_actual.get("t_irrupcion"),
        "t_Respuesta": cargarTiempoRespuesta,
        "t_ingreso": cargarTiempoIngreso,
        "t_RestanteCPU": t_Restante,
        "tiempoTotal_enColaDeListo": tiempoTotal_enColaDeListo,
        "CPU": False,
    }
    if not actualizar_proceso_enLista(vGlobal.listaListos, proceso_listo):
        vGlobal.listaListos.append(proceso_listo)
    vGlobal.aux = proceso_listo


# ---------- Tablas con rich ----------
def mostrarColaListos():
    """
    Muestra la cola de procesos 'Listos' que se encuentran en Memoria Principal.
    Presenta columnas relevantes (ID, arribo, tamaño, tiempo restante, etc.)
    y marca con 'CPU' aquellos procesos que están ejecutándose.

    ════════════════════════════════════════════════════════════════════════
    FIFO EN ESTA FUNCIÓN
    ════════════════════════════════════════════════════════════════════════
    - Esta tabla muestra los procesos en listaListos en el ORDEN que aparecen.
    - La ORDEN es importante porque representa el ORDEN FIFO de admisión.
    - Los procesos que aparecen primero fueron admitidos primero.
    - El campo "tiempoTotal_enColaDeListo" acumula cuánto tiempo esperó cada
      proceso en esta cola FIFO antes de obtener su turno en CPU.
    - Aunque la CPU la usa SRTF (el que menos tiempo restante), todos pasan
      por esta cola FIFO.
    """
    console = Console()
    table = Table(title="Procesos en memoria Principal --> Estado: 'Listo'", show_lines=True)
    cols = [
        ("ID Proceso", "yellow"),
        ("Tiempo Arribo", None),
        ("Tamaño", None),
        ("Tiempo Arribo a MP", None),
        ("Tiempo Irrupcion", None),
        ("Tiempo de Respuesta", None),
        ("Tiempo de Ingreso", None),
        ("Tiempo Restante de CPU", None),
        ("Tiempo de Total en Cola de Listos", None),
    ]
    for name, style in cols:
        table.add_column(name, justify="right", style=style or "", no_wrap=False)

    if vGlobal.listaListos:
        for p in vGlobal.listaListos:
            if not p.get("CPU"):
                table.add_row(
                    str(p.get("id", "xxx")),
                    str(p.get("t_arribo", "xxx")),
                    str(p.get("tamaño", "xxx")),
                    str(p.get("t_arribo_MP", "xxx")),
                    str(p.get("t_irrupcion", "xxx")),
                    str(p.get("t_Respuesta", "xxx")),
                    str(p.get("t_ingreso", "xxx")),
                    str(p.get("t_RestanteCPU", "xxx")),
                    str(p.get("tiempoTotal_enColaDeListo", "xxx")),
                )
        # si todos están en CPU (caso extremo) mostramos fila vacía de marcador
        if all(p.get("CPU") for p in vGlobal.listaListos):
            table.add_row(*["xxx"] * len(cols))
    else:
        table.add_row(*["xxx"] * len(cols))
    console.print(table)


def mostrarColaSuspendido():
    """
    Muestra la cola de procesos que están en memoria secundaria (suspendidos
    pero listos para ingreso). Incluye tiempos y tamaño para ayudar en la
    decisión de admisión/BestFit.

    ════════════════════════════════════════════════════════════════════════
    FIFO EN MEMORIA SECUNDARIA
    ════════════════════════════════════════════════════════════════════════
    - listaSuspendidos es una cola FIFO de procesos que NO caben en MP.
    - El orden mostrado aquí es el orden FIFO: los primeros fueron los primeros
      en ser rechazados por falta de espacio en MP.
    - Cuando libera espacio en MP, CARGAR_MPconMS() recorre esta cola en orden
      y promueve los primeros procesos de vuelta a listaListos.
    - La orden FIFO garantiza equidad: nadie espera indefinidamente en MS.
    """
    console = Console()
    table = Table(title="Procesos en memoria Secundaria --> Estado: 'Listo y Suspendido'", show_lines=True)
    headers = ["ID Proceso", "Tiempo Arribo", "Tamaño", "Tiempo Irrupcion", "Tiempo de Respuesta", "Tiempo de Ingreso", "Tiempo Restante de CPU"]
    for h in headers:
        table.add_column(h, justify="right")
    if vGlobal.listaSuspendidos:
        for p in vGlobal.listaSuspendidos:
            table.add_row(*(str(p.get(k, "xxx")) for k in ["id", "t_arribo", "tamaño", "t_irrupcion", "t_Respuesta", "t_ingreso", "t_RestanteCPU"]))
    else:
        table.add_row(*["xxx"] * len(headers))
    console.print(table)


def mover_aColaTerminados(proceso_actual: Dict):
    """
    Mueve un proceso a la lista de terminados y actualiza la memoria y las tablas.
    """
    actualizar_proceso_enLista(vGlobal.listaListos, proceso_actual)
    total_Retorno = vGlobal.T_simulador - proceso_actual.get("t_arribo_MP", vGlobal.T_simulador)
    instante_Retorno = vGlobal.T_simulador
    proceso_Terminado = {
        "id": proceso_actual.get("id"),
        "t_arribo": proceso_actual.get("t_arribo"),
        "tamaño": proceso_actual.get("tamaño"),
        "t_arribo_MP": proceso_actual.get("t_arribo_MP"),
        "t_irrupcion": proceso_actual.get("t_irrupcion"),
        "t_Respuesta": proceso_actual.get("t_Respuesta"),
        "t_Retorno": instante_Retorno,
        "total_Retorno": total_Retorno,
        "t_ingreso": proceso_actual.get("t_ingreso"),
        "tiempoTotal_enColaDeListo": (proceso_actual.get("tiempoTotal_enColaDeListo"))
    }
    if not actualizar_proceso_enLista(vGlobal.listaTerminados, proceso_Terminado):
        vGlobal.listaTerminados.append(proceso_Terminado)
    eliminarDeLista(vGlobal.listaListos, proceso_Terminado)
    #mostrarTablaTerminados()


def mostrarTablaTerminados():
    """
    Muestra una tabla con los procesos que ya terminaron, incluyendo tiempos
    de retorno y métricas acumuladas relevantes para el informe final.
    """
    console = Console()
    headers = [
        "ID Proceso", "Tiempo Arribo", "Tamaño", "Tiempo Arribo a MP", "Tiempo Irrupcion",
        "Tiempo de Ingreso", "Tiempo de Respuesta", "Instante de Retorno",
        "Tiempo transcurrido hasta el Retorno", "Tiempo Total en Cola de Listos"
    ]
    table = Table(title="Procesos Terminados --> Estado: 'Terminado'", show_lines=True)
    for h in headers:
        table.add_column(h, justify="center")
    if vGlobal.listaTerminados:
        for p in vGlobal.listaTerminados:
            table.add_row(*(str(p.get(k, "xxx")) for k in ["id", "t_arribo", "tamaño", "t_arribo_MP", "t_irrupcion", "t_ingreso", "t_Respuesta", "t_Retorno", "total_Retorno", "tiempoTotal_enColaDeListo"]))
    else:
        table.add_row(*["xxx"] * len(headers))
    console.print(table)


# ---------- Memoria y CPU ----------
def cargarProcesoAlojado(memoria: List, puntero: int, proceso_actual: Dict):
    """
    Asigna por referencia el dict del proceso a la partición seleccionada.
    """
    particion = memoria[puntero]
    particion["Proceso_alojado"] = proceso_actual
    particion["Fragmentacion_Interna"] = int(particion["TamañoTotal"] - proceso_actual.get("tamaño", 0))
    particion["Ocupado"] = True
    actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal, particion)


def activarProceso_en_CPU(memoria: List, puntero: int):
    """
    Marca el proceso alojado en la partición `puntero` como el que está usando
    la CPU. Actualiza la bandera `CPU` en `listaListos` para mantener una sola
    referencia activa y sincroniza la Memoria Principal.
    """
    proceso = memoria[puntero]["Proceso_alojado"]
    particion = memoria[puntero]
    proceso["CPU"] = True
    for p in vGlobal.listaListos:
        p["CPU"] = (p.get("id") == proceso.get("id"))
    actualizar_proceso_enLista(vGlobal.listaListos, proceso)
    actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal, particion)


def desactivarProceso_en_CPU(memoria: List, puntero: int):
    """
    Desactiva la bandera `CPU` para el proceso alojado en la partición `puntero`.
    Mantiene la partición marcada como ocupada hasta que sea liberada por
    `terminarProcesoAlojado` y sincroniza las estructuras.
    """
    proceso = memoria[puntero]["Proceso_alojado"]
    particion = memoria[puntero]
    proceso["CPU"] = False
    particion["Ocupado"] = True
    actualizar_proceso_enLista(vGlobal.listaListos, proceso)
    actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal, particion)


def terminarProcesoAlojado(memoria: List, puntero: int):
    """
    Libera la partición sin borrar el registro.
    """
    particion = memoria[puntero]
    particion["Ocupado"] = False
    actualizar_proceso_enMemoriaPrincipal(vGlobal.MemoriaPrincipal, particion)


def mostrarMemoriaPrincipal():
    """
    Imprime el estado actual de la Memoria Principal (particiones):
    contenido, fragmentación interna y disponibilidad. Muestra la partición
    del SO y las particiones de usuario.
    """
    console = Console()
    table = Table(title="Memoria Principal", show_lines=True)
    headers = ["Particion", "Tamaño Total", "Direccion inicio", "Tipo particion", "Proceso alojado", "Fragmentacion_Interna", "Ocupado"]
    for h in headers:
        table.add_column(h, justify="right")
    # mostrar SO primero
    particion_SO = vGlobal.MemoriaPrincipal[3]
    table.add_row(str(particion_SO["Particion"]), str(particion_SO["TamañoTotal"]), str(particion_SO["Dir_Comienzo"]), str(particion_SO["Dueño"]), "SO", str(particion_SO["Fragmentacion_Interna"]), "NO DISPONIBLE")
    for p in vGlobal.MemoriaPrincipal[:3]:
        ocupado_str = "NO DISPONIBLE" if p.get("Ocupado") else "DISPONIBLE"
        proc_alojado = p.get("Proceso_alojado", {})
        if proc_alojado:
            proc_id = proc_alojado.get("id", "Ninguno")
            table.add_row(str(p["Particion"]), str(p["TamañoTotal"]), str(p["Dir_Comienzo"]), str(p["Dueño"]), str(proc_id), str(p["Fragmentacion_Interna"]), ocupado_str)
        else:
            table.add_row(str(p["Particion"]), str(p["TamañoTotal"]), str(p["Dir_Comienzo"]), str(p["Dueño"]), "LIBRE", str(p["Fragmentacion_Interna"]), ocupado_str)
    console.print(table)


def mostrarProcesoCPU():
    """
    Muestra el proceso que actualmente está utilizando la CPU (si existe),
    incluyendo tamaño, partición y tiempo restante.
    """
    console = Console()
    table = Table(title="Proceso utilizando CPU --> Estado: 'En Ejecucion'", show_lines=True)
    for h in ["ID Proceso", "Tamaño", "Particion", "Tiempo Restante de CPU"]:
        table.add_column(h, justify="right")
    procesoEncontrado = False
    particion_en_uso = None
    for p in vGlobal.MemoriaPrincipal[:3]:
        if p.get("Proceso_alojado") and p["Proceso_alojado"].get("CPU"):
            procesoEncontrado = True
            particion_en_uso = p
            break
    if procesoEncontrado:
        for proc in vGlobal.listaListos:
            if proc.get("CPU"):
                table.add_row(str(proc.get("id")), str(proc.get("tamaño")), str(particion_en_uso.get("Particion")), str(proc.get("t_RestanteCPU")))
    else:
        table.add_row("xxx", "xxx", "xxx", "xxx")
    console.print(table)


def solo_mostrarTablas():
    """
    Imprime en consola todas las tablas de estado para el instante actual del
    simulador: lista de procesos, memoria, proceso en CPU, colas de listos y
    suspendidos. Se usa para interrupciones y pasos de depuración.
    """
    print(f"INSTANTE ACTUAL DEL SIMULADOR:>>>>>>>>>> {vGlobal.T_simulador} <<<<<<<<<<")
    print(f"MULTIPROGRAMACION:>>>>>>>>>> {vGlobal.multiprogramacion} <<<<<<<<<<")
    print("=" * 120)
    FunArchivos.mostrar_tabla(vGlobal.listaProcesos)
    print("=" * 120)
    mostrarMemoriaPrincipal()
    print("=" * 120)
    mostrarProcesoCPU()
    print("=" * 120)
    mostrarColaListos()
    print("=" * 120)
    mostrarColaSuspendido()
    print("=" * 120)
    #mostrarTablaTerminados()
    print(f"INSTANTE ACTUAL DEL SIMULADOR:>>>>>>>>>> {vGlobal.T_simulador} <<<<<<<<<<")
    print(f"MULTIPROGRAMACION:>>>>>>>>>> {vGlobal.multiprogramacion} <<<<<<<<<<")


def informe_final():
    console = Console()
    total_sim = vGlobal.T_simulador or 0
    rendimiento = (len(vGlobal.listaTerminados) / total_sim ) if total_sim > 0 else 0
    CPUociso_porcentaje = (vGlobal.T_CPU_ocioso / total_sim * 100) if total_sim > 0 else 0
    usoCPU_porcentaje = (vGlobal.T_usoCPU_TotalGeneral / total_sim * 100) if total_sim > 0 else 0

    promedioT_Espera = sum(p.get("tiempoTotal_enColaDeListo", 0) for p in vGlobal.listaTerminados) / max(1, vGlobal.cantTotalProcesos)
    promRetorno = sum(p.get("total_Retorno", 0) for p in vGlobal.listaTerminados) / max(1, vGlobal.cantTotalProcesos)

    table = Table(title="Informe de Rendimiento del simulador", show_lines=True)
    
    headers = ["Tiempo total de CPU ocioso", "Porcentaje CPU ocioso", "Tiempo de simulador", "Tiempo total de CPU utilizado", "uso de CPU%", "Rendimiento", "T.Espera Promedio", "T.Retorno Promedio"]
    for h in headers:
        table.add_column(h, justify="center")
    from rich.text import Text
    table.add_row(
        str(vGlobal.T_CPU_ocioso),
        f"{CPUociso_porcentaje:.2f} %",
        str(vGlobal.T_simulador),
        str(vGlobal.T_usoCPU_TotalGeneral),
        f"{usoCPU_porcentaje:.2f} %",
        f"{rendimiento:.4f} procesos/unidad de tiempo",
        Text(f"{promedioT_Espera:.2f}", style="yellow"),
        Text(f"{promRetorno:.2f}", style="yellow")
    )
    console.print(table)
    mostrarTablaTerminados()


def cabeEnAlgunaParticionLIBRE(procesoAct: Dict) -> bool:
    """
    Devuelve True si existe al menos una partición libre con tamaño suficiente.
    """
    for l in vGlobal.MemoriaPrincipal:
        if not l.get("Ocupado") and l.get("TamañoTotal", 0) >= procesoAct.get("tamaño", 0) and l.get("Dueño") != "SO":
            return True
    return False


def BestFitCICLO_ADMICION(ProcActual: Dict) -> Optional[int]:
    """
    Busca la partición con menor fragmentación interna donde quepa el proceso.
    Retorna el índice de la partición o None si no cabe.
    """
    menorFragmentacionInt = float("inf")
    posicionAsignada = None
    for i, particion in enumerate(vGlobal.MemoriaPrincipal):
        if not particion.get("Ocupado") and particion.get("Dueño") != "SO":
            frag = particion.get("TamañoTotal", 0) - ProcActual.get("tamaño", 0)
            if frag >= 0 and frag < menorFragmentacionInt:
                menorFragmentacionInt = frag
                posicionAsignada = i
    return posicionAsignada


def SuspendidosYListos():
    """
    Elimina de suspendidos los procesos que ya están en la lista de listos.
    """
    ids_listos = {p.get("id") for p in vGlobal.listaListos}
    vGlobal.listaSuspendidos[:] = [p for p in vGlobal.listaSuspendidos if p.get("id") not in ids_listos]


def eliminarDeLista(lista: List, proceso: Dict) -> bool:
    """
    Elimina el primer elemento que coincida por id en la lista.
    """
    for i, p in enumerate(lista):
        if p.get("id") == proceso.get("id"):
            lista.pop(i)
            return True
    return False



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
            break
    vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)