# 🚀 QUICK START - 15 MINUTOS

## LEE ESTO EN LOS PRÓXIMOS 15 MINUTOS

---

## 1️⃣ LOS 3 PROBLEMAS (2 min)

### Problema 1: TIEMPOS INCORRECTOS
```
❌ Usan: t_arribo (del CSV, cuando escriben el proceso)
✅ Deben: t_arribo_MP (cuándo entra realmente a MP)

EJEMPLO:
P1 llega CSV en T=0, pero multiprog lleno
P1 espera en MS hasta T=4 (ahora hay espacio)
❌ Tiempo espera = 4 - 0 = 4 (MALO, usa CSV)
✅ Tiempo espera = 4 - 4 = 0 (BUENO, usa MP entry)
```

### Problema 2: NO SRTF PREEMPTIVO
```
❌ Ejecutan proceso completo de una vez
✅ Deben ejecutar 1 ciclo, detectar preempsión

EJEMPLO:
P1(TR=5) está ejecutando
T=3: Llega P2(TR=2) más corto
❌ P1 sigue hasta terminar (5 ciclos más)
✅ P1 se desaloja, ejecuta P2 inmediatamente
```

### Problema 3: MULTIPROG SIN VALIDAR
```
❌ No validan límite 5 procesos
✅ Deben validar: len(listaListos) + len(suspendidos) <= 5 SIEMPRE

EJEMPLO:
Hay 5 procesos en multiprog, llega el 6to
❌ Lo admiten (¡ILEGAL!)
✅ Se queda en lista de procesos NUEVOS (no admitidos)
   Cuando termina un proceso admitido → libera espacio
   Recién ENTONCES se admite el pendiente
   
NOTA: cola_turnos = listaListos (mismo, diferente nombre)
```

---

## 2️⃣ LA SOLUCIÓN: 5 FASES (5 min)

```
FASE 1 (Persona A)
├─ Cambiar de: "ejecutar proceso completo"
└─ A: "ejecutar 1 ciclo por iteración"
   └─ Permite: detectar eventos

FASE 2 (Persona B) [Después de A]
├─ Crear: "cola_turnos" separada
└─ Ordenada: por SRTF (mín TR primero)
   └─ Permite: preempsión y multiprog

FASE 3 (Persona C) [Después de B]
├─ Ejecutar: 1 ciclo nada más
└─ Detectar: preempsión (nuevo < actual)
   └─ Permite: SRTF real

FASE 4 (Persona D) [Después de C]
├─ Validar: len(cola) + len(suspendidos) <= 5
└─ Integrar: en cada ciclo (no al inicio)
   └─ Permite: multiprogramación correcta

FASE 5 (Persona E) [Después de D]
├─ Flags: hay_arribi, hay_terminacion
├─ Mostrar: solo si eventos
└─ Integrar: t_arribo_MP en TODOS
   └─ Permite: tiempos correctos + display claro
```

---

## 3️⃣ CÓMO EMPEZAR HOY (8 min)

### PASO 1: MIRA LA CARPETA

Verifica que existan estos archivos:
- ✅ !ENTREGA_COMPLETA.md
- ✅ RESUMEN_REFACTORIZACION.md
- ✅ INDICE_MAESTRO.md
- ✅ COORDINACION_5_INTEGRANTES.md
- ✅ 0_ARQUITECTURA_NUEVA.md
- ✅ 1_GUIA_CICLOS_DE_TIEMPO.md (→ Persona A)
- ✅ 2_GUIA_COLA_DE_TURNOS.md (→ Persona B)
- ✅ 3_GUIA_SRTF_PREEMPTIVO.md (→ Persona C)
- ✅ 4_GUIA_MULTIPROG_INTEGRADA.md (→ Persona D)
- ✅ 5_GUIA_BANDERAS_EVENTOS.md (→ Persona E)

### PASO 2: ORDEN DE LECTURA (3 minutos por doc)

**HOY:**
```
1. Este archivo (quick start)
2. !ENTREGA_COMPLETA.md (5 min, resumen qué se entrega)
```

**MAÑANA (TODOS):**
```
3. COORDINACION_5_INTEGRANTES.md (10 min, cómo trabajan juntos)
4. 0_ARQUITECTURA_NUEVA.md (20 min, por qué cambiar)
```

**LUEGO:**
```
5. Cada persona su guía:
   - A: 1_GUIA_CICLOS_DE_TIEMPO.md
   - B: 2_GUIA_COLA_DE_TURNOS.md
   - C: 3_GUIA_SRTF_PREEMPTIVO.md
   - D: 4_GUIA_MULTIPROG_INTEGRADA.md
   - E: 5_GUIA_BANDERAS_EVENTOS.md
```

### PASO 3: IMPLEMENTAR

**Semana 1:** Persona A implementa (3-4 horas)  
**Semana 2:** Persona B implementa (2-3 horas, después de A)  
**Semana 2:** Persona C implementa (3-4 horas, después de B)  
**Semana 3:** Persona D implementa (3-4 horas, después de C)  
**Semana 3:** Persona E implementa (2-3 horas, después de D)  

**Final:**
```bash
python TPI_Listo.py < Lote_1.csv
python TPI_Listo.py < Lote_2.csv
python TPI_Listo.py < Lote_3.csv
```

---

## 4️⃣ NO OLVIDES (2 min)

### ⭐ REGLA ORO
**NO COPIES CÓDIGO**

→ Investiga cómo funciona en funcionesLisandro_prolijo.py  
→ Entiende el concepto  
→ Implementa TU VERSIÓN

### ⚠️ REGLA FASES
**NO SALTES ORDEN**

→ A debe terminar antes de B  
→ B debe terminar antes de C  
→ C debe terminar antes de D  
→ D debe terminar antes de E  

**RAZÓN:** Cada fase usa output de la anterior

### ✅ REGLA TESTS
**TODO TIENE TESTS**

Cada guía incluye 3-4 tests  
Corre los tests para verificar que funciona  
No avances sin pasar tests

---

## 🎯 TU CHECKLIST PARA HOY

- [ ] Leí este documento (quick start)
- [ ] Verifiqué que los 11 documentos existen
- [ ] Comprendí los 3 problemas
- [ ] Comprendí las 5 fases
- [ ] Voy a leer !ENTREGA_COMPLETA.md (próximo paso)

---

## 📞 QUICK HELP

**"¿Dónde empiezo?"**  
→ Lee !ENTREGA_COMPLETA.md

**"¿Cuánto tiempo toma?"**  
→ 3 semanas distribuidas (13-18 horas totales)

**"¿Puedo trabajar mientras otros no terminen?"**  
→ SÍ: Investiga tu guía, prepara tests, escribe pseudocódigo

**"¿Mi código tiene que ser igual al mejorado?"**  
→ NO: Investiga CÓMO lo hace, implementa diferente pero que funcione

**"¿Qué pasa si alguien se atrasa?"**  
→ Ver COORDINACION_5_INTEGRANTES.md, sección "Problemas frecuentes"

---

## 🚀 SIGUIENTE ACCIÓN

**Abre ahora:** `!ENTREGA_COMPLETA.md`

Está en la misma carpeta.

---

**TIEMPO TOTAL LECTURA: ~15 minutos**

✅ Comprendiste los 3 problemas  
✅ Comprendiste las 5 fases  
✅ Sabes dónde empezar  
✅ Listo para mañana
