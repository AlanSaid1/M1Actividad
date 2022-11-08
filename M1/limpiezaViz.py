from limpieza import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "white",
                 "r": .7}

    if agent.estado == 'limpiador':
        portrayal["Color"] = "green"  # Limpiadores son verdes
        portrayal["Layer"] = 2
        portrayal["r"] = .7
        portrayal["text"] = agent.movimientos
        portrayal["text_color"] = "black"
    elif agent.estado == 'sucia':
        portrayal["Color"] = "brown"  # Celdas sucias son cafes
        portrayal["Layer"] = 0
        portrayal["r"] = .7
    elif agent.estado == 'limpia':
        portrayal["Color"] = "white"  # Celdas limpias son blancas
        portrayal["Layer"] = 1
        portrayal["r"] = .7
    return portrayal


ancho = 10
alto = 10
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(LimpiadorModelo,
                       [grid],
                       "Dirty Cleaner Mode",
                       {"ancho": ancho, "alto": alto,
                        "numAgentes": 5, "suciedad": 50, "tiempoMax": 100})
server.port = 8521  # The default
server.launch()
