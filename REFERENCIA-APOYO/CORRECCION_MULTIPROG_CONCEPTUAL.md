# 🔧 CORRECCIÓN CONCEPTUAL: MULTIPROGRAMACIÓN Y ESTADOS

**Esta es una corrección importante al concepto de multiprogramación en todas las guías.**

---

## ❌ LO QUE ESCRIBÍ ANTES (INCORRECTO)

"Los procesos que llegan van a **Memoria Secundaria** (suspendidos)"

**Esto es INCORRECTO** porque confunde dos estados diferentes.

---

## ✅ LO CORRECTO

### Tres Estados de Procesos:

#### **ESTADO 1: NUEVO (No admitido aún)**
```
- Se queda en: LISTA DE NUEVOS / LISTA DE PROCESOS ORIGINALES
- Multiplprogramación: NO CUENTA
- Espera: Que se libere espacio (que multiprog < 5)
- Cuándo se admite: 
  * Cuando hay evento (arribi o terminación)
  * Y hay espacio (multiprog < 5)
```

#### **ESTADO 2: ADMITIDO (En Memoria Principal)**
```
- Se mueve a: cola_turnos / listaListos
- Multiprogramación: SÍ CUENTA (len = 1, 2, o 3)
- En la CPU: Uno de ellos está ejecutando
- Qué hace: Ejecuta instrucciones, ocupa partición
```

#### **ESTADO 3: SUSPENDIDO (Fue admitido, ahora en MS)**
```
- Se mueve a: listaSuspendidos
- Multiprogramación: SÍ CUENTA
- Razón: Fue admitido antes, ahora espera por I/O
- Cuándo regresa: Cuando I/O termina
```

---

## 📊 FÓRMULA DE MULTIPROGRAMACIÓN

```python
# CORRECTA:
multiprogramacion = len(listaListos) + len(listaSuspendidos)

# Límite: multiprog <= 5 (pueden estar EXACTAMENTE 5, pero no 6+)
# En otras palabras: NUNCA > 5

# Ejemplo:
cola_turnos = [P1, P2, P3]        # 3 en MP (= listaListos)
listaSuspendidos = [P4, P5]       # 2 en MS (fueron admitidos)
multiprog = 3 + 2 = 5              # ✅ LEGAL (exactamente 5, límite máximo)

# Llega P6:
P6_nuevo = LLEGA
if multiprog > 5:
    # Esto no pasaría porque estamos en 5, no en 6
    # Pero si estuviéramos en 5 y queremos admitir P6:
    RECHAZAR_P6
    P6_nuevo.estado = NUEVO  # Se queda en lista de NUEVOS
else:
    # Si multiprog < 5, podría haber espacio para P6
```

---

## 🔄 FLUJO DE ADMISIÓN EN CADA CICLO

```
CADA CICLO:

1. Detectar eventos (arribi o terminación)

2. Si multiprog < 5 Y hay procesos nuevos:
   └─ Traer de lista_nuevos → cola_turnos
      
3. Si hay terminación:
   └─ Remover de cola_turnos
   └─ Libera espacio
   └─ Si hay nuevos esperando → admitir siguiente
   
4. Si hay I/O completo de suspendido:
   └─ De listaSuspendidos → cola_turnos
   
5. Si multiprog == 5:
   └─ No admitir más procesos nuevos
   └─ Los nuevos esperan en lista_nuevos
```

## ⚠️ ACLARACIÓN IMPORTANTE: cola_turnos = listaListos

**Estos son SINÓNIMOS. Son la MISMA estructura.**

- `cola_turnos` (nombre usado en guías) = `listaListos` (nombre en código referencia)
- Ambos están en **Memoria Principal**
- Ambos funcionan como **FIFO con prioridad SRTF**
- Contienen procesos admitidos y listos para ejecutar

### Flujo Real de Búsqueda y Ejecución:

```
1. Buscar en listaListos (cola_turnos)
   └─ Recorrer: ¿quién tiene menor TR? (SRTF)
   └─ Elegir: proceso_elegido = el de mínimo TR

2. Acceder a MemoriaPrincipal
   └─ Buscar la partición donde está proceso_elegido
   └─ Usar punteros guardados para encontrar rápido
   └─ Acceder a los campos: proceso.t_RestanteCPU, etc.

3. Ejecutar 1 ciclo
   └─ proceso.t_RestanteCPU -= 1

4. Si termina (t_RestanteCPU == 0)
   └─ Marcar partición como LIBRE (en MemoriaPrincipal)
   └─ Remover de listaListos (cola_turnos)
   └─ Libera espacio para admitir nuevo
```

---

## 📍 DÓNDE SE USA BUSCARIGUIENTE()

En el código de referencia, `buscarSiguiente()` verifica:

```python
def buscarSiguiente():
    # ¿Hay procesos en lista de nuevos?
    if hay_procesos_nuevos():
        # ¿Hay espacio en multiprog?
        if multiprogramacion < 5:
            # Admitir nuevo
            return traer_nuevo()
    
    # ¿Hay ciclo ocioso?
    if cola_turnos.vacia() and listaSuspendidos.vacia():
        # No hay nada admitido ejecutando
        # Esperar a arribi o I/O
        return CICLO_OCIOSO
    
    # Si hay algo en cola_turnos, ejecutar
    return cola_turnos[0]
```

---

## 🎯 CORRECCIONES EN LAS GUÍAS

Se actualizaron automáticamente:

- ✅ `!QUICK_START_15_MIN.md` - Problema 3 corregido
- ✅ `0_ARQUITECTURA_NUEVA.md` - Problema 3 expandido
- ✅ `4_GUIA_MULTIPROG_INTEGRADA.md` - Fórmula corregida
- ⏳ Revisar si hay más referencias en otras guías

---

## ⚠️ IMPORTANTE PARA IMPLEMENTACIÓN

**Cuando revisen el código de referencia:**

Buscar dónde se distinguen estos tres estados:

1. **Lista de nuevos** - procesos no admitidos
2. **Cola de turnos** - procesos admitidos en MP
3. **listaSuspendidos** - procesos que fueron admitidos, ahora en MS

**La Persona D (multiprog) debe entender esta distinción perfectamente.**

---

**GRACIAS por la corrección.** Este concepto es CRÍTICO.
