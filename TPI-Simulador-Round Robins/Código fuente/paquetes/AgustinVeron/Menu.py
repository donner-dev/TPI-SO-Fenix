import msvcrt
import time
import sys
import os

#Variables globales

#Dimensiones de pantalla
xMaxPantalla = 95
yMaxPantalla = 35
#Posicion vertical de las opciones
pos_opciones = (yMaxPantalla//2)+12
pos_opciones2 = (yMaxPantalla//2)+6
#Colores para strings
NEGRITA = "\033[1m"
AZUL="\033[44m" 
ROJO="\033[41m" 
VERDE="\033[42m"
AMARILLO="\033[43m"
NEGRO="\033[30m"
BLANCO="\033[47m"
RESET = "\033[0m"
#Teclas
TECLA_ENTER    = '\r'
TECLA_ARRIBA   = '\xe0H'
TECLA_ABAJO    = '\xe0P'

#Clean Screen (Limpiar pantalla)
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

#Gotoxy (se posiciona en un punto específico de la pantalla)
def gotoxy(x, y):
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()

#Lee un caracter ingresado desde el teclado directamente desde el buffer de entrada
def read_single_key_windows():
    tecla_bytes = msvcrt.getch()
    if tecla_bytes == b'\xe0' or tecla_bytes == b'\x00':
        return tecla_bytes.decode('latin-1') + msvcrt.getch().decode('latin-1')  
    return tecla_bytes.decode('latin-1')

#Limpia el buffer de entrada del teclado
def limpiar_buffer_entrada():
    while msvcrt.kbhit():
        msvcrt.getch()

#Logo del engranaje
def mostrar_logo():
    '''
    ---por cada linea---
    Asigno string
    Me posiciono; imprimo
    '''
    mensajeOp = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),3); print(mensajeOp)
    mensajeOp = f"░{ROJO}++++++++++++++++++++{RESET}{NEGRO}%#{RESET}{VERDE}++++++++++++++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+13,4); print(mensajeOp)
    mensajeOp = f"░{ROJO}++++++++++++++++++++{RESET}{NEGRO}%#{RESET}{VERDE}++++++++++++++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+13,5); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++++++++++++++++{RESET}{NEGRO}%*:{RESET}{BLANCO}..{RESET}{NEGRO}-%#{RESET}{VERDE}+++++++++++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,6); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++++++++{RESET}{NEGRO}%%%#+++*%{RESET}{BLANCO}.....{RESET}{NEGRO}*%++++%%%*{RESET}{VERDE}+++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,7); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++++++{RESET}{NEGRO}%%:{RESET}{BLANCO}...{RESET}{NEGRO}%%={RESET}{BLANCO}..........{RESET}{NEGRO}%%*{RESET}{BLANCO}...{RESET}{NEGRO}#%*{RESET}{VERDE}+++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,8); print(mensajeOp)
    mensajeOp = f"░{ROJO}++++++{RESET}{NEGRO}%%{RESET}{BLANCO}.........................{RESET}{NEGRO}*%{RESET}{VERDE}+++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,9); print(mensajeOp)
    mensajeOp = f"░{ROJO}++++++++{RESET}{NEGRO}%#{RESET}{BLANCO}......{RESET}{NEGRO}:%%%%%%%+{RESET}{BLANCO}.......{RESET}{NEGRO}%#{RESET}{VERDE}++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+31,10); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++++++{RESET}{NEGRO}%%{RESET}{BLANCO}.....{RESET}{NEGRO}#%*{RESET}{AZUL}++++++++{RESET}{NEGRO}%%:{RESET}{BLANCO}....{RESET}{NEGRO}=%{RESET}{VERDE}++++++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,11); print(mensajeOp)
    mensajeOp = f"░{ROJO}+++{RESET}{NEGRO}%%%*={RESET}{BLANCO}.....{RESET}{NEGRO}%%{RESET}{AZUL}++++++++++++{RESET}{NEGRO}%:{RESET}{BLANCO}....{RESET}{NEGRO}:=#%%{RESET}{VERDE}++++{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,12); print(mensajeOp)
    mensajeOp = f"░{NEGRO}%%%%#{RESET}{BLANCO}.......{RESET}{NEGRO}:%{RESET}{AZUL}+++++++++++++{RESET}{NEGRO}%%{RESET}{BLANCO}........{RESET}{NEGRO}%%%%%{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+31,13); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++{RESET}{NEGRO}%%{RESET}{BLANCO}........{RESET}{NEGRO}%*{RESET}{AZUL}++++++++++++{RESET}{NEGRO}%#{RESET}{BLANCO}........{RESET}{NEGRO}%{RESET}{AMARILLO}+---{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,14); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++++{RESET}{NEGRO}*#%#{RESET}{BLANCO}....{RESET}{NEGRO}:%#{RESET}{AZUL}++++++++++{RESET}{NEGRO}%%{RESET}{BLANCO}.....{RESET}{NEGRO}%%#{RESET}{AMARILLO}+-----{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,15); print(mensajeOp)
    mensajeOp = f"░{AZUL}++++++++{RESET}{NEGRO}%%{RESET}{BLANCO}.....{RESET}{NEGRO}-%%#+++*%%#{RESET}{BLANCO}.....{RESET}{NEGRO}:%{RESET}{AMARILLO}+--------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+31,16); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++++++{RESET}{NEGRO}%#{RESET}{BLANCO}.......................{RESET}{NEGRO}:%%{RESET}{AMARILLO}-------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,17); print(mensajeOp)
    mensajeOp = f"░{AZUL}++++++{RESET}{NEGRO}*%#{RESET}{BLANCO}....{RESET}{NEGRO}-:{RESET}{BLANCO}...........{RESET}{NEGRO}.+{RESET}{BLANCO}....{RESET}{NEGRO}:%%{RESET}{AMARILLO}-------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+40,18); print(mensajeOp)
    mensajeOp = f"░{AZUL}++++++++{RESET}{NEGRO}*%%%%*+%%%{RESET}{BLANCO}.....={RESET}{NEGRO}%%*=%%#%%{RESET}{AMARILLO}---------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,19); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++++++++++++++++{RESET}{NEGRO}%-{RESET}{BLANCO}....{RESET}{NEGRO}%%{RESET}{AMARILLO}-----------------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+22,20); print(mensajeOp)
    mensajeOp = f"░{AZUL}+++++++++++++++++{RESET}{NEGRO}*%%%%%%{RESET}{AMARILLO}------------------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+13,21); print(mensajeOp)
    mensajeOp = f"░{AZUL}++++++++++++++++++++{RESET}{NEGRO}%*{RESET}{AMARILLO}--------------------{RESET}░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+13,22); print(mensajeOp)
    mensajeOp = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),23); print(mensajeOp)

#Logo de la carpeta
def mostrar_logo2():
    # El dibujo tiene aproximadamente 42 caracteres de ancho.
    mensajeOp = "        ............                                " 
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),5); print(mensajeOp)
    mensajeOp = "       .=-        .%.                               " 
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),6); print(mensajeOp)
    mensajeOp = "       .=:         %.......................         "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),7); print(mensajeOp)
    mensajeOp = "       .=:         .......................==.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),8); print(mensajeOp)
    mensajeOp = "       .+*================================++.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),9); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),10); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),11); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),12); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),13); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),14); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),15); print(mensajeOp)
    mensajeOp = "       .=:                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),16); print(mensajeOp)
    mensajeOp = "       .=-                                :=.       "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),17); print(mensajeOp)
    mensajeOp = "        ..:::::::::::::::::::::::::::::::::.        "
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),18); print(mensajeOp)

def creditos():
    limpiar_pantalla()
    for y in range(1, yMaxPantalla):
        for x in range(1, xMaxPantalla):
            if (x == 1) or (x == xMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
            if (y == 1) or (y == yMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
    mensajeOp = 'Créditos'
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),yMaxPantalla//2-6);print(mensajeOp)
    mensajeOp = '--------'
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),yMaxPantalla//2-5); print(mensajeOp)
    time.sleep(1.5)
    mensajeOp = 'SCRUM MASTER - Rojas, Lisandro Ezequiel'
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),yMaxPantalla//2-2); print(mensajeOp)
    time.sleep(1)
    mensajeOp = 'PROGRAMADOR - Verón, Raúl Vicente Agustín'
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),yMaxPantalla//2-1); print(mensajeOp)
    time.sleep(1)
    mensajeOp = 'EDITOR DE VIDEO - Sanchez Destang, Maximiliano'
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),yMaxPantalla//2); print(mensajeOp)
    time.sleep(1)
    mensajeOp = 'DOCUMENTADOR - Voelkli, Mauricio Leandro'
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),yMaxPantalla//2+1); print(mensajeOp)
    time.sleep(1)
    mensajeOp = 'ENCARGADO DEL SO - Donner, Isabel'
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),yMaxPantalla//2+2); print(mensajeOp)
    time.sleep(1)
    gotoxy(xMaxPantalla, yMaxPantalla + 2)

def mostrar_menu():
    #colocar recuadro
    for y in range(1, yMaxPantalla):
        for x in range(1, xMaxPantalla):
            if (x == 1) or (x == xMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
            if (y == 1) or (y == yMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
    #mostrar opciones
    mostrar_logo()
    mensajeOp = f"{NEGRITA}SIMULADOR DE GESTIÓN DE PROCESOS{RESET}"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2)+4,(yMaxPantalla//2)+8)
    print(mensajeOp)
    mensajeOp = "Use las flechas (⬆︎ ⬇︎) y presione (Enter):"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),(yMaxPantalla//2)+10)
    print(mensajeOp)
    mensajeOp = "(1)-Iniciar Simulacion"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),pos_opciones)
    print(mensajeOp)
    mensajeOp = "(2)-Créditos"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),pos_opciones+1)
    print(mensajeOp)
    mensajeOp = "(3)-Salir"
    gotoxy(((xMaxPantalla-len(mensajeOp))//2),pos_opciones+2)
    print(mensajeOp)
    gotoxy(3,yMaxPantalla-2)
    print("V0.1 - ROUND ROBINS",end="")
    gotoxy(xMaxPantalla-12,yMaxPantalla-2)
    print("U.T.N FRRe",end="")
    #posicion del puntero en la posicion maxima en x e y para dibujar toda la pantalla
    gotoxy(xMaxPantalla,yMaxPantalla+2)

#Desplazamiento y selección en el menú principal
def selec_opcion_menu1():
    # El índice de la opción seleccionada (0: Iniciar, 1: Créditos, 2: Salir)
    pos_puntero = 0
    tecla = ''
    NUM_OPCIONES = 3 
    X_PUNTERO = (xMaxPantalla // 2) - 15 
    while True:
        # 1) Borrar el puntero de la posición anterior
        pos_puntero_ant = pos_puntero
        # 2) Lectura de tecla (Espera activa por un input)
        tecla = read_single_key_windows()
        # 3) Lógica de movimiento (Solo se ejecuta si se presionó una tecla válida)
        if tecla == TECLA_ARRIBA:
            pos_puntero = (pos_puntero - 1) % NUM_OPCIONES
        elif tecla == TECLA_ABAJO:
            pos_puntero = (pos_puntero + 1) % NUM_OPCIONES
        elif tecla == TECLA_ENTER:
            # Sale del bucle cuando se presiona Enter
            break 
        # 4. Redibujar Puntero (Solo si la posición cambió o si se leyó una tecla)
        if tecla:
            # Borrar puntero antiguo: Imprimir un espacio ' ' en la posición vertical anterior.
            gotoxy(X_PUNTERO, pos_opciones + pos_puntero_ant)
            print(" ", end="", flush=True) 

            # Dibujar puntero nuevo: Imprimir la flecha '▶' en la nueva posición.
            gotoxy(X_PUNTERO, pos_opciones + pos_puntero)
            print("▶", end="", flush=True)
        # importante: Mover el cursor al final de la pantalla después de redibujar
        # para que el próximo "print" del sistema operativo no arruine el menú.
        gotoxy(xMaxPantalla, yMaxPantalla + 2)
    return pos_puntero + 1 # Devuelve 1, 2, o 3 (el número de opción)

#Desplazamiento y selección del menú para cargar procesos
def selec_opcion_menu2():
    limpiar_pantalla()
    mostrar_logo2()
    for y in range(1, yMaxPantalla):
        for x in range(1, xMaxPantalla):
            if (x == 1) or (x == xMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
            if (y == 1) or (y == yMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
    
    mensajeOp = "Use las flechas (⬆︎ ⬇︎) y presione (Enter)"
    gotoxy((xMaxPantalla-len(mensajeOp))//2+2,yMaxPantalla//2+4)
    print(mensajeOp)
    mensajeOp = "(1)-Cargar procesos mediante archivo (.csv)"
    gotoxy((xMaxPantalla-len(mensajeOp))//2,yMaxPantalla//2+6)
    print(mensajeOp)
    mensajeOp = "(2)-Carga manual de procesos"
    gotoxy((xMaxPantalla-len(mensajeOp))//2,yMaxPantalla//2+7)
    print(mensajeOp)
    # El índice de la opción seleccionada (0: Archivo, 1: Manual)
    pos_puntero = 0
    tecla = ''
    NUM_OPCIONES = 2 
    X_PUNTERO = (xMaxPantalla // 2) - 24 
    while True:
        # 1) Borrar el puntero de la posición anterior
        pos_puntero_ant = pos_puntero
        # 2) Lectura de tecla (Espera activa por un input)
        tecla = read_single_key_windows()
        # 3) Lógica de movimiento (Solo se ejecuta si se presionó una tecla válida)
        if tecla == TECLA_ARRIBA:
            pos_puntero = (pos_puntero - 1) % NUM_OPCIONES
        elif tecla == TECLA_ABAJO:
            pos_puntero = (pos_puntero + 1) % NUM_OPCIONES
        elif tecla == TECLA_ENTER:
            # Sale del bucle cuando se presiona Enter
            break 
        # 4. Redibujar Puntero (Solo si la posición cambió o si se leyó una tecla)
        if tecla:
            # Borrar puntero antiguo: Imprimir un espacio ' ' en la posición vertical anterior.
            gotoxy(X_PUNTERO, pos_opciones2 + pos_puntero_ant)
            print(" ", end="", flush=True) 
            # Dibujar puntero nuevo: Imprimir la flecha '▶' en la nueva posición.
            gotoxy(X_PUNTERO, pos_opciones2 + pos_puntero)
            print("▶", end="", flush=True)
        # importante: Mover el cursor al final de la pantalla después de redibujar
        # para que el próximo "print" del sistema operativo no arruine el menú.
        gotoxy(xMaxPantalla, yMaxPantalla + 2)
    return pos_puntero + 1 # Devuelve 1, 2, o 3 (el número de opción)


def ejecutarMenu():
    limpiar_pantalla()
    mostrar_menu()
    limpiar_buffer_entrada()
    paso1 = selec_opcion_menu1()
    if paso1 == 1:
        paso2 = selec_opcion_menu2()
    elif paso1 == 2:
        creditos()
    elif paso1 == 3:
        limpiar_pantalla()
        sys.exit()


#limpiar_pantalla()
#mostrar_menu()
#limpiar_buffer_entrada()
#paso1 = selec_opcion_menu1()
#if paso1 == 1:
#    paso2 = selec_opcion_menu2()
#elif paso1 == 2:
#    creditos()
#elif paso1 == 3:
#    limpiar_pantalla()
#    sys.exit()
