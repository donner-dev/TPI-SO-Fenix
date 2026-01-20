# ✅ CORRECCIONES FINALES - MULTIPROGRAMACIÓN

**Última actualización basada en aclaraciones del usuario**

---

## 🔧 Tres Correcciones Críticas

### 1️⃣ FÓRMULA: "nunca > 5" (NO "nunca >= 5")

**ANTES (INCORRECTO):**
```
multiprog = len(cola) + len(suspend)
NUNCA >= 5  ← Esto significa: nunca puede ser 5 o más
```

**AHORA (CORRECTO):**
```
multiprog = len(listaListos) + len(listaSuspendidos)
NUNCA > 5   ← Esto significa: pueden estar EXACTAMENTE 5, pero no 6+
Límite máximo: multiprog <= 5
```

**Ejemplo:**
```
len(listaListos) = 3
len(listaSuspendidos) = 2
multiprog = 5      ✅ LEGAL (es el máximo)

Llega P6:
- ¿multiprog > 5? NO (es = 5, no mayor)
- ¿Hay espacio? NO (multiprog == 5 ya)
- Acción: P6 se queda en lista de NUEVOS
```

---

### 2️⃣ cola_turnos = listaListos (SINÓNIMOS)

**ANTES (AMBIGUO):**
- Usaba "cola_turnos" en las guías
- No estaba claro si era diferente a "listaListos"
- Confusión sobre dónde estaban los procesos

**AHORA (CLARO):**
```
cola_turnos = listaListos
(mismo estructura, diferentes nombres en docs)

Ubicación: MEMORIA PRINCIPAL
Funcionamiento: FIFO con prioridad SRTF
Contiene: procesos admitidos y listos
Tamaño: 0-3 procesos (máximo 3 particiones)
```

**Aclaración importante:**
- El nombre "cola_turnos" enfatiza: "toman turnos para ejecutar"
- El nombre "listaListos" enfatiza: "están listos para ejecutar"
- Ambos es la MISMA estructura

---

### 3️⃣ FLUJO REAL: listaListos → MemoriaPrincipal por punteros

**CÓMO FUNCIONA EN REFERENCIA:**

```
PASO 1: Elegir proceso de listaListos
  └─ Buscar min(TR) entre todos los procesos en listaListos
  └─ Resultado: proceso_a_ejecutar

PASO 2: Acceder a MemoriaPrincipal usando punteros
  └─ Puntero guardado → partición específica
  └─ Acceder a campos de esa partición
  └─ Leer/escribir status, t_RestanteCPU, etc.

PASO 3: Ejecutar 1 ciclo
  └─ Decrementar TR
  └─ Actualizar en MemoriaPrincipal

PASO 4: Si termina
  └─ MemoriaPrincipal[partición] = LIBRE
  └─ Remover de listaListos
  └─ Libera espacio en multiprog

PASO 5: Si se suspende (I/O)
  └─ Remover de listaListos
  └─ Agregar a listaSuspendidos
  └─ Marcar partición como disponible
  └─ multiprog se mantiene igual (sigue siendo 5)
```

---

## 📊 ESTADOS FINALES (CORRECTOS)

### Estado NUEVO (No admitido)
```
- Ubicación: Lista de procesos NUEVOS (original)
- En multiprog: NO cuenta
- Qué espera: len(listaListos) + len(suspend) < 5
```

### Estado ADMITIDO
```
- Ubicación: listaListos (= cola_turnos)
- En MemoriaPrincipal: SÍ tiene partición asignada
- En multiprog: SÍ cuenta
- Qué hace: Espera su turno SRTF o está ejecutando
```

### Estado SUSPENDIDO
```
- Ubicación: listaSuspendidos
- Partición en MemoriaPrincipal: MARCADA (reservada)
- En multiprog: SÍ cuenta
- Razón: Fue admitido antes, ahora espera I/O
```

---

## 📝 DOCUMENTOS ACTUALIZADOS

✅ **!QUICK_START_15_MIN.md**
- Cambió "nunca >= 5" a "nunca > 5"
- Agregó nota sobre cola_turnos = listaListos

✅ **4_GUIA_MULTIPROG_INTEGRADA.md**
- Cambió fórmula (nunca > 5)
- Agregó sección "ACLARACIÓN CRÍTICA" sobre sinónimos
- Agregó sección "FLUJO REAL" con el acceso a MemoriaPrincipal

✅ **CORRECCION_MULTIPROG_CONCEPTUAL.md**
- Cambió "nunca >= 5" a "nunca > 5"
- Agregó sección "cola_turnos = listaListos"
- Agregó flujo real con punteros a MemoriaPrincipal

---

## 🎯 PARA LA PERSONA D (Multiprog)

**Investigar en funcionesLisandro_prolijo.py:**

1. ¿Dónde se define listaListos?
2. ¿Cómo se valida multiprog ANTES de admitir?
   - Línea exacta: `if validar_multiprog() > 5: return`
3. ¿Dónde se accede a MemoriaPrincipal?
   - Buscar: punteros, MemoriaPrincipal[índice]
4. ¿Cómo se marcan particiones como LIBRE/OCUPADO?
   - Buscar: status = "LIBRE", "OCUPADO", etc.
5. ¿Cómo se integra listaSuspendidos?
   - ¿Cuándo mueve de listaListos a listaSuspendidos?
   - ¿Cuándo regresa?

---

## ✨ LA VERDAD RESUMIDA

```
multiprogramacion = len(listaListos) + len(listaSuspendidos)

Máximo permitido: 5 procesos admitidos simultáneamente
(3 en MP + máximo 2 en MS, o 2 en MP + 3 en MS, etc.)

Procesos no admitidos: se quedan en lista de NUEVOS
(no cuentan en multiprog, esperan espacio)

Acceso a memoria: usar punteros guardados en listaListos
para encontrar la partición en MemoriaPrincipal
```

---

**ESTAS CORRECCIONES SON FINALES Y ESTÁN EN LAS GUÍAS.**
