import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        #leggo il nome inserito
        responsabile = self._view.input_responsabile.value
        #controllo che il campo non sia vuoto
        if responsabile is None or responsabile.strip() == "":
            self._view.show_alert("Inserisci il nome del responsabile")
            return
        #aggiorno il responsabile nel modello
        self._model.responsabile = responsabile.strip()
        #aggiorno il testo nella View
        self._view.txt_responsabile.value = (f"Responsabile: {self._model.responsabile}")
        #aggiorno l'interfaccia
        self._view.update()

    #mostra tutti gli strumenti presenti nel database
    def mostra_strumenti(self,e):
        #recupero gli strumenti dal modello
        strumenti = self._model.get_strumenti()

        #controllo se si è verificato un errore
        if strumenti is None:
            self._view.show_alert("Errore durante il recupero degli strumenti")
            return

        #svuoto la lista precedente
        self._view.lista_strumenti.controls.clear()
        #inserisco gli strumenti nella lista
        for strumento in strumenti:
            self._view.lista_strumenti.controls.append(ft.Text(str(strumento)))
            #se non ci sono strumenti
        if len(strumenti) == 0:
            self._view.lista_strumenti.controls.append(ft.Text("Nessuno strumento presente nel deposito"))
        #aggiorno l'interfaccia
        self._view.update()

    #cerco gli strumenti in base al tipo
    def cerca_strumenti(self,e):
        #leggo il tipo inserito dall'utente
        tipo = self._view.input_tipo_strumento.value

        #controllo che il campo non sia vuoto
        if tipo is None or tipo.strip() == "":
            self._view.show_alert("Inserisci il tipo di strumento da cercare")
            return

        #cerco gli strumenti nel modello
        strumenti = self._model.cerca_strumenti_per_tipo(tipo.strip())
        #controllo se si è verificato un errore
        if strumenti is None:
            self._view.show_alert("Errore durante la ricerca degli strumenti")
            return
        #svuoto i risultati della ricerca precedente
        self._view.lista_strumenti_ricerca.controls.clear()
        #inserisco gli strumenti trovati
        for strumento in strumenti:
            self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(strumento)))

        #se non ci sono risultati
        if len(strumenti) == 0:
            self._view.lista_strumenti_ricerca.controls.append(ft.Text("Nessuno strumento trovato"))

        #aggiorno l'interfaccia
        self._view.update()