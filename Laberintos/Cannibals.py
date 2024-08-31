from collections import deque

class State:
    def __init__(self, missionaries, cannibals, boat_position, path=None):
        # Inicializa el estado con el número de misioneros y caníbales en la orilla actual,
        # la posición del bote ('left' o 'right'), y el camino recorrido hasta este estado.
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat_position = boat_position
        self.path = path or []

    def is_valid(self):
        # Comprueba si el estado es válido:
        # 1. Los números de misioneros y caníbales están dentro del rango permitido (0-3).
        # 2. No hay más caníbales que misioneros en ninguna orilla.
        if not (0 <= self.missionaries <= 3 and 0 <= self.cannibals <= 3):
            return False
        if (self.missionaries and self.missionaries < self.cannibals) or \
           (3 - self.missionaries and 3 - self.missionaries < 3 - self.cannibals):
            return False
        return True

    def is_goal(self):
        # Verifica si todos los misioneros y caníbales están en la orilla derecha y el bote también.
        return self.missionaries == 0 and self.cannibals == 0 and self.boat_position == 'right'

    def generate_next_states(self):
        # Genera todos los posibles estados futuros a partir del estado actual:
        # Los movimientos posibles son 1 o 2 misioneros, 1 o 2 caníbales, o ambos.
        possible_moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        boat_shift = -1 if self.boat_position == 'left' else 1
        next_states = []

        for m, c in possible_moves:
            new_missionaries = self.missionaries + boat_shift * m
            new_cannibals = self.cannibals + boat_shift * c
            if 0 <= new_missionaries <= 3 and 0 <= new_cannibals <= 3:
                new_boat_position = 'right' if self.boat_position == 'left' else 'left'
                new_state = State(new_missionaries, new_cannibals, new_boat_position, self.path + [(m, c, new_boat_position)])
                if new_state.is_valid():
                    next_states.append(new_state)

        return next_states

    def __repr__(self):
        # Representa el estado en un formato amigable.
        return f"({self.missionaries}, {self.cannibals}, {self.boat_position})"

def bfs():
    # Implementa la búsqueda en anchura (BFS) para encontrar la solución al problema.
    initial_state = State(3, 3, 'left')
    queue = deque([initial_state])  # Cola inicial con el estado de partida.
    visited = set()  # Conjunto para rastrear los estados ya visitados.

    while queue:
        current_state = queue.popleft()  # Extrae el primer estado de la cola.

        if current_state.is_goal():
            # Si el estado actual es la solución, devuelve el camino hasta él.
            return current_state.path

        state_key = (current_state.missionaries, current_state.cannibals, current_state.boat_position)
        if state_key in visited:
            # Si el estado ya ha sido visitado, pasa al siguiente estado.
            continue
        visited.add(state_key)

        # Añade todos los estados válidos futuros a la cola para exploración posterior.
        queue.extend(state for state in current_state.generate_next_states() if (state.missionaries, state.cannibals, state.boat_position) not in visited)

    return None

# Ejecuta BFS para encontrar la solución al problema.
solution = bfs()

if solution:
    # Imprime el camino de la solución encontrada.
    print("Solution found:")
    for move in solution:
        print(f"Move {move[0]} missionary(ies) and {move[1]} cannibal(s) to the {move[2]} shore.")
else:
    # Imprime un mensaje si no se encontró una solución.
    print("No solution found.")
