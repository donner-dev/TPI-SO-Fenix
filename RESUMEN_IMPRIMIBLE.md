# 📊 RESUMEN IMPRIMIBLE: PLAN DE CORRECCIONES
## Una página para imprimir y llevar

---

## LAS 3 CORRECCIONES NECESARIAS

### ❌ PROBLEMA 1: TIEMPOS INCORRECTOS
**Causa**: Se usa `t_arribo` (del CSV) en lugar de `t_arribo_MP` (entrada real a MP)

**Solución rápida**:
1. Agregar `"t_arribo_MP": None` al crear proceso
2. En `mover_aColaListo()`: `proceso["t_arribo_MP"] = T_Simulacion`
3. En cálculos finales: usar `T - t_arribo_MP` en lugar de `T - t_arribo`

**Archivo**: `TPI_Listo.py`
**Tiempo**: 2-3 horas

---

### ❌ PROBLEMA 2: NO HAY PREEMPSIÓN SRTF
**Causa**: Loop ejecuta todo el proceso de una vez (es SJF)

**Solución rápida**:
1. Cambiar while a ciclo a ciclo: agregar `T_Simulacion += 1` dentro
2. En cada ciclo: detectar arribi con `buscarSiguiente()`
3. En cada ciclo: evaluar preempsión comparando `t_RestanteCPU`
4. Si `nuevo < actual` → desalojar actual, poner nuevo

**Archivo**: `TPI_Listo.py`
**Tiempo**: 3-4 horas

---

### ❌ PROBLEMA 3: MULTIPROGRAMACIÓN SIN VALIDAR
**Causa**: No se verifica que (CPU + Listos + Suspendidos) <= 5

**Solución rápida**:
1. Crear función `validar_multiprogramacion()`
2. Antes de cada admisión: `if mp >= 5: return`
3. En `CARGAR_MPconMS()`: también validar
4. Monitorear en debug para verificar

**Archivo**: `TPI_Listo.py`
**Tiempo**: 2-3 horas

---

## DISTRIBUCIÓN DE TRABAJO

| Persona | Tarea | Tiempo | Documentos |
|---------|-------|--------|-----------|
| **A** | Tiempos | 2-3h | PLAN sección 1 + MAPEO sección 1 |
| **B** | SRTF | 3-4h | PLAN sección 2 + MAPEO sección 2 |
| **C** | Multiprog | 2-3h | PLAN sección 3 + MAPEO sección 3 |
| **Todos** | Testing | 2-3h | EJEMPLOS_VISUALES.md |

**TOTAL**: ~13-16 horas

---

## CAMBIOS DE CÓDIGO (RESUMEN)

### TIEMPOS
```python
# 1. Agregar campo
proceso = {"t_arribo_MP": None, ...}

# 2. Registrar entrada
def mover_aColaListo(proceso):
    proceso["t_arribo_MP"] = T_Simulacion  # ← NUEVA LÍNEA
    listaMP_listos.append(proceso)

# 3. Usar en cálculos
t_espera = T_fin - proceso["t_arribo_MP"]  # ← NO t_arribo
t_retorno = T_fin - proceso["t_arribo_MP"]
```

### SRTF
```python
# 1. Ciclo a ciclo
while proceso["t_RestanteCPU"] > 0:
    proceso["t_RestanteCPU"] -= 1
    T_Simulacion += 1  # ← NUEVA LÍNEA
    
    # 2. Detectar arribi
    siguiente = buscarSiguiente()
    if siguiente and siguiente["t_arribo"] == T_Simulacion:
        ADMICION()
        
        # 3. Evaluar preempsión
        proximo = BuscarSRTF()
        if proximo and proximo["t_RestanteCPU"] < proceso["t_RestanteCPU"]:
            [desalojar y cambiar]
            break
```

### MULTIPROGRAMACIÓN
```python
# 1. Validar función
def validar_multiprogramacion():
    mp = len(listos) + len(suspendidos)
    if en_cpu: mp += 1
    return mp

# 2. Validar antes de admitir
def ADMICION():
    if validar_multiprogramacion() >= 5:
        return  # ← NUEVA LÍNEA
    
    for proceso in nuevos:
        if validar_multiprogramacion() >= 5:  # ← NUEVA LÍNEA
            break
        # admitir...
```

---

## VALIDACIÓN RÁPIDA

| Test | Esperado | Comando |
|------|----------|---------|
| **Tiempos** | `t_arribo_MP != None` | Ver que se registra |
| **Tiempos** | `t_retorno = T_fin - t_arribo_MP` | Calcular manualmente |
| **SRTF** | Tiempo total < antes | Comparar con SJF |
| **SRTF** | Hay preempsiones | Ver print "PREEMPSIÓN" |
| **Multiprog** | `mp <= 5` siempre | Monitorear cada ciclo |

---

## REFERENCIAS CLAVE

### En Proyecto Mejorado (`SIMULADOR.py`):
- **Tiempos**: `funcionesLisandro_prolijo.py` L180 `mover_aColaListo()`
- **SRTF**: `SIMULADOR.py` L95-220 `ejecutarTodo()`
- **Detección**: `SIMULADOR.py` L236-270 `buscarSiguiente()`
- **Preempsión**: Buscar "APROPIACION" en `SIMULADOR.py`
- **Multiprog**: `funcionesLisandro_prolijo.py` L585 `ADMICION_MULTI_5()`

---

## DOCUMENTOS DISPONIBLES

```
📁 trabajosSO/corrigiendo-TPI-SIMULADOR-SO/

├─ 📄 INICIO_RAPIDO.md
│  └─ COMIENZA AQUÍ
│
├─ 📄 PLAN_CORRECCIONES_ROUND_ROBIN.md
│  └─ Plan detallado (3 secciones)
│
├─ 📄 EJEMPLOS_VISUALES_CORRECCIONES.md
│  └─ Diagramas y ejemplos código
│
├─ 📄 MAPEO_PROYECTO_MEJORADO.md
│  └─ Referencias exactas al código mejorado
│
├─ 📄 ARBOL_DECISION_IMPLEMENTACION.md
│  └─ Paso a paso visual
│
└─ 📄 RESUMEN_IMPRIMIBLE.md (este)
   └─ Una página rápida
```

---

## ORDEN DE LECTURA RECOMENDADO

1. **ESTE DOCUMENTO** (5 min) ← Estás aquí
2. **INICIO_RAPIDO.md** (15 min)
3. **PLAN_CORRECCIONES_ROUND_ROBIN.md** (30 min, TU SECCIÓN)
4. **MAPEO_PROYECTO_MEJORADO.md** (20 min, TU SECCIÓN)
5. **EJEMPLOS_VISUALES_CORRECCIONES.md** (cuando necesites)
6. **ARBOL_DECISION_IMPLEMENTACION.md** (mientras implementas)

---

## CRONOGRAMA MÍNIMO

```
📅 DÍA 1 - Lunes
├─ 14:00-15:00: Leer documentos (TODOS)
├─ 15:00-18:00: Persona A implementa Tiempos
└─ 18:00+: Revisar avance

📅 DÍA 2 - Martes
├─ 10:00-13:00: Persona B implementa SRTF
├─ 13:00-16:00: Persona C implementa Multiprog
└─ 16:00+: Testing individual

📅 DÍA 3 - Miércoles
├─ 10:00-11:00: Integración del código
├─ 11:00-12:00: Testing con LOTE_1, LOTE_2, LOTE_3
├─ 12:00-13:00: Fixes finales
└─ 13:00+: LISTO para entregar
```

---

## CHECKLIST DE ENTREGA

- [ ] Tiempos calculan desde `t_arribo_MP`
- [ ] SRTF funciona ciclo a ciclo
- [ ] Hay preempsiones visibles
- [ ] Multiprogramación nunca > 5
- [ ] Código compila sin errores
- [ ] Probado con procesos.csv
- [ ] Probado con LOTE_1.csv
- [ ] Probado con LOTE_2.csv
- [ ] Probado con LOTE_3.csv
- [ ] Resultados mejoran respecto a antes
- [ ] Código está comentado
- [ ] NO hay código copiado (referenciado sí)
- [ ] Listo para presentar

---

## AYUDA RÁPIDA

| Pregunta | Respuesta |
|----------|-----------|
| ¿Por dónde empiezo? | INICIO_RAPIDO.md |
| ¿Qué tengo que hacer exactamente? | PLAN_CORRECCIONES_ROUND_ROBIN.md |
| ¿Dónde está la respuesta en el código mejorado? | MAPEO_PROYECTO_MEJORADO.md |
| ¿Cómo se vería el código correcto? | EJEMPLOS_VISUALES_CORRECCIONES.md |
| ¿Cuál es el siguiente paso? | ARBOL_DECISION_IMPLEMENTACION.md |

---

## RECUERDA

✅ Dividir el trabajo entre 3 personas
✅ Comunicarse frecuentemente
✅ Probar mientras implementas
✅ El proyecto mejorado es REFERENCIA, NO solución
✅ Aprender es más importante que copiar
✅ Cuando termines, profe estará feliz 😊

---

## COMANDOS ÚTILES (Python)

```python
# Monitorear tiempos
print(f"t_arribo={p['t_arribo']}, t_arribo_MP={p.get('t_arribo_MP', 'NO REGISTRADO')}")

# Monitorear SRTF
print(f"T={T}: CPU={p['id']}, TR={p['t_RestanteCPU']}")

# Monitorear multiprogramación
mp = len(listos) + len(suspendidos)
print(f"MP={mp}/5, Listos={len(listos)}, Suspendidos={len(suspendidos)}")

# Monitorear preempsión
if proximo['t_RestanteCPU'] < actual['t_RestanteCPU']:
    print("PREEMPSIÓN!")
```

---

## ¡ÉXITO! 🚀

Tienen todo lo que necesitan. 
No hay excusas. 
¡A CODEAR!

---

*Creado: 19 de enero de 2026*
*Última actualización: Hoy*
*Status: LISTO PARA USAR*
