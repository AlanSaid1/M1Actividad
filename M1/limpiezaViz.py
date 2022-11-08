#--------------------------------------------------------------
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
#--------------------------------------------------------------

from limpieza import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

#Propiedades de los agentes:

#Diccionario capaz de convertirse en objeto JSON.
#El parametro "agent" como el actor dentro de la tupla.
# Retorna los agentes en las celdas.
def agentPortrayal(agent):
    portrayal = {
                "Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "white",
                 "r": 0.7
                }

#Representa a los actores con color verde.
    if agent.estado == 'limpiador':
        portrayal["Color"] = "green"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.7
        portrayal["text"] = agent.movimientos
        portrayal["text_color"] = "black"

#Representa a las celdas sucias con color cafe.
    elif agent.estado == 'sucia':
        portrayal["Color"] = "brown"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.7

#Al limpiar las celdas estas se convierten en color blanco.
    elif agent.estado == 'limpia':
        portrayal["Color"] = "white"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.7

    return portrayal

#La variable grid dibuja las medidas de la tupla, asi como de los pixeles.
ancho = 10
alto = 10
grid = CanvasGrid(agentPortrayal, ancho, alto, 750, 750)
#Una vez que el servidor es creado, establecemos el puerto en el que escuchará.
server = ModularServer(limpiadorModelo,
                       [grid],
                       "Dirty Cleaner Mode",
                       {"ancho": ancho, "alto": alto,
                        "numAgentes": 5, "suciedad": 50, "tiempoMax": 100
                        })
server.port = 8521
server.launch()
