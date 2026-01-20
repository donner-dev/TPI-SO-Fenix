# 💻️ FASE 4: MULTIPROGRAMACIÓN INTEGRADA
## Control de len(listaListos) + len(listaSuspendidos) <= 5

**Responsable:** Persona D  
**Depende de:** FASE 1 (Ciclos) + FASE 2 (Cola) + FASE 3 (SRTF)  
**Tiempo estimado:** 3-4 horas  
**Bloqueante para:** FASE 5 (Banderas)

---

## ⚡ ACLARACIÓN CRÍTICA

**cola_turnos = listaListos** (mismo, diferente nombre)

Ambos:
- Están en **Memoria Principal**
- Funcionan como **FIFO con prioridad SRTF**
- Contienen procesos **admitidos y listos**
- El flujo real busca en listaListos, luego accede a MemoriaPrincipal por punteros

---

## 🎯 La Fórmula (CORRECTA)

```python
multiprogramacion = len(listaListos) + len(listaSuspendidos)

# Límite: multiprogramacion <= 5
# En otras palabras: NUNCA > 5
# (Pueden estar EXACTAMENTE 5, pero no 6+)

# Límites:
# - listaListos (= cola_turnos): 0-3 procesos (en MP)
# - listaSuspendidos: 0-4 procesos (en MS, ya fueron admitidos)
# - TOTAL admitidos: máximo 5
#
# IMPORTANTE - DIFERENCIA CRÍTICA:
# Procesos NO admitidos se quedan en lista de NUEVOS
# (no cuentan en multiprog, nunca entraron a MP)
```

---

## 🔄 FLUJO REAL CUANDO SE ELIGE Y EJECUTA

```
CADA CICLO:

1. Buscar proceso a ejecutar en listaListos
   ├─ Recorrer: buscar el de MENOR TR (SRTF)
   ├─ Elegir: proceso_a_ejecutar = min(listaListos, key=TR)
   └─ Retorna: proceso_elegido

2. Acceder a MemoriaPrincipal
   ├─ Usar punteros guardados → encontrar partición rápido
   ├─ Leer campos: proceso.t_RestanteCPU, status, etc.
   └─ Verificar: ¿está libre? ¿activo?

3. Ejecutar 1 ciclo
   ├─ proceso.t_RestanteCPU -= 1
   └─ Actualizar en MemoriaPrincipal

4. Si termina (t_RestanteCPU == 0)
   ├─ Marcar partición como LIBRE
   ├─ Remover de listaListos
   ├─ Libera espacio (multiprog -=)
   └─ Puede entrar nuevo de lista de NUEVOS

5. Si se suspende por I/O
   ├─ Remover de listaListos
   ├─ Agregar a listaSuspendidos
   ├─ Marcar partición como disponible
   └─ multiprog se mantiene (sigue siendo 5)
```

---

## 🔍 INVESTIGACIÓN EN funcionesLisandro_prolijo.py

### Pregunta 1: ¿Dónde se valida multiprogramación?
**Busca:**
- Función ADMICION_MULTI_5
- Líneas que checkean len(listos) o similar
- Condición que impide admitir

**Qué preguntar:**
> ¿Se valida ANTES de admitir un nuevo proceso?
> ¿O DESPUÉS?

---

### Pregunta 2: ¿Cómo integra ADMICION con listaListos?
**Busca:**
- Cómo mover de listaSuspendidos a cola_turnos
- Cuándo ocurre (cada evento? cada ciclo?)
- Validación de multiprog

**Qué preguntar:**
> ¿ADMICION es UNA función o varias?
> ¿Se ejecuta en cada ciclo o solo en eventos?

---

### Pregunta 3: ¿Qué hace si multiprog >= 5?
**Busca:**
- Qué sucede: ¿sale? ¿espera? ¿rechaza?
- Cómo quedan los procesos después

**Qué preguntar:**
> ¿Los procesos rechazados quedan donde?
> ¿Se reintentan después?

---

## 🛠️ Pasos para Implementar

### PASO 1: Crear validador

```python
def validar_multiprogramacion():
    mp = len(cola_turnos) + len(listaSuspendidos)
    return mp

def puede_admitir_nuevo():
    return validar_multiprogramacion() < 5
```

---

### PASO 2: Integrar en ADMICION_MULTI_5

```python
def ADMICION_MULTI_5():
    # 1. Validar multiprog
    if validar_multiprogramacion() >= 5:
        return  # No hacer nada
    
    # 2. Traer de suspendidos a cola_turnos
    while len(cola_turnos) < 3 and listaSuspendidos:
        if validar_multiprogramacion() >= 5:
            break
        proceso = listaSuspendidos.pop(0)  # FIFO
        agregar_a_cola_turnos(proceso)
        proceso.t_arribo_MP = T_actual  # FASE de tiempos
    
    # 3. Admitir nuevos procesos
    for proceso in listaProcesos:
        if validar_multiprogramacion() >= 5:
            break
        if proceso.t_arribo == T_actual and not proceso.admitido:
            if cabe_en_particion_MP(proceso):
                mover_aColaListo(proceso)
                agregar_a_cola_turnos(proceso)
            else:
                mover_aColaSuspendido(proceso)
            proceso.admitido = True
```

---

### PASO 3: Ejecutar ADMICION en eventos

```python
while haya_trabajo:
    T += 1
    
    hay_arribi = detectar_arribi(T)
    hay_terminacion = detectar_terminacion()
    
    # Ejecutar ADMICION SOLO si hay cambios
    if hay_arribi or hay_terminacion:
        ADMICION_MULTI_5()  # ← Validará multiprog
    
    # SRTF (FASE 3)
    # ...
```

---

### PASO 4: Actualizar cuando termina proceso

```python
def terminar_proceso(proceso):
    remover_de_cola_turnos(proceso)
    liberar_particion_en_MP(proceso)
    mover_aColaTerminados(proceso)
    
    # IMPORTANTE: Después de liberar, llamar ADMICION
    # para traer de suspendidos
    if listaSuspendidos:
        ADMICION_MULTI_5()
```

---

## ✅ Validación

### Test 1: No supera 5
```
Entrada: 10 procesos pequeños
Esperado:
  Nunca: len(cola_turnos) + len(listaSuspendidos) >= 5
  Algunos en cola_turnos, otros esperan en MS
```

### Test 2: Trae de suspendidos cuando hay espacio
```
Entrada:
  T=0: Entran P1, P2, P3 a cola_turnos (3)
  T=0: P4, P5 van a listaSuspendidos (2)
  T=5: P1 termina
Esperado:
  T=5: P4 pasa de suspendidos a cola_turnos
  cola_turnos = [P2, P3, P4]
  listaSuspendidos = [P5]
```

### Test 3: Rechaza si multiprog == 5
```
Entrada:
  cola_turnos = [P1, P2, P3]
  listaSuspendidos = [P4, P5]
  T=10: Llega P6
Esperado:
  P6 NO se admite (multiprog = 3 + 2 = 5)
  P6 queda pendiente en CSV/buffer
```

---

## 📝 Checklist de Implementación

- [ ] Creo función `validar_multiprogramacion()`
- [ ] Creo función `puede_admitir_nuevo()`
- [ ] ADMICION_MULTI_5() chequea multiprog ANTES
- [ ] ADMICION_MULTI_5() trae de suspendidos si hay espacio
- [ ] ADMICION_MULTI_5() se ejecuta en EVENTOS (arribi/terminación)
- [ ] terminar_proceso() llama ADMICION_MULTI_5()
- [ ] Pasé Test 1 (nunca supera 5)
- [ ] Pasé Test 2 (trae de suspendidos)
- [ ] Pasé Test 3 (rechaza si multiprog == 5)

---

## 🔗 Próximo Paso

Una vez que Multiprogramación funciona:
- **Persona E** comenzará BANDERAS de eventos
- **Todos** integran tiempos (`t_arribo_MP`)
