# ⚡ FASE 3: SRTF PREEMPTIVO
## Implementar Shortest Remaining Time First Correctamente

**Responsable:** Persona C  
**Depende de:** FASE 1 (Ciclos) + FASE 2 (Entender listaListos)  
**Tiempo estimado:** 3-4 horas  
**Bloqueante para:** FASE 4 (Multiprog integrada)

---

## 🎯 Qué Es SRTF vs SJF

### ❌ SJF (Lo que está ahora)
```
T=0: Llega P1(TR=10), P2(TR=2)
     Elige P1 porque llega primero (FIFO)
     Ejecuta P1 TODO DE UNA VEZ: T=0...T=10
T=10: P2 finalmente se ejecuta: T=10...T=12
Total: 12 unidades
```

### ✅ SRTF (Lo que necesitas)
```
T=0: Llega P1(TR=10)
     listaListos = [P1] (FIFO)
     SRTF busca: P1 tiene TR=10
     Ejecuta P1: TR=9

T=1: Ejecuta P1: TR=8
T=2: Ejecuta P1: TR=7
T=3: Llega P2(TR=2)  ← EVENTO
     listaListos = [P1, P2] (FIFO se mantiene)
     SRTF busca: P1 TR=7 vs P2 TR=2
     PREEMPSIÓN: P2 < P1, desaloja P1
     Ejecuta P2: TR=1

T=4: Ejecuta P2: TR=0 → TERMINA
     Ahora listaListos = [P1]
     
T=5: Ejecuta P1: TR=6
     ...
T=11: P1 termina
Total: 11 unidades (mejoró!)
```

---

## 🔍 INVESTIGACIÓN EN funcionesLisandro_prolijo.py

### Pregunta 1: ¿Cómo se ejecuta SOLO 1 ciclo?
**Busca:**
- Dónde se hace `proceso.t_RestanteCPU -= 1`
- ¿Está dentro de un while anidado o es acción única?
- ¿Qué sucede después?

**Qué preguntar:**
> Después de hacer `proceso.t_RestanteCPU -= 1`, ¿se SALE del loop? ¿O continúa ejecutando más ciclos?

---

### Pregunta 2: ¿Cómo se detecta preempsión?
**Busca:**
- Función BuscarSRTF: recorre `listaListos` buscando menor TR
- Compara `proceso_actual.TR` con el siguiente de menor TR
- Qué hace si `siguiente.TR < actual.TR`

**Qué preguntar:**
> ¿Existe una función que evalúa si debe hacer preempsión?
> ¿Cómo se maneja el proceso desalojado?

---

### Pregunta 3: ¿Qué pasa al desalojar?
**Busca:**
- Cómo se marca que no está en CPU
- Se quita de la bandera CPU (probablemente `CPU=False`)
- Pero SIGUE en `listaListos` (NO se mueve)

**Qué preguntar:**
> ¿El proceso desalojado sigue en listaListos?
> ¿Solo se cambia la bandera CPU?

---

## 🛠️ Pasos para Implementar

### PASO 1: Ejecutar SOLO 1 ciclo por iteración

**Cambiar de:**
```python
while proceso.t_RestanteCPU > 0:
    proceso.t_RestanteCPU -= 1  # Ejecuta TODO
    # Aquí está el problema
```

**A:**
```python
# En cada ciclo del simulador:
if len(listaListos) > 0:
    # BuscarSRTF recorre listaListos buscando menor TR
    proceso_actual = BuscarSRTF(listaListos)
    
    # Ejecuta SOLO 1 ciclo
    proceso_actual.t_RestanteCPU -= 1
    
    # Marca que está en CPU (importante para preempsión)
    proceso_actual['CPU'] = True
    
    # SALE del loop automáticamente
    # El siguiente ciclo (T+=1) volverá a buscar
```

---

### PASO 2: Crear función BuscarSRTF

**Esta función ya debería existir, pero verifica que:**
- Recorre `listaListos` de izquierda a derecha
- Compara `t_RestanteCPU` de cada proceso
- Retorna el primero con MENOR `t_RestanteCPU`

```python
def BuscarSRTF(lista_procesos):
    """Recorre lista y retorna proceso con menor t_RestanteCPU"""
    if not lista_procesos:
        return None
    
    menor_proceso = lista_procesos[0]
    for proceso in lista_procesos[1:]:
        if proceso.get('t_RestanteCPU', 0) < menor_proceso.get('t_RestanteCPU', 0):
            menor_proceso = proceso
    
    return menor_proceso
```

---

### PASO 3: Detectar y manejar preempsión

**Después de ejecutar 1 ciclo:**
```python
# Acaba de ejecutarse proceso_actual
proceso_actual.t_RestanteCPU -= 1

# Chequear si hay preempsión
siguiente_mejor = BuscarSRTF(listaListos)

if siguiente_mejor and siguiente_mejor != proceso_actual:
    # Comparar TR
    if siguiente_mejor.get('t_RestanteCPU') < proceso_actual.get('t_RestanteCPU'):
        # HAY PREEMPSIÓN
        # Desalojar proceso_actual
        proceso_actual['CPU'] = False  # Marca que no está en CPU
        # siguiente_mejor toma CPU en próximo ciclo
        print(f"PREEMPSIÓN: {siguiente_mejor['id']} desaloja a {proceso_actual['id']}")
```

---

### PASO 4: Integración en ciclo principal

```python
while haya_trabajo():
    T += 1
    
    # Detectar eventos: nuevos procesos llegan
    # (FASE 1)
    
    # Admisión a memoria (Fase 4)
    # (valida multiprogramación)
    
    # ===== SRTF PREEMPTIVO (FASE 3) =====
    if len(listaListos) > 0:
        proceso_actual = BuscarSRTF(listaListos)
        
        if proceso_actual:
            # Ejecuta 1 ciclo
            proceso_actual['t_RestanteCPU'] -= 1
            proceso_actual['CPU'] = True
            
            # Chequea preempsión
            siguiente = BuscarSRTF(listaListos)
            if siguiente and siguiente != proceso_actual:
                if siguiente.get('t_RestanteCPU') < proceso_actual.get('t_RestanteCPU'):
                    # PREEMPSIÓN
                    proceso_actual['CPU'] = False
            
            # Chequea si terminó
            if proceso_actual['t_RestanteCPU'] <= 0:
                listaListos.remove(proceso_actual)
                # Actualizar multiprogramación
    
    # Banderas de evento (FASE 5)
```

---

## ✅ Validación

### Test 1: Ejecuta 1 ciclo por iteración
```
Entrada: P1(TR=5) solo en listaListos
Esperado:
  T=1: P1.TR = 4, P1 en CPU
  T=2: P1.TR = 3, P1 en CPU
  T=3: P1.TR = 2, P1 en CPU
  T=4: P1.TR = 1, P1 en CPU
  T=5: P1.TR = 0, se remove de listaListos
Total de ciclos ejecutados: 5
```

### Test 2: SRTF sin preempsión
```
Entrada: 
  P1(TR=10) en T=0, listaListos = [P1]
  P2(TR=2) en T=0, listaListos = [P1, P2]
Esperado:
  T=1: SRTF busca menor TR → P2(2) < P1(10) → Ejecuta P2, TR=1
  T=2: SRTF busca menor TR → P2(1) < P1(10) → Ejecuta P2, TR=0 (termina)
  T=3: listaListos = [P1], Ejecuta P1, TR=9
  T=4: Ejecuta P1, TR=8
  ...
  T=12: P1.TR=0 (termina)
```

### Test 3: Con preempsión
```
Entrada:
  T=0: P1(TR=10) entra → listaListos = [P1]
  T=3: P2(TR=2) entra → listaListos = [P1, P2]
  
Esperado:
  T=1: SRTF: P1 en CPU, TR=9
  T=2: SRTF: P1 en CPU, TR=8
  T=3: Llega P2, listaListos = [P1, P2]
       SRTF busca: P2(2) < P1(7)
       PREEMPSIÓN: Desaloja P1, P2 en CPU
  T=4: SRTF: P2 en CPU, TR=1
  T=5: SRTF: P2 en CPU, TR=0 (termina)
       listaListos = [P1]
  T=6: SRTF: P1 en CPU, TR=6
  ...
  T=11: P1.TR=0 (termina)
```

### Test 4: Empate y FIFO
```
Entrada:
  listaListos = [P1(TR=5), P2(TR=5), P3(TR=3)]
  
Esperado:
  T=1: SRTF busca: P3(3) < P1(5) y P2(5) → Ejecuta P3, TR=2
  T=2: SRTF busca: P3(2) < P1(5) y P2(5) → Ejecuta P3, TR=1
  T=3: SRTF busca: P3(1) < P1(5) y P2(5) → Ejecuta P3, TR=0 (termina)
       listaListos = [P1, P2]
  T=4: SRTF busca: P1(5) = P2(5) (empate)
       → Elige P1 (primero en lista = FIFO)
       Ejecuta P1, TR=4
```

---

## 📝 Checklist de Implementación

- [ ] Leí cómo se ejecuta SOLO 1 ciclo actualmente
- [ ] Entiendo por qué un while infinito es un problema
- [ ] Creé o verifiqué función BuscarSRTF
- [ ] BuscarSRTF recorre listaListos buscando menor TR
- [ ] En empate, BuscarSRTF respeta FIFO (primero en lista)
- [ ] Implemente ejecución de 1 ciclo por iteración
- [ ] Implementé detección de preempsión
- [ ] Cuando hay preempsión, desalojo con `CPU=False`
- [ ] Integré en ciclo principal
- [ ] Pasé Test 1 (ejecuta 1 ciclo)
- [ ] Pasé Test 2 (SRTF sin preempsión)
- [ ] Pasé Test 3 (con preempsión)
- [ ] Pasé Test 4 (empate con FIFO)
- [ ] Verificué que listaListos se mantiene en FIFO (NO se reordena)

---

## 🔗 Próximo Paso

Una vez que SRTF funciona:
- **Persona D** comienza con MULTIPROG (valida len(listaListos) + len(listaSuspendidos) <= 5)
- **Persona E** comienza con BANDERAS (integra t_arribo_MP, eventos)
