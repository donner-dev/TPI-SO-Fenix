# ÁRBOL DE DECISIÓN: CÓMO IMPLEMENTAR LAS CORRECCIONES
## Guía Visual paso a paso

---

## 🌳 ÁRBOL 1: AGREGAR t_arribo_MP

```
┌─ ¿Dónde se CREA el proceso (del CSV)?
│  ├─ Encontré la función que lee CSV
│  │  └─ Estructura inicial del proceso
│  │
│  ├─ ✅ ACCIÓN: Agregar campo
│  │  │
│  │  ├─ proceso = {
│  │  │      "id": id,
│  │  │      "t_arribo": csv_arribo,
│  │  │      "t_arribo_MP": None,  ← AGREGAR ESTA LÍNEA
│  │  │      "tamaño": tamaño,
│  │  │      ...
│  │  │  }
│  │  │
│  │  └─ Guardar y seguir
│  │
│  └─ ¿No encontré?
│     └─ Ver MAPEO_PROYECTO_MEJORADO.md sección 1
│
├─ ¿Dónde se MUEVE a listaListos?
│  ├─ Encontré función mover_aColaListo() o similar
│  │  └─ ✅ ACCIÓN: Registrar el tiempo
│  │     │
│  │     ├─ def mover_aColaListo(proceso):
│  │     │      proceso["t_arribo_MP"] = T_Simulacion  ← AGREGAR
│  │     │      # resto del código...
│  │     │      listaMP_listos.append(proceso)
│  │     │
│  │     └─ Guardar y seguir
│  │
│  └─ ¿No encontré?
│     └─ Buscar dónde se hace: listaMP_listos.append()
│
└─ ¿Dónde se CALCULA tiempo final?
   ├─ Encontré función informe_final() o similar
   │  └─ ✅ ACCIÓN: Cambiar cálculo
   │     │
   │     ├─ # ANTES (MAL):
   │     │  # t_espera = T - proceso["t_arribo"]
   │     │  
   │     │  # DESPUÉS (CORRECTO):
   │     │  t_espera = T - proceso["t_arribo_MP"]
   │     │
   │     └─ Probar con procesos.csv
   │
   └─ ¿No encontré?
      └─ Buscar dónde se imprime/calcula el informe
```

---

## 🌳 ÁRBOL 2: IMPLEMENTAR SRTF CICLO A CICLO

```
┌─ ¿DÓNDE ESTÁ EL LOOP PRINCIPAL?
│  ├─ Encontré el while que ejecuta procesos
│  │  └─ ✅ ACCIÓN 1: Cambiar a ciclo a ciclo
│  │     │
│  │     ├─ # ANTES (MAL):
│  │     │  while proceso["t_RestanteCPU"] > 0:
│  │     │      proceso["t_RestanteCPU"] -= 1
│  │     │      [todo el proceso se ejecuta]
│  │     │
│  │     │  # DESPUÉS (CORRECTO):
│  │     │  while proceso["t_RestanteCPU"] > 0:
│  │     │      proceso["t_RestanteCPU"] -= 1
│  │     │      T_Simulacion += 1  ← AGREGAR
│  │     │      
│  │     │      # [AQUÍ se puede interrumpir]
│  │     │
│  │     └─ Continuar con Acción 2
│  │
│  └─ ¿No encontré?
│     └─ Buscar while con t_RestanteCPU > 0
│
├─ ✅ ACCIÓN 2: Detectar arribi EN ESTE CICLO
│  ├─ # Dentro del while:
│  │  siguiente = buscarSiguiente()
│  │  if siguiente and siguiente["t_arribo"] == T_Simulacion:
│  │      # Hay un proceso que llega AHORA
│  │      ADMICION()
│  │
│  └─ Continuar con Acción 3
│
├─ ✅ ACCIÓN 3: Evaluar preempsión EN ESTE CICLO
│  ├─ # Dentro del while, después de admitir:
│  │  proximo_srtf = BuscarSRTF()
│  │  if proximo_srtf and proximo_srtf["id"] != proceso["id"]:
│  │      if proximo_srtf["t_RestanteCPU"] < proceso["t_RestanteCPU"]:
│  │          # PREEMPSIÓN OCURRE
│  │          print("PREEMPSIÓN!")
│  │          proceso["CPU"] = False  # desalojar
│  │          proceso = proximo_srtf  # nuevo
│  │          break  # salir, ejecutar nuevo
│  │
│  └─ Continuar con función buscarSiguiente()
│
└─ ¿Necesitas implementar buscarSiguiente()?
   ├─ # Buscar el PRÓXIMO proceso
   │  def buscarSiguiente():
   │      for p in listaNuevos:
   │          if not admitido and t_arribo <= T_Simulacion:
   │              return p  # FIFO: primero encontrado
   │      
   │      for p in listaNuevos:
   │          if not admitido and t_arribo > T_Simulacion:
   │              return p  # próximo futuro
   │      
   │      return None
   │
   └─ Y BuscarSRTF()?
      └─ # Buscar el de menor t_RestanteCPU
         def BuscarSRTF():
             menor_tr = inf
             elegido = None
             
             for proc in listaMP_listos:
                 if proc["t_RestanteCPU"] < menor_tr:
                     menor_tr = proc["t_RestanteCPU"]
                     elegido = proc
             
             # Retornar índice de partición
             if elegido:
                 for i, part in enumerate(listaMP):
                     if part["Proceso_alojado"]["id"] == elegido["id"]:
                         return i
             return None
```

---

## 🌳 ÁRBOL 3: VALIDAR MULTIPROGRAMACIÓN <= 5

```
┌─ ¿DÓNDE ESTÁ LA FUNCIÓN DE ADMISIÓN?
│  ├─ Encontré ADMICION() o similar
│  │  └─ ✅ ACCIÓN 1: Crear validador
│  │     │
│  │     ├─ def validar_multiprogramacion():
│  │     │      mp = len(listaMP_listos) + len(listaSuspendidos)
│  │     │      if hay_proceso_en_cpu:
│  │     │          mp += 1
│  │     │      return mp
│  │     │
│  │     └─ Continuar con Acción 2
│  │
│  └─ ¿No encontré?
│     └─ Buscar función que admite procesos
│
├─ ✅ ACCIÓN 2: Validar ANTES de admitir a listaListos
│  ├─ # Al inicio de ADMICION():
│  │  if validar_multiprogramacion() >= 5:
│  │      return  # No admitir nada
│  │
│  │  # Dentro del loop:
│  │  for proceso in listaNuevos:
│  │      if validar_multiprogramacion() >= 5:
│  │          break  # No admitir más
│  │
│  │      if cabe_en_MP(proceso):
│  │          mover_aColaListo(proceso)
│  │      else:
│  │          mover_aColaSuspendido(proceso)
│  │
│  └─ Continuar con Acción 3
│
├─ ✅ ACCIÓN 3: Validar en función CARGAR_MPconMS
│  ├─ # Cuando traes de MS a MP:
│  │  def CARGAR_MPconMS():
│  │      while len(listaMP_listos) < 3:
│  │          if validar_multiprogramacion() >= 5:  ← VALIDAR
│  │              break
│  │          
│  │          for suspendido in listaSuspendidos:
│  │              if cabe_en_MP(suspendido):
│  │                  mover_aColaListo(suspendido)
│  │                  break
│  │          else:
│  │              break
│  │
│  └─ Continuar con monitoreo
│
└─ ✅ ACCIÓN 4: Monitorear (debugging)
   ├─ # En ADMICION, imprimir:
   │  mp = validar_multiprogramacion()
   │  print(f"T={T}: MP={mp}, " +
   │        f"Listos={len(listos)}, " +
   │        f"Suspendidos={len(suspendidos)}")
   │  if mp >= 5:
   │      print("  → MP >= 5, NO ADMITIR")
   │
   └─ Probar con LOTE_1, LOTE_2, LOTE_3
```

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

### Corrección 1: Tiempos ✓
```
[ ] Agregar campo t_arribo_MP
    [ ] En estructura inicial de proceso
    [ ] Inicializado a None o vacio
    [ ] Comentario explicando qué es

[ ] Registrar al mover a listaListos
    [ ] En función mover_aColaListo()
    [ ] Asignar: proceso["t_arribo_MP"] = T_Simulacion
    [ ] ANTES de agregar a listaListos

[ ] Usar en cálculos finales
    [ ] En informe_final() o equivalente
    [ ] Cambiar: t_arribo → t_arribo_MP
    [ ] En AMBAS fórmulas: t_espera Y t_retorno

[ ] Validación
    [ ] Probar con procesos.csv
    [ ] Tiempos tienen sentido
    [ ] No hay negativos ni ceros extraños
```

### Corrección 2: SRTF ✓
```
[ ] Loop ciclo a ciclo
    [ ] Cambiar while para ejecutar 1 ciclo
    [ ] Agregar T_Simulacion += 1
    [ ] NO todo de una vez

[ ] Detectar arribi cada ciclo
    [ ] Implementar buscarSiguiente()
    [ ] Llamar dentro del while
    [ ] Verificar t_arribo == T_Simulacion (exacto)

[ ] Evaluar preempsión cada ciclo
    [ ] Implementar BuscarSRTF()
    [ ] Comparar t_RestanteCPU
    [ ] Si nuevo < actual → preempt

[ ] Manejar desalojo
    [ ] Proceso desalojado regresa a Listos
    [ ] Con t_RestanteCPU actualizado
    [ ] Nuevo entra a CPU

[ ] Validación
    [ ] Probar con LOTE_1.csv
    [ ] Hay preempsiones
    [ ] Tiempo total es menor que antes
```

### Corrección 3: Multiprogramación ✓
```
[ ] Función de validación
    [ ] validar_multiprogramacion() existe
    [ ] Cuenta: Listos + Suspendidos + (CPU)
    [ ] Retorna número <= 5

[ ] Validar antes de admitir
    [ ] En ADMICION() al inicio
    [ ] En loop de cada proceso
    [ ] ANTES de mover_aColaListo()

[ ] Validar en CARGAR_MPconMS
    [ ] Mientras trae de MS a MP
    [ ] ANTES de mover_aColaListo()

[ ] Monitoreo/Debugging
    [ ] Print de MP actual en cada ciclo
    [ ] Verifica nunca > 5
    [ ] Si > 5 → ERROR encontrado

[ ] Validación
    [ ] Probar LOTE_1, LOTE_2, LOTE_3
    [ ] NUNCA ve MP > 5
    [ ] Procesos se distribuyen bien
```

---

## 🧪 TESTING RÁPIDO

### Test 1: ¿Tiempos se calculan correctamente?
```bash
Input: procesos.csv simple (P1: T=0, TR=5)
Output: Verificar que t_arribo_MP está registrado
        t_retorno = t_fin - t_arribo_MP (correcto)
```

### Test 2: ¿SRTF funciona?
```bash
Input: P1(TR=10) T=0, P2(TR=2) T=3
Output: Ver que ocurre preempsión en T=3
        P1 ejecuta 3 ciclos, P2 ejecuta 2 ciclos, P1 7 ciclos
        Tiempo total < 18
```

### Test 3: ¿Multiprogramación <= 5?
```bash
Input: LOTE_1.csv (5+ procesos)
Output: Monitorear MP cada ciclo
        NUNCA ve MP > 5
        Si ve > 5 → BUG
```

---

## 🔧 TROUBLESHOOTING

| Síntoma | Causa Probable | Solución |
|---------|---|---|
| Tiempos siguen siendo incorrectos | `t_arribo_MP` no se usa en cálculos | Verificar fórmula final usa `t_arribo_MP` |
| SRTF no funciona (sigue SJF) | Loop no es ciclo a ciclo | Verificar `T_Simulacion += 1` dentro del while |
| No hay preempsiones | `buscarSiguiente()` no detecta arribi | Usar == en comparación (no <=) |
| Multiprogramación > 5 | No se valida antes de admitir | Agregar `if mp >= 5: return` |
| Código compila pero da errores | Referencias incorrectas | Verificar nombres de listas (listaListos vs listaMP) |

---

## 📞 PREGUNTAS FRECUENTES

**P: ¿Dónde exactamente va el `t_arribo_MP = T_Simulacion`?**
R: En `mover_aColaListo()`, ANTES de `listaMP_listos.append()` o equivalente.

**P: ¿El loop debe cambiar TODO o solo una parte?**
R: Solo la parte de "avanza 1 ciclo CPU". El resto del código sigue dentro.

**P: ¿Cómo sé si hay preempsión?**
R: Mira si un proceso en Listos de repente tiene menor TR que el que está en CPU. Imprime un mensaje.

**P: ¿Qué pasa si multiprogramación = 5?**
R: NO se puede admitir nada más. Esperar a que alguien termine.

**P: ¿Se pueden copiar funciones del proyecto mejorado?**
R: NO. Úsalas como REFERENCIA, escribe tus propias funciones.

---

## 🎯 META FINAL

Cuando termines, el simulador debe:

✅ Calcular tiempos correctamente (desde `t_arribo_MP`)
✅ Implementar SRTF con preempsión (ciclo a ciclo)
✅ Respetar multiprogramación <= 5 (siempre)
✅ Pasar todos los tests de validación
✅ Hacer feliz al profesor/a 😊

---

¡Sigue este árbol de decisión y llegarás a la solución! 🚀
