# 📍 FASE 1: CICLOS DE TIEMPO
## Implementar Incremento Unitario del Simulador

**Responsable:** Persona A  
**Tiempo estimado:** 3-4 horas  
**Bloqueante para:** Todas las otras fases

---

## 🎯 Qué Necesitas Lograr

Convertir el simulador de:
- ❌ "Ejecuta TODO el proceso de una vez" (salta de T=0 a T=10)
- ✅ "Ejecuta 1 ciclo, incrementa tiempo, repite" (T=0, T=1, T=2...)

---

## 🔍 INVESTIGACIÓN EN funcionesLisandro_prolijo.py

### Pregunta 1: ¿Dónde está el loop principal?
**Busca:**
- Función que se llama desde SIMULADOR.py
- Un `while` que parece ser el ciclo de ejecución
- Cómo se llama esa función

**Qué preguntar:**
- ¿Cuál es el punto de entrada (la función principal)?
- ¿Qué valida ese while para seguir ejecutando?

---

### Pregunta 2: ¿Cómo se incrementa el tiempo?
**Busca:**
- Variable que representa el tiempo (probablemente `T_Simulacion`)
- Dónde se incrementa (busca `+= 1`)
- Cuántas veces se incrementa en cada iteración del loop

**Qué preguntar:**
- ¿Se incrementa dentro del loop de ejecución?
- ¿O se incrementa después de hacer algo importante?

---

### Pregunta 3: ¿Qué ocurre en CADA incremento?
**Busca:**
- Qué sucede DESPUÉS de incrementar tiempo
- ¿Se detectan eventos?
- ¿Se ejecuta una acción inmediatamente?

**Qué preguntar:**
- ¿Se llama a ADMICION en cada ciclo?
- ¿Se ejecuta SRTF en cada ciclo?
- ¿O solo en ciertos instantes?

---

## 🧠 Conceptos Clave

### El Ciclo Unitario

En el proyecto mejorado el flujo es aproximadamente:

```
T = 0
mientras haya_trabajo:
    
    # 1. Incrementar tiempo
    T += 1
    
    # 2. Detectar eventos
    ¿Hay procesos que llegan en T?
    ¿Hay procesos que terminan en T?
    
    # 3. Si hay eventos → hacer cosas
    if hay_arribi:
        ADMICION()
    if hay_terminacion:
        Liberar partición, traer de MS
    
    # 4. Ejecutar SRTF (1 ciclo)
    proceso_actual.TR -= 1
    
    # 5. Mostrar info (si hay cambios)
    if mostrar_tablas:
        mostrar()
```

---

### Detectar Eventos en T

Un "evento" es algo que sucede en el instante actual:

- ✅ **Arribo:** `¿Hay procesos con t_arribo == T?`
- ✅ **Terminación:** `¿Hay procesos con t_RestanteCPU == 0 después de ejecutar?`
- ✅ **Ambos:** Si los dos ocurren en el mismo instante

---

## 🛠️ Pasos para Implementar

### PASO 1: Encontrar el loop principal actual

**En TPI_Listo.py busca:**
- La función que se ejecuta para simular
- El while que itera sobre procesos
- Dónde se modifica t_RestanteCPU

**Pregunta a responder:**
> ¿Cuántas veces se ejecuta el cuerpo del while cuando process.TR = 5?

---

### PASO 2: Cambiar estructura de loop

**LO QUE ESTÁ AHORA:**
```python
while proceso.TR > 0:
    proceso.TR -= 1
    # [el loop termina cuando TR = 0]
    # [no hay forma de "pausar" en medio]
```

**LO QUE NECESITAS:**
```python
T = inicio_del_tiempo  # probablemente 0 u otro valor

while haya_trabajo:
    # Incrementar tiempo PRIMERO
    T += 1
    
    # Hacer cosas que dependen de T
    # (admisión, detección, etc.)
    
    # DESPUÉS ejecutar 1 ciclo
    if hay_proceso_ejecutando:
        proceso_actual.TR -= 1
    
    # SALIR si no hay trabajo
    if no_hay_procesos_en_listos and no_hay_procesos_en_suspendidos:
        break
```

---

### PASO 3: Separar "detección de eventos" del "ejecutar proceso"

**Necesitas dos cosas:**

1. **Función para detectar arribi:**
   ```python
   def hay_procesos_que_llegan(T_actual):
       # Buscar en listaProcesos
       # si alguno tiene t_arribo == T_actual
       # return True/False
   ```

2. **Función para detectar terminación:**
   ```python
   def detectar_terminacion(proceso):
       # Después de hacer proceso.TR -= 1
       # if proceso.TR == 0:
       #     return True
   ```

---

### PASO 4: Manejar el "tiempo inactivo" (ciclos ociosos)

En el proyecto mejorado cuando NO hay procesos en listos, pero hay en suspendidos:

- ¿Se quedan esperando?
- ¿Se avanza directamente al próximo arribo?
- ¿Se incrementa igual el tiempo del simulador?

**Pregunta a investigar:**
> En funcionesLisandro_prolijo.py, ¿qué hace la función `CiclosOciosos`?

---

## ✅ Validación

### Test 1: Tiempo incrementa correctamente
```
Entrada: P1(TR=5) en T=0
Esperado: 
  T=1: P1.TR=4
  T=2: P1.TR=3
  T=3: P1.TR=2
  T=4: P1.TR=1
  T=5: P1.TR=0 (TERMINA)
```

### Test 2: Se detecta arribo en tiempo intermedio
```
Entrada: 
  P1(TR=10) en T=0
  P2(TR=5) en T=3
Esperado:
  T=1: P1 ejecuta (TR=9)
  T=2: P1 ejecuta (TR=8)
  T=3: P1 ejecuta (TR=7) + P2 LLEGA ← Se detecta
```

### Test 3: Ciclos ociosos se manejan
```
Entrada:
  P1(TR=5) en T=10
  P2(TR=3) en T=5 (pero entra a suspendidos)
Esperado:
  T=1-5: ¿Ciclos ociosos? (P1 no ha llegado)
  T=10: P1 comienza
```

---

## 📝 Checklist de Implementación

- [✅] Encontré el loop principal en TPI_Listo.py
- [✅] Identifiqué dónde se incrementa/decrementa tiempo
- [✅] Cambié la estructura a ciclo unitario (T += 1 en CADA iteración)
- [✅] Creo función `hay_procesos_que_llegan(T)` activa bandera de tablas al ingresar procesos en ADMICION_MULTI_5()
- [✅] Creo función `detectar_terminacion(proceso)`
- [✅] Manejo ciclos ociosos (sin bloquear el simulador)
- [ ] Pasé Test 1 (tiempo incrementa correctamente)
- [ ] Pasé Test 2 (detecta arribi en T intermedio)
- [ ] Pasé Test 3 (maneja ciclos ociosos)

---

## 🔗 Próximo Paso

Una vez que el incremento unitario funcione:
- **Persona B** comienza con COLA DE TURNOS
- **Persona C** espera COLA DE TURNOS para hacer SRTF
- **Persona D** espera TODO para MULTIPROG
- **Persona E** espera TODO para BANDERAS

