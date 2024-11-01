import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from construccionSTL import main_function  



def crear_megagrafo(
    lado_xy: List[List[int]],
    lado_yz: List[List[int]],
    lado_xz: List[List[int]],
    conecciones_xy: List[List[int]],
    conecciones_yz: List[List[int]],
    conecciones_xz: List[List[int]]
) -> Tuple[List[List[int]], List[List[List[int]]]]:

    grafo = []
    padres = {}

    # Crear nodos del grafo
    for i, nodo in enumerate(lado_xy):
        for j, nodo2 in enumerate(lado_xz):
            if nodo2[0] == nodo[0]:
                for k, nodo3 in enumerate(lado_yz):
                    if nodo3[1] == nodo[1] and nodo3[0] == nodo2[1]:
                        nodoaux = [nodo[0], nodo[1], nodo2[1]]
                        palabranodoaux = str(nodoaux)
                        padres[palabranodoaux] = [i, j, k]
                        if nodoaux not in grafo:
                            grafo.append(nodoaux)

    # Crear conexiones entre nodos
    grafo_conexiones = [[] for _ in grafo]
    for i, nodo in enumerate(grafo):
        palabranodo = str(nodo)
        aux = padres[palabranodo]
        aux1, aux2, aux3 = aux

        for nodo2 in grafo:
            if nodo == nodo2:
                continue

            palabranodo2 = str(nodo2)
            Aaux = padres[palabranodo2]
            Aaux1, Aaux2, Aaux3 = Aaux
            si1 = si2 = si3 = False
            if Aaux1 in conecciones_xy[aux1]:
                si1 = True
            if Aaux2 in conecciones_xz[aux2]:
                si2 = True
            if Aaux3 in conecciones_yz[aux3]:
                si3 = True

            if (si1 and si2 and Aaux3 == aux3) or (si1 and si3 and Aaux2 == aux2) or (si2 and si3 and Aaux1 == aux1) or (si1 and si2 and si3):
                grafo_conexiones[i].append(nodo2)

    return grafo, grafo_conexiones


def plot_megagrafo(megagrafo: Tuple[List[List[int]], List[List[List[int]]]]):
    grafo, grafo_conexiones = megagrafo
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot nodes
    for nodo in grafo:
        ax.scatter(nodo[0], nodo[1], nodo[2], c='b', marker='o')

    # Plot edges
    for i, conexiones in enumerate(grafo_conexiones):
        for conexion in conexiones:
            x = [grafo[i][0], conexion[0]]
            y = [grafo[i][1], conexion[1]]
            z = [grafo[i][2], conexion[2]]
            ax.plot(x, y, z, c='r')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()




if __name__ == "__main__":
    # lado_xy = [[0, 0], [1, 0], [1, 1], [0, 1]]
    # lado_yz = [[0, 0], [1, 0], [1, 1], [0, 1]]
    # lado_xz = [[0, 0], [1, 0], [1, 1], [0, 1]]
    # conecciones_xy = [[1, 3], [0, 2], [1, 3], [2, 0]]
    # conecciones_yz = [[1, 3], [0, 2], [1, 3], [2, 0]]
    # conecciones_xz = [[1, 3], [0, 2], [1, 3], [2, 0]]

    
    lado_xy = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]
    lado_yz = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]
    lado_xz = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]
    conecciones_xy = [[1, 3, 4], [0, 2, 4], [1, 3, 4], [2, 0, 4], [0, 1, 2, 3]]
    conecciones_yz = [[1, 3, 4], [0, 2, 4], [1, 3, 4], [2, 0, 4], [0, 1, 2, 3]]
    conecciones_xz = [[1, 3, 4], [0, 2, 4], [1, 3, 4], [2, 0, 4], [0, 1, 2, 3]]

   

    megagrafo = crear_megagrafo(lado_xy, lado_yz, lado_xz, conecciones_xy, conecciones_yz, conecciones_xz)
    
    plot_megagrafo(megagrafo)
    main_function(megagrafo)
    
    