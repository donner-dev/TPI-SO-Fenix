# ⚡ FASE 3: SRTF PREEMPTIVO
## Implementar Shortest Remaining Time First Correctamente

**Responsable:** Persona C  
**Depende de:** FASE 1 (Ciclos) + FASE 2 (Cola de Turnos)  
**Tiempo estimado:** 3-4 horas  
**Bloqueante para:** FASE 4 (Multiprog integrada)

---

## 🎯 Qué Es SRTF vs SJF

### ❌ SJF (Lo que está ahora)
```
T=0: Llega P1(TR=10), P2(TR=2)
     Elige P1 porque no hay alternativa
     Ejecuta P1 TODO DE UNA VEZ: T=0...T=10
T=10: P2 finalmente se ejecuta: T=10...T=12
Total: 12 unidades
```

### ✅ SRTF (Lo que necesitas)
```
T=0: Llega P1(TR=10)
     Cola de turnos = [P1]
     Ejecuta P1: TR=9
T=1: Ejecuta P1: TR=8
T=2: Ejecuta P1: TR=7
T=3: Llega P2(TR=2)  ← EVENTO
     Cola de turnos se reordena = [P2, P1]
     Detecta: P2.TR=2 < P1.TR=7
     PREEMPSIÓN: Desaloja P1, pone P2 en CPU
     Ejecuta P2: TR=1
T=4: Ejecuta P2: TR=0 → TERMINA
T=5: P1 regresa: TR=6
     ...
T=11: P1 termina
Total: 11 unidades
```

---

## 🔍 INVESTIGACIÓN EN funcionesLisandro_prolijo.py

### Pregunta 1: ¿Cómo se ejecuta SOLO 1 ciclo?
**Busca:**
- Dónde se hace `proceso.TR -= 1`
- ¿Está dentro de un while anidado o es acción única?
- ¿Qué sucede después?

**Qué preguntar:**
> Después de hacer `proceso.TR -= 1`, ¿se SALE del loop? ¿O continúa?

---

### Pregunta 2: ¿Cómo se detecta preempsión?
**Busca:**
- Función que elige siguiente proceso de Cola de Turnos
- Comparación entre `proceso_actual.TR` y `siguiente.TR`
- Qué hace si `siguiente.TR < actual.TR`

**Qué preguntar:**
> ¿Existe una función que evalúa si hay preempsión?
> ¿Cómo se desaloja el proceso actual?

---

### Pregunta 3: ¿Qué pasa al desalojar?
**Busca:**
- Cómo se mueve un proceso de "ejecutando" a "listo"
- Se queda en listaListos pero regresa a Cola de Turnos
- ¿O se saca de ambas?

**Qué preguntar:**
> ¿El proceso desalojado sigue en listaListos?
> ¿O se lo suspende?

---

## 🛠️ Pasos para Implementar

### PASO 1: Ejecutar SOLO 1 ciclo

**Cambiar de:**
```python
while proceso.TR > 0:
    proceso.TR -= 1  # Ejecuta TODO
```

**A:**
```python
if proceso in cola_turnos:
    proceso.TR -= 1  # Ejecuta 1 ciclo
    # Sale automáticamente del loop
    # (el loop principal continúa)
```

---

### PASO 2: Detectar proceso a ejecutar

```python
def obtener_siguiente_de_turnos():
    # Cola de Turnos está ordenada por SRTF
    # El primero es el que debe ejecutar
    if cola_turnos:
        return cola_turnos[0]
    return None
```

---

### PASO 3: Implementar preempsión

```python
def hay_preempcion(proceso_actual, siguiente_candidato):
    if siguiente_candidato is None:
        return False
    return siguiente_candidato.TR < proceso_actual.TR

def desalojar_proceso(proceso):
    # Remover de CPU (bandera)
    # Mantener en listaListos
    # Mantener en cola_turnos (se reordenará)
    # El siguiente en Cola de Turnos toma CPU
    pass
```

---

### PASO 4: Integrar en el ciclo principal

```python
while haya_trabajo:
    T += 1
    
    # Detectar eventos (FASE 1)
    # Ejecutar admisión (FASE 4)
    
    # SRTF: Ejecutar 1 ciclo
    proceso_actual = obtener_siguiente_de_turnos()
    if proceso_actual:
        proceso_actual.TR -= 1
        
        # Chequear preempsión
        siguiente = obtener_siguiente_de_turnos()  # Recalcula order
        if hay_preempcion(proceso_actual, siguiente):
            desalojar_proceso(proceso_actual)
            # siguiente toma CPU en próximo ciclo
    
    # Banderas de evento (FASE 5)
```

---

## ✅ Validación

### Test 1: Ejecuta 1 ciclo por iteración
```
Entrada: P1(TR=5) solo
Esperado:
  T=1: P1.TR = 4
  T=2: P1.TR = 3
  T=3: P1.TR = 2
  T=4: P1.TR = 1
  T=5: P1.TR = 0 (termina)
Total de ciclos ejecutados: 5
```

### Test 2: SRTF sin preempsión
```
Entrada: 
  P1(TR=10) en T=0
  P2(TR=2) en T=0
Esperado:
  Cola de turnos comienza: [P2(TR=2), P1(TR=10)]
  T=1: Ejecuta P2, TR=1
  T=2: Ejecuta P2, TR=0 (termina)
  T=3: Ejecuta P1, TR=9
  ...
  T=12: P1 termina
```

### Test 3: Con preempsión
```
Entrada:
  P1(TR=10) en T=0
  P2(TR=2) en T=3
Esperado:
  T=1: Ejecuta P1, TR=9
  T=2: Ejecuta P1, TR=8
  T=3: Ejecuta P1, TR=7, luego P2 llega
       PREEMPSIÓN detectada (2 < 7)
       P2 se pone en CPU
  T=4: Ejecuta P2, TR=1
  T=5: Ejecuta P2, TR=0 (termina)
  T=6: Ejecuta P1, TR=6
  ...
  T=11: P1 termina
```

---

## 📝 Checklist de Implementación

- [ ] Cambié estructura para ejecutar 1 ciclo por iteración
- [ ] Creé función `obtener_siguiente_de_turnos()`
- [ ] Creé función `hay_preempcion(actual, siguiente)`
- [ ] Creé función `desalojar_proceso(proceso)`
- [ ] Integré en loop principal del ciclo (FASE 1)
- [ ] Pasé Test 1 (ejecuta 1 ciclo)
- [ ] Pasé Test 2 (SRTF sin preempsión)
- [ ] Pasé Test 3 (con preempsión)
- [ ] Cola de Turnos se reordena después de preempsión

---

## 🔗 Próximo Paso

Una vez que SRTF funciona:
- **Persona D** comienza con MULTIPROG (integración)
- **Persona E** comenzará BANDERAS de eventos
