#include "ProgramacionDinamica.h"
#include <vector>

using namespace std;

// Calcula el seam de mínima energía con programación dinámica en O(n·m).
vector<int> encontrarSeamPD(const vector<vector<double>>& energia) {
    int n = energia.size();
    if (n == 0) return {};

    int m = energia[0].size();
    if (m == 0) return {};

    vector<vector<double>> pd(n, vector<double>(m));
    vector<vector<int>> padre(n, vector<int>(m, -1));

    for (int j = 0; j < m; j++) {
        pd[0][j] = energia[0][j];
    }

    for (int i = 1; i < n; i++) {
        for (int j = 0; j < m; j++) {
            int mejorCol = j;
            double mejorCosto = pd[i - 1][j];

            if (j > 0 && pd[i - 1][j - 1] < mejorCosto) {
                mejorCosto = pd[i - 1][j - 1];
                mejorCol = j - 1;
            }

            if (j + 1 < m && pd[i - 1][j + 1] < mejorCosto) {
                mejorCosto = pd[i - 1][j + 1];
                mejorCol = j + 1;
            }

            pd[i][j] = energia[i][j] + mejorCosto;
            padre[i][j] = mejorCol;
        }
    }

    int mejorCol = 0;
    double mejorSuma = pd[n - 1][0];

    for (int j = 1; j < m; j++) {
        if (pd[n - 1][j] < mejorSuma) {
            mejorSuma = pd[n - 1][j];
            mejorCol = j;
        }
    }

    vector<int> seam(n);
    int col = mejorCol;

    for (int i = n - 1; i >= 0; i--) {
        seam[i] = col;
        col = padre[i][col];
    }

    return seam;
}