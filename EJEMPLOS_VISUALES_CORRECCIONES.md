# EJEMPLOS VISUALES DE LAS CORRECCIONES
## Diagramas y Ejemplos Prácticos

---

## CORRECCIÓN 1: TIEMPOS (t_arribo vs t_arribo_MP)

### ❌ ACTUAL (INCORRECTO)

```
ARCHIVO CSV:
Proceso, t_arribo, tamaño, t_irrupcion
P1,      0,       100,    10
P2,      3,       80,     8
P3,      5,       50,     5

T=0: P1 llega al sistema
     ↓ Se admite INMEDIATAMENTE a listaListos
     ↓ TIEMPO ACTUAL = t_arribo = 0

T=1-10: P1 ejecutando

T=10: P1 termina
      Tiempos calculados:
      - t_espera = T - t_arribo = 10 - 0 = 10 ✗ INCORRECTO
        (debería ser 0 porque entró inmediatamente)
      - t_retorno = T - t_arribo = 10 - 0 = 10 ✗ INCORRECTO

T=3: P2 llega al sistema
     [pero P3 ya ocupó espacio en MP]
     P2 va a Suspendidos (MS)

T=5: P3 llega al sistema
     Cabe en MP → Se mueve a listaListos
     t_arribo_MP = 5

T=11: P2 finalmente se admite a listaListos (de Suspendidos)
      Tiempos calculados:
      - t_espera = T - t_arribo = 11 - 3 = 8 ✗ INCORRECTO
        (no debe contar el tiempo que estuvo en SISTEMA, solo en MS)
      - t_retorno = 11 - 3 = 8 ✗ INCORRECTO
```

### ✅ CORRECTO

```
MISMO ARCHIVO CSV

T=0: P1 llega al sistema (t_arribo = 0)
     ↓ Se admite INMEDIATAMENTE a listaListos
     ↓ SE REGISTRA: t_arribo_MP = 0

T=1-10: P1 ejecutando

T=10: P1 termina
      Tiempos calculados:
      - t_espera = T - t_arribo_MP = 10 - 0 = 10 ✓ CORRECTO
      - t_retorno = T - t_arribo_MP = 10 - 0 = 10 ✓ CORRECTO

T=3: P2 llega al sistema (t_arribo = 3)
     [P3 ya ocupó espacio en MP]
     P2 va a Suspendidos (MS)
     SE REGISTRA: t_arribo_MP = None (aún no entra a MP)

T=5: P3 llega al sistema (t_arribo = 5)
     Cabe en MP → Se mueve a listaListos
     SE REGISTRA: t_arribo_MP = 5

T=11: P2 finalmente se admite a listaListos (libera espacio)
      SE REGISTRA: t_arribo_MP = 11  ← Aquí es cuando REALMENTE entra
      Tiempos calculados:
      - t_espera = T - t_arribo_MP = 11 - 11 = 0 ✓ CORRECTO
        (no pasó tiempo en cola de listaListos)
      - t_retorno = 11 - 11 = 0 ✓ CORRECTO

T=19: P2 termina
      Tiempos finales correctos
```

### 📝 Cambios de Código Necesarios

**1. Agregar campo:**
```python
proceso = {
    "id": ...,
    "t_arribo": t_arribo,        # ORIGINAL: del CSV
    "t_arribo_MP": None,          # NUEVO: registrar aquí
    "tamaño": ...,
    "t_irrupcion": ...,
    "t_RestanteCPU": ...,
}
```

**2. Registrar cuando entra a Listos:**
```python
def mover_aColaListo(proceso):
    # ... código existente ...
    proceso["t_arribo_MP"] = T_Simulacion  # ← AGREGAR ESTA LÍNEA
    listaMP_listos.append(proceso)  # o similar
```

**3. Recalcular en informe:**
```python
# ANTES (MAL):
t_espera_promedio = sum(p["t_espera"] for p in terminados) / len(terminados)

# DESPUÉS (CORRECTO):
t_espera_promedio = sum(T_termino[i] - p["t_arribo_MP"] for p in terminados) / len(terminados)

# O si guardas t_espera al terminar:
def mover_aColaTerminados(proceso):
    t_espera = T_Simulacion - proceso["t_arribo_MP"]  # ← USAR t_arribo_MP
    t_retorno = T_Simulacion - proceso["t_arribo_MP"]
    
    terminados.append({
        ...proceso...,
        "t_espera": t_espera,
        "t_retorno": t_retorno,
    })
```

---

## CORRECCIÓN 2: SRTF CON PREEMPSIÓN

### ❌ ACTUAL (SJF - NO ES PREEMPSIÓN)

```
PROGRAMA ACTUAL:
T=0: Lee P1(TR=10), P2(TR=2)
     
     Elige P1 (SRTF dice: elige el que está listo con menor TR)
     [pero hay solo P1 listo]
     
     ENTRA EN LOOP:
     while P1.t_RestanteCPU > 0:
         P1.t_RestanteCPU -= 1
         [resta 1]
         P1.t_RestanteCPU -= 1
         [resta 1]
         ... SIGUE EJECUTANDO ...
         
     SALE DEL LOOP CUANDO T_RestanteCPU == 0
     
     [P2 NUNCA SE DETECTÓ, PORQUE EL LOOP NO SE INTERRUMPE]
     
T=10: P1 TERMINA
      Ahora recién se detecta P2
```

**Problema**: No hay PREEMPSIÓN porque no se interrumpe el loop

### ✅ CORRECTO (CICLO A CICLO con Preempsión)

```
PROGRAMA MEJORADO:
T=0: Lee P1(TR=10), P2(TR=2) que llega en T=3
     
     Elige P1 (el único listo)
     
     ENTRA EN LOOP CICLO A CICLO:
     
T=0: P1.t_RestanteCPU = 10
     P1.t_RestanteCPU -= 1  → P1.TR = 9
     T_Simulacion = 1
     ¿Hay arribi en T=1? No
     ¿Preempsión? No (no hay otros listos)
     [CONTINÚA LOOP]

T=1: P1.t_RestanteCPU = 9
     P1.t_RestanteCPU -= 1  → P1.TR = 8
     T_Simulacion = 2
     ¿Hay arribi en T=2? No
     ¿Preempsión? No
     [CONTINÚA LOOP]

T=2: P1.t_RestanteCPU = 8
     P1.t_RestanteCPU -= 1  → P1.TR = 7
     T_Simulacion = 3
     ¿Hay arribi en T=3? SÍ, P2 ← AQUÍ SE DETECTA
     ADMICION_MULTI_5()  [agregar P2 a listaListos]
     
     P1 en CPU: TR = 7
     P2 en Listos: TR = 2
     
     ¿Preempsión SRTF? 
     Comparar: P2.TR (2) < P1.TR (7)? SÍ
     → DESALOJAR P1, TRAER P2
     [SALIR DEL LOOP, P1 regresa a Listos]

T=3: [nuevo ciclo]
     Elige P2 (menor TR)
     P2 en CPU: TR = 2
     P2.t_RestanteCPU -= 1  → P2.TR = 1
     T_Simulacion = 4
     ¿Hay arribi? No
     ¿Preempsión? Comparar P2 con P1... No hay que preempt
     [CONTINÚA LOOP]

T=4: P2.t_RestanteCPU = 1
     P2.t_RestanteCPU -= 1  → P2.TR = 0
     T_Simulacion = 5
     ¿Hay arribi? No
     ¿Preempsión? P2 terminó (TR=0)
     [SALIR DEL LOOP, P2 termina]

T=5: [nuevo ciclo]
     Elige P1 (único listo)
     P1 en CPU: TR = 7
     [sigue ejecutando]
```

**Resultado**: P1 ejecuta 3 ciclos, P2 ejecuta 2 ciclos, P1 ejecuta 7 ciclos

### 📝 Cambios de Código Necesarios

**1. Loop debe ser CICLO A CICLO:**
```python
# MAL (actual):
while proceso.t_RestanteCPU > 0:
    proceso.t_RestanteCPU -= 1
    # [no hay forma de interrumpir]

# CORRECTO:
while proceso.t_RestanteCPU > 0:
    proceso.t_RestanteCPU -= 1
    T_Simulacion += 1
    
    # [AQUÍ SE PUEDE INTERRUMPIR]
    siguiente = buscarSiguiente()  # ¿Llega alguien EN ESTE CICLO?
    if siguiente y siguiente.t_arribo == T_Simulacion:
        # Hay un nuevo arribo AHORA
        ADMICION_MULTI_5()
        
        # Evaluar preempsión
        proximo_srtf = BuscarSRTF()
        if proximo_srtf.id != proceso.id:
            if proximo_srtf.TR < proceso.TR:
                # PREEMPSIÓN
                proceso.CPU = False  # desalojar
                proceso = proximo_srtf  # nuevo en CPU
                break  # salir, ejecutar nuevo proceso
```

**2. La clave: DETECTAR y EVALUAR EN CADA CICLO:**
```
Seudocódigo:
for cada_ciclo:
    ejecutar 1 ciclo CPU
    avanzar tiempo 1
    
    detectar_arribi_este_ciclo()
    if hay_arribo:
        admitir_procesos()
        evaluar_preempsion()
        if preempto:
            cambiar_proceso_cpu()
            break  # salir de este while
```

---

## CORRECCIÓN 3: MULTIPROGRAMACIÓN <= 5

### ❌ ACTUAL (SIN VALIDAR)

```
ÁRBOL DE DECISIÓN ACTUAL (INCORRECTO):

¿Llega proceso? SÍ
  ↓
¿Cabe en MP? SÍ
  ↓
¿Hay espacio en Listos? SÍ
  ↓
ADMITIR A LISTOS ← SIN VALIDAR MULTIPROGRAMACION
  ↓
listaListos: [P1, P2, P3, P4, P5]  ← 5 procesos en MP
listaSuspendidos: [P6, P7]  ← 2 procesos en MS
TOTAL: 5 + 2 = 7 ✗ INCORRECTO (debería ser max 5)

O mejor:
ejecucion: 1 (P1 en CPU)
listos: 4 (P2, P3, P4, P5)
suspendidos: 2 (P6, P7)
TOTAL: 1 + 4 + 2 = 7 ✗ INCORRECTO
```

### ✅ CORRECTO (CON VALIDACIÓN)

```
ÁRBOL DE DECISIÓN CORRECTO:

¿Llega proceso? SÍ
  ↓
¿multiprogramacion < 5? ← NUEVA VALIDACIÓN
  ├─ NO
  │  └─ NO ADMITIR, esperar a que alguien termine
  │
  └─ SÍ
     ↓
     ¿Cabe en MP?
     ├─ SÍ
     │  ├─ listaListos + listaSuspendidos + (1 si CPU) < 5?
     │  │  ├─ SÍ → ADMITIR A LISTOS
     │  │  └─ NO → NO ADMITIR (¡pero esto no debería ocurrir!)
     │  └─
     │
     └─ NO (no cabe)
        ├─ listaListos + listaSuspendidos + (1 si CPU) < 5?
        │  ├─ SÍ → ADMITIR A SUSPENDIDOS
        │  └─ NO → NO ADMITIR (¡pero esto no debería ocurrir!)
        └─

RESULTADOS VÁLIDOS:
ejecucion: 1 (P1 en CPU)
listos: 2 (P2, P3)
suspendidos: 2 (P4, P5)
TOTAL: 1 + 2 + 2 = 5 ✓ CORRECTO

O también válido:
ejecucion: 1 (P1 en CPU)
listos: 3 (P2, P3, P4)
suspendidos: 1 (P5)
TOTAL: 1 + 3 + 1 = 5 ✓ CORRECTO

Pero NUNCA:
ejecucion: 1
listos: 4
suspendidos: 1
TOTAL: 6 ✗ INCORRECTO
```

### 📝 Cambios de Código Necesarios

**1. Función de validación:**
```python
def validar_multiprogramacion():
    """
    Retorna el nivel actual de multiprogramacion.
    No debe exceder 5 EN NINGÚN MOMENTO.
    """
    mp = len(listaListos) + len(listaSuspendidos)
    # Si hay proceso en CPU, también cuenta
    if hay_proceso_ejecutando:
        mp += 1
    return mp

def puede_admitir():
    """Retorna True si se puede admitir otro proceso"""
    return validar_multiprogramacion() < 5
```

**2. Validar ANTES de admitir:**
```python
def ADMICION():  # función de admisión
    if not puede_admitir():
        return  # No admitir nada
    
    for proceso in listaProcesos:
        if no_ha_sido_procesado(proceso):
            
            # VERIFICAR ANTES DE ADMITIR
            if validar_multiprogramacion() >= 5:
                break  # No admitir más
            
            if cabe_en_MP(proceso):
                mover_aColaListo(proceso)
            else:
                mover_aColaSuspendido(proceso)
```

**3. Validar en CARGAR_MPconMS:**
```python
def CARGAR_MPconMS():
    """Traer procesos de MS a MP cuando hay espacio"""
    while len(listaListos) < 3:  # máximo 3 en MP
        
        # VALIDAR MULTIPROGRAMACION
        if validar_multiprogramacion() >= 5:
            break  # No traer más
        
        # Buscar un suspendido que quepa
        for suspendido in listaSuspendidos:
            if cabe_en_MP(suspendido):
                mover_aColaListo(suspendido)
                break
        else:
            break  # Ninguno cabe
```

---

## TABLA COMPARATIVA: ANTES vs DESPUÉS

| Aspecto | ❌ ANTES (Incorrecto) | ✅ DESPUÉS (Correcto) |
|---------|-----|------|
| **t_arribo** | Se usa para calcular tiempos | Se usa solo como referencia |
| **t_arribo_MP** | NO existe | Se registra cuando entra a Listos |
| **t_espera** | = T_fin - t_arribo | = T_fin - t_arribo_MP |
| **t_retorno** | = T_fin - t_arribo | = T_fin - t_arribo_MP |
| **Loop CPU** | Avanza TODO de una vez | Ciclo a ciclo |
| **Detección arribi** | Se pierden muchos | Se detectan TODOS |
| **Preempsión** | NO ocurre (es SJF) | Ocurre en cada ciclo |
| **Validación MP** | NO se hace | Se valida ANTES de admitir |
| **Multiprogr. <= 5** | NO garantizado | SÍ garantizado |

---

## TESTING Y VALIDACIÓN

### Prueba 1: Tiempos Correctos

```
Input: procesos.csv con P1(TR=5) en T=0

ANTES (incorrecto):
t_retorno = 5 - 0 = 5
t_espera = 5 - 0 = 5

DESPUÉS (correcto):
t_arribo_MP = 0 (entra inmediatamente a Listos)
t_retorno = 5 - 0 = 5  (IGUAL, porque entra inmediatamente)
t_espera = 5 - 0 = 5   (IGUAL, porque entra inmediatamente)

Input: procesos.csv con P1(TR=5) en T=0, P2(TR=3) en T=2
       P2 no cabe en MP, va a Suspendidos

ANTES (incorrecto):
P2 t_retorno = 8 - 2 = 6
P2 t_espera = 8 - 2 = 6

DESPUÉS (correcto):
P2 t_arribo = 2 (del CSV)
P2 t_arribo_MP = 5 (cuando entra a MP)
P2 t_retorno = 8 - 5 = 3 ← CORRECTO, tiempo real en sistema
P2 t_espera = 8 - 5 = 3  ← CORRECTO, tiempo real esperando
```

### Prueba 2: SRTF Funciona

```
Input: P1(TR=10) en T=0, P2(TR=2) en T=3

ANTES (SJF):
T=0-10: P1 ejecuta (no se interrumpe)
T=10: P1 termina
T=10-18: P2 ejecuta
Tiempo total: 18

DESPUÉS (SRTF):
T=0-3: P1 ejecuta (TR: 10→7)
T=3: P2 llega (TR=2)
     Preempsión: P2 < P1 (2 < 7)
T=3-5: P2 ejecuta (TR: 2→0)
T=5: P2 termina
T=5-12: P1 ejecuta (TR: 7→0)
Tiempo total: 12 ← MEJOR (6 unidades ahorradas)
```

### Prueba 3: Multiprogramación <= 5

```
Monitorear en cada ciclo:
print(f"T={T}: Ejecución=1, Listos={len(listos)}, " +
      f"Suspendidos={len(suspendidos)}, TOTAL={1+len(listos)+len(suspendidos)}")

Verificar que NUNCA diga: TOTAL=6 o más
```

---

¡Con estos ejemplos debería quedar clara la implementación!
