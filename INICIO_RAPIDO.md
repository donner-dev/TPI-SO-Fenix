# 🚀 INICIO RÁPIDO: GUÍA DE CORRECCIONES ROUND ROBIN
## Resumen Ejecutivo - Comienza Aquí

---

## 📌 EL PROBLEMA (Feedback del Profesor)

Tres cosas deben corregirse:

### ❌ Problema 1: Tiempos Incorrectos
- **Qué está mal**: Se usa `t_arribo` (del CSV) para calcular tiempos
- **Qué debe ser**: Usar `t_arribo_MP` (cuando REALMENTE entra a memoria)
- **Impacto**: TODOS los tiempos de retorno y espera son INCORRECTOS

### ❌ Problema 2: No hay Preempsión SRTF
- **Qué está mal**: El código avanza directamente hasta que termina el proceso
- **Qué debe ser**: Avanzar CICLO A CICLO para detectar llegadas intermedias
- **Impacto**: Es SJF (Shortest Job First), NO SRTF (Shortest Remaining Time First)

### ❌ Problema 3: Multiprogramación no se valida
- **Qué está mal**: Puede haber más de 5 procesos (CPU + Listos + Suspendidos)
- **Qué debe ser**: NUNCA debe exceder 5 en ningún momento
- **Impacto**: No respeta la restricción de multiprogramación

---

## 📚 DOCUMENTOS CREADOS PARA TI

He creado 4 documentos guía (en la carpeta del proyecto):

### 1. **PLAN_CORRECCIONES_ROUND_ROBIN.md** ← COMIENZA AQUÍ
- Explicación detallada de cada problema
- Pasos específicos para corregir
- Estrategia de trabajo en equipo
- Referencias al código mejorado

### 2. **EJEMPLOS_VISUALES_CORRECCIONES.md**
- Diagramas antes/después
- Ejemplos concretos de código
- Pruebas de validación
- Tablas comparativas

### 3. **MAPEO_PROYECTO_MEJORADO.md**
- Referencias EXACTAS al proyecto mejorado
- Líneas específicas dónde mirar
- Cómo adaptar código
- Checklist de implementación

### 4. **EXPLICACION_FIFO.md** (ya existente)
- Concepto de FIFO + SRTF
- Estructura de datos
- Sincronización con referencias

---

## 🎯 PLAN DE ACCIÓN (Resumen)

### 📋 Corrección 1: Tiempos (2-3 horas)

**Lo que necesitas:**
- Agregar campo `t_arribo_MP` en estructura de proceso
- Registrar cuando proceso entra a listaListos
- Usar `t_arribo_MP` en cálculos finales

**Referencias:**
- Ver `funcionesLisandro_prolijo.py` función `mover_aColaListo()` L180
- Ver `funcionesLisandro_prolijo.py` función `mover_aColaTerminados()` L260

**Validación:**
```
Input: P1(TR=5) en T=0
✓ Antes: t_retorno = 5 - 0 = 5
✓ Después: t_retorno = 5 - 0 = 5 (debería ser igual porque entra ya)

Input: P1(TR=5) T=0, P2(TR=3) T=2 sin espacio en MP
✓ Antes: P2 t_retorno = 8 - 2 = 6 (INCORRECTO)
✓ Después: P2 t_retorno = 8 - 5 = 3 (CORRECTO)
```

---

### 📋 Corrección 2: SRTF (3-4 horas)

**Lo que necesitas:**
- Cambiar loop a **ciclo a ciclo** (no ejecutar todo de una vez)
- Detectar arribi en **CADA CICLO**
- Evaluar preempsión en **CADA CICLO**

**Referencias:**
- Ver `SIMULADOR.py` función `ejecutarTodo()` L95-220
- Ver `SIMULADOR.py` función `buscarSiguiente()` L236-270
- Buscar "APROPIACION" en `SIMULADOR.py` para ver preempsión

**Validación:**
```
Input: P1(TR=10) T=0, P2(TR=2) T=3
✗ Antes (SJF): T=0-10 P1, T=10-18 P2 → Total=18
✓ Después (SRTF): T=0-3 P1, T=3-5 P2, T=5-12 P1 → Total=12
```

---

### 📋 Corrección 3: Multiprogramación (2-3 horas)

**Lo que necesitas:**
- Crear función `validar_multiprogramacion()`
- Validar ANTES de cada admisión
- Nunca permitir (CPU + Listos + Suspendidos) > 5

**Referencias:**
- Ver `SIMULADOR.py` L135-155 comentarios
- Ver `funcionesLisandro_prolijo.py` función `ADMICION_MULTI_5()` L585
- Ver `funcionesLisandro_prolijo.py` función `CARGAR_MPconMS()` L570

**Validación:**
```
Monitorear en cada ciclo:
✓ CPU: 1
✓ Listos: 2
✓ Suspendidos: 2
✓ TOTAL: 5 ← CORRECTO

✗ CPU: 1
✗ Listos: 3
✗ Suspendidos: 2
✗ TOTAL: 6 ← INCORRECTO (nunca debe ocurrir)
```

---

## 👥 DIVIDIR TRABAJO EN EQUIPO (5 PERSONAS)

### Persona A: Agregar campo `t_arribo_MP`
**Qué hacer:**
1. Leer "PLAN_CORRECCIONES_ROUND_ROBIN.md" sección 1a
2. Leer "MAPEO_PROYECTO_MEJORADO.md" sección 1
3. Implementar:
   - Agregar campo `t_arribo_MP` en estructura de proceso
   - Inicializar en None
   - Documentar bien
4. Coordinar con Persona B (cada 30 min)
5. Probar que estructura no rompe nada

**Tiempo**: 1-2 horas
**Archivos a modificar**: `TPI_Listo.py`

---

### Persona B: Registrar y usar `t_arribo_MP`
**Qué hacer:**
1. Leer "PLAN_CORRECCIONES_ROUND_ROBIN.md" sección 1b
2. Leer "MAPEO_PROYECTO_MEJORADO.md" sección 1
3. Implementar:
   - Registrar `t_arribo_MP` cuando proceso entra a listaListos
   - Usar en cálculos finales de tiempos
   - Verificar que **NO** usa `t_arribo` en cálculos
4. Coordinar con Persona A (cada 30 min)
5. Probar con `procesos.csv` simple

**Tiempo**: 1-2 horas
**Archivos a modificar**: `TPI_Listo.py`

---

### Persona C: Loop ciclo-a-ciclo + detectar arribi
**Qué hacer:**
1. Leer "PLAN_CORRECCIONES_ROUND_ROBIN.md" sección 2a
2. Leer "MAPEO_PROYECTO_MEJORADO.md" sección 2
3. Implementar:
   - Cambiar loop a avanzar **UN CICLO** por iteración
   - Detectar arribi en **CADA CICLO**
   - Movilizar procesos desde Suspendidos según sea necesario
4. Coordinar con Persona D (cada 30 min)
5. Probar que estructura no rompe nada

**Tiempo**: 1.5-2 horas
**Archivos a modificar**: `TPI_Listo.py`

---

### Persona D: Evaluar preempsión SRTF
**Qué hacer:**
1. Leer "PLAN_CORRECCIONES_ROUND_ROBIN.md" sección 2b
2. Leer "MAPEO_PROYECTO_MEJORADO.md" sección 2
3. Implementar:
   - Evaluar preempsión en **CADA CICLO**
   - Buscar si hay proceso más corto en Listos
   - Si existe → desalojar actual + meter el nuevo
   - Desalojado regresa a Listos
4. Coordinar con Persona C (cada 30 min)
5. Probar con `LOTE_1.csv`

**Tiempo**: 1.5-2 horas
**Archivos a modificar**: `TPI_Listo.py`

---

### Persona E: Multiprogramación + Testing
**Qué hacer (Parte 1 - Multiprogramación):**
1. Leer "PLAN_CORRECCIONES_ROUND_ROBIN.md" sección 3
2. Leer "MAPEO_PROYECTO_MEJORADO.md" sección 3
3. Implementar:
   - Función `validar_multiprogramacion()`
   - Validar ANTES de cada admisión
   - Nunca permitir (CPU + Listos + Suspendidos) > 5
4. Probar con `LOTE_2.csv`

**Qué hacer (Parte 2 - Testing):**
1. Cuando Personas A+B terminen → Validar Tiempos
2. Cuando Personas C+D terminen → Validar SRTF
3. Hacer testing final con todos los lotes
4. Generar informe de validación

**Tiempo**: 2-3 horas
**Archivos a modificar**: `TPI_Listo.py`

---

## ⏰ CRONOGRAMA SUGERIDO (5 PERSONAS - TRABAJO EN PARALELO)

```
REUNIÓN INICIAL (HOY - 30 min):
  - Todos leen este documento + PLAN_CORRECCIONES_ROUND_ROBIN.md
  - Se asignan Personas A, B, C, D, E
  - Se acepta cronograma de 2-3 días
  - Personas A↔B coordinan (teléfono/Discord)
  - Personas C↔D coordinan (teléfono/Discord)

DÍA 1 (Tarde - 3-4 horas EN PARALELO):
  - Persona A: Agrega field `t_arribo_MP` (1-2h)
  - Persona B: Se prepara leyendo (mientras A trabaja)
  - Persona C: Implementa loop ciclo-a-ciclo (1.5-2h)
  - Persona D: Se prepara leyendo (mientras C trabaja)
  - Persona E: Se prepara leyendo + planifica testing

DÍA 2 (Mañana - 3-4 horas EN PARALELO):
  - Persona A: Integra cambios con Persona B
  - Persona B: Registra y usa `t_arribo_MP` en cálculos (1-2h)
  - Persona C: Integra cambios con Persona D
  - Persona D: Evalúa preempsión SRTF (1.5-2h)
  - Persona E: Implementa validación multiprogramación (2-3h)

DÍA 2-3 (Tarde - 1-2 horas):
  - Persona E: Valida Tiempos (revisa A+B)
  - Persona E: Valida SRTF (revisa C+D)
  - Todos juntos: Validación cruzada

DÍA 3 (Mañana - 1 hora):
  - Persona E: Testing final con 3 lotes
  - Persona E: Generar informe de validación
  - LISTO para entregar

TOTAL: ~9-12 horas (EN PARALELO = mucho mejor)
Por persona: 1.5-2.5 horas (muy manejable)
```

**VENTAJAS**:
- ✅ Trabajo más rápido (2-3 días vs 4-5)
- ✅ Todos participan activamente
- ✅ Menos esperas entre tareas
- ✅ Mejor distribución de carga
- ✅ Más oportunidades de aprender juntos

---

## 🧪 TESTING MIENTRAS TRABAJAS

### Para Tiempos:
```python
# Al terminar un proceso, imprimir:
print(f"P{id}: t_arribo={t_arribo}, t_arribo_MP={t_arribo_MP}, " +
      f"t_espera={T_fin - t_arribo_MP}, t_retorno={T_fin - t_arribo_MP}")
```

### Para SRTF:
```python
# En cada ciclo, imprimir:
print(f"T={T}: P{id_actual} en CPU (TR={TR_actual}), " +
      f"Listos={[ids_en_listos]}")
# Si hay preempsión:
print(f"  → PREEMPSIÓN: P{id_nuevo} desaloja a P{id_actual}")
```

### Para Multiprogramación:
```python
# Antes de admitir, imprimir:
mp = len(listos) + len(suspendidos) + (1 si CPU)
print(f"T={T}: MP={mp}, Listos={len(listos)}, Suspendidos={len(suspendidos)}")
if mp >= 5:
    print(f"  → NO ADMITIR (MP={mp} >= 5)")
```

---

## 🔍 VERIFICACIÓN FINAL

Antes de entregar, chequear:

### ✅ Tiempos Correctos
- [ ] Campo `t_arribo_MP` existe en estructura de proceso
- [ ] Se registra cuando entra a listaListos
- [ ] Se usa en cálculos finales (no `t_arribo`)
- [ ] Resultados tienen sentido

### ✅ SRTF Implementado
- [ ] Loop avanza ciclo a ciclo, NO todo de una vez
- [ ] Se detectan arribi cada ciclo
- [ ] Se evalúa preempsión cada ciclo
- [ ] Procesos pueden ser desalojados
- [ ] Desalojados regresan a Listos

### ✅ Multiprogramación Validada
- [ ] Función de validación existe
- [ ] Se valida ANTES de cada admisión
- [ ] NUNCA excede 5 (probar los 3 lotes)
- [ ] Monitoreo muestra conteo correcto

### ✅ General
- [ ] Código compila sin errores
- [ ] Se probó con `procesos.csv`
- [ ] Se probó con `LOTE_1.csv`, `LOTE_2.csv`, `LOTE_3.csv`
- [ ] Resultados tienen sentido (mejores que antes)
- [ ] Profesora está satisfecha

---

## 📞 SI TE ATASCAS

1. **Pregunta 1**: ¿Dónde está `t_arribo` en el código?
   → Busca donde se crea proceso desde CSV

2. **Pregunta 2**: ¿Dónde se mueve a listaListos?
   → Función `mover_aColaListo()` o similar

3. **Pregunta 3**: ¿Dónde se calcula tiempo de espera AHORA?
   → Función que genera informe final

4. **Pregunta 4**: ¿Cuántas iteraciones hace el loop actualmente?
   → Abre proyecto mejorado y ve `ejecutarTodo()`

5. **Pregunta 5**: ¿Cómo se detectan nuevos arribi?
   → Mira `buscarSiguiente()` en proyecto mejorado

---

## 🎓 RECURSOS

- 📄 `PLAN_CORRECCIONES_ROUND_ROBIN.md` - Plan detallado
- 📄 `EJEMPLOS_VISUALES_CORRECCIONES.md` - Diagramas y ejemplos
- 📄 `MAPEO_PROYECTO_MEJORADO.md` - Referencias al código mejorado
- 📄 `EXPLICACION_FIFO.md` - Conceptos de FIFO/SRTF
- 📁 `trabajoPythonVisualStudioCode-SIMULADOR+MAS+EXPLICADO` - Proyecto mejorado (referencia)

---

## 💪 ¡VAMOS A HACERLO!

Este es un trabajo grande pero REALIZABLE. 

**Recuerda:**
- Dividir el trabajo
- Comunicarse en equipo
- Probar cada parte
- No copiar, aprender
- El proyecto mejorado es REFERENCIA, no solución

¡Éxito! 🚀

---

## 🔗 PRÓXIMOS PASOS

1. **HOY (30 min)**: Reunión de equipo
   - Todos leen este documento
   - Se asignan Personas A, B, C, D, E
   - A↔B se intercambian contacto
   - C↔D se intercambian contacto
   - Se define cómo compartir código (rama, archivo, etc)

2. **HOY (Tarde)**: Comienza DÍA 1
   - Personas A y C comienzan implementación EN PARALELO
   - Personas B, D, E se preparan leyendo

3. **MAÑANA (Mañana)**: Continúa DÍA 2
   - Personas B y D comienzan implementación EN PARALELO
   - Persona A y C preparan integración
   - Persona E implementa validación

4. **MAÑANA (Tarde - DÍA 2-3)**: Validación cruzada
   - Persona E valida todo

5. **PASADO (Mañana)**: Testing final
   - Persona E ejecuta tests
   - Todos validan resultados

6. **ENTREGAR**: Código funcional con 5 firmas

---

## 📞 COMUNICACIÓN DURANTE EL PROYECTO

- **Personas A ↔ B**: Llamadas/mensajes cada 30 min (coordinan Tiempos)
- **Personas C ↔ D**: Llamadas/mensajes cada 30 min (coordinan SRTF)
- **Persona E**: Avisa al grupo cuando está validando
- **Si algo rompe**: Reunión de 10 minutos (todos)
- **Fin de día**: Reunión corta (5 min) para resumir

---

## 📊 TABLA RESUMEN

| Persona | Tarea | Tiempo | Empieza | Depende de |
|---------|-------|--------|---------|-----------|
| A | Agregar `t_arribo_MP` | 1-2h | DÍA 1 tarde | Nada |
| B | Usar `t_arribo_MP` | 1-2h | DÍA 2 mañana | Persona A |
| C | Loop ciclo-a-ciclo | 1.5-2h | DÍA 1 tarde | Nada |
| D | Preempsión SRTF | 1.5-2h | DÍA 2 mañana | Persona C |
| E | Validación + Testing | 2-3h | DÍA 2 tarde | A, B, C, D |

**Duración total**: 2-3 días de calendario (no secuencial)

---

¿Preguntas? ¡Revisa los documentos primero! La respuesta probablemente está en:
- PLAN_CORRECCIONES_ROUND_ROBIN.md
- EJEMPLOS_VISUALES_CORRECCIONES.md
- MAPEO_PROYECTO_MEJORADO.md
