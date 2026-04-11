#!/usr/bin/env python3
"""
Test de integración: verifica que los 5 algoritmos den energía 4.3 en input/ejemplo.txt.
Ejecutar desde el directorio raíz del proyecto: python3 source/test.py
"""

import subprocess
import sys
import os

# Asegurarse de que los módulos Python del proyecto sean importables
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from programacion_dinamica import encontrar_seam_pd
from backtracking import encontrar_seam_backtracking

EXPECTED_ENERGY = 4.3
TOLERANCE = 1e-6
INPUT_FILE = "input/ejemplo.txt"


def leer_energia(ruta):
    with open(ruta) as f:
        n, m = map(int, f.readline().split())
        return [list(map(float, f.readline().split())) for _ in range(n)]


def energia_seam(energia, seam):
    return sum(energia[i][seam[i]] for i in range(len(seam)))


def run_cpp(alg):
    """Corre el binario ./seam en modo numérico y extrae la energía total."""
    result = subprocess.run(
        ["./seam", "--numerico", INPUT_FILE, "--algoritmo", alg],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        if "Energía total:" in line:
            return float(line.split(":")[1].strip())
    return None


def main():
    energia = leer_energia(INPUT_FILE)

    results = {}

    # Algoritmos Python
    results["python-pd"] = energia_seam(energia, encontrar_seam_pd(energia))
    results["python-bt"] = energia_seam(energia, encontrar_seam_backtracking(energia))

    # Algoritmos C++
    for alg in ["fb", "bt", "pd"]:
        results[f"cpp-{alg}"] = run_cpp(alg)

    all_pass = True
    for name, e in results.items():
        ok = e is not None and abs(e - EXPECTED_ENERGY) < TOLERANCE
        print(f"  {name}: energía={e}  [{'PASS' if ok else 'FAIL'}]")
        if not ok:
            all_pass = False

    print()
    print("PASS" if all_pass else "FAIL")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
