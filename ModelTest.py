from model.model import Model

myModel = Model()
myModel.getTeams(2015)
myModel.buildGraph(2015)
v0 = list(myModel._grafo.nodes)[0]
print(v0)
vicini = myModel.getSortedNeighbors(v0)

#for v in vicini:
#   print(v[1], v[0])

path = myModel.getPercorso(v0)
print(path[0])
print(path[1])