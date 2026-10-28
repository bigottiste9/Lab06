from database.DB_connect import get_connection
from model import strumento
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        #mi collego al database
        conn = get_connection()

        #se la connesione non è disponibile, restituisco None
        if conn is None:
            return None

        try:
            #creo il cursore per eseguire la query SQL
            cursor = conn.cursor(dictionary=True)

            #leggo tutti gli strumenti
            query = "SELECT * FROM strumento"
            cursor.execute(query)

            #recupero tutte le righe restituite dalla query
            risutati=cursor.fetchall()

            #creo una lista di oggetti Strumento
            strumenti = []
            for riga in risutati:
                strumento = Strumento(riga["codice"], riga["tipo"], riga["marca"], riga["anno_acquisto"], riga["valore"], riga["disponibile"])
                strumenti.append(strumento)
                return strumenti
        except Exception as e:
            print("Errore durante la ricerca degli strumenti : ", e)
            return None
        finally:
            #chiudo la connesione al database
            conn.close()

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        #controllo che il tipo sia stato inserito
        if tipo is None or tipo.strip() == "":
            return []
        #mi collego al database
        conn = get_connection()
        #se la connesione non è disponibile, restituisco None
        if conn is None:
            return None
        try:
            #creo il cursore
            cursor = conn.cursor(dictionary=True)
            #cerco gli strumenti del tipo indicato
            query = "SELECT * FROM strumento WHERE tipo = %s"
            cursor.execute(query, (tipo.strip(),))
            #recupero i risultati
            risutati = cursor.fetchall()
            #creo la lista degli strumenti trovati
            strumenti = []
            for riga in risutati:
                strumento = Strumento(riga["codice"], riga["tipo"], riga["marca"], riga["anno_acquisto"], riga["valore"], riga["disponibile"])
                strumenti.append(strumento)
                return strumenti
        except Exception as e:
            print("Errore durante la ricerca degli strumenti : ", e)
            return None
        finally:
            #chiudo la connesione al database
            conn.close()
