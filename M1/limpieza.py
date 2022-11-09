# --------------------------------------------------------------
# M1. Actividad
#
# Fecha: 07-Nov-2022
# Autores:
#           A01746210 Alan Said Martinez Guzman
#           A01752789 Luis Humberto Romero Perez
#
# Simulación de agentes capaces de limpiar celdas de una tupla
# que contienen objetos situados aleatoriamente. Siendo los
# movimientos de los agentes automatizados logrando moverse por
# toda la tupla hasta lograr limpiarla por completo o que el tiempo
# se haya agotado.
# --------------------------------------------------------------

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation

# Estas librerias contienen 3 metodos; agents, scheduler y model
# Agents: Permite manipular a los agentes en tanto a sus movimientos y
# caracteristicas.
# Scheduler: Es un modelo especial que controla el orden en el que los
# agentes son activados.
# Model: Es la visualización.


class Celda(Agent):
    # Constructor que permite que la clase inicialice los atributos del objeto.
    def __init__(self, unique_id, model):
        # Representa la clase padre.
        super().__init__(unique_id, model)
        self.estado = ''
        self.sigEstado = ''

    # La función limpia la celda.
    # Recibe como parametros la lista de los agentes contenidos en los nodos.
    # Regresa una actualización del conteo de las celdas ya limpias.
    def step(self):
        contenido = len(self.model.grid.get_cell_list_contents(self.pos))
        if (contenido > 1):
            if (self.estado == 'sucia'):
                self.sigEstado = 'limpia'
                self.model.celdasLimpias += 1

        else:
            self.sigEstado = self.estado

    def advance(self):
        self.estado = self.sigEstado


class limpiadorAgente(Agent):
    # Funcion que inicializa las variables que contiene cada uno
    # de los agentes. Lleva un registro del estado del agente
    # respecto a las casillas. En el modelo regresa la cantidad
    # de movimientos realizados por cada agente.
    def __init__(self, unique_id: int, model: Model) -> None:
        # Representa la clase padre.
        super().__init__(unique_id, model)
        self.sigEstado = None
        self.estado = 'limpiador'
        self.movimientos = 0

    # Limpia la celda sucia al agente caer en esta.
    def step(self):

        if (self.pos in self.model.coordenadasSucias):
            self.model.coordenadasSucias.remove(self.pos)
            self.sigEstado = self.pos
            self.model.posicionesSiguientes[self.unique_id] = self.pos
        # El agente se mueve.
        else:
            vecinos = self.model.grid.get_neighborhood(self.pos, moore=True,
                                                       include_center=False)
            # Al incluir una propiedad de tipo random, el agente elige una de
            # las 8 direcciones para moverse.
            nuevaPosicion = self.random.choice(vecinos)
            contenido = self.model.grid.get_cell_list_contents(nuevaPosicion)
            if (not self.model.grid.out_of_bounds(nuevaPosicion) and
                    ((len(contenido) <= 1)) and
                    (nuevaPosicion not in self.model.posicionesSiguientes)):
                self.sigEstado = nuevaPosicion
                self.model.grid.move_agent(self, self.sigEstado)
                self.model.posicionesSiguientes[self.unique_id] = nuevaPosicion
                self.movimientos += 1
            else:
                self.sigEstado = self.pos
                self.model.posicionesSiguientes[self.unique_id] = self.pos

    # Avanza a la siguiente casilla de la tupla.
    def advance(self):
        self.model.grid.move_agent(self, self.sigEstado)


class limpiadorModelo(Model):
    # Funcion que inicializa los variables en el modelo limpiador.
    # Lleva un registro del tiempo, celdas sucias y limpias.
    # Estas variables al finalizar el programa nos regresan un control de
    # lo obtenido con el modelo.
    def __init__(self, ancho, alto, numAgentes, suciedad, tiempoMax):
        self.numAgentes = numAgentes
        self.grid = MultiGrid(ancho, alto, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.celdasSucias = (ancho * alto * suciedad) // 100
        self.celdasLimpias = 0
        self.coordenadasSucias = []
        self.tiempoMax = tiempoMax
        self.tiempo = tiempoMax
        self.posicionesSiguientes = {}

        # Crear y registrar las celdas sucias tomando en cuenta nuestro alto
        # y ancho de tupla aleatoriamente.
        id = 0
        for _ in range(self.celdasSucias):
            X = self.random.randrange(ancho)
            Y = self.random.randrange(alto)
            while ((X, Y) in self.coordenadasSucias):
                X = self.random.randrange(ancho)
                Y = self.random.randrange(alto)
            self.coordenadasSucias.append((X, Y))
            a = Celda(id, self)
            a.estado = 'sucia'
            self.schedule.add(a)
            self.grid.place_agent(a, (X, Y))
            id += 1

        # Inicializar agentes.
        for _ in range(numAgentes):
            a = limpiadorAgente(id, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (ancho // 2, alto // 2))
            id += 1

    def step(self):
        # Al ya no existir coordenadas sucias o se haya llegado al tiempo
        # máximo posible, termina el programa.
        if (len(self.coordenadasSucias) <= 0 or self.tiempo <= 0):
            self.running = False
            print(f"Tiempo que tardo en limpiar: \
                {self.tiempoMax - self.tiempo}")
            print(f"Porcentaje de celdas sucias limpiadas: \
                {(self.celdasLimpias * 100) / self.celdasSucias}%")
            return
        else:
            self.tiempo -= 1
        self.schedule.step()
