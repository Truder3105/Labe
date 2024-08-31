import sys

class Nodo():
    def __init__(self, estado, padre, accion):
        self.estado = estado
        self.padre = padre
        self.accion = accion

class FronteraPila():
    def __init__(self):
        self.frontera = []

    def agregar(self, nodo):
        self.frontera.append(nodo)

    def contiene_estado(self, estado):
        return any(nodo.estado == estado for nodo in self.frontera)

    def vacia(self):
        return len(self.frontera) == 0

    def remover(self):
        if self.vacia():
            raise Exception("frontera vacía")
        else:
            nodo = self.frontera[-1]
            self.frontera = self.frontera[:-1]
            return nodo

class FronteraCola(FronteraPila):
    def remover(self):
        if self.vacia():
            raise Exception("frontera vacía")
        else:
            nodo = self.frontera[0]
            self.frontera = self.frontera[1:]
            return nodo

class Laberinto():
    def __init__(self, nombre_archivo):
        # Lee el archivo y determina el alto y ancho del laberinto
        with open(nombre_archivo) as archivo:
            contenido = archivo.read()

        # Verifica que haya un punto de inicio y un objetivo
        if contenido.count("A") != 1:
            raise Exception("El laberinto debe tener exactamente un punto de inicio")
        if contenido.count("B") != 1:
            raise Exception("El laberinto debe tener exactamente un objetivo")

        # Determina el alto y el ancho del laberinto
        contenido = contenido.splitlines()
        self.altura = len(contenido)
        self.ancho = max(len(linea) for linea in contenido)

        # Registra las paredes
        self.paredes = []
        for i in range(self.altura):
            fila = []
            for j in range(self.ancho):
                try:
                    if contenido[i][j] == "A":
                        self.inicio = (i, j)
                        fila.append(False)
                    elif contenido[i][j] == "B":
                        self.objetivo = (i, j)
                        fila.append(False)
                    elif contenido[i][j] == " ":
                        fila.append(False)
                    else:
                        fila.append(True)
                except IndexError:
                    fila.append(False)
            self.paredes.append(fila)

        self.solucion = None

    def mostrar(self):
        solucion = self.solucion[1] if self.solucion is not None else None
        print()
        for i, fila in enumerate(self.paredes):
            for j, col in enumerate(fila):
                if col:
                    print("█", end="")
                elif (i, j) == self.inicio:
                    print("A", end="")
                elif (i, j) == self.objetivo:
                    print("B", end="")
                elif solucion is not None and (i, j) in solucion:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def vecinos(self, estado):
        fila, col = estado
    
        # Todas las posibles acciones
        candidatos = [
            ("arriba", (fila - 1, col)),
            ("abajo", (fila + 1, col)),
            ("izquierda", (fila, col - 1)),
            ("derecha", (fila, col + 1))
        ]

        # Asegura que las acciones sean válidas y dentro de los límites del laberinto
        resultado = []
        for accion, (f, c) in candidatos:
            # Verifica que esté dentro de los límites del laberinto y que la posición no sea una pared
            if 0 <= f < self.altura and 0 <= c < self.ancho and not self.paredes[f][c]:
                resultado.append((accion, (f, c)))

        return resultado

    def resolver(self):
        """Encuentra una solución para el laberinto, si existe."""

        # Mantiene un registro del número de estados explorados
        self.num_explorados = 0

        # Inicializa la frontera solo en la posición inicial
        inicio = Nodo(estado=self.inicio, padre=None, accion=None)
        frontera = FronteraPila()  # Línea para pasar de búsqueda por expansión (FronteraCola()) a búsqueda profunda (FronteraPila())
        frontera.agregar(inicio)

        # Inicializa un conjunto explorado vacío
        self.explorado = set()

        # Continúa repitiendo hasta encontrar la solución
        while True:
            # Si no queda nada en la frontera, no hay camino
            if frontera.vacia():
                raise Exception("sin solución")

            # Elige un nodo de la frontera
            nodo = frontera.remover()
            self.num_explorados += 1

            # Si el nodo es el objetivo, entonces tenemos una solución
            if nodo.estado == self.objetivo:
                acciones = []
                celdas = []

                # Sigue los nodos padres para encontrar una solución
                while nodo.padre is not None:
                    acciones.append(nodo.accion)
                    celdas.append(nodo.estado)
                    nodo = nodo.padre
                acciones.reverse()
                celdas.reverse()
                self.solucion = (acciones, celdas)
                return

            # Marca el nodo como explorado
            self.explorado.add(nodo.estado)

            # Añade vecinos a la frontera
            for accion, estado in self.vecinos(nodo.estado):
                if not frontera.contiene_estado(estado) and estado not in self.explorado:
                    hijo = Nodo(estado=estado, padre=nodo, accion=accion)
                    frontera.agregar(hijo)

    def generar_imagen(self, nombre_archivo, mostrar_solucion=True, mostrar_explorado=False):
        from PIL import Image, ImageDraw
        tam_celda = 50
        borde_celda = 2

        # Crea una imagen en blanco
        img = Image.new(
            "RGBA",
            (self.ancho * tam_celda, self.altura * tam_celda),
            "negro"
        )
        dibujar = ImageDraw.Draw(img)

        solucion = self.solucion[1] if self.solucion is not None else None
        for i, fila in enumerate(self.paredes):
            for j, col in enumerate(fila):

                # Paredes
                if col:
                    relleno = (40, 40, 40)

                # Inicio
                elif (i, j) == self.inicio:
                    relleno = (255, 0, 0)

                # Objetivo
                elif (i, j) == self.objetivo:
                    relleno = (0, 171, 28)

                # Solución
                elif solucion is not None and mostrar_solucion and (i, j) in solucion:
                    relleno = (220, 235, 113)

                # Exploración
                elif solucion is not None and mostrar_explorado and (i, j) in self.explorado:
                    relleno = (212, 97, 85)

                # Celda Vacía
                else:
                    relleno = (237, 240, 252)

                # Dibuja la celda
                dibujar.rectangle(
                    [(j * tam_celda + borde_celda, i * tam_celda + borde_celda),
                     ((j + 1) * tam_celda - borde_celda, (i + 1) * tam_celda - borde_celda)],
                    fill=relleno
                )

        img.save(nombre_archivo)

if len(sys.argv) != 2:
    sys.exit("Uso: python Labe.py Labe.txt")

m = Laberinto(sys.argv[1])
print("Laberinto:")
m.mostrar()
print("Resolviendo...")
m.resolver()
print("Estados Explorados:", m.num_explorados)
print("Solución:")
m.mostrar()
m.generar_imagen("Laberinto.png", mostrar_explorado=True)  # mostrar_explorado=True
