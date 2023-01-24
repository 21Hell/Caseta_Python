import datetime




class Item:
    def __init__(self, nombre, codigo, estado, tipo):
        self.nombre = nombre
        self.codigo = codigo
        #Estados: Prestado, Disponible, Dañado
        self.estado = estado
        self.tipo = tipo
    


class ItemManager:
    def __init__(self):
        self.items = []

    def actualizar_item(self, item, nombre, codigo, estado, tipo):
        item.nombre = nombre
        item.codigo = codigo
        item.estado = estado
        item.tipo = tipo
        print("Item actualizado exitosamente")

    def agregar_item(self, item):
        #Agregar al csv
        with open('Inventario.csv', 'a') as file:
            file.write(f"{item.nombre},{item.codigo},{item.estado},{item.tipo} \n")
            print("Item agregado exitosamente")

    def cambiar_estado(self, item, estado):
        item.estado = estado
        # Actualizar el CSV
        self.guardar_items()
        print("Estado cambiado exitosamente")

    def guardar_items(self):
        print("Guardando Items")
        with open('Inventario.csv', 'w') as file:
            for item in self.items:
                file.write(f"{item.nombre},{item.codigo},{item.estado},{item.tipo} \n")

    def actualizar_items(self):
        self.items = []
        self.cargar_items()

    def mostrar_items(self):
        #mostar Estado de los items
        table = ''
        for item in self.items:
            table += f"Item: {item.nombre} - {item.codigo} - {item.estado} - {item.tipo} \n"
        return table

    def getItemfromCode(self, code):
        for item in self.items:
            if item.codigo == code:
                print("Item encontrado")
                return item
        return None

    def cargar_items(self):
        print("Cargando Items")
        with open('Inventario.csv', 'r') as file:
            for line in file:
                line = line.strip()
                nombre, codigo, estado, tipo = line.split(',')
                item = Item(nombre, codigo, estado, tipo)
                self.items.append(item)

class Ticket:
    # Usuario del Ticket
    # Fecha de apertura del ticket
    # Abirto o cerrado
    # Lista de Items
    def __init__(self, usuario, fecha, estado, items):
        self.usuario = usuario
        self.fecha = fecha
        self.estado = estado
        self.items = items
    
    def agregar_item(self, item):
        self.items.append(item)

    def cerrar_ticket(self):
        self.estado = "Cerrado"


class TicketManager:
    def __init__(self):
        self.tickets = []

    def agregar_ticket(self, ticket):
        self.tickets.append(ticket)

    def mostrar_tickets_abiertos(self):
        table = ''
        for ticket in self.tickets:
            if ticket.estado == "Abierto":
                table += f"Ticket: {ticket.usuario} - {ticket.fecha} - {ticket.estado} - {ticket.items} \n"
        return table

    def mostrar_tickets_cerrados(self):

        table = ''
        for ticket in self.tickets:
            if ticket.estado == "Cerrado":
                table += f"Ticket: {ticket.usuario} - {ticket.fecha} - {ticket.estado} - {ticket.items} \n"
        return table

    def mostrar_tickets(self):
        table = ''
        for ticket in self.tickets:
            table += f"Ticket: {ticket.usuario} - {ticket.fecha} - {ticket.estado} - {ticket.items} \n"
        return table

    def buscar_ticket(self, usuario):
        for ticket in self.tickets:
            if ticket.usuario == usuario:
                return ticket
        return None

    def buscar_ticket_por_fecha(self, fecha):
        for ticket in self.tickets:
            if ticket.fecha == fecha:
                return ticket
        return None

    # Guardar Tickets en CSV
    def guardar_tickets(self):
        print("Guardando Tickets")
        with open('Tickets.csv', 'w') as file:
            for ticket in self.tickets:
                file.write(f"{ticket.usuario},{ticket.fecha},{ticket.estado},{ticket.items} \n")
    def cambiar_estado(self, ticket, estado):
        ticket.estado = estado

    

item_manager = ItemManager()
item_manager.cargar_items()

# Cambiar estado de un item
item = item_manager.items[0]
item_manager.cambiar_estado(item, "Prestado")



print(item_manager.mostrar_items())