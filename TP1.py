#*******CONSTANTES GLOBALES**********************************************
CONTORNO_CELDA = [ (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1) ]
MAX_CELULAS_VIVAS = 3
MIN_CELULAS_VIVAS = 2
VIVA = "#"
MUERTA = "."

"""
Conway's Game of Life
---------------------

https://es.wikipedia.org/wiki/Juego_de_la_vida

El "tablero de juego" es una malla formada por cuadrados ("células") que se
extiende por el infinito en todas las direcciones. Cada célula tiene 8 células
vecinas, que son las que están próximas a ella, incluidas las diagonales. Las
células tienen dos estados: están "vivas" o "muertas" (o "encendidas" y
"apagadas"). El estado de la malla evoluciona a lo largo de unidades de tiempo
discretas (se podría decir que por turnos). El estado de todas las células se
tiene en cuenta para calcular el estado de las mismas al turno siguiente.
Todas las células se actualizan simultáneamente.

Las transiciones dependen del número de células vecinas vivas:

* Una célula muerta con exactamente 3 células vecinas vivas "nace" (al turno
  siguiente estará viva).
* Una célula viva con 2 ó 3 células vecinas vivas sigue viva, en otro caso
  muere o permanece muerta (por "soledad" o "superpoblación").
"""


def main():
    """
    Función principal del programa. Crea el estado inicial de Game of LIfe
    y muestra la simulación paso a paso mientras que el usuaio presione
    Enter.
    """
    lista2 = ["..............................",
             "..............................",
             "................#.............",
             ".................#............",
             "...............###............",
             "......##......................",
             "...#...#..#...................",
             "....#.........................",
             "...........#..................",
             "...#.........#....###.........",
             "....#.......#.#...............",
             "...#..........#...............",
             ".............#.##.............",
             "....#.........................",
             "..................###.........",]
    
    lista = ["..............................",
             "..............................",
             "................#.............",
             ".................#............",
             "...............###............",
             "..............................",
             "..............................",
             "..............................",
             "..............................",
             "..............................",
             "..............................",
             "..............................",
             "..............................",
             "..............................",
             "..............................",]
    
#    life = life_crear([
#        '..........',
#        '..........',
#        '..........',
#        '.....#....',
#        '......#...',
#        '....###...',
#        '..........',
#        '..........',
#    ])

    life = life_crear(lista2)
    while True:
        for linea in life_mostrar(life):
            print(linea)
        print()
        input("Presione Enter para continuar, CTRL+C para terminar")
        print()
        life = life_siguiente(life)

def life_crear(mapa):
    """
    Crea el estado inicial de Game of life a partir de una disposición
    representada con los caracteres '.' y '#'.

    `mapa` debe ser una lista de cadenas, donde cada cadena representa una
    fila del tablero, y cada caracter puede ser '.' (vacío) o '#' (célula).
    Todas las filas deben tener la misma cantidad decaracteres.

    Devuelve el estado del juego, que es una lista de listas donde cada
    sublista representa una fila, y cada elemento de la fila es False (vacío)
    o True (célula).
    """
        
    return [ [celda == VIVA for celda in fila] for fila in mapa ]


def pruebas_life_crear():
    """Prueba el correcto funcionamiento de life_crear()."""
    # Para cada prueba se utiliza la instrucción `assert <condición>`, que
    # evalúa que la <condición> sea verdadera, y lanza un error en caso
    # contrario.
    assert life_crear([]) == []
    assert life_crear(['.']) == [[False]]
    assert life_crear(['#']) == [[True]]
    assert life_crear(['#.', '.#']) == [[True, False], [False, True]]
    print("SUCCESFUL life_crear")

def life_mostrar(life):
    """
    Crea una representación del estado del juego para mostrar en pantalla.

    Recibe el estado del juego (inicialmente creado con life_crear()) y
    devuelve una lista de cadenas con la representación del tablero para
    mostrar en la pantalla. Cada una de las cadenas representa una fila
    y cada caracter debe ser '.' (vacío) o '#' (célula).
    """
    life_tablero = [ [ VIVA if celda else MUERTA for celda in fila] for fila in life ]

    return [ "".join(fila) for fila in life_tablero ]
     

def pruebas_life_mostrar():
    """Prueba el correcto funcionamiento de life_mostrar()."""
    assert life_mostrar([]) == []
    assert life_mostrar([[False]]) == ['.']
    assert life_mostrar([[True]]) == ['#']
    assert life_mostrar([[True, False], [False, True]]) == ['#.', '.#']
    print("SUCCESFUL life_mostrar")

def cant_adyacentes(life, f, c):
    """
    Calcula la cantidad de células adyacentes a la celda en la fila `f` y la
    columna `c`.

    Importante: El "tablero" se considera "infinito": las celdas del borde
    izquierdo están conectadas a la izquierda con las celdas del borde
    derecho, y viceversa. Las celdas del borde superior están conectadas hacia
    arriba con las celdas del borde inferior, y viceversa.
    """
    cantidad_ady = 0

    for fil,col in CONTORNO_CELDA:
        fila = ( f + fil ) % len( life )
        columna = ( c + col ) % len( life[0] )

        cantidad_ady += 1 if life[fila][columna] else 0

    return cantidad_ady

def pruebas_cant_adyacentes():
    """Prueba el correcto funcionamiento de cant_adyacentes()."""
    assert cant_adyacentes(life_crear(['.']), 0, 0) == 0
    assert cant_adyacentes(life_crear(['..', '..']), 0, 0) == 0
    assert cant_adyacentes(life_crear(['..', '..']), 0, 1) == 0
    assert cant_adyacentes(life_crear(['##', '..']), 0, 0) == 2
    assert cant_adyacentes(life_crear(['##', '..']), 0, 1) == 2
    assert cant_adyacentes(life_crear(['#.', '.#']), 0, 0) == 4
    assert cant_adyacentes(life_crear(['##', '##']), 0, 0) == 8
    assert cant_adyacentes(life_crear(['.#.', '#.#', '.#.']), 1, 1) == 4
    assert cant_adyacentes(life_crear(['.#.', '..#', '.#.']), 1, 1) == 3
    print("SUCCESFUL cantidad_adyacentes")

def celda_siguiente(life, f, c):
    """
    Calcula el estado siguiente de la celda ubicada en la fila `f` y la
    columna `c`.

    Devuelve True si en la celda (f, c) habrá una célula en la siguiente
    iteración, o False si la celda quedará vacía.
    """
    adyacentes = cant_adyacentes(life, f, c)
    
    if not life[f][c]:
        return adyacentes == MAX_CELULAS_VIVAS
        
    return adyacentes == MIN_CELULAS_VIVAS or adyacentes == MAX_CELULAS_VIVAS
    

def pruebas_celda_siguiente():
    """Prueba el correcto funcionamiento de celda_siguiente()."""
    assert celda_siguiente(life_crear(['.']), 0, 0) == False
    assert celda_siguiente(life_crear(['..', '..']), 0, 0) == False
    assert celda_siguiente(life_crear(['..', '..']), 0, 1) == False
    assert celda_siguiente(life_crear(['##', '..']), 0, 0) == True
    assert celda_siguiente(life_crear(['##', '..']), 0, 1) == True
    assert celda_siguiente(life_crear(['#.', '.#']), 0, 0) == False
    assert celda_siguiente(life_crear(['##', '##']), 0, 0) == False
    assert celda_siguiente(life_crear(['.#.', '#.#', '.#.']), 1, 1) == False
    assert celda_siguiente(life_crear(['.#.', '..#', '.#.']), 1, 1) == True
    print("SUCCESFUL celda_siguiente")

def life_siguiente(life):
    """
    Calcula el siguiente estado del juego.

    Recibe el estado actual del juego (lista de listas de False/True) y
    devuelve un _nuevo_ estado que representa la siguiente iteración según las
    reglas del juego.

    Importante: El "tablero" se considera "infinito": las celdas del borde
    izquierdo están conectadas a la izquierda con las celdas del borde
    derecho, y viceversa. Las celdas del borde superior están conectadas hacia
    arriba con las celdas del borde inferior, y viceversa.
    """
    
    #APORTADO POR LA CATEDRA
    #siguiente = []
    #for f in range(len(life)):
    #  fila = []
    #    for c in range(len(life[0])):
    #        fila.append(celda_siguiente(life, f, c))
    #    siguiente.append(fila)
    #return siguiente
    return [ [ celda_siguiente(life,f,c) for c in range( len( life[0] ) ) ] for f in range( len( life ) ) ]


def pruebas():
    """Ejecuta todas las pruebas"""
    pruebas_life_crear()
    pruebas_life_mostrar()
    pruebas_cant_adyacentes()
    pruebas_celda_siguiente()

pruebas()

main()
