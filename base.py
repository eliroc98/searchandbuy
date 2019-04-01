import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('search&buy')
sheetVenditori = sheet.get_worksheet(0)
sheetRecensioni_Venditori = sheet.get_worksheet(1)
sheetRecensioni_Prodotti = sheet.get_worksheet(2)
sheetProdotti = sheet.get_worksheet(3)
sheetOfferte = sheet.get_worksheet(4)
sheetClienti = sheet.get_worksheet(5)
sheetAcquisti = sheet.get_worksheet(6)
sheetPreferenze = sheet.get_worksheet(7)
sheetPrenotazioni = sheet.get_worksheet(8)


class Venditore:
    def __init__(self, email, password, nome, cognome, tipo_attività, telefono, iva):
        self.email =email
        self.password =password
        self.nome = nome
        self.cognome = cognome 
        self.tipo_attività = tipo_attività
        self.telefono = telefono
        self.iva = iva
    
    def save(self):
        row = [self.email,self.password,self.nome,self.cognome,self.tipo_attività,self.telefono,self.iva]
        sheetVenditori.append_row(row)
    
    def update(self):
        index = Venditore.row_index_by_email(self.email)
        sheetVenditori.update_cell(index, 2,self.password)
        sheetVenditori.update_cell(index, 3,self.nome)
        sheetVenditori.update_cell(index, 4,self.cognome)
        sheetVenditori.update_cell(index, 5,self.tipo_attività)
        sheetVenditori.update_cell(index, 6,self.telefono)
        sheetVenditori.update_cell(index, 7,self.iva)
    
    def delete(self):
        sheetVenditori.delete_row(Venditore.row_index_by_email(self.email))

    @classmethod
    def row_index_by_email(cls,email):
        cell = sheetVenditori.find(email)
        return cell.row
    
    def json(self):
        return {
                'Nome': self.nome, 
                'Cognome': self.cognome, 
                'Email': self.email, 
                'Password': self.password,
                'Tipo Attività':self.tipo_attività,
                'Telefono':self.telefono,
                'IVA':self.iva
                }

    @classmethod
    def row_to_Venditore(cls, row):
        v = Venditore(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        return(v)
    
    @classmethod
    def get_Venditore(cls, venditore):
        cell = sheetVenditori.find(venditore)
        row = sheetVenditori.row_values(cell.row)
        item = Venditore.row_to_Venditore(row)
        return item

class Cliente:
    def __init__(self, email, password, nome, cognome, pagamento, privacy):
        self.email =email
        self.password =password
        self.nome = nome
        self.cognome = cognome 
        self.pagamento = pagamento
        self.privacy = privacy
    
    def save(self):
        row = [self.email,self.password,self.nome,self.cognome,self.pagamento,self.privacy]
        sheetClienti.append_row(row)
    
    def update(self):
        index = Cliente.row_index_by_email(self.email)
        sheetClienti.update_cell(index, 2,self.password)
        sheetClienti.update_cell(index, 3,self.nome)
        sheetClienti.update_cell(index, 4,self.cognome)
        sheetClienti.update_cell(index, 5,self.pagamento)
        sheetClienti.update_cell(index, 6,self.privacy)
    
    def delete(self):
        sheetClienti.delete_row(Cliente.row_index_by_email(self.email))

    @classmethod
    def row_index_by_email(cls,email):
        cell = sheetClienti.find(email)
        return cell.row
    
    def json(self):
        return {
                'Nome': self.nome, 
                'Cognome': self.cognome, 
                'Email': self.email, 
                'Password': self.password,
                'Pagamento':self.pagamento,
                'Privacy':self.privacy
                }

    @classmethod
    def row_to_Cliente(cls, row):
        v = Cliente(row[0],row[1],row[2],row[3],row[4],row[5])
        return(v)
    
    @classmethod
    def get_Cliente(cls, cliente):
        cell = sheetClienti.find(cliente)
        row = sheetClienti.row_values(cell.row)
        item = Cliente.row_to_Cliente(row)
        return item
    
class RecensioneVenditore:
    def __init__(self, email_venditore, email_cliente, recensione):
        self.email_venditore =email_venditore
        self.email_cliente= email_cliente
        self.recensione =recensione
    
    def save(self):
        row = [self.email_venditore,self.email_cliente,self.recensione]
        sheetRecensioni_Venditori.append_row(row)
    
    def update(self):
        index = RecensioneVenditore.row_index_by_emails(self.email_venditore, self.email_cliente)
        sheetRecensioni_Venditori.update_cell(index, 3,self.recensione)
    
    def delete(self):
        sheetRecensioni_Venditori.delete_row(RecensioneVenditore.row_index_by_emails(self.email_venditore, self.email_cliente))

    @classmethod
    def row_index_by_emails(cls,email_venditore, email_cliente):
        cell_list = sheetRecensioni_Venditori.findall(email_venditore)
        for cell in cell_list:
            if sheetRecensioni_Venditori.cell(cell.row,2).value==email_cliente:
                return cell.row
        raise Exception()
    
    def json(self):
        return {
                'Email venditore': self.email_venditore, 
                'Email cliente': self.email_cliente, 
                'Recensione': self.recensione
        }

    @classmethod
    def row_to_RecensioneVenditore(cls, row):
        v = RecensioneVenditore(row[0],row[1],row[2])
        return(v)
    
    @classmethod
    def get_RecensioneVenditore(cls, email_venditore, email_cliente):
        row = sheetRecensioni_Venditori.row_values(RecensioneVenditore.row_index_by_emails(email_venditore, email_cliente))
        item = RecensioneVenditore.row_to_RecensioneVenditore(row)
        if item:
            return item
        raise Exception()
    
class RecensioneProdotto:
    def __init__(self, email_cliente, prodotto, recensione):
        self.email_cliente= email_cliente
        self.prodotto = prodotto
        self.recensione =recensione
    
    def save(self):
        row = [self.email_cliente,self.prodotto,self.recensione]
        sheetRecensioni_Prodotti.append_row(row)
    
    def update(self):
        index = RecensioneProdotto.row_index_by_email_and_product(self.email_cliente, self.prodotto)
        sheetRecensioni_Prodotti.update_cell(index, 3,self.recensione)
    
    def delete(self):
        sheetRecensioni_Prodotti.delete_row(RecensioneVenditore.row_index_by_emails(self.email_cliente, self.prodotto))

    @classmethod
    def row_index_by_email_and_product(cls, email_cliente, prodotto):
        cell_list = sheetRecensioni_Prodotti.findall(email_cliente)
        for cell in cell_list:
            if sheetRecensioni_Prodotti.cell(cell.row,2).value==prodotto:
                return cell.row
        raise Exception()
    
    def json(self):
        return {
                'Email cliente': self.email_cliente, 
                'Prodotto': self.prodotto,
                'Recensione': self.recensione
        }

    @classmethod
    def row_to_RecensioneProdotto(cls, row):
        v = RecensioneProdotto(row[0],row[1],row[2])
        return(v)
    
    @classmethod
    def get_RecensioneProdotto(cls, email_cliente, prodotto):
        row = sheetRecensioni_Prodotti.row_values(RecensioneProdotto.row_index_by_email_and_product(email_cliente, prodotto))
        item = RecensioneProdotto.row_to_RecensioneProdotto(row)
        if item:
            return item
        raise Exception()

class Prodotto:
    def __init__(self, tipologia, nome, caratteristiche, prezzo, tipologia_spedizione, venditore):
        self.tipologia =tipologia
        self.caratteristiche =caratteristiche
        self.nome = nome
        self.prezzo = prezzo 
        self.tipologia_spedizione = tipologia_spedizione
        self.venditore = venditore
    
    def save(self):
        row = [self.tipologia,self.nome,self.caratteristiche,self.prezzo,self.tipologia_spedizione,self.venditore]
        sheetProdotti.append_row(row)
    
    def update(self):
        index = Prodotto.row_index_by_name(self.nome)
        sheetProdotti.update_cell(index, 1,self.tipologia)
        sheetProdotti.update_cell(index, 3,self.caratteristiche)
        sheetProdotti.update_cell(index, 4,self.prezzo)
        sheetProdotti.update_cell(index, 5,self.tipologia_spedizione)
        sheetProdotti.update_cell(index, 6,self.venditore)
    
    def delete(self):
        sheetProdotti.delete_row(Prodotto.row_index_by_name(self.nome))

    @classmethod
    def row_index_by_name(cls,name):
        cell = sheetProdotti.find(name)
        return cell.row
        
    
    def json(self):
        return {
                'Nome': self.nome, 
                'Tipologia': self.tipologia, 
                'Caratteristiche': self.caratteristiche, 
                'Prezzo': self.prezzo,
                'Tipologia Spedizione':self.tipologia_spedizione,
                'Venditore':self.venditore
                }

    @classmethod
    def row_to_Prodotto(cls, row):
        v = Prodotto(row[0],row[1],row[2],row[3],row[4],row[5])
        return(v)
    
    @classmethod
    def get_Prodotto(cls, prodotto):
        cell = sheetProdotti.find(prodotto)
        row = sheetProdotti.row_values(cell.row)
        item = Prodotto.row_to_Prodotto(row)
        return item

class Offerta:
    def __init__(self, codice, prodotto, offerta, data_inizio, data_fine):
        self.codice = codice
        self.prodotto = prodotto
        self.offerta = offerta
        self.data_inizio = data_inizio
        self.data_fine = data_fine  
    
    def save(self):
        row = [self.codice,self.prodotto,self.offerta,self.data_inizio, self.data_fine]
        sheetOfferte.append_row(row)
    
    def update(self):
        index = Offerta.row_index_by_code(self.codice)
        sheetOfferte.update_cell(index, 2,self.prodotto)
        sheetOfferte.update_cell(index, 3,self.offerta)
        sheetOfferte.update_cell(index, 4,self.data_inizio)
        sheetOfferte.update_cell(index, 5,self.data_fine)
    
    def delete(self):
        sheetOfferte.delete_row(Offerta.row_index_by_code(self.codice))

    @classmethod
    def row_index_by_code(cls,code):
        cell = sheetOfferte.find(code)
        return cell.row
        
    
    def json(self):
        return {
                'Codice': self.codice,
                'Prodotto': self.prodotto, 
                'Offerta': self.offerta, 
                'Data Inizio': self.data_inizio,
                'Data Fine': self.data_fine
                }

    @classmethod
    def row_to_Offerta(cls, row):
        v = Offerta(row[0],row[1],row[2],row[3], row[4])
        return(v)
    
    @classmethod
    def get_Offerta(cls, codice):
        cell = sheetOfferte.find(codice)
        row = sheetOfferte.row_values(cell.row)
        item = Offerta.row_to_Offerta(row)
        return item

class Acquisto:
    def __init__(self, codice_carrello, cliente, data):
        self.codice_carrello = codice_carrello
        self.cliente = cliente
        self.data = data
    
    def save(self):
        row = [self.codice_carrello,self.cliente,self.data]
        sheetAcquisti.append_row(row)
    
    def update(self):
        index = Acquisto.row_index_by_code(self.codice_carrello)
        sheetAcquisti.update_cell(index, 2,self.cliente)
        sheetAcquisti.update_cell(index, 3,self.data)
    
    def delete(self):
        sheetAcquisti.delete_row(Acquisto.row_index_by_code(self.codice_carrello))

    @classmethod
    def row_index_by_code(cls,code):
        cell = sheetAcquisti.find(code)
        return cell.row
        
    
    def json(self):
        return {
                'Codice Carrello': self.codice_carrello,
                'Cliente': self.cliente, 
                'Data': self.data
                }

    @classmethod
    def row_to_Acquisto(cls, row):
        v = Acquisto(row[0],row[1],row[2])
        return(v)
    
    @classmethod
    def get_Acquisto(cls, codice):
        cell = sheetAcquisti.find(codice)
        row = sheetAcquisti.row_values(cell.row)
        item = Acquisto.row_to_Acquisto(row)
        return item

class Preferenza:
    def __init__(self, cliente, tipologia):
        self.cliente = cliente
        self.tipologia = tipologia
    
    def save(self):
        row = [self.cliente,self.tipologia]
        sheetPreferenze.append_row(row)
    
    def update(self):
        index = Preferenza.row_index_by_client_and_type(self.cliente, self.tipologia)
        sheetPreferenze.update_cell(index, 1,self.cliente)
        sheetPreferenze.update_cell(index, 2,self.tipologia)
    
    def delete(self):
        sheetPreferenze.delete_row(Preferenza.row_index_by_client_and_type(self.cliente, self.tipologia))

    @classmethod
    def row_index_by_client_and_type(cls,cliente, tipologia):
        cell_list = sheetPreferenze.findall(cliente)
        for cell in cell_list:
            if sheetPreferenze.cell(cell.row,2).value==tipologia:
                return cell.row
        raise Exception()      
    
    def json(self):
        return {
                'Cliente': self.cliente, 
                'Tipologia': self.tipologia
                }

    @classmethod
    def row_to_Preferenza(cls, row):
        v = Preferenza(row[0],row[1])
        return(v)
    
    @classmethod
    def get_Preferenza(cls, cliente, tipologia):
        row = sheetPreferenze.row_values(Preferenza.row_index_by_client_and_type(cliente, tipologia))
        item = Preferenza.row_to_Preferenza(row)
        if item:
            return item
        raise Exception()

class Prenotazione:
    def __init__(self, codice, cliente, prodotto, quantità):
        self.cliente = cliente
        self.prodotto = prodotto
        self.quantità= quantità
        self.codice = codice
    
    def save(self):
        row = [self.codice, self.cliente,self.prodotto, self.quantità]
        sheetPrenotazioni.append_row(row)
    
    def update(self):
        index = Prenotazione.row_index_by_code_client_product(self.codice, self.cliente, self.prodotto)
        sheetPrenotazioni.update_cell(index, 2,self.cliente)
        sheetPrenotazioni.update_cell(index, 3,self.prodotto)
        sheetPrenotazioni.update_cell(index, 4,self.quantità)
    
    def delete(self):
        sheetPrenotazioni.delete_row(Prenotazione.row_index_by_code_client_product(self.codice, self.cliente,self.prodotto))

    @classmethod
    def row_index_by_code_client_product(cls,codice, cliente, prodotto):
        cell_list = sheetPrenotazioni.findall(codice)
        cell_list2=[]
        for cell in cell_list:
            if sheetPrenotazioni.cell(cell.row,2).value==cliente & sheetPrenotazioni.cell(cell.row,3).value==prodotto:
                return cell.row
        raise Exception()      
    
    def json(self):
        return {
                'Codice Carrello': self.codice, 
                'Cliente': self.cliente,
                'Prodotto': self.prodotto,
                'Quantità': self.quantità
                }

    @classmethod
    def row_to_Prenotazione(cls, row):
        v = Prenotazione(row[0],row[1],row[2], row[3])
        return(v)
    
    @classmethod
    def get_Prenotazione(cls, codice, cliente,prodotto):
        row = sheetPrenotazioni.row_values(Prenotazione.row_index_by_code_client_product(codice,cliente,prodotto))
        item = Prenotazione.row_to_Prenotazione(row)
        if item:
            return item
        raise Exception()
    