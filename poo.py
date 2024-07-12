import heapq

CAMINO = 0
EDIFICIO = 1
TORRE = 2
CABANHA = 3

class Mapa:
    def __init__(self, filas, columnas):
        self.matriz = self.generar_matriz(filas, columnas)

    def generar_matriz(self, filas, columnas):
        matriz = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                fila.append(CAMINO)
            matriz.append(fila)
        return matriz

    def introducir_obstaculos(self):
        while True:
            try:
                filao = input("Introduzca la fila del obstáculo (o 'exit' para salir): ")
                if filao.lower() == 'exit':
                    break
                filao = int(filao)
                columnao = int(input("Introduzca la columna del obstáculo: "))
                if 0 <= filao < len(self.matriz) and 0 <= columnao < len(self.matriz[0]) and self.matriz[filao][columnao] == CAMINO:
                    tipo_de_obstaculo = int(input("Introduzca el tipo de obstáculo (1 para EDIFICIO, 2 para TORRE, 3 para CABANHA): "))
                    if tipo_de_obstaculo in [EDIFICIO, TORRE, CABANHA]:
                        self.matriz[filao][columnao] = tipo_de_obstaculo
                    else:
                        print("El tipo de obstáculo es inválido. Use 1, 2, o 3.")
                else:
                    print("Coordenadas fuera de rango o celda no transitable.")
            except ValueError:
                print("Entrada inválida. Introduzca números enteros.")

    def definir_puntos(self):
        while True:
            try:
                fila_inicio = int(input("Introduzca la fila del punto de inicio: "))
                columna_inicio = int(input("Introduzca la columna del punto de inicio: "))
                fila_destino = int(input("Introduzca la fila del punto de destino: "))
                columna_destino = int(input("Introduzca la columna del punto de destino: "))

                if 0 <= fila_inicio < len(self.matriz) and 0 <= columna_inicio < len(self.matriz[0]) and \
                   0 <= fila_destino < len(self.matriz) and 0 <= columna_destino < len(self.matriz[0]) and \
                   self.matriz[fila_inicio][columna_inicio] == CAMINO and self.matriz[fila_destino][columna_destino] == CAMINO:
                    return (fila_inicio, columna_inicio), (fila_destino, columna_destino)
                else:
                    print("Coordenadas fuera de rango o son obstáculos.")
            except ValueError:
                print("Entrada inválida. Introduzca números enteros.")

    def imprimir(self, inicio, destino, ruta=None):
        simbolos = {CAMINO: '.',
                    CABANHA: 'X',
                    TORRE: '&',
                    EDIFICIO: '#'}
        for i, fila in enumerate(self.matriz):
            for j, celda in enumerate(fila):
                if (i, j) == inicio:
                    print('S', end=' ')
                elif (i, j) == destino:
                    print('D', end=' ')
                elif ruta and (i, j) in ruta:
                    print('*', end=' ')
                else:
                    print(simbolos.get(celda, celda), end=' ')
            print()

    def agregar_obstaculo(self, fila, columna, tipo):
        if 0 <= fila < len(self.matriz) and 0 <= columna < len(self.matriz[0]):
            if self.matriz[fila][columna] == CAMINO and tipo in [EDIFICIO, TORRE, CABANHA]:
                self.matriz[fila][columna] = tipo
            else:
                print("No se puede agregar el obstáculo en esta posición.")
        else:
            print("Coordenadas fuera de rango.")

    def quitar_obstaculo(self, fila, columna):
        if 0 <= fila < len(self.matriz) and 0 <= columna < len(self.matriz[0]):
            if self.matriz[fila][columna] != CAMINO:
                self.matriz[fila][columna] = CAMINO
            else:
                print("La celda no tiene un obstáculo.")
        else:
            print("Coordenadas fuera de rango.")


class AEstrella:
    def __init__(self, mapa, inicio, destino):
        self.mapa = mapa
        self.inicio = inicio
        self.destino = destino

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def encontrar_ruta(self):
        filas = len(self.mapa.matriz)
        columnas = len(self.mapa.matriz[0])

        lista_abierta = []
        lista_cerrada = set()

        heapq.heappush(lista_abierta, (0, self.inicio))
        came_from = {}
        g_score = {self.inicio: 0}
        f_score = {self.inicio: self.heuristica(self.inicio, self.destino)}

        while lista_abierta:
            _, current = heapq.heappop(lista_abierta)

            if current == self.destino:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.inicio)
                return path[::-1]

            lista_cerrada.add(current)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                vecino = (current[0] + dx, current[1] + dy)

                if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                    if self.mapa.matriz[vecino[0]][vecino[1]] == EDIFICIO:
                        continue

                    tentative_g_score = g_score[current] + 1

                    if vecino in lista_cerrada and tentative_g_score >= g_score.get(vecino, float('inf')):
                        continue
                    if tentative_g_score < g_score.get(vecino, float('inf')):
                        came_from[vecino] = current
                        g_score[vecino] = tentative_g_score
                        f_score[vecino] = tentative_g_score + self.heuristica(vecino, self.destino)
                        if vecino not in [i[1] for i in lista_abierta]:
                            heapq.heappush(lista_abierta, (f_score[vecino], vecino))

        return None


def main():
    filas = int(input("Ingrese el número de filas: "))
    columnas = int(input("Ingrese el número de columnas: "))

    mapa = Mapa(filas, columnas)
    mapa.introducir_obstaculos()
    inicio, destino = mapa.definir_puntos()

    while True:
        accion = input("¿Quieres agregar o quitar un obstáculo? (agregar/quitar/continuar): ").lower()
        if accion in ['agregar', 'quitar']:
            fila = int(input("Ingresa la fila del obstáculo: "))
            columna = int(input("Ingresa la columna del obstáculo: "))
            if accion == 'agregar':
                tipo = int(input("Introduzca el tipo de obstáculo (1 para EDIFICIO, 2 para TORRE, 3 para CABANHA): "))
                mapa.agregar_obstaculo(fila, columna, tipo)
            elif accion == 'quitar':
                mapa.quitar_obstaculo(fila, columna)
            mapa.imprimir(inicio, destino)
        elif accion == 'continuar':
            break

    a_estrella = AEstrella(mapa, inicio, destino)
    ruta = a_estrella.encontrar_ruta()

    if ruta:
        mapa.imprimir(inicio, destino, ruta)
    else:
        print("No se encontró un CAMINO desde el punto de inicio al destino.")


if __name__ == "__main__":
    main()
