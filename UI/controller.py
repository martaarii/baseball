import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI

        self._selectedTeam = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.append(ft.Text("Inserire l'anno"))
            return
        self._model.buildGraph(self._view._ddAnno.value)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        n, a = self._model.printGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f"Il grafo è costituito da {n} archi e {a} archi"))
        self._view.update_page()

    def handleDettagli(self, e):
        vicini = self._model.getSortedNeighbors(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {self._selectedTeam}"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} salario: {v[1]}"))
            self._view.update_page()

    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        path, peso = self._model.getPercorso1(self._selectedTeam)
        self._view._txt_result.controls.append(
            ft.Text("Elenco dei nodi del percorso più lungo:"))
        for n in path:
            self._view._txt_result.controls.append(ft.Text(f"{n}"))
        self._view._txt_result.controls.append(ft.Text(f"Peso totale: {peso}"))
        self._view.update_page()
    def fillDDYear(self):
        years = self._model.getAllYears()
        yearDD = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options= yearDD
        # yearsDD = []
        # for y in years:
        # yearsDD.append(ft.dropdown.Option(y))
        self._view.update_page()
    def handleDDYearSelection(self,e):
        teams = self._model.getTeams(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"Ho trovato {len(teams)} squadre "
                    f"nell'anno {self._view._ddAnno.value}"))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(data=t,text=t.teamCode, on_click=self.readDDTeams)
            )
        self._view.update_page()
    def readDDTeams(self,e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data
        print(f"readdDTeams called -- {self._selectedTeam.name}")
