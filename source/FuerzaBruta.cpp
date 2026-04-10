#include "FuerzaBruta.h"
#include <vector>

using namespace std;

// Recorre recursivamente todos los caminos posibles desde (fila, col) hasta la última fila.
void recorrerFB(const vector<vector<double>>& energia,
              int fila,
              int col,
              vector<int>& actual,
              vector<int>& mejor,
              double suma,
              double& mejorSuma) {

    int n = energia.size();
    int m = energia[0].size();

    actual.push_back(col);
    suma += energia[fila][col];

    if (fila == n - 1) {
        if (mejor.empty() || suma < mejorSuma) {
            mejor = actual;
            mejorSuma = suma;
        }
    } else {
        for (int j = col - 1; j <= col + 1; j++) {
            if (j >= 0 && j < m) {
                recorrerFB(energia, fila + 1, j, actual, mejor, suma, mejorSuma);
            }
        }
    }

    actual.pop_back();
}

// Prueba todas las columnas de inicio y devuelve el seam de mínima energía por fuerza bruta.
std::vector<int> encontrarSeamFuerzaBruta(const std::vector<std::vector<double>>& energia) {
    int n = energia.size();
    int m = energia[0].size();

    vector<int> mejor;
    vector<int> actual;
    double mejorSuma = -1;

    for (int j = 0; j < m; j++) {
        recorrerFB(energia, 0, j, actual, mejor, 0, mejorSuma);
    }

    return mejor;
}