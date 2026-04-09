import subprocess, time, random, os, sys, csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))
from backtracking import encontrar_seam_backtracking
from programacion_dinamica import encontrar_seam_pd

BENCHMARK = './benchmark'
REPS = 3

def generar_matriz(n, m, tipo='random', seed=42):
    rng = random.Random(seed)
    if tipo == 'random':
        return [[round(rng.uniform(0, 100), 2) for _ in range(m)] for _ in range(n)]
    elif tipo == 'uniforme':
        return [[5.0] * m for _ in range(n)]
    elif tipo == 'columna_baja':
        # una columna con energia casi 0 para que la poda corte rapido
        col = m // 2
        mat = [[round(rng.uniform(50, 100), 2) for _ in range(m)] for _ in range(n)]
        for i in range(n):
            mat[i][col] = 0.01
        return mat

def guardar_matriz(mat, path):
    n, m = len(mat), len(mat[0])
    with open(path, 'w') as f:
        f.write(f"{n} {m}\n")
        for fila in mat:
            f.write("  ".join(f"{v:.2f}" for v in fila) + "\n")

def leer_matriz(path):
    with open(path) as f:
        n, m = map(int, f.readline().split())
        return [list(map(float, f.readline().split())) for _ in range(n)]

def medir_cpp(archivo, alg):
    # corre el benchmark de c++ y devuelve tiempo en ms
    tiempos = []
    for _ in range(REPS):
        try:
            r = subprocess.run([BENCHMARK, archivo, alg], capture_output=True, text=True, timeout=120)
            t = float(r.stdout.strip().split()[0])
            tiempos.append(t)
        except:
            return None
    return np.mean(tiempos)

def medir_python(energia, alg):
    tiempos = []
    for _ in range(REPS):
        t0 = time.perf_counter()
        if alg == 'bt':
            encontrar_seam_backtracking(energia)
        else:
            encontrar_seam_pd(energia)
        t1 = time.perf_counter()
        tiempos.append((t1 - t0) * 1000)
    return np.mean(tiempos)

# ==== experimento 1: escalabilidad con matrices cuadradas ====

def exp_escalabilidad():
    print("=== exp 1: escalabilidad ===")

    sizes = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    sizes_pd = sizes + [50, 100, 200, 500, 1000]

    resultados = []

    for n in sorted(set(sizes_pd)):
        print(f"  n={n}", end="", flush=True)
        path = f"experimentos/random_{n}x{n}.txt"
        mat = generar_matriz(n, n)
        guardar_matriz(mat, path)

        fila = {'n': n}

        # fb solo hasta 18
        if n <= 18:
            fila['fb_cpp'] = medir_cpp(path, 'fb')
        else:
            fila['fb_cpp'] = None

        # bt cpp hasta 22, bt python hasta 18
        if n <= 22:
            fila['bt_cpp'] = medir_cpp(path, 'bt')
        else:
            fila['bt_cpp'] = None

        if n <= 18:
            fila['bt_py'] = medir_python(mat, 'bt')
        else:
            fila['bt_py'] = None

        fila['pd_cpp'] = medir_cpp(path, 'pd')
        fila['pd_py'] = medir_python(mat, 'pd')

        resultados.append(fila)
        print(f"  ok")

    # guardar csv
    with open('experimentos/exp1_escalabilidad.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['n', 'fb_cpp', 'bt_cpp', 'pd_cpp', 'bt_py', 'pd_py'])
        w.writeheader()
        w.writerows(resultados)

    # graficar
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    for alg, color, label in [('fb_cpp', 'red', 'FB C++'), ('bt_cpp', 'blue', 'BT C++'), ('bt_py', 'purple', 'BT Python')]:
        ns = [r['n'] for r in resultados if r[alg] is not None]
        ts = [r[alg] for r in resultados if r[alg] is not None]
        if ns:
            ax1.plot(ns, ts, 'o-', color=color, label=label)

    ax1.set_yscale('log')
    ax1.set_xlabel('n')
    ax1.set_ylabel('tiempo (ms)')
    ax1.set_title('FB y BT (escala log)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    for alg, color, label in [('pd_cpp', 'green', 'PD C++'), ('pd_py', 'orange', 'PD Python')]:
        ns = [r['n'] for r in resultados if r[alg] is not None]
        ts = [r[alg] for r in resultados if r[alg] is not None]
        ax2.plot(ns, ts, 's-', color=color, label=label)

    ax2.set_xlabel('n')
    ax2.set_ylabel('tiempo (ms)')
    ax2.set_title('PD: O(n*m)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('experimentos/exp1_escalabilidad.png', dpi=150)
    plt.close()

# ==== experimento 2: efecto de la poda ====

def exp_poda():
    print("=== exp 2: efecto de la poda ===")

    n, m = 14, 14
    resultados = []

    for tipo in ['random', 'uniforme', 'columna_baja']:
        path = f"experimentos/{tipo}_{n}x{m}.txt"
        mat = generar_matriz(n, m, tipo)
        guardar_matriz(mat, path)

        fb = medir_cpp(path, 'fb')
        bt = medir_cpp(path, 'bt')
        print(f"  {tipo}: fb={fb:.1f}ms  bt={bt:.1f}ms  speedup={fb/bt:.0f}x")
        resultados.append({'tipo': tipo, 'fb_cpp': fb, 'bt_cpp': bt})

    with open('experimentos/exp2_poda.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['tipo', 'fb_cpp', 'bt_cpp'])
        w.writeheader()
        w.writerows(resultados)

    # grafico de barras
    fig, ax = plt.subplots(figsize=(8, 5))
    tipos = [r['tipo'] for r in resultados]
    x = np.arange(len(tipos))
    ax.bar(x - 0.17, [r['fb_cpp'] for r in resultados], 0.34, label='FB', color='red')
    ax.bar(x + 0.17, [r['bt_cpp'] for r in resultados], 0.34, label='BT', color='blue')
    ax.set_xticks(x)
    ax.set_xticklabels(tipos)
    ax.set_ylabel('tiempo (ms)')
    ax.set_title('efecto de la poda (14x14)')
    ax.legend()
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('experimentos/exp2_poda.png', dpi=150)
    plt.close()

# ==== experimento 3: filas fijas, variando columnas ====

def exp_columnas():
    print("=== exp 3: variando columnas (n=15) ===")

    n = 15
    cols = [3, 5, 8, 10, 15, 20, 30, 50]
    resultados = []

    for m in cols:
        path = f"experimentos/cols_{n}x{m}.txt"
        mat = generar_matriz(n, m)
        guardar_matriz(mat, path)

        fila = {'m': m}
        fila['fb_cpp'] = medir_cpp(path, 'fb') if m <= 20 else None
        fila['bt_cpp'] = medir_cpp(path, 'bt')
        fila['pd_cpp'] = medir_cpp(path, 'pd')
        resultados.append(fila)
        print(f"  m={m} done")

    with open('experimentos/exp3_columnas.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['m', 'fb_cpp', 'bt_cpp', 'pd_cpp'])
        w.writeheader()
        w.writerows(resultados)

    fig, ax = plt.subplots(figsize=(8, 5))
    for alg, color, label in [('fb_cpp', 'red', 'FB'), ('bt_cpp', 'blue', 'BT'), ('pd_cpp', 'green', 'PD')]:
        ms = [r['m'] for r in resultados if r[alg] is not None]
        ts = [r[alg] for r in resultados if r[alg] is not None]
        if ms:
            ax.plot(ms, ts, 'o-', color=color, label=label)
    ax.set_yscale('log')
    ax.set_xlabel('columnas')
    ax.set_ylabel('tiempo (ms)')
    ax.set_title('n=15 fijo, variando columnas')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('experimentos/exp3_columnas.png', dpi=150)
    plt.close()

# ==== main ====

if __name__ == '__main__':
    os.makedirs('experimentos', exist_ok=True)

    if not os.path.exists(BENCHMARK):
        print("compilar primero: g++ -std=c++17 -O2 -o benchmark source/benchmark.cpp source/FuerzaBruta.cpp source/Backtracking.cpp source/ProgramacionDinamica.cpp")
        sys.exit(1)

    exp_escalabilidad()
    exp_poda()
    exp_columnas()
    print("\nlisto, resultados en experimentos/")
