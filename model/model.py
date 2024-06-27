import copy
import itertools
import copy


from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):

        self._allTeams = []
        self._grafo = nx.Graph()
        self._idMap_teams = {}
        self._bestPath = []
        self._bestObjVal = 0

    def buildGraph(self, year):
        self._grafo.clear()
        if len(self._allTeams) == 0:
            print("Lista squadre vuota")
            # ritorno perchè non ha senso creare il grafo se non ho nodi
            return
        self._grafo.add_nodes_from(self._allTeams)
        myedges = list(itertools.combinations(self._allTeams, 2))
        self._grafo.add_edges_from(myedges)

        # aggiungo i pesi
        salaries = DAO.getSalaryOfTeams(year, self._idMap_teams)
        for e in self._grafo.edges:
            self._grafo[e[0]][e[1]]["weight"] = salaries[e[0]] + salaries[e[1]]
    def getSortedNeighbors(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[v0][v]["weight"]))
        viciniTuple.sort(key=lambda x: x[1], reverse=True)
        return viciniTuple

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeams(self, year):
        self._allTeams = DAO.getTeamsYear(year)
        self._idMap_teams = {t.ID: t for t in self._allTeams}

        return self._allTeams

    def printGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def _getScore(self, listNodes):
        if len(listNodes) == 1:
            return 0
        score = 0
        # sommo i pesi degli archi del cammino
        for i in range(0, len(listNodes)-1):
            # sommo i pesi degli archi del cammino
            score += self._grafo[listNodes[i]][listNodes[i+1]]["weight"]
        return score

    def _ricorsione(self, parziale):

        if self._getScore(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._getScore(parziale)

        for v in self._grafo.neighbors(parziale[-1]):
            edgW = self._grafo[parziale[-1]][v]["weight"]
            if v not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > edgW:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()
    def getPercorso(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestObjVal
    def getPercorso1(self, v0):
        self._bestPath = []
        self._bestObjVal = 0
        parziale = [v0]
        listaVicini = []

        for v in self._grafo.neighbors(v0):
            edg = self._grafo[v][v0]["weight"]
            listaVicini.append((v,edg))

        listaVicini.sort(key=lambda x: x[1], reverse=True)
        parziale.append(listaVicini[0][0])
        self.ricorsione2(parziale)
        parziale.pop()

        return self._bestPath, self._bestObjVal

    def ricorsione2(self, parziale):
        if self._getScore(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._getScore(parziale)
        listaVicini = []
        for v in self._grafo.neighbors(parziale[-1]):
            edgW = self._grafo[parziale[-1]][v]["weight"]
            listaVicini.append((v, edgW))
            listaVicini.sort(key=lambda x: x[1], reverse=True)

        for v1 in listaVicini:
            if v1 not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > v1[1]:
                parziale.append(v1[0])
                self.ricorsione2(parziale)
                parziale.pop()
                return
