# 🏗️ ARQUITECTURA NUEVA: Refactorización Round Robin
## Guía de Refactorización Completa (No es 3 correcciones puntuales)

---

## 🎯 La Realidad

Lo que necesitan NO es "agregar campos" o "hacer ciclo a ciclo". Es una **refactorización arquitectónica completa** del flujo de ejecución.

**La profe pedía 3 cosas**, pero la arquitectura actual hace que sea imposible implementarlas correctamente sin rediseñar el sistema:

1. ✅ Tiempos correctos (`t_arribo_MP`)
2. ✅ SRTF con preempsión **REAL** (no SJF)
3. ✅ Multiprogramación <= 5 **en todo momento**

---

## 📋 La Arquitectura Actual (Round Robin) - ❌ PROBLEMA

```
FLUJO ACTUAL:
┌─────────────────┐
│ Lee procesos CSV│
└────────┬────────┘
         │
    ┌────▼──────────────────────┐
    │ Admisión (función separada)│
    │ [solo al inicio]           │
    └────┬─────────────────────┘
         │
    ┌────▼──────────────────┐
    │ Loop SRTF (función)   │
    │ [ejecuta TODO el proceso]
    │ [NO detecta arribi]   │
    └────┬─────────────────┘
         │
    ┌────▼──────────────────┐
    │ Multiprog (validación) │
    │ [separada del flujo]   │
    └────┬─────────────────┘
         │
    ┌────▼──────────────────┐
    │ Informe final         │
    │ [tiempos incorrectos] │
    └──────────────────────┘

PROBLEMAS:
- Admisión SOLO al inicio → No respeta multiprogramación en tiempo de ejecución
- Loop ejecuta TODO → No detecta arribi, no hay preempsión real
- Multiprog desacoplada → No se valida integrada
- Tiempos = t_arribo (CSV) → Debería ser t_arribo_MP
- Confunde "procesos no admitidos" con "procesos suspendidos"
  (nuevos deberían quedar en lista de NUEVOS, no ir a MS)
```

---

## ✅ LA ARQUITECTURA NUEVA (Funcionesándro_prolijo.py)

```
FLUJO NUEVO:
┌──────────────────────────┐
│ Inicializar estructuras  │
│ - Cola de Turnos         │
│ - Banderas de eventos    │
│ - Estado de MP/MS        │
└────────┬────────────────┘
         │
    ┌────▼─────────────────────────────┐
    │ CICLO PRINCIPAL (ciclo a ciclo)   │
    │                                   │
    │  T_Simulacion = 0                │
    │  while quedan_procesos:           │
    │    ┌─────────────────────────┐   │
    │    │ 1. Detectar eventos     │   │
    │    │    - ¿Hay arribos(T)?   │   │
    │    │    - ¿Hay terminación?  │   │
    │    │    - ¿Ambos?           │   │
    │    └────────┬────────────────┘   │
    │             │                     │
    │    ┌────────▼────────────────┐   │
    │    │ 2. Ejecutar Admisión    │   │
    │    │    (si hay eventos)      │   │
    │    │    - ADMICION_MULTI_5() │   │
    │    │    - Validar MP <= 5    │   │
    │    │    - Actualizar colas   │   │
    │    └────────┬────────────────┘   │
    │             │                     │
    │    ┌────────▼────────────────┐   │
    │    │ 3. Ejecutar SRTF        │   │
    │    │    (si hay proceso)      │   │
    │    │    - Elige de cola turnos│   │
    │    │    - Ejecuta 1 ciclo     │   │
    │    │    - Chequea preempsión  │   │
    │    └────────┬────────────────┘   │
    │             │                     │
    │    ┌────────▼────────────────┐   │
    │    │ 4. Mostrar tablas       │   │
    │    │    (si banderas activas) │   │
    │    │    - Solo en eventos    │   │
    │    └────────┬────────────────┘   │
    │             │                     │
    │    ┌────────▼────────────────┐   │
    │    │ 5. Incrementar tiempo   │   │
    │    │    T_Simulacion += 1    │   │
    │    └────────┬────────────────┘   │
    │             │                     │
    │    repetir...                    │
    └─────────────┬────────────────────┘
         │
    ┌────▼──────────────────┐
    │ Informe final         │
    │ [tiempos correctos]   │
    └──────────────────────┘

VENTAJAS:
✅ Ciclo unitario → Detecta arribi en cada instante
✅ Admisión integrada → Respeta multiprog en todo momento
✅ Cola de turnos separada → SRTF funciona realmente
✅ Banderas de eventos → Solo muestra info relevante
✅ Tiempos = t_arribo_MP → Calculados correctamente
```

---

## 🔧 Componentes a Implementar (ORDEN IMPORTANTE)

### **FASE 1: CICLOS DE TIEMPO** (Responsable: Persona A)
- Convertir loop de "ejecuta todo el proceso" a "incrementa 1 ciclo de tiempo"
- Que el tiempo avance UNITARIAMENTE (T=0, T=1, T=2, ...)
- Detectar **EVENTOS** en cada ciclo: ¿Hay arribi en T? ¿Termina algo?

### **FASE 2: COLA DE TURNOS** (Responsable: Persona B)
- Crear estructura separada de listaListos
- Cola de Turnos = FIFO de procesos listos en CPU (máx 3)
- Esta cola se usa SOLO para SRTF, no es listaListos
- Mantener sincronización: Cola de Turnos ⊂ listaListos

### **FASE 3: SRTF PREEMPTIVO** (Responsable: Persona C)
- Usar Cola de Turnos para elegir proceso (menor t_RestanteCPU)
- En cada ciclo: ¿Hay preempsión? (¿Llegó uno con TR < actual?)
- Ejecutar SOLO 1 ciclo del proceso, luego SALIR del loop

### **FASE 4: MULTIPROGRAMACIÓN INTEGRADA** (Responsable: Persona D)
- ADMICION_MULTI_5() funciona en cada evento (no solo inicio)
- Valida: `len(colaListos) + len(listaSuspendidos) <= 5`
- Revisa cola de turnos + suspendidos para decidir

### **FASE 5: BANDERAS DE EVENTOS** (Responsable: Persona E + Testing)
- Agregar banderas: `hay_arribi`, `hay_terminacion`, `mostrar_tablas`
- Solo mostrar info cuando cambió algo
- Validar tiempos con `t_arribo_MP`

---

## 📚 Documentos que Crearemos

1. **Este documento** (arquitectura general)
2. **GUIA_CICLOS_DE_TIEMPO.md** → Cómo implementar incremento unitario
3. **GUIA_COLA_DE_TURNOS.md** → Estructura y sincronización
4. **GUIA_SRTF_PREEMPTIVO.md** → Cómo implementar preempsión REAL
5. **GUIA_MULTIPROG_INTEGRADA.md** → Validación en tiempo de ejecución
6. **GUIA_BANDERAS_EVENTOS.md** → Sistema de eventos
7. **GUIA_INVESTIGACION_PROLIJO.md** → Cómo leer funcionesLisandro_prolijo.py

---

## 🗺️ Dónde Investigar en funcionesLisandro_prolijo.py

NO COPIEN. INVESTIGUEN:

### Para CICLOS:
- Buscar: cómo se incrementa T_Simulacion
- Preguntar: ¿Dónde ocurre el loop principal?
- Notar: ¿Cuántos ciclos se ejecutan por iteración?

### Para COLA DE TURNOS:
- Buscar: estructura separada de listaListos
- Preguntar: ¿Cómo se diferencia de admisión?
- Notar: ¿Cuántos procesos máximo?

### Para SRTF:
- Buscar: función que elige proceso (menor TR)
- Preguntar: ¿Cómo se compara t_RestanteCPU?
- Notar: ¿Se ejecuta 1 ciclo o todo de una vez?

### Para MULTIPROG:
- Buscar: dónde se valida len(listos) + len(suspendidos)
- Preguntar: ¿Cuándo se ejecuta esta validación?
- Notar: ¿Se integra con admisión?

### Para BANDERAS:
- Buscar: variables booleanas para eventos
- Preguntar: ¿Cuándo se activan/desactivan?
- Notar: ¿Cuándo se muestran las tablas?

---

## ✨ Lo Importante

**Esto es INVESTIGACIÓN DIRIGIDA, no "copia y pega".**

Cada persona:
1. Lee su guía de componente
2. Busca en funcionesLisandro_prolijo.py
3. ENTIENDE el concepto
4. Implementa SU VERSION en TPI_Listo.py

El objetivo NO es que sea igual, es que sea **correcto y funcione** como describe la profe.

---

## 📅 Orden de Implementación

1. **CICLOS** (FASE 1) → Base de todo
2. **COLA DE TURNOS** (FASE 2) → Estructura para SRTF
3. **SRTF** (FASE 3) → Usar cola de turnos
4. **MULTIPROG** (FASE 4) → Se integra con todo
5. **BANDERAS** (FASE 5) → Última capa

**No intenten hacer todo a la vez.** Una fase depende de la anterior.

