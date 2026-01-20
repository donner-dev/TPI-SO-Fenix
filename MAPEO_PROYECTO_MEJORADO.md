# MAPEO: CÓMO ADAPTAR EL CÓDIGO MEJORADO AL ROUND ROBIN
## Referencias Exactas del Proyecto Mejorado

---

## 1️⃣ CORRECCIÓN 1: TIEMPOS (t_arribo_MP)

### 🎯 Objetivo
Usar `t_arribo_MP` (cuando realmente entra a MP) en lugar de `t_arribo` (del CSV)

### 📍 Dónde está en el Proyecto Mejorado

#### Archivo: `SIMULADOR.py`

**Línea ~115**: Comentario sobre t_arribo_MP
```python
# En ejecutarTodo() docstring:
# El proceso ejecutado está alojado en:
# MemoriaPrincipal[puntero_actual]["Proceso_alojado"]
```

**Línea ~145-160**: En comentario de FIFO
```python
# Describe cómo se usa t_arribo_MP para sincronización
```

#### Archivo: `funcionesLisandro_prolijo.py`

**Función `mover_aColaListo()` (línea ~180)**:
```python
def mover_aColaListo(proceso_actual: Dict):
    marcar_procesoNuevo_Ingresado(proceso_actual)
    tiempoArriboMemPrincipal = vGlobal.T_simulador  # ← ESTE ES t_arribo_MP
    
    proceso_listo = {
        "id": proceso_actual.get("id"),
        "t_arribo": proceso_actual.get("t_arribo"),
        "t_arribo_MP": tiempoArriboMemPrincipal,  # ← AQUÍ SE REGISTRA
        "t_RestanteCPU": ...,
        ...
    }
```

**Función `mover_aColaTerminados()` (línea ~260)**:
```python
def mover_aColaTerminados(proceso_actual: Dict):
    total_Retorno = vGlobal.T_simulador - proceso_actual.get("t_arribo_MP", vGlobal.T_simulador)
    # ↑ CALCULA usando t_arribo_MP, NO t_arribo
    
    proceso_Terminado = {
        "id": proceso_actual.get("id"),
        "t_Retorno": instante_Retorno,
        "total_Retorno": total_Retorno,  # ← TIEMPO CORRECTO
        ...
    }
```

### ✅ Implementar en TPI_Listo.py

**Paso 1**: Agregar campo en creación de proceso
```python
# Buscar dónde se crea el proceso desde CSV
# Agregar:
proceso = {
    "id": id_proceso,
    "t_arribo": tiempo_arribo_csv,
    "t_arribo_MP": None,  # ← AGREGAR
    "tamaño": tamaño,
    "t_irrupcion": duracion,
    ...
}
```

**Paso 2**: Registrar cuando entra a listaListos
```python
# Buscar función mover_aColaListo (o equivalente)
def mover_aColaListo(proceso):
    # AL COMIENZO:
    proceso["t_arribo_MP"] = T_Simulacion  # ← AGREGAR ESTA LÍNEA
    
    # resto del código...
    listaMP.append(proceso)
```

**Paso 3**: Usar en cálculos finales
```python
# En informe_final() o donde se calcula t_espera/t_retorno:
for proceso in listaTerminados:
    # ANTES (INCORRECTO):
    # t_espera = T_fin - proceso["t_arribo"]
    
    # DESPUÉS (CORRECTO):
    t_espera = T_fin - proceso["t_arribo_MP"]
    t_retorno = T_fin - proceso["t_arribo_MP"]
```

---

## 2️⃣ CORRECCIÓN 2: SRTF CON PREEMPSIÓN

### 🎯 Objetivo
Hacer ciclo a ciclo, detectar arribi, evaluar preempsión cada ciclo

### 📍 Dónde está en el Proyecto Mejorado

#### Archivo: `SIMULADOR.py`

**Función `ejecutarTodo()` (líneas 95-220)**: ESTA ES LA CLAVE
```python
def ejecutarTodo(puntero_actual: int):
    # ... inicialización ...
    
    while proceso.get("t_RestanteCPU") > 0:
        # ════════════════════════════════════════
        # ACTUALIZACIÓN AUTOMÁTICA POR REFERENCIA
        # ════════════════════════════════════════
        proceso = vGlobal.MemoriaPrincipal[puntero_actual]["Proceso_alojado"]
        
        # ════════════════════════════════════════
        # CONSUMIR CPU 1 CICLO
        # ════════════════════════════════════════
        proceso["t_RestanteCPU"] -= 1
        vGlobal.T_simulador += 1  # ← AVANZA 1 CICLO
        vGlobal.T_usoCPU_TotalGeneral += 1
        
        # ════════════════════════════════════════
        # DETECTAR ARRIBO EN ESTE CICLO
        # ════════════════════════════════════════
        siguiente = buscarSiguiente()  # ← DETECTA SI HAY ALGO
        if (siguiente is not None) and \
           (vGlobal.multiprogramacion < 5) and \
           (siguiente.get("t_arribo") == vGlobal.T_simulador):
            # ← AQUÍ SE DETECTA ARRIBO EN ESTE CICLO EXACTO
            banderaMostrarTablas = True
            Lis.ADMICION_MULTI_5()  # Admitir nuevo
        
        # ════════════════════════════════════════
        # SUMAR TIEMPO DE ESPERA (cada ciclo)
        # ════════════════════════════════════════
        for p in vGlobal.listaListos:
            if p["id"] != proceso["id"]:
                p["tiempoTotal_enColaDeListo"] += 1
        
        # ... más validaciones ...
        
        # ════════════════════════════════════════
        # SI EL PROCESO TERMINA EN ESTE CICLO
        # ════════════════════════════════════════
        if proceso.get("t_RestanteCPU") < 1:
            # Desalojar, mover a terminados
            # Buscar siguiente con SRTF
            nuevo_puntero = Lis.BuscarSRTF()
            # ... cambio de contexto ...
        
        # ════════════════════════════════════════
        # EVALUAR PREEMPSIÓN SRTF EN ARRIBO
        # ════════════════════════════════════════
        if (siguiente is not None) and \
           (vGlobal.multiprogramacion < 5) and \
           (siguiente.get("t_arribo") <= vGlobal.T_simulador):
            # ← AQUÍ OCURRE LA PREEMPSIÓN
            Lis.ADMICION_MULTI_5()
            nuevo_puntero = Lis.BuscarSRTF()
            if (nuevo_puntero is not None):
                proc_nuevo = vGlobal.MemoriaPrincipal[nuevo_puntero]["Proceso_alojado"]
                if (proc_nuevo.get("id") != proceso.get("id")):
                    if proc_nuevo.get("t_RestanteCPU") < proceso.get("t_RestanteCPU"):
                        # ← PREEMPSIÓN OCURRE AQUÍ
                        print(f"=================APROPIACION DE CPU==================")
                        Lis.desactivarProceso_en_CPU(...)
                        puntero_actual = nuevo_puntero
                        Lis.activarProceso_en_CPU(...)
                        proceso = vGlobal.MemoriaPrincipal[puntero_actual]["Proceso_alojado"]
                        # ← Sale del while, próximo proceso en CPU
```

**Función `buscarSiguiente()` (líneas 236-270)**:
```python
def buscarSiguiente():
    """
    Busca el siguiente proceso pendiente de admisión o el próximo arribo futuro.
    Recorre listaProcesos EN ORDEN (FIFO).
    """
    pendiente = None
    for p in vGlobal.listaProcesos:
        # PRIMERO: procesos que ya llegaron pero no se admitieron
        if (p.get("bandera_baja_logica") is False) and \
           (p.get("t_arribo") <= vGlobal.T_simulador):
            return p  # ← Retorna el PRIMERO que encontró
        
        # SEGUNDO: proceso que llega EN ESTE CICLO
        if (p.get("t_arribo") == vGlobal.T_simulador):
            return p  # ← Lo detecta
    
    # TERCERO: próximo arribo futuro
    for p in vGlobal.listaProcesos:
        if (p.get("t_arribo") > vGlobal.T_simulador) and \
           (p.get("bandera_baja_logica") is False):
            return p
    
    return None
```

### ✅ Implementar en TPI_Listo.py

**Paso 1**: Cambiar loop principal a ciclo a ciclo
```python
# ANTES (MAL):
while proceso["t_RestanteCPU"] > 0:
    proceso["t_RestanteCPU"] -= 1
    # [sal del loop cuando termina]

# DESPUÉS (CORRECTO):
while proceso["t_RestanteCPU"] > 0:
    # Consumir 1 ciclo CPU
    proceso["t_RestanteCPU"] -= 1
    T_Simulacion += 1  # ← AQUÍ, avanza 1
    
    # Detectar arribi EN ESTE CICLO
    siguiente = buscarSiguiente()
    if siguiente and siguiente["t_arribo"] == T_Simulacion:
        # Admitir procesos
        ADMICION()
        
        # Evaluar preempsión
        proximo = BuscarSRTF()
        if proximo and proximo["id"] != proceso["id"]:
            if proximo["t_RestanteCPU"] < proceso["t_RestanteCPU"]:
                # PREEMPSIÓN
                [desalojar proceso]
                [poner proximo]
                break  # Salir, ejecutar proximo
```

**Paso 2**: Implementar `buscarSiguiente()` correctamente
```python
def buscarSiguiente():
    """Busca el PRÓXIMO proceso que necesita atención en THIS ciclo"""
    # Recorrer listaNuevos EN ORDEN
    for proceso in listaNuevos:
        # ¿Ya llegó y no se admitió?
        if not proceso["admitido"] and proceso["t_arribo"] <= T_Simulacion:
            return proceso
    
    # ¿Hay próximo futuro?
    for proceso in listaNuevos:
        if not proceso["admitido"] and proceso["t_arribo"] > T_Simulacion:
            return proceso
    
    return None
```

**Paso 3**: Implementar `BuscarSRTF()` correctamente
```python
def BuscarSRTF():
    """Busca proceso en listaListos (listaMP) con menor t_RestanteCPU"""
    if len(listaMP) == 0:
        return None
    
    menor_tr = float("inf")
    proceso_elegido = None
    
    for proc in listaListos:  # o listaMP[i]["Proceso_alojado"]
        if proc.get("t_RestanteCPU") > 0 and proc.get("t_RestanteCPU") < menor_tr:
            menor_tr = proc.get("t_RestanteCPU")
            proceso_elegido = proc
    
    if proceso_elegido is None:
        return None
    
    # Retorna el índice de la partición, no el proceso
    for i, particion in enumerate(listaMP):
        if particion["Proceso_alojado"].get("id") == proceso_elegido.get("id"):
            return i
    
    return None
```

---

## 3️⃣ CORRECCIÓN 3: MULTIPROGRAMACIÓN <= 5

### 🎯 Objetivo
Validar que (CPU + Listos + Suspendidos) nunca > 5

### 📍 Dónde está en el Proyecto Mejorado

#### Archivo: `SIMULADOR.py`

**Línea ~135-155**: Comentarios sobre multiprogramación
```python
# En SIMULADOR.py docstring:
# "manteniendo multiprogramación <= 5"
```

#### Archivo: `funcionesLisandro_prolijo.py`

**Función `ADMICION_MULTI_5()` (línea 585-614)**: CLAVE
```python
def ADMICION_MULTI_5():
    # Actualizar conteo
    vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)
    
    # ← VALIDAR AQUÍ
    if vGlobal.multiprogramacion >= 5:
        return  # No admitir si ya hay 5
    
    # Si hay espacio en MP y < 5 multiprogramación:
    if len(vGlobal.listaListos) < 3 and vGlobal.listaSuspendidos:
        CARGAR_MPconMS()  # Traer de MS a MP
    
    # Admitir nuevos
    while vGlobal.multiprogramacion < 5:  # ← VALIDAR EN CADA ITERACIÓN
        cambios = False
        for proceso in vGlobal.listaProcesos:
            if proceso.get("bandera_baja_logica") is False and \
               proceso.get("t_arribo") <= vGlobal.T_simulador:
                
                if len(vGlobal.listaListos) < 3 and cabeEnAlgunaParticionLIBRE(proceso):
                    mover_aColaListo(proceso)
                    puntero = BestFitCICLO_ADMICION(vGlobal.aux)
                    if puntero is not None:
                        cargarProcesoAlojado(...)
                    cambios = True
                else:
                    mover_aColaSuspendido(proceso)
                    cambios = True
                
                # VALIDAR DESPUÉS DE CADA ADMISIÓN
                vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)
                if vGlobal.multiprogramacion >= 5:  # ← AQUÍ VALIDA
                    return
        
        if not cambios:
            break
    
    vGlobal.multiprogramacion = len(vGlobal.listaListos) + len(vGlobal.listaSuspendidos)
```

**Función `CARGAR_MPconMS()` (línea 570-583)**:
```python
def CARGAR_MPconMS():
    """Carga MP con procesos desde suspendidos"""
    while len(vGlobal.listaListos) < 3:  # Máximo 3 en MP
        cambios = False
        for ingresa in list(vGlobal.listaSuspendidos):
            if cabeEnAlgunaParticionLIBRE(ingresa):
                mover_aColaListo(ingresa)
                puntero = BestFitCICLO_ADMICION(vGlobal.aux)
                if puntero is not None:
                    cargarProcesoAlojado(...)
                cambios = True
        
        SuspendidosYListos()  # Eliminar de suspendidos
        if not cambios:
            break
```

### ✅ Implementar en TPI_Listo.py

**Paso 1**: Crear función de validación
```python
def validar_multiprogramacion():
    """
    Calcula el nivel actual de multiprogramación.
    multiprogramacion = Listos + Suspendidos [+ CPU si hay]
    """
    mp = len(listaMP_listos) + len(listaSuspendidos)
    
    # Si hay proceso ejecutándose, también cuenta
    # (depende de cómo lo implementes)
    
    return mp

def puede_admitir():
    """Retorna True si se puede admitir otro proceso"""
    return validar_multiprogramacion() < 5
```

**Paso 2**: Validar ANTES de cada admisión
```python
def ADMICION():
    """Admitir procesos respetando multiprogramación <= 5"""
    
    # Actualizar conteo
    mp = validar_multiprogramacion()
    
    # Si ya hay 5, no admitir nada
    if mp >= 5:
        return
    
    # Intentar admitir procesos
    for proceso in listaNuevos:
        if no_ha_sido_admitido(proceso) and \
           proceso["t_arribo"] <= T_Simulacion:
            
            # VALIDAR ANTES DE ADMITIR
            if validar_multiprogramacion() >= 5:
                break  # No admitir más
            
            if cabe_en_MP(proceso):
                mover_aColaListo(proceso)
            else:
                mover_aColaSuspendido(proceso)
```

**Paso 3**: Validar en CARGAR_MPconMS
```python
def CARGAR_MPconMS():
    """Traer procesos de MS a MP cuando hay espacio"""
    while len(listaMP_listos) < 3:  # Máximo 3 en MP
        
        # VALIDAR MULTIPROGRAMACION
        if validar_multiprogramacion() >= 5:
            break
        
        # Buscar suspendido que quepa
        for suspendido in listaSuspendidos:
            if cabe_en_MP(suspendido):
                mover_aColaListo(suspendido)
                break
        else:
            break  # Ninguno cabe
```

**Paso 4**: Monitorear en cada ciclo (para debugging)
```python
# En el loop principal o en ADMICION:
if debug_mode:
    mp = validar_multiprogramacion()
    print(f"T={T_Simulacion}: MP={mp}, " +
          f"Listos={len(listaMP_listos)}, " +
          f"Suspendidos={len(listaSuspendidos)}")
    
    if mp > 5:
        print("ERROR: ¡Multiprogramación > 5!")
```

---

## 📋 RESUMEN DE REFERENCIAS

| Corrección | Archivo Mejorado | Función/Línea | Qué ver |
|------------|------------------|---------------|---------|
| **Tiempos** | funcionesLisandro_prolijo.py | mover_aColaListo() L180 | Cómo se registra t_arribo_MP |
| **Tiempos** | funcionesLisandro_prolijo.py | mover_aColaTerminados() L260 | Cálculo con t_arribo_MP |
| **SRTF** | SIMULADOR.py | ejecutarTodo() L95-220 | Loop ciclo a ciclo |
| **SRTF** | SIMULADOR.py | buscarSiguiente() L236-270 | Detección de arribi |
| **SRTF** | SIMULADOR.py | Buscar "APROPIACION" | Evaluación preempsión |
| **Multiprog** | SIMULADOR.py | L135-155 comentarios | Concepto multiprogramación |
| **Multiprog** | funcionesLisandro_prolijo.py | ADMICION_MULTI_5() L585 | Validación antes admisión |
| **Multiprog** | funcionesLisandro_prolijo.py | CARGAR_MPconMS() L570 | Validación en MS→MP |

---

## 🎓 CONSEJOS PRÁCTICOS

1. **NO COPIAR CÓDIGO**: Leerlo para entender, escribir ustedes
2. **Mantener estructura**: TPI_Listo.py usa listas, no estado_global
3. **Probar cada corrección**: Implementar una, probar, luego siguiente
4. **Usar print() para debugging**: Ver qué pasa en cada ciclo
5. **Comparar con proyecto mejorado**: Si algo no funciona, mirar cómo lo hace

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] Tiempos: Campo t_arribo_MP agregado
- [ ] Tiempos: Se registra al mover a listaListos
- [ ] Tiempos: Se usa en cálculos finales
- [ ] SRTF: Loop es ciclo a ciclo
- [ ] SRTF: Se detectan arribi en cada ciclo
- [ ] SRTF: Se evalúa preempsión en cada ciclo
- [ ] SRTF: Procesos pueden ser desalojados
- [ ] Multiprog: Función de validación existe
- [ ] Multiprog: Se valida ANTES de admitir
- [ ] Multiprog: Nunca excede 5

¡Éxito con las correcciones! 🚀
