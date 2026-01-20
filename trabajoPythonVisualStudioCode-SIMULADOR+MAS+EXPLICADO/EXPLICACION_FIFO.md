# CONCEPTO FIFO (First In-First Out) EN EL SIMULADOR

## Resumen Ejecutivo

Este simulador usa una **estrategia FIFO para ADMISIÓN de procesos** (cuándo y en qué orden ingresan a memoria), pero utiliza **SRTF (Shortest Remaining Time First) para PLANIFICACIÓN de CPU** (cuál proceso entra a ejecutarse).

---

## 1. FLUJO GENERAL DE FIFO

```
┌─────────────────────────────────────────────────────────────────┐
│ listaProcesos (del archivo CSV) - FIFO de origen               │
│ Se recorre secuencialmente en ADMICION_MULTI_5()                │
└────────────────┬────────────────────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │ ¿Cabe en MP?    │
        └────────┬────────┘
           ╱      ╲
        SÍ╱        ╲NO
         ╱          ╲
        ╱            ╲
   ┌───▼───┐      ┌──▼──────────┐
   │Listos │      │Suspendidos  │
   │(MP)   │      │(MS)         │
   └───────┘      └─────────────┘
      FIFO           (espera FIFO)
                     cuando haya
                     espacio en MP
```

---

## 2. ESTRUCTURA DE DATOS Y REFERENCIAS

### 2.1. listaListos (Cola FIFO en Memoria Principal)
- **Es una lista Python** que mantiene procesos en **orden FIFO**.
- Cada elemento es un **diccionario del proceso**.
- **Máximo 3 procesos** simultáneamente en MP.

### 2.2. MemoriaPrincipal (Particiones)
- **Es una lista de 4 particiones** (3 de usuario + 1 del SO).
- Cada partición tiene un campo `"Proceso_alojado": {}`
- Este dict `Proceso_alojado` es la **MISMA REFERENCIA** que está en `listaListos`.

### 2.3. El Puente: Referencias Compartidas
```python
# Cuando se admite un proceso:
mover_aColaListo(proceso)  # → agrega a listaListos
vGlobal.aux = proceso_listo  # guarda referencia

# Luego:
cargarProcesoAlojado(MP, puntero, vGlobal.aux)
# → MP[puntero]["Proceso_alojado"] = vGlobal.aux
#   (MISMA referencia, no una copia)

# Resultado:
listaListos[i] y MP[j]["Proceso_alojado"] 
apuntan al MISMO diccionario en memoria

# Por eso:
listaListos[i]["t_RestanteCPU"] -= 1
# TAMBIÉN actualiza:
MP[j]["Proceso_alojado"]["t_RestanteCPU"]
```

---

## 3. FIFO EN ADMISIÓN (Planificador a Largo Plazo)

### Algoritmo en ADMICION_MULTI_5():

```python
# 1. Primero, traer suspendidos a listos (FIFO)
CARGAR_MPconMS()  # recorre listaSuspendidos en orden

# 2. Luego, admitir nuevos procesos (FIFO de listaProcesos)
for proceso in listaProcesos:
    if not admitido and llegó:
        if cabe en MP:
            mover_aColaListo(proceso)  # añade al final (FIFO)
        else:
            mover_aColaSuspendido(proceso)  # espera en MS
```

### Características FIFO:
- Los **primeros procesos** que arriban y **caben en MP** entran primero.
- Los que **no caben** esperan en `listaSuspendidos` (MS).
- Cuando libera espacio, trae a los **primeros suspendidos** (FIFO).
- **Garantía de equidad**: nadie espera indefinidamente.

---

## 4. FIFO EN MEMORIA Y GESTIÓN DE PARTICIONES

### 4.1. Inserción en listaListos (FIFO append)
```python
# En mover_aColaListo():
proceso_listo = {...}
if not actualizar_proceso_enLista(vGlobal.listaListos, proceso_listo):
    vGlobal.listaListos.append(proceso_listo)  # ← FIFO: se añade al final
```

### 4.2. Relación con MemoriaPrincipal
```python
# El proceso está en:
# - listaListos[i]: la cola FIFO de listos
# - MP[j]["Proceso_alojado"]: la partición j

# Son la MISMA referencia:
listaListos[i] is MP[j]["Proceso_alojado"]  # True

# Cambios se sincronizan automáticamente:
listaListos[i]["t_RestanteCPU"] = 5
print(MP[j]["Proceso_alojado"]["t_RestanteCPU"])  # imprime 5
```

### 4.3. Actualización de referencias
```python
# actualizar_proceso_enLista() muta el dict existente:
def actualizar_proceso_enLista(lista, proceso_actualizado):
    for p in lista:
        if p.get("id") == proceso_actualizado.get("id"):
            p.update(proceso_actualizado)  # muta el mismo dict
            return True
    return False

# Esto asegura que MP también se actualice automáticamente
```

---

## 5. FIFO vs SRTF: Diferencia Crucial

| Aspecto | FIFO (Admisión) | SRTF (CPU) |
|---------|-----------------|-----------|
| **¿Qué controla?** | Cuándo y en qué orden ingresan a MP | Cuál entra a ejecutarse en CPU |
| **¿Dónde actúa?** | ADMICION_MULTI_5() | BuscarSRTF() |
| **¿Respeta orden?** | Sí, ordena por llegada | No, elige el de menor t_RestanteCPU |
| **¿Puede haber preemción?** | No (admisión es determinística) | Sí (SRTF reemplaza si llega uno con TR < TR actual) |

### Ejemplo:
```
Tiempo 0: Llega P1 (TR=10), P2 (TR=5)
         Admisión FIFO: P1 entra a MP primero, P2 después
         
         CPU (SRTF): P2 entra a CPU porque TR=5 < TR=10
         
Tiempo 5: P2 termina, P1 continúa (ya estaba en CPU)
```

---

## 6. RECORRIDO DE LISTAS CON FIFO

### 6.1. En buscarSiguiente() (Detectar arribos)
```python
def buscarSiguiente():
    # Recorre listaProcesos EN ORDEN (FIFO del CSV)
    for p in vGlobal.listaProcesos:
        if (p.get("bandera_baja_logica") is False) and (p.get("t_arribo") <= vGlobal.T_simulador):
            return p  # retorna el PRIMERO encontrado (FIFO)
```

### 6.2. En ADMICION_MULTI_5() (Admitir procesos)
```python
# Recorre listaProcesos EN ORDEN (FIFO)
for proceso in vGlobal.listaProcesos:
    if proceso.get("bandera_baja_logica") is False and proceso.get("t_arribo") <= vGlobal.T_simulador:
        if len(vGlobal.listaListos) < 3 and cabeEnAlgunaParticionLIBRE(proceso):
            mover_aColaListo(proceso)  # añade FIFO al final
        else:
            mover_aColaSuspendido(proceso)  # espera en MS
```

### 6.3. En CARGAR_MPconMS() (Traer de MS a MP)
```python
# Recorre listaSuspendidos EN ORDEN (FIFO)
while len(vGlobal.listaListos) < 3:
    for ingresa in list(vGlobal.listaSuspendidos):  # orden FIFO
        if cabeEnAlgunaParticionLIBRE(ingresa):
            mover_aColaListo(ingresa)
            puntero = BestFitCICLO_ADMICION(vGlobal.aux)
            if puntero is not None:
                cargarProcesoAlojado(...)
```

---

## 7. CAMPOS QUE RASTREAN FIFO

### 7.1. tiempoTotal_enColaDeListo
```python
# En ejecutarTodo(), cada ciclo:
for p in vGlobal.listaListos:
    if p["id"] != proceso["id"]:
        p["tiempoTotal_enColaDeListo"] += 1  # acumula tiempo en cola FIFO
```
- **¿Qué mide?**: Cuánto tiempo esperó cada proceso en la cola FIFO.
- **¿Por qué importante?**: Indica la "justicia" del planificador.

### 7.2. t_arribo_MP
```python
# Registra cuándo entró el proceso a MP (en listaListos)
"t_arribo_MP": tiempoArriboMemPrincipal  # = vGlobal.T_simulador cuando entra
```
- Permite rastrear cuándo pasó de MS a MP.

### 7.3. bandera_baja_logica
```python
# En listaProcesos, marca si ya fue admitido
"bandera_baja_logica": False/True
```
- `False`: proceso aún no ha sido admitido (espera en cola de listaProcesos).
- `True`: proceso ya fue admitido (en listaListos o listaSuspendidos).

---

## 8. SINCRONIZACIÓN AUTOMÁTICA (El Truco)

El simulador evita inconsistencias usando **referencias compartidas**, no copias:

```python
# MAL (copias):
listaListos.append(copy.deepcopy(proceso))
MP[i]["Proceso_alojado"] = copy.deepcopy(proceso)
# → Si cambias listaListos[j]["campo"], MP[i]["Proceso_alojado"]["campo"] NO cambia

# BIEN (referencias):
proceso_ref = {...}
listaListos.append(proceso_ref)
vGlobal.aux = proceso_ref
cargarProcesoAlojado(MP, puntero, vGlobal.aux)
# → Si cambias listaListos[j]["campo"], MP[i]["Proceso_alojado"]["campo"] TAMBIÉN cambia
```

---

## 9. DIAGRAMA COMPLETO DE FLUJO

```
┌───────────────────────────────────┐
│ main() - Loop Principal           │
│ (Coordina todo)                   │
└────────────┬──────────────────────┘
             │
             ▼
┌───────────────────────────────────────────┐
│ buscarSiguiente()                         │
│ ¿Hay proceso nuevo o futuro?             │
│ (Recorre listaProcesos FIFO)              │
└────────────┬──────────────────────────────┘
             │
             ├─ Hay proceso futuro → CiclosOciosos()
             │
             ├─ Hay proceso nuevo (t_arribo == T_sim)
             │  ▼
             │ ┌────────────────────────────────┐
             │ │ ADMICION_MULTI_5()             │
             │ │ (Planificador Largo Plazo)     │
             │ │ - Recorre listaProcesos FIFO   │
             │ │ - Admite en listaListos        │
             │ │ - Rechaza a listaSuspendidos   │
             │ │ - Promueve de MS a MP (FIFO)   │
             │ └────┬─────────────────────────────┘
             │      │
             │      ▼
             │   listaListos (FIFO)
             │   listaSuspendidos (FIFO)
             │
             ├─ Sin procesos pendientes → break
             │
             ▼
        ┌───────────────────────────────┐
        │ BuscarSRTF()                  │
        │ (Planificador Corto Plazo)    │
        │ - Busca menor t_RestanteCPU   │
        │ - Retorna índice MP[i]        │
        └────────┬──────────────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │ ejecutarTodo(puntero)    │
        │ - Ejecuta proceso en CPU │
        │ - Consume 1 ciclo CPU    │
        │ - Actualiza t_RestanteCPU
        │ - Maneja preemción SRTF  │
        │ - Detecta arribos        │
        └──────────────────────────┘
```

---

## 10. RESUMEN: ¿Cómo se relaciona FIFO con la Memoria Principal?

1. **Admisión FIFO**: `listaProcesos` → `listaListos` (si cabe) o `listaSuspendidos`
2. **Referencias compartidas**: `listaListos[i]` = `MP[j]["Proceso_alojado"]`
3. **Sincronización automática**: Cambiar uno actualiza ambos simultáneamente
4. **Eficiencia**: Evita copias redundantes y mantiene consistencia
5. **Equidad FIFO**: Garantiza que procesos no esperen indefinidamente
6. **Flexibilidad SRTF**: Permite preemción en CPU sin romper el FIFO de admisión

---

## 11. PUNTOS CLAVE PARA RECORDAR

✓ **FIFO admite**, **SRTF ejecuta**  
✓ **Misma referencia** en listaListos y MemoriaPrincipal  
✓ **Automatización de cambios** por referencias compartidas  
✓ **Equidad garantizada** por FIFO en admisión  
✓ **tiempoTotal_enColaDeListo** mide espera FIFO  
✓ **Recorridos en orden** en ADMICION_MULTI_5(), CARGAR_MPconMS(), buscarSiguiente()
