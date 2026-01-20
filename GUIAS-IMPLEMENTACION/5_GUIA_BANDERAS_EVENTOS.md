# 🚩 FASE 5: BANDERAS DE EVENTOS
## Sistema de Eventos y Mostrar Tablas Solo Cuando Corresponde

**Responsable:** Persona E + Testing  
**Depende de:** TODAS las fases anteriores  
**Tiempo estimado:** 2-3 horas  

---

## 🎯 Qué Son Banderas de Eventos

NO mostrar tablas en CADA ciclo. Solo mostrar cuando pasa algo:

- ✅ **Llega un proceso** (`hay_arribi`)
- ✅ **Termina un proceso** (`hay_terminacion`)
- ✅ **Ambos ocurren al mismo tiempo** (caso especial)
- ❌ **Nada sucede** → No mostrar

---

## 🔍 INVESTIGACIÓN EN funcionesLisandro_prolijo.py

### Pregunta 1: ¿Hay banderas booleanas?
**Busca:**
- Variables `hay_arribi`, `mostrar_tablas`, etc.
- Variables que se activan/desactivan
- Lógica para decidir cuándo mostrar

**Qué preguntar:**
> ¿Cómo se definen estas banderas?
> ¿Se resetean cada ciclo?

---

### Pregunta 2: ¿Cuándo se muestran las tablas?
**Busca:**
- Dónde se llama `mostrarColaListos()`, etc.
- Qué condición lo permite/prohíbe
- Si está dentro de `if banderas`

**Qué preguntar:**
> ¿Se muestran tablas en CADA ciclo o solo en eventos?

---

## 🛠️ Pasos para Implementar

### PASO 1: Definir banderas

```python
# Al inicio del loop
hay_arribi = False
hay_terminacion = False
mostrar_tablas = False
```

---

### PASO 2: Detectar y activar banderas

```python
while haya_trabajo:
    T += 1
    
    # Resetear banderas
    hay_arribi = False
    hay_terminacion = False
    
    # Detectar arribi
    if detectar_arribi(T):
        hay_arribi = True
    
    # Ejecutar SRTF
    proceso = obtener_siguiente_de_turnos()
    if proceso:
        proceso.TR -= 1
        if proceso.TR == 0:
            hay_terminacion = True
            terminar_proceso(proceso)
    
    # Decidir mostrar
    if hay_arribi or hay_terminacion:
        mostrar_tablas = True
    else:
        mostrar_tablas = False
```

---

### PASO 3: Mostrar SOLO si banderas activas

```python
while haya_trabajo:
    # ... (ciclos, ejecutar, etc.)
    
    # Al final del ciclo:
    if mostrar_tablas:
        print(f"\n=== INSTANTE T={T} ===")
        if hay_arribi:
            print("[EVENTO] Procesos arriban al sistema")
        if hay_terminacion:
            print("[EVENTO] Proceso finaliza ejecución")
        
        mostrarColaListos()
        mostrarColaSuspendido()
        mostrarMemoriaPrincipal()
        mostrarTablaTerminados()
```

---

### PASO 4: Caso especial - Arribi Y Terminación simultáneamente

```python
while haya_trabajo:
    T += 1
    
    hay_arribi = False
    hay_terminacion = False
    
    # Detectar ambos
    if detectar_arribi(T):
        hay_arribi = True
    
    # Ejecutar
    proceso = obtener_siguiente_de_turnos()
    if proceso:
        proceso.TR -= 1
        if proceso.TR == 0:
            hay_terminacion = True
    
    # Mostrar si hay cambios
    if hay_arribi or hay_terminacion:
        if hay_arribi and hay_terminacion:
            print("\n[EVENTO SIMULTÁNEO] Arribi Y Terminación en T={T}")
        else:
            print(f"\n[EVENTO] T={T}")
        
        mostrarTablas()
```

---

## ✅ Validación

### Test 1: No muestra en ciclos vacíos
```
Entrada:
  P1(TR=5) único proceso
  Ciclos T=1, T=2, T=3, T=4 sin cambios
Esperado:
  Solo 2 salidas:
    T=0: Arribi de P1
    T=5: Terminación de P1
  Ciclos 1-4: SIN salida de tablas
```

### Test 2: Muestra en arribi
```
Entrada:
  T=5: Llega P2 (P1 ejecutando)
Esperado:
  T=5: Mostrar tablas (flag hay_arribi=True)
```

### Test 3: Muestra en terminación
```
Entrada:
  T=5: P1 termina
Esperado:
  T=5: Mostrar tablas (flag hay_terminacion=True)
```

### Test 4: Muestra cuando ambos
```
Entrada:
  T=5: P1 termina Y P2 llega
Esperado:
  T=5: Mostrar tablas (AMBAS banderas True)
  Print: "[EVENTO SIMULTÁNEO]"
```

---

## 📝 Checklist de Implementación

- [ ] Creo banderas `hay_arribi`, `hay_terminacion`, `mostrar_tablas`
- [ ] Reseteo banderas al inicio de cada ciclo
- [ ] Detecto arribi y activo flag
- [ ] Detecto terminación y activo flag
- [ ] Solo muestro tablas si `mostrar_tablas == True`
- [ ] Manejo caso especial (ambos eventos)
- [ ] Pasé Test 1 (no muestra en vacíos)
- [ ] Pasé Test 2 (muestra en arribi)
- [ ] Pasé Test 3 (muestra en terminación)
- [ ] Pasé Test 4 (muestra cuando ambos)

---

## 🎯 INTEGRACIÓN FINAL: t_arribo_MP

**TODOS deben hacer esto:**

En ADMICION_MULTI_5(), cuando se admite un proceso a cola_turnos:

```python
def agregar_a_cola_turnos(proceso):
    # Registrar cuándo entra a MP (NO cuando llegó al CSV)
    if proceso.t_arribo_MP is None:
        proceso.t_arribo_MP = T_Simulacion  # ← TIEMPO ACTUAL
    
    # Agregar a cola
    cola_turnos.append(proceso)  # (o insertar ordenado)
```

En terminar_proceso():

```python
def mover_aColaTerminados(proceso):
    # Calcular tiempos CORRECTOS
    t_espera = T_Simulacion - proceso.t_arribo_MP
    t_retorno = T_Simulacion - proceso.t_arribo_MP
    
    # Guardar en resultado
    listaTerminados.append({
        'id': proceso.id,
        't_espera': t_espera,
        't_retorno': t_retorno,
        # ...
    })
```

---

## 🎓 TESTING FINAL

Después de implementar TODO:

1. **Prueba con Lote 1** (procesos pequeños, entra todo a MP)
2. **Prueba con Lote 2** (mezcla de tamaños, algunos en MS)
3. **Prueba con Lote 3** (grandes, mucho tiempo en MS)

**Validar:**
- ✅ No hay mensajes en ciclos sin eventos
- ✅ Multiprogramación nunca >= 5
- ✅ Tiempos de retorno/espera son coherentes
- ✅ Preempsión ocurre (comprobar cola_turnos reordenada)
- ✅ Ciclos ociosos se manejan correctamente

---

## 🔗 Próximo Paso

¡LISTO! Refactorización arquitectónica completa.
