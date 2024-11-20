import matplotlib.pyplot as plt

# Coordenadas de los nodos
x = [0, 1]
y = [0, 1]

# Crear la figura y los ejes
fig, ax = plt.subplots()

# Dibujar los nodos con un tamaño mayor
ax.scatter(x, y, color='red', s=500, zorder=5)

# Conectar los nodos con una arista azul
ax.plot(x, y, color='blue', zorder=1)

# Etiquetas para los nodos
for i in range(len(x)):
    ax.text(x[i], y[i], f'({x[i]}, {y[i]})', fontsize=12, ha='right')

# Configurar los ejes con un rango un poco más grande
ax.set_xlim(-0.2, 1.2)
ax.set_ylim(-0.2, 1.2)
ax.set_aspect('equal')
ax.grid(True)

# Mostrar el gráfico
plt.title("Gráfico de dos nodos conectados por una arista")
plt.xlabel("Eje X")
plt.ylabel("Eje Y")
plt.show()
