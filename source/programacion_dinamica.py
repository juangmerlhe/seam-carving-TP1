"""
Seam Carving — Programación Dinámica
======================================
Construye una tabla `pd` donde pd[i][j] acumula la mínima energía posible
para llegar desde cualquier celda de la primera fila hasta la celda (i, j).
En cada celda se registra también el índice `padre[i][j]`, es decir, la columna
de la fila anterior desde la que se llegó con menor costo. Al finalizar el
llenado, se localiza el mínimo en la última fila y se reconstruye el seam
hacia atrás siguiendo los punteros de padre.

Complejidad temporal:  O(n · m)  — dos pasadas: llenado + traceback.
Complejidad espacial:  O(n · m)  — matrices `pd` y `padre` del mismo tamaño.
"""


def encontrar_seam_pd(energia: list[list[float]]) -> list[int]:
    """
    Encuentra el seam vertical de mínima energía usando Programación Dinámica.

    Parameters
    ----------
    energia : Matriz n×m de valores de energía (flotantes).

    Returns
    -------
    Lista de n enteros, donde el i-ésimo valor es la columna del seam en la fila i.
    """
    n = len(energia)
    if n == 0:
        return []

    m = len(energia[0])
    if m == 0:
        return []

    # Tabla de costos acumulados y tabla de punteros padre
    pd:     list[list[float]] = [[0.0] * m for _ in range(n)]
    padre:  list[list[int]]   = [[-1]  * m for _ in range(n)]

    # Caso base: primera fila
    for j in range(m):
        pd[0][j] = energia[0][j]

    # Llenado de la tabla fila a fila
    for i in range(1, n):
        for j in range(m):
            mejor_col  = j
            mejor_costo = pd[i - 1][j]

            if j > 0 and pd[i - 1][j - 1] < mejor_costo:
                mejor_costo = pd[i - 1][j - 1]
                mejor_col   = j - 1

            if j + 1 < m and pd[i - 1][j + 1] < mejor_costo:
                mejor_costo = pd[i - 1][j + 1]
                mejor_col   = j + 1

            pd[i][j]    = energia[i][j] + mejor_costo
            padre[i][j] = mejor_col

    # Buscar la columna con menor costo en la última fila
    mejor_col  = 0
    mejor_suma = pd[n - 1][0]

    for j in range(1, m):
        if pd[n - 1][j] < mejor_suma:
            mejor_suma = pd[n - 1][j]
            mejor_col  = j

    # Reconstrucción del seam mediante traceback
    seam: list[int] = [0] * n
    col = mejor_col

    for i in range(n - 1, -1, -1):
        seam[i] = col
        col = padre[i][col]

    return seam
