import datetime




class Item:
    def __init__(self, nombre, codigo, estado, tipo, cantidad_prestado):
        self.nombre = nombre
        self.codigo = codigo
        #Estados: Prestado, Disponible, Dañado
        self.estado = estado
        self.tipo = tipo
        self.cantidad_prestado = cantidad_prestado

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



