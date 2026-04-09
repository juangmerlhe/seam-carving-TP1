"""
Seam Carving — Backtracking
============================
Explora recursivamente todos los caminos posibles desde cada columna de la
primera fila hasta la última, eligiendo en cada paso entre las tres columnas
adyacentes (j-1, j, j+1). Se aplica una PODA que descarta ramas cuya suma
acumulada ya supera la mejor solución encontrada hasta el momento.

Complejidad temporal:  O(m · 3^n)  — sin poda; con poda mejora en la
                        práctica, pero el peor caso sigue siendo exponencial.
Complejidad espacial:  O(n)  — pila de recursión + lista `actual` (longitud n).
"""

from typing import Optional


def _recorrer_bt(
    energia: list[list[float]],
    fila: int,
    col: int,
    actual: list[int],
    mejor: list[int],
    suma: float,
    mejor_suma: list[float],   # lista mutable para simular paso por referencia
) -> None:
    """
    Función recursiva auxiliar.

    Parameters
    ----------
    energia     : Matriz de energías de la imagen.
    fila        : Fila actual en la recursión.
    col         : Columna actual.
    actual      : Camino en construcción.
    mejor       : Mejor camino encontrado hasta ahora (se modifica in-place).
    suma        : Energía acumulada del camino actual.
    mejor_suma  : Lista de un elemento que contiene la mejor suma (paso por ref.).
    """
    n = len(energia)
    m = len(energia[0])

    actual.append(col)
    suma += energia[fila][col]

    # PODA: si ya superamos la mejor suma conocida, no seguir
    if mejor and suma >= mejor_suma[0]:
        actual.pop()
        return

    if fila == n - 1:
        # Caso base: llegamos a la última fila
        if not mejor or suma < mejor_suma[0]:
            mejor[:] = list(actual)   # actualizar in-place (equivale a mejor = actual)
            mejor_suma[0] = suma
    else:
        # Paso recursivo: explorar columnas adyacentes válidas
        for j in range(col - 1, col + 2):
            if 0 <= j < m:
                _recorrer_bt(energia, fila + 1, j, actual, mejor, suma, mejor_suma)

    actual.pop()


def encontrar_seam_backtracking(energia: list[list[float]]) -> list[int]:
    """
    Encuentra el seam vertical de mínima energía usando Backtracking.

    Parameters
    ----------
    energia : Matriz n×m de valores de energía (flotantes).

    Returns
    -------
    Lista de n enteros, donde el i-ésimo valor es la columna del seam en la fila i.
    """
    m = len(energia[0])

    mejor: list[int] = []
    actual: list[int] = []
    mejor_suma: list[float] = [-1.0]   # -1 indica "aún sin solución"

    for j in range(m):
        _recorrer_bt(energia, 0, j, actual, mejor, 0.0, mejor_suma)

    return mejor
