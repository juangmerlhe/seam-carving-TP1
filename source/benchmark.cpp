#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include "FuerzaBruta.h"
#include "Backtracking.h"
#include "ProgramacionDinamica.h"

using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 3) {
        cerr << "uso: ./benchmark <archivo> <fb|bt|pd>" << endl;
        return 1;
    }

    // leer matriz
    ifstream f(argv[1]);
    int n, m;
    f >> n >> m;
    vector<vector<double>> energia(n, vector<double>(m));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            f >> energia[i][j];

    string alg = argv[2];

    // medir tiempo
    auto inicio = chrono::high_resolution_clock::now();
    vector<int> seam;
    if (alg == "fb") seam = encontrarSeamFuerzaBruta(energia);
    else if (alg == "bt") seam = encontrarSeamBacktracking(energia);
    else if (alg == "pd") seam = encontrarSeamPD(energia);
    auto fin = chrono::high_resolution_clock::now();

    double ms = chrono::duration<double, milli>(fin - inicio).count();

    double total = 0;
    for (int i = 0; i < n; i++) total += energia[i][seam[i]];

    // imprime: tiempo_ms energia_total
    cout << ms << " " << total << endl;
    return 0;
}
