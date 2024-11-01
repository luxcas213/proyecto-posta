import os
import numpy as np
from pathlib import Path

# Obtén la ruta correcta de la carpeta de Descargas
directorio_descargas = Path.home() / "Downloads"

# Asegúrate de que la carpeta de Descargas existe
if not directorio_descargas.exists():
    print("La carpeta de Descargas no existe en la ruta especificada.")
else:
    # Nombre del archivo STL
    archivo_stl = directorio_descargas / 'objeto.stl'

    # Vértices del grafo 3D (octaedro)
    vertices = [
        [1, 0, 0],   # Vértice 0
        [-1, 0, 0],  # Vértice 1
        [0, 1, 0],   # Vértice 2
        [0, -1, 0],  # Vértice 3
        [0, 0, 1],   # Vértice 4
        [0, 0, -1]   # Vértice 5
    ]

    # Conexiones entre vértices
    connections = [
        [2, 5, 3, 4],  # Vértice 0
        [5, 2, 3, 4],  # Vértice 1
        [4, 5, 1, 0],  # Vértice 2
        [4, 1, 0, 5],  # Vértice 3
        [1, 2, 0, 3],  # Vértice 4
        [1, 0, 2, 3]   # Vértice 5
    ]

    # Función para calcular la normal de un triángulo dado por tres puntos
    def calcular_normal(v1, v2, v3):
        v1, v2, v3 = np.array(v1), np.array(v2), np.array(v3)
        normal = np.cross(v2 - v1, v3 - v1)
        return normal / np.linalg.norm(normal) if np.linalg.norm(normal) != 0 else [0, 0, 0]

    # Generar triángulos a partir de las conexiones
    def generar_triangulos(vertices, connections):
        triangulos = []
        for i, conn in enumerate(connections):
            for j in range(len(conn)):
                v1 = vertices[i]
                v2 = vertices[conn[j]]
                v3 = vertices[conn[(j + 1) % len(conn)]]
                triangulos.append((v1, v2, v3))
        return triangulos

    # Función para guardar los triángulos en un archivo STL
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

    # Generación de triángulos y guardado del archivo STL
    triangulos = generar_triangulos(vertices, connections)
    guardar_stl(triangulos)
    print(f"Archivo STL guardado en: {archivo_stl}")
