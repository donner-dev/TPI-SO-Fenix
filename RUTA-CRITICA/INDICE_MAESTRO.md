# 📚 ÍNDICE MAESTRO - REFACTORIZACIÓN ARQUITECTÓNICA
## Guía Completa para el Equipo

---

## 🚀 COMIENZA AQUÍ

### 0️⃣ **RESUMEN_REFACTORIZACION.md** ⭐ LECTURA MUY RÁPIDA
**Tiempo:** 5 min

Lee esto primero para entender qué se cambió y por qué.

---

### 1️⃣ **COORDINACION_5_INTEGRANTES.md** ⭐ LECTURA OBLIGATORIA
**Tiempo:** 10 min

Lee esto SEGUNDO como equipo.

Contiene:
- Distribución de trabajo (Personas A-E)
- Orden estricto de fases
- Checkpoints de validación
- Problemas frecuentes
- Comunicación entre equipos

---

## 📖 COMPRENSIÓN GENERAL (Todo el Equipo)

### 2️⃣ **0_ARQUITECTURA_NUEVA.md**
**Tiempo:** 15 min

Entiende POR QUÉ necesitan refactorizar.

Contiene:
- Comparación: arquitectura actual (mala) vs nueva (correcta)
- Flujo general de 5 fases
- Componentes a implementar
- Dónde investigar en funcionesLisandro_prolijo.py

---

## 🎯 GUÍAS POR PERSONA (Lectura Individual)

### PERSONA A: CICLOS DE TIEMPO
📄 **1_GUIA_CICLOS_DE_TIEMPO.md**  
⏱️ 3-4 horas  
🎯 Convertir loop a incremento unitario de tiempo

**Necesitas:**
- Leer 0_ARQUITECTURA_NUEVA.md
- Investigar funcionesLisandro_prolijo.py
- Implementar in TPI_Listo.py
- Pasar 3 tests de validación

---

### PERSONA B: COLA DE TURNOS
📄 **2_GUIA_COLA_DE_TURNOS.md**  
⏱️ 2-3 horas  
🎯 Crear estructura separada para SRTF  
🔴 **DEPENDE DE:** Persona A (Fase 1)

**Necesitas:**
- Leer 0_ARQUITECTURA_NUEVA.md
- Esperar a que A termine
- Investigar funcionesLisandro_prolijo.py
- Implementar in TPI_Listo.py
- Pasar 4 tests de validación

---

### PERSONA C: SRTF PREEMPTIVO
📄 **3_GUIA_SRTF_PREEMPTIVO.md**  
⏱️ 3-4 horas  
🎯 Implementar SRTF real (no SJF)  
🔴 **DEPENDE DE:** Personas A + B (Fases 1-2)

**Necesitas:**
- Leer 0_ARQUITECTURA_NUEVA.md
- Esperar a que B termine
- Investigar funcionesLisandro_prolijo.py
- Implementar in TPI_Listo.py
- Pasar 3 tests de validación

---

### PERSONA D: MULTIPROGRAMACIÓN
📄 **4_GUIA_MULTIPROG_INTEGRADA.md**  
⏱️ 3-4 horas  
🎯 Validar len(cola) + len(suspend) <= 5  
🔴 **DEPENDE DE:** Personas A + B + C (Fases 1-3)

**Necesitas:**
- Leer 0_ARQUITECTURA_NUEVA.md
- Esperar a que C termine
- Investigar funcionesLisandro_prolijo.py
- Implementar in TPI_Listo.py
- Pasar 3 tests de validación

---

### PERSONA E: BANDERAS DE EVENTOS
📄 **5_GUIA_BANDERAS_EVENTOS.md**  
⏱️ 2-3 horas  
🎯 Mostrar tablas SOLO en eventos  
🔴 **DEPENDE DE:** TODAS (Fases 1-4)

**Necesitas:**
- Leer 0_ARQUITECTURA_NUEVA.md
- Esperar a que D termine
- Investigar funcionesLisandro_prolijo.py
- Implementar in TPI_Listo.py
- Pasar 4 tests de validación
- **INTEGRACIÓN:** Todos agregan `t_arribo_MP`

---

## 📍 INVESTIGACIÓN EN CÓDIGO MEJORADO

### Qué Debe Buscar Cada Persona

**PERSONA A (Ciclos):**
- Función principal que se ejecuta
- Cómo se incrementa T_Simulacion
- Qué sucede en cada iteración

**PERSONA B (Cola Turnos):**
- ¿Existe estructura separada de listaListos?
- Cómo se agrega/remueve procesos
- Límite máximo (probablemente 3)

**PERSONA C (SRTF):**
- Dónde se ejecuta SOLO 1 ciclo
- Cómo se detecta preempsión
- Cómo se desaloja un proceso

**PERSONA D (Multiprog):**
- Función ADMICION_MULTI_5
- Validación de len(listos) + len(suspend)
- Cuándo se trae de MS a MP

**PERSONA E (Banderas):**
- Variables booleanas para eventos
- Cuándo se setean/resetean
- Condiciones para mostrar tablas

---

## 🧪 VALIDACIÓN Y TESTING

### Por Cada Fase

```
FASE 1 (A):      3 tests
FASE 2 (B):      4 tests
FASE 3 (C):      3 tests
FASE 4 (D):      3 tests
FASE 5 (E):      4 tests
INTEGRACIÓN:     3 Lotes CSV
```

### Cómo Validar

Cada guía contiene:
- Tests específicos para su fase
- Entrada/Salida esperada
- Cómo ejecutar manualmente

Ejecutar después:
```bash
python TPI_Listo.py < Lote_1.csv
python TPI_Listo.py < Lote_2.csv
python TPI_Listo.py < Lote_3.csv
```

---

## 🎯 HITOS PRINCIPALES

### Semana 1

- [ ] TODOS leen 0_ARQUITECTURA_NUEVA.md
- [ ] TODOS leen COORDINACION_5_INTEGRANTES.md
- [ ] A comienza FASE 1
- [ ] B, C, D, E leen sus guías + investigan

### Semana 2

- [ ] A termina FASE 1 ✅
- [ ] B comienza FASE 2 (con A)
- [ ] C, D, E investigan más, bocetean

### Semana 3

- [ ] B termina FASE 2 ✅
- [ ] C comienza FASE 3 (con A + B)
- [ ] D, E investigan, bocetean

### Semana 4

- [ ] C termina FASE 3 ✅
- [ ] D comienza FASE 4 (con A + B + C)
- [ ] E investiga más, bocetea

### Semana 5

- [ ] D termina FASE 4 ✅
- [ ] E comienza FASE 5 (con TODO)
- [ ] TODOS preparan integración de t_arribo_MP

### Semana 6

- [ ] E termina FASE 5 ✅
- [ ] TODOS integran t_arribo_MP
- [ ] TODOS testean con Lotes
- [ ] Presentación

---

## 📞 CANALES DE COMUNICACIÓN

### Diarios
- **Reunión matutina:** Checkear progreso
- **Chat grupal:** Problemas bloqueantes
- **Archivo de logs:** Qué se hizo cada día

### Entre Personas
- A → B (cuando FASE 1 lista)
- B → C (cuando FASE 2 lista)
- C → D (cuando FASE 3 lista)
- D → E (cuando FASE 4 lista)
- E → TODOS (cuando FASE 5 lista)

### Con la Profe
- Dudas arquitectónicas: pregunta A (Ciclos)
- Dudas SRTF: pregunta C (SRTF)
- Dudas Multiprog: pregunta D (Multiprog)

---

## ✨ FILOSOFÍA DE LA GUÍA

> No es "copia el código de funcionesLisandro_prolijo.py"
>
> Es **"INVESTIGA cómo lo hace, ENTIENDE, e IMPLEMENTA tu versión"**

Cada persona:
1. Lee la guía (conceptos)
2. Busca en código mejorado (comprensión)
3. Implementa en TPI_Listo.py (aplicación)
4. Valida con tests (verificación)

---

## 🎓 CÓMO NO FRACASAR

### ❌ Errores Comunes

- **NO esperar el turno** → Quedarán atrás
- **Copiar código sin entender** → Fallarán los tests
- **Implementar sin investigar** → Código incorrecto
- **NO validar con tests** → Bugs ocultos

### ✅ Camino al Éxito

- **Lee la guía primero** (conceptos claros)
- **Investiga el código mejorado** (entiende)
- **Implementa paso a paso** (valida continuamente)
- **Pasa todos los tests** (confianza)
- **Comunica con siguiente persona** (sincronización)

---

## 📚 DOCUMENTOS ANTIGUOS

**ESTOS ESTÁN OBSOLETOS** (fueron para la arquitectura antigua):
- ~~1_INICIO_RAPIDO.md~~
- ~~2_PLAN_CORRECCIONES_ROUND_ROBIN.md~~
- ~~3_EJEMPLOS_VISUALES_CORRECCIONES.md~~
- ~~4_MAPEO_PROYECTO_MEJORADO.md~~
- ~~5_ARBOL_DECISION_IMPLEMENTACION.md~~
- ~~6_RESUMEN_IMPRIMIBLE.md~~
- ~~8_EXPLICACION_MULTIPROGRAMACION_MEJORADA.md~~
- ~~9_CHULETA_MULTIPROGRAMACION.md~~

**USA ESTOS EN CAMBIO:**
- 0_ARQUITECTURA_NUEVA.md (entendimiento)
- 1_GUIA_CICLOS_DE_TIEMPO.md (implementación A)
- 2_GUIA_COLA_DE_TURNOS.md (implementación B)
- 3_GUIA_SRTF_PREEMPTIVO.md (implementación C)
- 4_GUIA_MULTIPROG_INTEGRADA.md (implementación D)
- 5_GUIA_BANDERAS_EVENTOS.md (implementación E)
- COORDINACION_5_INTEGRANTES.md (coordinación)

---

## 🚀 ¡VAMOS!

**Paso 1:** Toda el equipo lee estos documentos:
1. COORDINACION_5_INTEGRANTES.md
2. 0_ARQUITECTURA_NUEVA.md

**Paso 2:** Cada persona comienza su fase EN ORDEN

**Paso 3:** Sigan los checkpoints y tests

**Paso 4:** Comuniquen cuando esté lista su fase

**Paso 5:** Testing final con los 3 Lotes

**Paso 6:** ¡Presentación al equipo y a la profe!

---

**¡ÉXITO EN LA REFACTORIZACIÓN!**
