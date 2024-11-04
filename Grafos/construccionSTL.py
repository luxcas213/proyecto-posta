from typing import List, Tuple
import numpy as np
from pathlib import Path
from stl import mesh # type: ignore

def main_function(megagrafo: Tuple[List[List[float]], List[List[int]]]) -> None:
    
    def create_3d_object(coordinates):
        vertices = np.array(coordinates)

        mesh_object = mesh.Mesh(np.zeros(vertices.shape[0], dtype=mesh.Mesh.dtype))
        for i, vertex in enumerate(vertices):
            mesh_object.vectors[i] = vertex
        return mesh_object

    def export_stl(mesh_object, filename):
        output_file = Path.home() / "Downloads" / filename
        mesh_object.save(str(output_file))

    def crearCaras(objeto):
        con, ver = objeto
        caras=[]

        for i in range(len(con)):
            for j in range(len(ver)):
                if j in con[i]:
                    for k in range(len(ver)):
                        if k!=j and k in con[i]:
                            caras.append([i,j,k])
                            if j not in con[k]:
                                con[j].append(k)
                            if k not in con[j]:
                                con[k].append(j)

                            if i in con[j]:
                                con[j].remove(i)
                            if i in con[k]:
                                con[k].remove(i)
        return caras 

    def llamarIndice(lista, coords):
        out = []
        for i in lista:
            in1=coords[i[0]]
            in2=coords[i[1]]
            in3=coords[i[2]]
            out.append([in1,in2,in3])
        return out

    def sacarIteraciones(caras):
        vistos= set()
        resultado= []
        for i in caras:
            if frozenset(i) not in vistos:
                resultado.append(i)
                vistos.add(frozenset(i))
        return resultado

    def figure():
        vertices = megagrafo[0]
        connections = megagrafo[1]
        return connections, vertices

    def translate(figure):
        connections, vertices= figure
        for ver in range(len(vertices)):
            k=-1
            for i in connections:
                k+=1
                for j in range(len(i)):
                    if vertices[ver]==connections[k][j]:
                        connections[k][j]=ver
        return connections, vertices
    

    
    object3D = create_3d_object(llamarIndice(sacarIteraciones(crearCaras(translate(figure()))),translate(figure())[1]))
    export_stl(object3D,"output.stl")
    print("Objeto creado")