# PLAN DE CORRECCIONES PARA ROUND ROBIN
## Guía de Trabajo para Corregir los Problemas Identificados

---

## ANÁLISIS DE LOS 3 PROBLEMAS PRINCIPALES

### 📋 Problema 1: TIEMPOS DE RETORNO Y ESPERA (Cálculo Incorrecto)

#### ❌ Problema Identificado
- **Dónde está**: Cálculo actual usa `t_arribo` (arribo al sistema desde CSV)
- **Por qué es malo**: Los tiempos deben calcularse desde **t_arribo a la cola de Listos** (cuando realmente entra a MP)
- **Impacto**: Los promedios de retorno y espera son INCORRECTOS, invalidan toda la simulación

#### ✅ Concepto Correcto (en proyecto mejorado)

**En el proyecto mejorado** (`SIMULADOR.py` y `funcionesLisandro_prolijo.py`):
```
- t_arribo: cuando llega al sistema (CSV)
- t_arribo_MP: cuando REALMENTE entra a memoria principal (listaListos)
  → Este es el punto desde el que se calcula espera y retorno
```

**Campos que necesitas agregar:**
```python
"t_arribo_MP": None  # ← Registrar CUÁNDO entra a listaListos
```

#### 🔧 Pasos para Corregir

**Paso 1.1**: En la estructura de proceso, agregar campo `t_arribo_MP`
- Cuando creas un proceso, inicializa: `"t_arribo_MP": None`

**Paso 1.2**: Al mover a listaListos, registrar el tiempo
- Cuando `mover_aColaListo()` ocurra (o equivalente), guardar:
  ```
  proceso["t_arribo_MP"] = T_Simulacion  # tiempo actual
  ```

**Paso 1.3**: Recalcular tiempos finales usando `t_arribo_MP`
- En el informe final, en lugar de:
  ```python
  # MAL:
  t_espera = T_Simulacion - proceso["t_arribo"]
  ```
  
- Hacer:
  ```python
  # CORRECTO:
  t_espera = T_Simulacion - proceso["t_arribo_MP"]
  t_retorno = T_Simulacion - proceso["t_arribo_MP"]
  ```

**Paso 1.4**: Validar en tablas intermedias
- Las tablas que muestran estado de listos y suspendidos deben mostrar `t_arribo_MP`
- Ver función `mostrarColaListos()` en proyecto mejorado

#### 📌 Archivos a revisar en proyecto mejorado
- `SIMULADOR.py` línea ~150-200: ver cómo se registra `t_arribo_MP`
- `funcionesLisandro_prolijo.py` función `mover_aColaListo()`: ver dónde se asigna
- `funcionesLisandro_prolijo.py` función `mover_aColaTerminados()`: ver recálculo de tiempos

---

### 📋 Problema 2: SRTF CON PREEMPSIÓN (No está implementado)

#### ❌ Problema Identificado
- **Dónde está**: El loop principal avanza tiempo hasta que termina el proceso COMPLETO
- **Por qué es malo**: NO permite:
  - Detectar llegadas intermedias de procesos
  - Evaluar preempsión (desalojo) cuando llega un proceso con menor TR
  - Es SJF (shortest job first), NO SRTF (shortest remaining time first)

#### ✅ Concepto Correcto (en proyecto mejorado)

**En SRTF con preempsión:**
```
Tiempo 0: Ejecuta P1 (TR=10)
Tiempo 3: LLEGA P2 (TR=2)
         - Se DETECTA la llegada
         - Se compara: TR_P2 (2) < TR_P1 (7)
         - P2 DESALOJA a P1 de CPU
         - P1 regresa a LISTOS con TR=7
         - P2 entra a CPU

Tiempo 5: P2 termina
         - P1 regresa a CPU con TR=7
```

**Lo que hace el Round Robin actual:**
```
Tiempo 0: Ejecuta P1 (TR=10)
         [AVANZA DIRECTAMENTE A TIEMPO 10]
Tiempo 10: P1 termina
          [NO se enteró que P2 llegó en tiempo 3]
```

#### 🔧 Pasos para Corregir

**Paso 2.1**: Cambiar estructura del loop principal
- En lugar de avanzar hasta que termina el proceso:
  ```python
  # MAL (actual):
  while proceso.t_RestanteCPU > 0:
      proceso.t_RestanteCPU -= 1
      # [después] busca siguiente
  
  # CORRECTO (SRTF):
  while proceso.t_RestanteCPU > 0:
      proceso.t_RestanteCPU -= 1
      T_Simulacion += 1
      
      # Detectar si hay ARRIBO EN ESTE CICLO
      siguiente = buscarSiguiente()
      if siguiente llega en T_Simulacion:
          # Evaluar preempsión SRTF aquí
          if siguiente.t_RestanteCPU < proceso.t_RestanteCPU:
              # DESALOJAR proceso actual
              # Poner siguiente en CPU
              break  # salir del while, siguiente en CPU
  ```

**Paso 2.2**: Función `buscarSiguiente()` debe detectar ESTE CICLO
- Buscar proceso que llega EN el instante actual (T_Simulacion)
- NO necesita ser el próximo, solo los del instante actual

**Paso 2.3**: Evaluar preempsión SRTF cada ciclo
- Comparar: `proceso_nuevo.t_RestanteCPU < proceso_en_cpu.t_RestanteCPU`
- Si es verdad, DESALOJAR y llevar nuevo a CPU
- El anterior regresa a LISTOS con TR actualizado

**Paso 2.4**: Manejar múltiples llegadas en un instante
- Si llegan varios procesos en el MISMO INSTANTE:
  - Admitirlos todos (ADMICION_MULTI_5)
  - Elegir el de menor TR con BuscarSRTF()
  - Si ese tiene TR < proceso_en_cpu, hacer preempsión

#### 📌 Archivos a revisar en proyecto mejorado
- `SIMULADOR.py` función `ejecutarTodo()` líneas 95-205:
  - Ver cómo se maneja el loop CICLO A CICLO (no todo de una vez)
  - Ver detección de arribos DENTRO del loop
  - Ver preempsión SRTF en líneas ~170-190

- `SIMULADOR.py` función `buscarSiguiente()` líneas 220-270:
  - Ve que recorre `listaProcesos` para detectar el próximo
  - Compara `t_arribo <= T_simulador`

- Buscar comentarios "APROPIACION" en SIMULADOR.py
  - Muestra exactamente cómo se implementa preempsión

---

### 📋 Problema 3: CONTROL DE MULTIPROGRAMACIÓN (No se valida correctamente)

#### ❌ Problema Identificado
- **Restricción**: `(Ejecución + Listos + Listos/Suspendidos) <= 5` EN TODO MOMENTO
- **Dónde falla**: Probablemente en función de admisión (no valida antes de admitir)
- **Impacto**: Se admiten más de 5 procesos simultáneamente

#### ✅ Concepto Correcto

**La fórmula ES:**
```python
multiprogramacion = len(listaListos) + len(listaSuspendidos) + (1 si hay proceso en CPU else 0)
                  = len(listaListos) + len(listaSuspendidos) + (1 o 0)
```

**Nunca debe exceder 5:**
```
Ejemplo válido:
- CPU: 1 proceso (P1 en ejecución)
- Listos: 2 procesos (P2, P3 esperando CPU)
- Suspendidos: 2 procesos (P4, P5 en MS esperando espacio en MP)
- Total: 1 + 2 + 2 = 5 ✓ VÁLIDO

Ejemplo INVÁLIDO (lo que pasa ahora):
- CPU: 1 proceso
- Listos: 3 procesos (DEMASIADOS para MP)
- Suspendidos: 2 procesos
- Total: 1 + 3 + 2 = 6 ✗ INCORRECTO
```

#### 🔧 Pasos para Corregir

**Paso 3.1**: Entender dónde se calcula multiprogramacion
- Busca en TPI_Listo.py dónde se incrementa/decrementa
- Probablemente en función de admisión

**Paso 3.2**: Revisar función de admisión
- Debe VALIDAR ANTES de admitir:
  ```python
  # ANTES de mover a listaListos:
  if len(listaListos) + len(listaSuspendidos) < 5:
      # Permitir admisión
      if cabe_en_particion():
          mover_aColaListo(proceso)
      else:
          mover_aColaSuspendido(proceso)
  else:
      # NO permitir, ignorar proceso por ahora
  ```

**Paso 3.3**: Validar la restricción de proceso en CPU
- Cuando proceso entra a CPU, ese conteo TAMBIÉN cuenta hacia los 5
- Cuando termina, libera un "slot"

**Paso 3.4**: Implementar función de validación
```python
def validar_multiprogramacion():
    """Retorna True si multiprogramacion <= 5"""
    mp = len(listaListos) + len(listaSuspendidos)
    # Agregar 1 si hay proceso en CPU
    if hay_proceso_en_cpu:
        mp += 1
    return mp <= 5
```

**Paso 3.5**: Llamar ANTES de cualquier admisión
- En admisión, validar: `if validar_multiprogramacion():`
- En CARGAR_MPconMS (traer de MS a MP), también validar

#### 📌 Archivos a revisar en proyecto mejorado
- `SIMULADOR.py` línea ~155: Ver cómo se valida `vGlobal.multiprogramacion < 5`
- `funcionesLisandro_prolijo.py` función `ADMICION_MULTI_5()` líneas 585-614:
  - Ver validación antes de cada admisión
  - Ver cómo se actualiza multiprogramacion

- `funcionesLisandro_prolijo.py` función `CARGAR_MPconMS()` líneas 570-583:
  - Ver que también valida multiprogramacion

---

## RESUMEN DE CAMBIOS NECESARIOS

| Aspecto | Cambio | Archivo | Función |
|---------|--------|---------|---------|
| **Tiempos** | Agregar `t_arribo_MP` | TPI_Listo.py | Donde se crea proceso |
| **Tiempos** | Registrar cuando entra a Listos | TPI_Listo.py | `mover_aColaListo()` |
| **Tiempos** | Recalcular usando `t_arribo_MP` | TPI_Listo.py | `informe_final()` |
| **SRTF** | Cambiar loop a CICLO A CICLO | TPI_Listo.py | Función principal |
| **SRTF** | Detectar arribi cada ciclo | TPI_Listo.py | Loop de ejecución |
| **SRTF** | Evaluar preempsión cada ciclo | TPI_Listo.py | Loop de ejecución |
| **Multiprog** | Validar ANTES de admitir | TPI_Listo.py | `ADMICION()` |
| **Multiprog** | Validar en CARGAR_MPconMS | TPI_Listo.py | `CARGAR_MPconMS()` |

---

## ESTRATEGIA DE TRABAJO EN EQUIPO

### Fase 1: Preparación (1-2 horas)
1. **Todos leen** el documento EXPLICACION_FIFO.md (proyecto mejorado)
2. **Todos leen** este plan de correcciones
3. **Dividen roles**:
   - Persona A: Correcciones de Tiempos
   - Persona B: Correcciones de SRTF
   - Persona C: Correcciones de Multiprogramación

### Fase 2: Implementación (3-4 horas)
1. Cada persona trabaja en su sección
2. Realizan cambios basados en el proyecto mejorado como REFERENCIA
3. Prueban con archivo `procesos.csv` simple

### Fase 3: Integración y Testing (2 horas)
1. Ejecutan todos juntos
2. Verifican con los 3 lotes de prueba
3. Comparan resultados con proyecto mejorado

### Fase 4: Validación (1 hora)
1. Verifican que cumplan las 3 correcciones
2. Validan tiempos, SRTF, multiprogramación

---

## PREGUNTAS CLAVE QUE DEBEN RESPONDER

Antes de empezar cada corrección, respondan:

### Para Corrección 1 (Tiempos):
- [ ] ¿Dónde en el código se crea un nuevo proceso? 
- [ ] ¿Dónde se mueve a listaListos?
- [ ] ¿Dónde se calcula tiempo de espera AHORA?
- [ ] ¿Qué valor de tiempo debería usar CORRECTAMENTE?

### Para Corrección 2 (SRTF):
- [ ] ¿Cuántas iteraciones hace el loop AHORA?
- [ ] ¿En qué momento se detectan nuevos arribi?
- [ ] ¿Dónde se evalúa si hay preempsión?
- [ ] ¿Qué sucede si un proceso llega en el medio de la ejecución de otro?

### Para Corrección 3 (Multiprogramación):
- [ ] ¿Cómo se cuenta actualmente la multiprogramación?
- [ ] ¿Se valida ANTES de cada admisión?
- [ ] ¿Qué sucede cuando multiprogramación == 5 y llega otro proceso?

---

## REFERENCIAS PUNTUALES DEL PROYECTO MEJORADO

### Para Tiempos:
📄 `SIMULADOR.py` líneas 144-159 (mover_aColaListo con t_arribo_MP)
📄 `EXPLICACION_FIFO.md` sección 9 (tabla de campos que rastrean FIFO)

### Para SRTF:
📄 `SIMULADOR.py` líneas 95-210 (ejecutarTodo con ciclo a ciclo)
📄 `SIMULADOR.py` líneas 236-270 (buscarSiguiente detectando arribi)
📄 Buscar "APROPIACION" en SIMULADOR.py

### Para Multiprogramación:
📄 `SIMULADOR.py` línea 155 (validación multiprogramacion < 5)
📄 `funcionesLisandro_prolijo.py` líneas 585-614 (ADMICION_MULTI_5 con validación)

---

## CHECKLIST DE VALIDACIÓN FINAL

Antes de entregar, validen:

### ✓ Tiempos Corregidos
- [ ] `t_arribo_MP` se registra cuando entra a Listos
- [ ] Tiempos de espera se calculan desde `t_arribo_MP`
- [ ] Tiempos de retorno se calculan desde `t_arribo_MP`
- [ ] Informe final muestra tiempos correctos

### ✓ SRTF con Preempsión
- [ ] Loop ejecuta CICLO A CICLO, no todo de una vez
- [ ] Se detectan arribi en CADA CICLO
- [ ] Se evalúa preempsión en CADA CICLO
- [ ] Un proceso puede ser desalojado por otro con menor TR
- [ ] El desalojado regresa a Listos

### ✓ Multiprogramación Validada
- [ ] (Ejecución + Listos + Suspendidos) nunca > 5
- [ ] Se valida ANTES de admitir
- [ ] Se actualiza correctamente al admitir/terminar

### ✓ General
- [ ] Código compila sin errores
- [ ] Se prueba con los 3 lotes
- [ ] Resultados tienen sentido
- [ ] Profesora está satisfecha 😊

---

## NOTAS IMPORTANTES

⚠️ **NO copiar código del proyecto mejorado**
- Usarlo como REFERENCIA conceptual
- Escribir el código ustedes para aprender

⚠️ **Mantener estructura original del Round Robin**
- Solo hacer cambios necesarios para las correcciones
- No refactorizar todo el código

⚠️ **Probar DURANTE el proceso**
- No dejar todo para el final
- Verificar cada corrección funciona

⚠️ **Comunicación en equipo**
- Coordinar cambios para evitar conflictos
- Revisar mutuamente el código

---

## PRÓXIMOS PASOS

1. **Hoy**: Leer plan + entender los 3 problemas
2. **Mañana**: Implementar Corrección 1 (Tiempos)
3. **Mañana + tarde**: Implementar Corrección 2 (SRTF)
4. **Pasado mañana**: Implementar Corrección 3 (Multiprogramación)
5. **Pasado mañana + tarde**: Testing + validación
6. **Entregar**: Código limpio y documentado

¡ÉXITO! 💪
