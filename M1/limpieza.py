from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
import numpy as np


class Celda(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.estado = ''
        self.sigEstado = ''

    # Limpiar celda
    def step(self):
        contenido = len(self.model.grid.get_cell_list_contents(self.pos))
        if (contenido > 1):
            if (self.estado == 'sucia'):
                self.sigEstado = 'limpia'
                self.model.celdasLimpias += 1
                # print(f"Limpie la celda {self.pos}")
        else:
            self.sigEstado = self.estado

    def advance(self):
        self.estado = self.sigEstado


class LimpiadorAgente(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.sigEstado = None
        self.estado = 'limpiador'
        self.movimientos = 0

    def step(self):
        # Limpiar celda
        if (self.pos in self.model.coordenadasSucias):
            self.model.coordenadasSucias.remove(self.pos)
        else:
            # Moverse
            vecinos = self.model.grid.get_neighborhood(self.pos, moore=True,
                                                       include_center=False)
            nuevaPosicion = self.random.choice(vecinos)
            contenido = self.model.grid.get_cell_list_contents(nuevaPosicion)
            if (not self.model.grid.out_of_bounds(nuevaPosicion) and
                    ((len(contenido) <= 1))):
                self.sigEstado = nuevaPosicion
                self.movimientos += 1
            else:
                self.sigEstado = self.pos

    def advance(self):
        self.model.grid.move_agent(self, self.sigEstado)


class LimpiadorModelo(Model):
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

        # Crear y registrar celdas sucias
        id = 0
        for _ in range(self.celdasSucias):
            x = self.random.randrange(ancho)
            y = self.random.randrange(alto)
            while ((x, y) in self.coordenadasSucias):
                x = self.random.randrange(ancho)
                y = self.random.randrange(alto)
            self.coordenadasSucias.append((x, y))
            a = Celda(id, self)
            a.estado = 'sucia'
            self.schedule.add(a)
            self.grid.place_agent(a, (x, y))
            id += 1

        # Inicializar agentes
        for _ in range(numAgentes):
            a = LimpiadorAgente(id, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (ancho // 2, alto // 2))
            id += 1

    def step(self):
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
