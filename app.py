import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask
from flask_restful import Resource, reqparse, Api
import ast
import json

app = Flask(__name__)
api = Api(app)

from base import *

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

class Venditori_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Nome', type=str, required=False, help='Nome venditore')
    parser.add_argument('Cognome', type=str, required=False, help='Cognome venditore')
    parser.add_argument('Password', type=str, required=False, help='Password venditore')
    parser.add_argument('Tipo_Attività', type=str, required=False, help='Tipo_Attività venditore')
    parser.add_argument('Telefono', type=str, required=False, help='Telefono venditore')
    parser.add_argument('IVA', type=str, required=False, help='IVA venditore')

    def get(self,venditore):
        try:
            item = Venditore.get_Venditore(venditore)
            return item.json()
        except:
            return {'Messaggio': 'Venditore non trovato'}
    
    def post(self, venditore):
        try:
            if sheetVenditori.find(venditore):
                return {'Messaggio':'Il venditore con la email {} esiste già'.format(venditore)}
        except:
            args = Venditori_List.parser.parse_args()
            item = Venditore(venditore,args['Password'],args['Nome'],args['Cognome'],args['Tipo_Attività'],args['Telefono'],args['IVA'])
            item.save()
            return item.json()

    def put(self, venditore):
        args = Venditori_List.parser.parse_args()
        try:
            item = Venditore.get_Venditore(venditore)
            item.nome =  item.nome if not args['Nome'] else args['Nome']
            item.cognome = item.cognome if not args['Cognome'] else args['Cognome']
            item.password = item.password if not args['Password'] else args['Password']
            item.tipo_attività = item.tipo_attività if not args['Tipo_Attività'] else args['Tipo_Attività']
            item.telefono =item.telefono if not args['Telefono'] else args['Telefono']
            item.iva = item.iva if not args['IVA'] else args['IVA']
            item.update()
            return {'Venditore':item.json()}
        except:
            item = Venditore(venditore,args['Password'],args['Nome'],args['Cognome'],args['Tipo_Attività'],args['Telefono'],args['IVA'])
            item.save()
            return item.json()

    def delete(self, venditore):
        try:
            item = Venditore.get_Venditore(venditore)
            item.delete()
            return {'Messaggio': '{} è stato eliminato dai record'.format(venditore)}
        except:
            return {'Messaggio': '{} non è tra i record'.format(venditore)}

class All_Venditori(Resource):
    def get(self):
        return {'Venditori': sheetVenditori.get_all_records()}

class Clienti_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Nome', type=str, required=False, help='Nome cliente')
    parser.add_argument('Cognome', type=str, required=False, help='Cognome cliente')
    parser.add_argument('Password', type=str, required=False, help='Password cliente')
    parser.add_argument('Pagamento', type=str, required=False, help='Pagamento cliente')
    parser.add_argument('Privacy', type=str, required=False, help='Privacy cliente')

    def get(self,cliente):
        try:
            item = Cliente.get_Cliente(cliente)
            return item.json()
        except:
            return {'Messaggio': 'Cliente non trovato'}
    
    def post(self, cliente):
        try:
            if sheetClienti.find(cliente):
                return {'Messaggio':'Il cliente con la email {} esiste già'.format(cliente)}
        except:
            args = Clienti_List.parser.parse_args()
            item = Cliente(cliente,args['Password'],args['Nome'],args['Cognome'],args['Pagamento'],args['Privacy'])
            item.save()
            return item.json()

    def put(self, cliente):
        args = Clienti_List.parser.parse_args()
        try:
            item = Cliente.get_Cliente(cliente)
            item.nome = item.nome if not args['Nome'] else args['Nome']
            item.cognome = item.cognome if not args['Cognome'] else args['Cognome']
            item.password = item.password if not args['Password'] else args['Password']
            item.pagamento = item.pagamento if not args['Pagamento'] else args['Pagamento']
            item.privacy = item.privacy if not args['Privacy'] else args['Privacy']
            item.update()
            return {'Cliente':item.json()}
        except:
            item = Cliente(cliente,args['Password'],args['Nome'],args['Cognome'],args['Pagamento'],args['Privacy'])
            item.save()
            return item.json()

    def delete(self, cliente):
        try:
            item = Cliente.get_Cliente(cliente)
            item.delete()
            return {'Messaggio': '{} è stato eliminato dai record'.format(cliente)}
        except:
            return {'Messaggio': '{} non è tra i record'.format(cliente)}

class All_Clienti(Resource):
    def get(self):
        return {'Clienti': sheetClienti.get_all_records()}

class RecensioniVenditore_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Recensione', type=str, required=False, help='Recensione')
    parser.add_argument('Cliente', type=str, required=False, help='Cliente')

    def get(self,venditore):
        args = RecensioniVenditore_List.parser.parse_args()
        try:
            item = RecensioneVenditore.get_RecensioneVenditore(venditore, args['Cliente'])
            return item.json()
        except:
            return {'Messaggio': 'Recensione non trovata'}
    
    def post(self, venditore):
        args = RecensioniVenditore_List.parser.parse_args()
        try:
            if RecensioneVenditore.row_index_by_emails(venditore,c):
                return {'Messaggio':'La recensione con email venditore '+venditore+' e email cliente '+args['Cliente']+' esiste già'}
        except:
            args = RecensioniVenditore_List.parser.parse_args()
            item = RecensioneVenditore(venditore,args['Cliente'],args['Recensione'])
            item.save()
            return item.json()

    def put(self, venditore):
        args = RecensioniVenditore_List.parser.parse_args()
        try:
            item = RecensioneVenditore.get_RecensioneVenditore(venditore, args['Cliente'])
            item.recensione = item.recensione if not args['Recensione'] else args['Recensione']
            item.update()
            return {'Recensione':item.json()}
        except:
            item = RecensioneVenditore(venditore, args['Cliente'],args['Recensione'])
            item.save()
            return item.json()

    def delete(self, venditore):
        args = RecensioniVenditore_List.parser.parse_args()
        try:
            item = RecensioneVenditore.get_RecensioneVenditore(venditore, args['Cliente'])
            item.delete()
            return {'Messaggio': 'La recensione è stata eliminata dai record'}
        except:
            return {'Messaggio': 'La recensione non è tra i record'}

class All_RecensioniVenditore(Resource):
    def get(self):
        return {'Recensioni': sheetRecensioni_Venditori.get_all_records()}

class RecensioniProdotto_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Recensione', type=str, required=False, help='Recensione')
    parser.add_argument('Cliente', type=str, required=False, help='Cliente')

    def get(self,prodotto):
        try:
            args = Venditori_List.parser.parse_args()
            item = RecensioneProdotto.get_RecensioneProdotto(args['Cliente'], prodotto)
            return item.json()
        except:
            return {'Messaggio': 'Recensione non trovata'}
    
    def post(self, prodotto):
        args = Venditori_List.parser.parse_args()
        try:
            if RecensioneProdotto.row_index_by_email_and_product(args['Cliente'], prodotto):
                return {'Messaggio':'La recensione con email cliente '+args['Cliente']+' e prodotto '+prodotto+' esiste già'}
        except:
            item = RecensioneProdotto(args['Cliente'],prodotto,args['Recensione'])
            item.save()
            return item.json()

    def put(self, prodotto):
        args = RecensioniProdotto_List.parser.parse_args()
        try:
            item = RecensioneProdotto.get_RecensioneProdotto(args['Cliente'], prodotto)
            item.recensione = item.recensione if not args['Recensione'] else args['Recensione']
            item.update()
            return {'Recensione':item.json()}
        except:
            item = RecensioneProdotto(args['Cliente'],prodotto,args['Recensione'])
            item.save()
            return item.json()

    def delete(self, prodotto):
        args = RecensioniProdotto_List.parser.parse_args()
        try:
            item = RecensioneProdotto.get_RecensioneProdotto(args['Cliente'], prodotto)
            item.delete()
            return {'Messaggio': 'La recensione è stata eliminata dai record'}
        except:
            return {'Messaggio': 'La recensione non è tra i record'}

class All_RecensioniProdotto(Resource):
    def get(self):
        return {'Recensioni': sheetRecensioni_Prodotti.get_all_records()}

class Prodotti_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Venditore', type=str, required=False, help='Venditore prodotto')
    parser.add_argument('Tipologia', type=str, required=False, help='Tipologia prodotto')
    parser.add_argument('Caratteristiche', type=str, required=False, help='Caratteristiche prodotto')
    parser.add_argument('Prezzo', type=float, required=False, help='Prezzo prodotto')
    parser.add_argument('Tipologia spedizione', type=str, required=False, help='Tipologia spedizione prodotto')

    def get(self,prodotto):
        try:
            item = Prodotto.get_Prodotto(prodotto)
            return item.json()
        except:
            return {'Messaggio': 'Prodotto non trovato'}
    
    def post(self, prodotto):
        try:
            if sheetProdotti.find(prodotto):
                return {'Messaggio':'Il prodotto con il nome {} esiste già'.format(prodotto)}
        except:
            args = Prodotti_List.parser.parse_args()
            item = Prodotto(args['Tipologia'],prodotto,args['Caratteristiche'],args['Prezzo'],args['Tipologia spedizione'],args['Venditore'])
            item.save()
            return item.json()

    def put(self, prodotto):
        args = Prodotti_List.parser.parse_args()
        try:
            item = Prodotto.get_Prodotto(prodotto)
            item.tipologia = item.tipologia if not args['Tipologia'] else args['Tipologia']
            item.venditore = item.venditore if not args['Venditore'] else args['Venditore']
            item.caratteristiche = item.caratteristiche if not args['Caratteristiche'] else args['Caratteristiche']
            item.prezzo = item.prezzo if not args['Prezzo'] else args['Prezzo']
            item.tipologia_spedizione = item.tipologia_spedizione if not args['Tipologia spedizione'] else args['Tipologia spedizione']
            item.update()
            return {'Prodotto':item.json()}
        except:
            item = Prodotto(args['Tipologia'],prodotto,args['Caratteristiche'],args['Prezzo'],args['Tipologia spedizione'],args['Venditore'])
            item.save()
            return item.json()

    def delete(self, prodotto):
        try:
            item = Prodotto.get_Prodotto(prodotto)
            item.delete()
            return {'Messaggio': '{} è stato eliminato dai record'.format(prodotto)}
        except:
            return {'Messaggio': '{} non è tra i record'.format(prodotto)}

class All_Prodotti(Resource):
    def get(self):
        return {'Prodotti': sheetProdotti.get_all_records()}

class Offerte_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Prodotto', type=str, required=False, help='Prodotto offerta')
    parser.add_argument('Offerta', type=str, required=False, help='Offerta')
    parser.add_argument('Data Inizio', type=str, required=False, help='Data inizio offerta')
    parser.add_argument('Data Fine', type=str, required=False, help='Data fine offerta')

    def get(self,offerta):
        try:
            item = Offerta.get_Offerta(offerta)
            return item.json()
        except:
            return {'Messaggio': 'Offerta non trovata'}
    
    def post(self, offerta):
        try:
            if sheetOfferte.find(offerta):
                return {'Messaggio':'L\'offerta con il codice {} esiste già'.format(offerta)}
        except:
            args = Offerte_List.parser.parse_args()
            item = Offerta(offerta, args['Prodotto'], args['Offerta'],args['Data Inizio'],args['Data Fine'])
            item.save()
            return item.json()

    def put(self, offerta):
        args = Offerte_List.parser.parse_args()
        try:
            item = Offerta.get_Offerta(offerta)
            item.prodotto = item.prodotto if not args['Prodotto'] else args['Prodotto']
            item.offerta = item.offerta if not args['Offerta'] else args['Offerta']
            item.data_inizio = item.data_inizio if not args['Data Inizio'] else args['Data Inizio']
            item.data_fine = item.data_fine if not args['Data Fine'] else args['Data Fine']
            item.update()
            return {'Offerta':item.json()}
        except:
            item = Offerta(offerta,args['Prodotto'],args['Offerta'],args['Data Inizio'],args['Data Fine'])
            item.save()
            return item.json()

    def delete(self, offerta):
        try:
            item = Offerta.get_Offerta(offerta)
            item.delete()
            return {'Messaggio': '{} è stato eliminato dai record'.format(offerta)}
        except:
            return {'Messaggio': '{} non è tra i record'.format(offerta)}

class All_Offerte(Resource):
    def get(self):
        return {'Offerte': sheetOfferte.get_all_records()}

class Acquisti_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Cliente', type=str, required=False, help='Cliente acquisto')
    parser.add_argument('Data', type=str, required=False, help='Data acquisto')

    def get(self,acquisto):
        try:
            item = Acquisto.get_Acquisto(acquisto)
            return item.json()
        except:
            return {'Messaggio': 'Acquisto non trovato'}
    
    def post(self, acquisto):
        try:
            if sheetAcquisti.find(acquisto):
                return {'Messaggio':'L\'acquisto con il codice {} esiste già'.format(acquisto)}
        except:
            args = Acquisti_List.parser.parse_args()
            item = Acquisto(acquisto, args['Cliente'], args['Data'])
            item.save()
            return item.json()

    def put(self, acquisto):
        args = Acquisti_List.parser.parse_args()
        try:
            item = Acquisto.get_Acquisto(acquisto)
            item.cliente = item.cliente if not args['Cliente'] else args['Cliente']
            item.data = item.data if not args['Data'] else args['Data']
            item.update()
            return {'Acquisto':item.json()}
        except:
            item = Acquisto(acquisto,args['Cliente'],args['Data'])
            item.save()
            return item.json()

    def delete(self, acquisto):
        try:
            item = Acquisto.get_Acquisto(acquisto)
            item.delete()
            return {'Messaggio': '{} è stato eliminato dai record'.format(acquisto)}
        except:
            return {'Messaggio': '{} non è tra i record'.format(acquisto)}

class All_Acquisti(Resource):
    def get(self):
        return {'Acquisti': sheetAcquisti.get_all_records()}

class Preferenze_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Tipologia', type=str, required=False, help='Tipologia')

    def get(self,cliente):
        args = Preferenze_List.parser.parse_args()
        try:
            item = Preferenza.get_Preferenza(cliente, args['Tipologia'])
            return item.json()
        except:
            return {'Messaggio': 'Preferenza non trovata'}
    
    def post(self, cliente):
        args = Preferenze_List.parser.parse_args()
        try:
            if Preferenza.row_index_by_client_and_type(cliente,args['Tipologia']):
                return {'Messaggio':'La preferenza con cliente '+cliente+' e tipologia '+args['Tipologia']+' esiste già'}
        except:
            args = Preferenze_List.parser.parse_args()
            item = Preferenza(cliente,args['Tipologia'])
            item.save()
            return item.json()

#c'è ma non ha senso
    def put(self, cliente):
        args = Preferenze_List.parser.parse_args()
        try:
            item = Preferenza.get_Preferenza(cliente, args['Tipologia'])
            item.tipologia = item.tipologia if not args['Tipologia'] else args['Tipologia']
            item.update()
            return {'Preferenza':item.json()}
        except:
            item = Preferenza(cliente, args['Tipologia'])
            item.save()
            return item.json()

    def delete(self, cliente):
        args = Preferenze_List.parser.parse_args()
        try:
            item = Preferenza.get_Preferenza(cliente, args['Tipologia'])
            item.delete()
            return {'Messaggio': 'La preferenza è stata eliminata dai record'}
        except:
            return {'Messaggio': 'La preferenza non è tra i record'}

class All_Preferenze(Resource):
    def get(self):
        return {'Preferenze': sheetPreferenze.get_all_records()}

class Prenotazioni_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Cliente', type=str, required=False, help='Cliente prenotazione')
    parser.add_argument('Prodotto', type=str, required=False, help='Prodotto prenotazione')
    parser.add_argument('Quantità', type=int, required=False, help='Quantità prenotazione')

    def get(self,codice_carrello):
        args = Prenotazioni_List.parser.parse_args()
        try:
            item = Prenotazione.get_Prenotazione(codice_carrello, args['Cliente'], args['Prodotto'])
            return item.json()
        except:
            return {'Messaggio': 'Prenotazione non trovata'}
        
    
    def post(self, codice_carrello):
        args = Prenotazioni_List.parser.parse_args()
        try:
            if Prenotazione.get_Prenotazione(codice_carrello, args['Cliente'], args['Prodotto']):
                return {'Messaggio':'La prenotazione esiste già'}
        except:
            args = Prenotazioni_List.parser.parse_args()
            item = Prenotazione(codice_carrello, args['Cliente'], args['Prodotto'],args['Quantità'])
            item.save()
            return item.json()

    def put(self, codice_carrello):
        args = Prenotazioni_List.parser.parse_args()
        try:
            item = Prenotazione.get_Prenotazione(codice_carrello,args['Cliente'],args['Prodotto'])
            item.quantità = item.quantità if not args['Quantità'] else args['Quantità']
            item.update()
            return {'Prenotazione':item.json()}
        except:
            item = Prenotazione(codice_carrello,args['Cliente'],args['Prodotto'],args['Quantità'])
            item.save()
            return item.json()

    def delete(self, codice_carrello):
        args = Prenotazioni_List.parser.parse_args()
        try:
            item = Prenotazione.get_Prenotazione(codice_carrello, args['Cliente'],args['Prodotto'])
            item.delete()
            return {'Messaggio': 'La prenotazione dell\'elemento nel carrello {} è stato eliminato dai record'.format(codice_carrello)}
        except:
            return {'Messaggio': 'La prenotazione dell\'elemento nel carrello {} non è tra i record'.format(codice_carrello)}

class All_Prenotazioni(Resource):
    def get(self):
        return {'Prenotazioni': sheetPrenotazioni.get_all_records()}

@app.route('/')
def funcroute():
    return 'Benvenuti su searchandbuyapi!'

api.add_resource(All_Venditori, '/Venditori')
api.add_resource(Venditori_List, '/Venditori/<string:venditore>')
api.add_resource(All_Clienti, '/Clienti')
api.add_resource(Clienti_List, '/Clienti/<string:cliente>')
api.add_resource(All_RecensioniVenditore, '/RecensioniVenditore')
api.add_resource(RecensioniVenditore_List, '/RecensioniVenditore/<string:venditore>')
api.add_resource(All_RecensioniProdotto, '/RecensioniProdotto')
api.add_resource(RecensioniProdotto_List, '/RecensioniProdotto/<string:prodotto>')
api.add_resource(All_Prodotti, '/Prodotti')
api.add_resource(Prodotti_List, '/Prodotti/<string:prodotto>')
api.add_resource(All_Offerte, '/Offerte')
api.add_resource(Offerte_List, '/Offerte/<string:offerta>')
api.add_resource(All_Acquisti, '/Acquisti')
api.add_resource(Acquisti_List, '/Acquisti/<string:acquisto>')
api.add_resource(All_Preferenze, '/Preferenze')
api.add_resource(Preferenze_List, '/Preferenze/<string:cliente>')
api.add_resource(All_Prenotazioni, '/Prenotazioni')
api.add_resource(Prenotazioni_List, '/Prenotazioni/<string:codice_carrello>')
if __name__=='__main__':
    app.run(debug=True)
