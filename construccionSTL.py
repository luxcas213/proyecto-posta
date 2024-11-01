from typing import List, Tuple
import numpy as np
from pathlib import Path

def main_function(megagrafo: Tuple[List[List[float]], List[List[int]]]) -> None:
    directorio_descargas = Path.home() / "Downloads"
    archivo_stl = directorio_descargas / 'objeto.stl'
    vertices = megagrafo[0]
    connections = megagrafo[1]

    def calcular_normal(v1, v2, v3):
        v1, v2, v3 = np.array(v1), np.array(v2), np.array(v3)
        normal = np.cross(v2 - v1, v3 - v1)
        return normal / np.linalg.norm(normal) if np.linalg.norm(normal) != 0 else [0, 0, 0]

    def generar_triangulos(vertices, connections):
        triangulos = []
        for i, conn in enumerate(connections):
            for j in range(len(conn)):
                # Formamos triángulos utilizando el vértice actual y dos vértices consecutivos en la lista de conexiones
                v1 = np.array(vertices[i])
                v2 = np.array(vertices[conn[j]])
                v3 = np.array(vertices[conn[(j + 1) % len(conn)]])
                triangulos.append((v1, v2, v3))
        return triangulos

    def guardar_stl(triangulos, archivo=archivo_stl):
        with open(archivo, 'w') as file:
            file.write("solid objeto\n")
            for tri in triangulos:
                v1, v2, v3 = tri
                normal = calcular_normal(v1, v2, v3)
                file.write(f"  facet normal {normal[0]} {normal[1]} {normal[2]}\n")
                file.write("    outer loop\n")
                for v in (v1, v2, v3):
                    file.write(f"      vertex {v[0]} {v[1]} {v[2]}\n")
                file.write("    endloop\n")
                file.write("  endfacet\n")
            file.write("endsolid objeto\n")

    triangulos = generar_triangulos(vertices, connections)
    guardar_stl(triangulos)
    print(f"Archivo STL guardado en: {archivo_stl}")

if __name__ == "__main__":
    vertices = [
        [1, 0, 0],   # Vértice 0
        [-1, 0, 0],  # Vértice 1
        [0, 1, 0],   # Vértice 2
        [0, -1, 0],  # Vértice 3
        [0, 0, 1],   # Vértice 4
        [0, 0, -1]   # Vértice 5
    ]

    # Definimos las conexiones (aristas) entre los vértices del octaedro
    connections = [
        [5, 2, 4, 3],  # Vértice 0 se conecta con 5, 2, 4, 3
        [5, 2, 3, 4],  # Vértice 1 se conecta con 5, 2, 3, 4
        [4, 1, 0, 5],  # Vértice 2 se conecta con 4, 1, 0, 5
        [4, 1, 0, 5],  # Vértice 3 se conecta con 4, 1, 0, 5
        [1, 2, 0, 3],  # Vértice 4 se conecta con 1, 2, 0, 3
        [1, 3, 0, 2]   # Vértice 5 se conecta con 1, 3, 0, 2
    ]

    main_function((vertices, connections))
