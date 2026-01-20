# 📊 FASE 2: COLA DE TURNOS
## Estructura Separada para SRTF

**Responsable:** Persona B  
**Depende de:** FASE 1 (Ciclos de Tiempo)  
**Tiempo estimado:** 2-3 horas  
**Bloqueante para:** FASE 3 (SRTF), FASE 4 (Multiprog)

---

## 🎯 Qué Es la Cola de Turnos

**NO es listaListos.**

Es una **cola SEPARADA** que contiene **SOLO** los procesos que están listos para ejecutarse EN LA CPU.

```
listaListos (procesos en Memoria Principal):
├─ P1 (en partición A, CPU=True/False)
├─ P2 (en partición B, CPU=True/False)
└─ P3 (en partición C, CPU=True/False)

Cola de Turnos (procesos que pueden usar CPU):
├─ P1 (TR=10)
└─ P2 (TR=5)

← P3 está en listaListos pero FUERA de Cola de Turnos
  porque está esperando algo (ej: I/O, espacio, etc.)
```

---

## 🔍 INVESTIGACIÓN EN funcionesLisandro_prolijo.py

### Pregunta 1: ¿Existe una cola separada de listaListos?
**Busca:**
- Variables que NO sean `listaListos`, `listaSuspendidos`, etc.
- Algo que contenga procesos "en turno" o "ready"
- Estructura con máx 3 procesos (particiones)

**Qué preguntar:**
- ¿Cómo se llama esta estructura?
- ¿Se inicializa al mismo tiempo que listaListos?

---

### Pregunta 2: ¿Cómo se alimenta la Cola de Turnos?
**Busca:**
- Dónde se AGREGA un proceso a la Cola de Turnos
- ¿Es lo mismo que agregarlo a listaListos?
- ¿O es una acción adicional?

**Qué preguntar:**
- ¿Se llena en ADMICION_MULTI_5?
- ¿Se llena al traer de suspendidos?

---

### Pregunta 3: ¿Cómo se diferencia del orden en listaListos?
**Busca:**
- La Cola de Turnos se ordena por algo diferente a FIFO
- Probablemente por `t_RestanteCPU` (SRTF)
- O se recorre diferente cada vez

**Qué preguntar:**
- ¿Se modifica la Cola de Turnos después de cada ciclo?
- ¿O se recalcula cada vez que se necesita?

---

## 🧠 Conceptos Clave

### Diferencia Fundamental

```
listaListos:
- Orden: FIFO (primero en llegar, primero en la lista)
- Propósito: Saber qué procesos hay en MP
- Uso: Conocer estado general

Cola de Turnos:
- Orden: SRTF (menor t_RestanteCPU primero)
- Propósito: Elegir quién ejecuta ahora
- Uso: Seleccionar siguiente proceso para CPU
```

### Sincronización

```
Evento: Llega P4
↓
mover_aColaListo(P4)  → Agrega a listaListos
                        Asigna partición en MP
↓
cola_turnos.append(P4) → Agrega a Cola de Turnos (si cabe)
                         ← NUEVA acción
↓
Ahora P4 está en AMBAS estructuras, pero:
- En listaListos: en posición de FIFO
- En cola_turnos: ordenado por SRTF
```

---

## 🛠️ Pasos para Implementar

### PASO 1: Crear estructura Cola de Turnos

**En el estado global (estado_global.py o donde guardes datos):**

```python
# NUEVA ESTRUCTURA
cola_turnos = []  # Máximo 3 procesos

# ¿Cómo inicializarla?
# Busca en funcionesLisandro_prolijo.py dónde se inicializa
```

**Preguntas a responder:**
- ¿Dónde inicializas las estructuras al startup?
- ¿Es una lista normal de Python? ¿O estructura especial?

---

### PASO 2: Agregar proceso a Cola de Turnos

**Necesitas una función que:**
1. Reciba un proceso
2. Lo agregue en la posición correcta (por SRTF, NO FIFO)
3. Valide que no exceda 3 procesos

```python
def agregar_a_cola_turnos(proceso):
    # ¿Cómo insertar ordenado por t_RestanteCPU?
    # Busca en funcionesLisandro_prolijo.py cómo lo hace
    pass
```

**Investigación:**
- ¿Usa `.insert()` para insertar en posición correcta?
- ¿Usa `.sort()` después de agregar?
- ¿Cómo determina la posición?

---

### PASO 3: Remover proceso de Cola de Turnos

**Cuando:**
- El proceso termina (`t_RestanteCPU == 0`)
- Se lo desaloja (preempsión)
- Se lo suspende

```python
def remover_de_cola_turnos(proceso):
    # Buscar por ID o referencia
    # Remover de la lista
    pass
```

---

### PASO 4: Mantener sincronización

**Regla de oro:**
- Si un proceso está en `listaListos` Y en `cola_turnos`: está listo para ejecutar
- Si está en `listaListos` pero NO en `cola_turnos`: está esperando algo
- Si está en `listaSuspendidos`: NO puede estar en `cola_turnos`

---

## ✅ Validación

### Test 1: Se agrega ordenado por SRTF
```
Entrada:
  Agregar P1(TR=10)
  Agregar P2(TR=5)
  Agregar P3(TR=8)
  
Esperado cola_turnos:
  [P2(TR=5), P3(TR=8), P1(TR=10)]  ← Ordenado por TR
```

### Test 2: No excede 3 procesos
```
Entrada:
  Agregar P1, P2, P3 (3 procesos)
  Intentar agregar P4
  
Esperado:
  cola_turnos.length == 3
  P4 NO está en cola_turnos
  ← Pero PODRÍA estar en listaListos si fue admitido
```

### Test 3: Al remover se reordena
```
Entrada:
  cola_turnos = [P2(TR=5), P3(TR=8), P1(TR=10)]
  Remover P2
  
Esperado:
  cola_turnos = [P3(TR=8), P1(TR=10)]
```

### Test 4: Sincronización con listaListos
```
Entrada:
  listaListos = [P1, P2, P3]
  cola_turnos = [P2, P1]
  
Esperado:
  - P3 está en listaListos
  - P3 NO está en cola_turnos
  - Cuando P3 entra a cola_turnos:
    - Sigue en listaListos (NO se mueve)
    - Se agrega a cola_turnos
```

---

## 📝 Checklist de Implementación

- [ ] Creé estructura `cola_turnos`
- [ ] Inicializó `cola_turnos = []` en setup
- [ ] Implementé función `agregar_a_cola_turnos(proceso)`
- [ ] Implementé función `remover_de_cola_turnos(proceso)`
- [ ] Agrego procesos ordenados por SRTF (menor TR primero)
- [ ] Remover procesa correctamente
- [ ] Pasé Test 1 (se agrega ordenado)
- [ ] Pasé Test 2 (no excede 3)
- [ ] Pasé Test 3 (reorden al remover)
- [ ] Pasé Test 4 (sincronización con listaListos)

---

## 🔗 Próximo Paso

Una vez que Cola de Turnos funcione:
- **Persona C** comienza con SRTF (usa Cola de Turnos)
- **Persona D** puede comenzar MULTIPROG (revisa Cola de Turnos)
- **Persona E** espera para BANDERAS

