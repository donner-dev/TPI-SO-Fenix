# 📊 FASE 2: COLA DE TURNOS
## Entender listaListos (= cola_turnos)

**Responsable:** Persona B  
**Depende de:** FASE 1 (Ciclos de Tiempo)  
**Tiempo estimado:** 1-2 horas  
**Bloqueante para:** FASE 3 (SRTF), FASE 4 (Multiprog)

---

## 🎯 ¿Qué Es listaListos?

**`listaListos` ES la cola de turnos. Son el MISMO nombre.**

Se llama `listaListos` porque refiere al estado **LISTO** del proceso en el simulador.

Es una **lista en Memoria Principal** que contiene **todos los procesos que están listos** para ejecutarse.

```
Flujo de procesos en el simulador:
1. Llega P1 → estado NUEVO (en lista_nuevos)
2. Se admite P1 → estado LISTO (entra a listaListos)
   - Se le asigna una partición en MemoriaPrincipal
   - AHORA está en listaListos
3. SRTF elige a P1 → se ejecuta en CPU
4. P1 termina → se libera partición

En cualquier ciclo:
listaListos contiene TODOS los procesos en estado LISTO
- Ordenados por FIFO (orden de llegada: primero en llegar, primero en la lista)
- PERO cuando SRTF elige, selecciona el de MENOR t_RestanteCPU
- Si hay empate en t_RestanteCPU, SRTF respeta el orden FIFO
```

---

## 🔑 Concepto Crítico: FIFO + SRTF

**Los procesos en listaListos están en ORDEN FIFO.**

Cuando SRTF busca quién ejecutar:
1. **Recorre la lista** de izquierda a derecha
2. **Busca el proceso con menor t_RestanteCPU**
3. **Si hay empate (mismo TR):** elige el primero que encuentra = **respeta FIFO**

```
Ejemplo 1: Diferentes t_RestanteCPU
listaListos = [P1(TR=10), P2(TR=5), P3(TR=8)]
SRTF elige: P2 (menor TR=5)

Ejemplo 2: Mismo t_RestanteCPU (empate)
listaListos = [P1(TR=5), P2(TR=5), P3(TR=3)]
SRTF elige: P3 (menor TR=3)

Ejemplo 3: Todos iguales (empate total)
listaListos = [P1(TR=5), P2(TR=5), P3(TR=5)]
SRTF elige: P1 (primero en la lista, respeta FIFO)
```

---

## 🔍 INVESTIGACIÓN EN funcionesLisandro_prolijo.py

### Pregunta 1: ¿Cómo se inicializa listaListos?
**Busca en funcionesLisandro_prolijo.py:**
- Dónde se crea `listaListos`
- ¿Es una lista vacía al inicio?
- ¿Se inicializa en estado_global.py?

**Qué preguntar:**
- ¿Hay algo especial en su inicialización?
- ¿Se modifica solo al admitir procesos?

---

### Pregunta 2: ¿Cómo se agregan procesos a listaListos?
**Busca:**
- Función que agrega un proceso a listaListos
- ¿Siempre lo agrega al final? (FIFO)
- ¿O a veces lo inserta en otra posición?

**Qué preguntar:**
- Cuando se admite un proceso, ¿se hace `listaListos.append(proceso)`?
- ¿O hay lógica especial de ordenamiento?

---

### Pregunta 3: ¿Cómo SRTF busca el siguiente proceso?
**Busca:**
- Función BuscarSRTF o similar
- Itera listaListos y busca el menor t_RestanteCPU
- ¿Qué pasa si hay empate?

**Qué preguntar:**
- ¿Si dos procesos tienen el MISMO TR, cuál elige?
- ¿El primero en la lista (FIFO)?

---

## 🧠 Conceptos Clave

### 1. listaListos = Orden FIFO

Los procesos EN MEMORIA PRINCIPAL están en `listaListos` en orden FIFO:

```
Ciclo 1: Llega P1 → listaListos = [P1]
Ciclo 2: Llega P2 → listaListos = [P1, P2]
Ciclo 3: Llega P3 → listaListos = [P1, P2, P3]
```

**La partición NO determina el orden:**

```
MemoriaPrincipal tiene 3 particiones (A, B, C)
P1 usa partición B
P2 usa partición A
P3 usa partición C

Pero en listaListos siempre es: [P1, P2, P3]
La partición es solo INFORMACIÓN del simulador, no afecta el orden
```

### 2. SRTF Busca el de Menor TR

Cuando ejecutar un ciclo, SRTF **recorre listaListos y busca el proceso con menor t_RestanteCPU:**

```
listaListos = [P1(TR=10), P2(TR=5), P3(TR=8)]
                     ↑              ↑              ↑
SRTF recorre: compara 10 vs 5 (5 es menor)
              compara 5 vs 8 (5 es menor)
              → Elige P2
```

### 3. Empate de TR: FIFO Desempata

Si dos procesos tienen **IGUAL t_RestanteCPU**, SRTF elige el **primero en la lista:**

```
listaListos = [P1(TR=5), P2(TR=5), P3(TR=3)]

Busca menor TR:
- P1 TR=5 (candidato)
- P2 TR=5 (igual, pero está después → no se elige)
- P3 TR=3 (es menor que 5 → se elige)

Resultado: ejecuta P3

----

listaListos = [P1(TR=5), P2(TR=5), P3(TR=5)]

Busca menor TR:
- P1 TR=5 (candidato, primera ocurrencia)
- P2 TR=5 (igual, pero está después)
- P3 TR=5 (igual, pero está después)

Resultado: ejecuta P1 (respeta FIFO en caso de empate)
```

### 4. NO es Necesario Mover Procesos

**NO hay que hacer operaciones complicadas:**
- NO hacer `cola_turnos.pop()`
- NO hacer `cola_turnos.insert()`
- NO hacer `cola_turnos.sort()`

**Solo:**
1. Cuando se admite un proceso → `listaListos.append(proceso)`
2. Cuando SRTF elige → recorrer listaListos, buscar menor TR
3. Cuando termina → `listaListos.remove(proceso)`

---

## 🛠️ Pasos para Implementar

### PASO 1: Entender la estructura actual

**En estado_global.py o donde guardes datos:**

```python
listaListos = []  # Lista de procesos EN MEMORIA PRINCIPAL, en orden FIFO
```

**Verificar:**
- ¿Cómo se inicializa?
- ¿Se vuelca a vaciar en algún punto?

---

### PASO 2: Buscar función BuscarSRTF (o similar)

**En funcionesLisandro_prolijo.py:**
- Busca una función que recorre `listaListos`
- Busca el proceso con MENOR `t_RestanteCPU`
- Lo ejecuta

```python
def BuscarSRTF():
    # Recorre listaListos
    # Encuentra proceso con menor t_RestanteCPU
    # Retorna ese proceso
    pass
```

**Verificar:**
- ¿Cómo itera la lista?
- ¿Qué pasa si listaListos está vacía?

---

### PASO 3: Verificar agregar/remover procesos

**Cuando se ADMITE un proceso:**
```python
listaListos.append(proceso)  # Se agrega al FINAL (FIFO)
```

**Cuando TERMINA un proceso:**
```python
listaListos.remove(proceso)  # Se quita de la lista
```

**Cuando se SUSPENDE (I/O):**
```python
listaListos.remove(proceso)
listaSuspendidos.append(proceso)
```

---

### PASO 4: Nada más que hacer

**En esta fase NO hay que:**
- Crear nuevas estructuras
- Reordenar la lista
- Hacer operaciones complicadas

**Solo investigar cómo SRTF funciona sobre listaListos**

---

## ✅ Validación

### Test 1: Verificar orden FIFO
```
Entrada:
  Admitir P1 (TR=10)
  Admitir P2 (TR=5)
  Admitir P3 (TR=8)
  
Esperado en listaListos:
  [P1(TR=10), P2(TR=5), P3(TR=8)]  ← En orden de FIFO
  
NO debería ser:
  [P2, P3, P1]  ← Eso sería ordenado por TR (INCORRECTO)
```

### Test 2: SRTF elige el menor TR
```
Entrada:
  listaListos = [P1(TR=10), P2(TR=5), P3(TR=8)]
  Llamar BuscarSRTF()
  
Esperado:
  Retorna P2 (tiene menor TR=5)
```

### Test 3: Empate desempatado por FIFO
```
Entrada:
  listaListos = [P1(TR=5), P2(TR=5), P3(TR=3)]
  Llamar BuscarSRTF()
  
Esperado:
  Retorna P3 (menor TR=3)
  
Luego:
  listaListos = [P1(TR=5), P2(TR=5)]
  Llamar BuscarSRTF()
  
Esperado:
  Retorna P1 (primero con TR=5, respeta FIFO)
```

### Test 4: Empate total
```
Entrada:
  listaListos = [P1(TR=5), P2(TR=5), P3(TR=5)]
  Llamar BuscarSRTF() 3 veces
  
Esperado:
  1ª llamada: P1 (primero)
  2ª llamada: P2 (segundo)
  3ª llamada: P3 (tercero)
  
← Respeta FIFO en empate total
```

---

## 📝 Checklist de Implementación

- [ ] Leí cómo se inicializa `listaListos`
- [ ] Entiendo que listaListos está en orden FIFO
- [ ] Encontré la función BuscarSRTF (o similar)
- [ ] Entiendo que BuscarSRTF recorre listaListos buscando menor TR
- [ ] Verifiqué que en empate, SRTF respeta FIFO
- [ ] Pasé Test 1 (orden FIFO)
- [ ] Pasé Test 2 (SRTF elige menor TR)
- [ ] Pasé Test 3 (empate desempatado por FIFO)
- [ ] Pasé Test 4 (empate total respeta FIFO)
- [ ] Documenté cómo BuscarSRTF funciona

---

## 🔗 Próximo Paso

Una vez que entiendas cómo funciona listaListos + SRTF:
- **Persona C** comienza con SRTF Preemptivo (ejecuta 1 ciclo y detecta si llegan nuevos)
- **Persona D** comienza MULTIPROG (valida len(listaListos) + len(listaSuspendidos) <= 5)
- **Persona E** espera para BANDERAS

