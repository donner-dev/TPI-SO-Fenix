# Modulo Central de estado
# este archivo será el único lugar donde se definen las variables compartidas
# los demas modulos tienen que importar este archivo
# el archivo main tambien lo importa, se les dara los valores iniciales ahi al arrancar la ejecucion del simulador#

#variables a manipular
T_simulador=None 
T_CPU_ocioso=0 #este acumula los lapsos de tiempo que no hay procesos para ejecutar
T_usoCPU_TotalGeneral=None
multiprogramacion=None
aux=None
cantTotalProcesos=0
archivo=None
#listas inician sin elementos
listaProcesos=[]
listaSuspendidos=[]
listaListos=[] #procesos cargados en memoria
listaTerminados=[]
MemoriaPrincipal=[    #informacion de las particiones
    {
        "Particion": 1,
        "TamañoTotal": 250,
        "Dir_Comienzo":151,
        "Dueño": "usuario",
        "Proceso_alojado": {}, #MemoriaPrincipal[puntero]["Proceso_alojado"]= asigna VARIABLE_proceso_actual, asigna el diccionario completo del proceso
        "Fragmentacion_Interna":0,
        "Ocupado": False
    },
    {
        "Particion": 2,
        "TamañoTotal": 150,
        "Dir_Comienzo":51,
        "Dueño": "usuario",
        "Proceso_alojado": {},
        "Fragmentacion_Interna":0,
        "Ocupado": False
    },
    {
        "Particion": 3,
        "TamañoTotal": 50,
        "Dir_Comienzo":0,
        "Dueño": "usuario",
        "Proceso_alojado": {},
        "Fragmentacion_Interna":0,
        "Ocupado": False
    },
    {
        "Particion": 0,
        "TamañoTotal": 100,
        "Dir_Comienzo":251,
        "Dueño": "SO",
        "Proceso_alojado":{},#es la particion de sistema operativo, no necesita contenido en proceso alojado
        "Fragmentacion_Interna":0,
        "Ocupado": True
    }
]



# ejemplo de uso:
# moduloA.py
## import estado_global
## 
## def registrar_arribo(valor):
##     estado_global.T_sumulador = valor
# 
# moduloB.py 
## import estado_global
## 
## def mostrar_estado():
##     print("T simuladcion:", estado_global.T_sumulador) #
