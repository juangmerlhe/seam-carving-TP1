# TP1 — Seam Carving

Implementación de seam carving con tres algoritmos: Fuerza Bruta, Backtracking y Programación Dinámica.

## Requisitos

- `g++` con soporte C++17
- `make`
- `python3` con `matplotlib` y `numpy` (para la experimentación)

## Compilación

```bash
make          # compila el binario ./seam
make benchmark  # compila el binario ./benchmark
```

## Ejecución

### Modo numérico

Recibe una matriz de energía y devuelve la costura de mínima energía como índices de columna (1-based) separados por espacio.

```bash
./seam --numerico input/ejemplo.txt --algoritmo pd
./seam --numerico input/ejemplo.txt --algoritmo fb
./seam --numerico input/ejemplo.txt --algoritmo bt
```

### Modo imagen

Elimina N costuras de una imagen y guarda el resultado en `output/imagenes/`.

```bash
./seam --imagen img/foto.jpg --algoritmo pd --iteraciones 50
```

Los parámetros `--algoritmo` aceptan `fb` (fuerza bruta), `bt` (backtracking) o `pd` (programación dinámica).

## Test de integración

Verifica que los 5 algoritmos (3 en C++, 2 en Python) devuelvan la misma energía mínima en el ejemplo del enunciado:

```bash
python3 source/test.py
```

Salida esperada: `PASS` para todos los algoritmos con energía 4.3.

## Experimentación

```bash
python3 experimentar.py
```

Genera gráficos de escalabilidad, efecto de la poda y variación por columnas en la carpeta `experimentos/`.
