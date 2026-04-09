#include "Backtracking.h"
#include <vector>

using namespace std;

void recorrerBT(const vector<vector<double>>& energia,
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

    //PODA
    if (!mejor.empty() && suma >= mejorSuma) {
        actual.pop_back();
        return;
    }

    if (fila == n - 1) {
        if (mejor.empty() || suma < mejorSuma) {
            mejor = actual;
            mejorSuma = suma;
        }
    } else {
        for (int j = col - 1; j <= col + 1; j++) {
            if (j >= 0 && j < m) {
                recorrerBT(energia, fila + 1, j, actual, mejor, suma, mejorSuma);
            }
        }
    }

    actual.pop_back();
}

std::vector<int> encontrarSeamBacktracking(const std::vector<std::vector<double>>& energia) {
    int m = energia[0].size();

    vector<int> mejor;
    vector<int> actual;
    double mejorSuma = -1;

    for (int j = 0; j < m; j++) {
        recorrerBT(energia, 0, j, actual, mejor, 0, mejorSuma);
    }

    return mejor;
}
