# 🎯 DISTRIBUCIÓN DE TRABAJO Y COORDINACIÓN
## Plan de ejecución para 5 integrantes

---

## 📋 Distribución de Responsabilidades

| Persona | Fase | Guía | Tiempo | Depende de |
|---------|------|------|--------|-----------|
| **A** | 1: Ciclos | 1_GUIA_CICLOS_DE_TIEMPO.md | 3-4h | - |
| **B** | 2: Cola Turnos | 2_GUIA_COLA_DE_TURNOS.md | 2-3h | A |
| **C** | 3: SRTF | 3_GUIA_SRTF_PREEMPTIVO.md | 3-4h | A + B |
| **D** | 4: Multiprog | 4_GUIA_MULTIPROG_INTEGRADA.md | 3-4h | A + B + C |
| **E** | 5: Banderas | 5_GUIA_BANDERAS_EVENTOS.md | 2-3h | Todas |

**TOTAL ESTIMADO: 15-18 horas**

---

## 📅 Orden Estricto

**NO se puede comenzar una fase si la anterior no funciona.**

```
PERSONA A (FASE 1)
    ↓ (cuando funcione)
PERSONA B (FASE 2)
    ↓ (cuando funcione)
PERSONA C (FASE 3)
    ↓ (cuando funcione)
PERSONA D (FASE 4)
    ↓ (cuando funcione)
PERSONA E (FASE 5)
```

---

## 🔄 Paralelización Parcial

Mientras A trabaja:
- B puede **leer** guía 2 y funcionesLisandro_prolijo.py
- B puede **planificar** pero NO implementar

Mientras B trabaja:
- C puede **leer** guía 3 y funcionesLisandro_prolijo.py
- C puede empezar a **bocetar** ideas (pero NO tocar código)

**Regla:** Implementar DESPUÉS de que la fase anterior funcione.

---

## 🎯 Lo Que TODOS Deben Hacer (Integración Final)

Una vez que FASE 5 esté lista:

### Paso 1: Agregar campo `t_arribo_MP`
```python
proceso = {
    'id': ...,
    't_arribo': csv_time,
    't_arribo_MP': None,  # ← AGREGAR AQUÍ
    'tamaño': ...,
    # ...
}
```

### Paso 2: Registrar cuando entra a cola_turnos
```python
# En agregar_a_cola_turnos():
if proceso.t_arribo_MP is None:
    proceso.t_arribo_MP = T_Simulacion
```

### Paso 3: Calcular tiempos correctos
```python
# En mover_aColaTerminados():
t_espera = T_Simulacion - proceso.t_arribo_MP
t_retorno = T_Simulacion - proceso.t_arribo_MP
```

---

## 📊 Checkpoints de Validación

Cada persona debe **PROBAR su FASE** antes de pasar a la siguiente:

### Checkpoint A (Persona A)
✅ Ciclos incrementan unitariamente  
✅ Se detectan eventos (arribi/terminación)  
✅ El tiempo NO salta  

```bash
# Test simple: P1(TR=5)
# Esperado: 5 iteraciones del loop
```

### Checkpoint B (Persona B - con Persona A)
✅ Cola de Turnos se crea y agrega procesos  
✅ Máximo 3 procesos  
✅ Se ordena por SRTF  

```bash
# Test: Agregar P1(TR=10), P2(TR=5), P3(TR=8)
# Esperado: [P2, P3, P1]
```

### Checkpoint C (Persona C - con A + B)
✅ SRTF ejecuta 1 ciclo por iteración  
✅ Preempsión ocurre cuando hay proceso más corto  
✅ Cola se reordena  

```bash
# Test: P1(TR=10) T=0, P2(TR=2) T=3
# Esperado: Preempsión en T=3
```

### Checkpoint D (Persona D - con A + B + C)
✅ Multiprog nunca >= 5  
✅ Trae de suspendidos cuando hay espacio  
✅ ADMICION se ejecuta en eventos  

```bash
# Test: 10 procesos pequeños
# Esperado: Algunos en suspendidos, nunca > 5 total
```

### Checkpoint E (Persona E - con TODO)
✅ Banderas funcionan  
✅ Tablas solo en eventos  
✅ t_arribo_MP se registra y usa  
✅ Tiempos finales correctos  

```bash
# Test completo con Lote 1
# Esperado: 2-3 salidas de tablas (arribi y terminación)
```

---

## 🚨 Problemas Frecuentes

### Si la Fase 1 falla
- ¿El loop principal sigue? ¿O se bloquea?
- ¿T se incrementa o se queda igual?
- Revisar: ¿La condición del while está correcta?

### Si la Fase 2 falla
- ¿Los procesos se agregan a cola_turnos?
- ¿Se ordenan por SRTF (menor TR primero)?
- Revisar: ¿Se reordena después de cada cambio?

### Si la Fase 3 falla
- ¿Se ejecuta 1 ciclo por iteración?
- ¿La preempsión se detecta?
- Revisar: ¿Se compara correctamente `siguiente.TR < actual.TR`?

### Si la Fase 4 falla
- ¿Se valida multiprog ANTES de admitir?
- ¿len(cola_turnos) + len(suspendidos) nunca >= 5?
- Revisar: ¿ADMICION se ejecuta en EVENTOS, no siempre?

### Si la Fase 5 falla
- ¿Las banderas se resetean cada ciclo?
- ¿Las tablas se muestran SOLO en eventos?
- Revisar: ¿Hay condición `if mostrar_tablas`?

---

## 📞 Comunicación Entre Equipos

**Persona A → Persona B:**
"Fase 1 lista. Ciclos incrementan unitariamente. Puedes comenzar Fase 2."

**Persona B → Persona C:**
"Fase 2 lista. Cola de Turnos ordena por SRTF. Puedes comenzar Fase 3."

**Persona C → Persona D:**
"Fase 3 lista. SRTF ejecuta 1 ciclo y hace preempsión. Puedes comenzar Fase 4."

**Persona D → Persona E:**
"Fase 4 lista. Multiprog validada. Puedes comenzar Fase 5."

**Persona E → TODOS:**
"Fase 5 lista. Integren t_arribo_MP en sus códigos. Testing con Lotes."

---

## 🧪 TESTING CON LOS 3 LOTES

Una vez que TODO funciona:

```bash
# Lote 1: Procesos pequeños
python TPI_Listo.py < Lote_1.csv
# Esperado: Poco tiempo en MS, cosas entran rápido

# Lote 2: Mezcla
python TPI_Listo.py < Lote_2.csv
# Esperado: Algunos en MS, preempsión visible

# Lote 3: Procesos grandes
python TPI_Listo.py < Lote_3.csv
# Esperado: Mucho tiempo en MS, largas colas
```

**Validación:**
- ✅ No hay errores
- ✅ Resultados coherentes
- ✅ Multiprog nunca > 5
- ✅ Tiempos de retorno/espera sensatos

---

## 📚 Documentación a Leer

### Cada Persona Lee (EN ORDEN):

1. **Este documento** (coordinación general)
2. **0_ARQUITECTURA_NUEVA.md** (entender el diseño completo)
3. **Su guía de fase** (1, 2, 3, 4 o 5)
4. **funcionesLisandro_prolijo.py** en proyecto mejorado (investigar)
5. Guías de Persona anterior (cuando esté lista la fase previa)

---

## 🎓 Lo MÁS IMPORTANTE

> **NO copien código. ENTIENDAN qué hace, y implementen SU VERSIÓN.**
>
> El objetivo no es que sea idéntico, sino que **FUNCIONE CORRECTAMENTE** según lo que pide la profe.

---

## ✅ Hito Final

Cuando TODO esté listo:

- [ ] Fase 1: Ciclos unitarios ✅
- [ ] Fase 2: Cola de Turnos ✅
- [ ] Fase 3: SRTF preemptivo ✅
- [ ] Fase 4: Multiprog integrada ✅
- [ ] Fase 5: Banderas de eventos ✅
- [ ] Integración: t_arribo_MP ✅
- [ ] Testing: 3 Lotes ✅
- [ ] Presentación al equipo ✅

**¡ÉXITO!**
