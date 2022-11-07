from limpieza import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "white",
                 "r": .5}

    if agent.estado == 'limpiador':
        portrayal["Color"] = "blue"  # Limpiadores son verdes
        portrayal["Layer"] = 2
        portrayal["r"] = .5
    elif agent.estado == 'sucia':
        portrayal["Color"] = "brown"  # Celdas sucias son cafes
        portrayal["Layer"] = 0
        portrayal["r"] = .5
    elif agent.estado == 'limpia':
        portrayal["Color"] = "gray"  # Celdas sucias son cafes
        portrayal["Layer"] = 1
        portrayal["r"] = .5
    return portrayal


ancho = 28
alto = 28
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(LimpiadorModelo,
                       [grid],
                       "Dirty Cleaner Mode",
                       {"ancho": ancho, "alto": alto,
                        "numAgentes": 15, "suciedad": 15, "tiempoMax": 30})
server.port = 8521  # The default
server.launch()
