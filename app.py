
import item as it
import codigobarra as cb
import PySimpleGUI as sg
import random
import os
import datetime
sg.theme('DarkAmber')   # Add a touch of color

# Crear un TicketManager
ticket_manager = it.TicketManager()
item_manager = it.ItemManager()

layoutPrincipal = [
    [sg.Text('App Caseta')],
    # Agregar Item al Inventario con Código de Barras
    [sg.Button('Agregar Item', key='-AGREGAR-', size=(60, 5),)],
    # Ver Inventario
    [sg.Button('Ver Inventario', key='-INVENTARIO-', size=(60, 5))],
    # Ver Tickets
    [sg.Button('Ver Tickets', key='-TICKETS-ABIERTOS-', size=(60, 5))],
    # Generar Ticket
    [sg.Button('Generar Ticket', key='-TICKET-', size=(60, 5))],
    # Agregar Usuario
    [sg.Button('Agregar Usuario', key='-USUARIO-', size=(60, 5))],
    # Salir
    [sg.Button('Salir', key='-SALIR-', size=(60, 5))]
]
VentanaPrincipal = sg.Window('App Caseta', layoutPrincipal, modal=True)


def VentanaAgregar():
    layoutAgregar = [
        [sg.Text('Agregar Item')],
        [sg.Text('Nombre: '), sg.Input(key='-NOMBRE-')],
        # Código de Barras EAN13
        [sg.Text('Código de Barras: '), sg.Input(key='-BARRA-', default_text=random.randint(100000000000, 999999999999))],
        # Descrición del Item
        [sg.Text('Descripción: '), sg.Input(key='-DESCRIPCION-')],
        # Estado del Item (Ej: Prestado, Disponible, Dañado)
        [sg.Text('Estado: '), sg.Listbox(values=('Disponible', 'Dañado', 'Prestado'), size=(
            20, 3), key='-ESTADO-', default_values=['Disponible'])],
        [sg.Button('Agregar', key='-AGREGAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]
    VentanaAgregar = sg.Window('Agregar Item', layoutAgregar, modal=True)
    while True:
        event, values = VentanaAgregar.read()
        if event == sg.WIN_CLOSED or event == '-CANCELAR-':
            break
        elif event == '-AGREGAR-':
            nombre = values['-NOMBRE-']
            codigo = values['-BARRA-']
            # Descripcion o Tipo de Item (Ej: Material,Herramienta etc)
            descripcion_tipo = values['-DESCRIPCION-']
            # Estado del Item (Ej: Prestado, Disponible, Dañado)
            estado = values['-ESTADO-']
            estado = estado[0]
            cb.generar_codigo_barras(codigo, nombre)
            item_manager.agregar_item(nombre, codigo, estado, descripcion_tipo)
            sg.popup('Item Agregado')
            break




def Obtener(nombre):
    csv = nombre+'.csv'
    lista = []
    open(csv, 'r')
    for line in open(csv, 'r'):
        line = line.strip()
        line = line.split(',')
        lista.append(line)
    return lista


def ValidarControl(control):
    # Valida que el numero de exista en el csv en cualquier linea columna 3
    items = Obtener("Usuarios")
    for item in items:
        if control == item[2]:
            return True
    return False


def VentanaInventario():
    items = Obtener("Inventario")
    nombresItems = []
    estadosItems = []
    tiposItems = []
    codigoItems = []
    for item in items:
        nombresItems.append(item[0])
        codigoItems.append(item[1])
        estadosItems.append(item[2])
        tiposItems.append(item[3])
    Ojetos = []
    for i in range(len(nombresItems)):
        Ojetos.append(
            f'Nombre: {nombresItems[i]} | Estado: {estadosItems[i]} | Tipo: {tiposItems[i]} | Código: {codigoItems[i]}')
    layoutInventario = [
        [sg.Text('Inventario')],
        [sg.Listbox(values=Ojetos, size=(60, 10), key='-INVENTARIO-')],
        [sg.Button('Salir', key='-SALIR-')]
    ]
    VentanaInventario = sg.Window('Inventario', layoutInventario, modal=True)
    while True:
        event, values = VentanaInventario.read()
        if event == sg.WIN_CLOSED or event == '-SALIR-':
            break





def VentanaTicketsAbiertos():
    tickets = Obtener("Tickets")
    layoutTickets = [
        [sg.Text('Tickets')],
        [sg.Listbox(values=tickets, size=(60, 10), key='-TICKETS-')],
        [sg.Button('Salir', key='-SALIR-')]
    ]
    VentanaTickets = sg.Window('Tickets', layoutTickets, modal=True)
    while True:
        event, values = VentanaTickets.read()
        if event == sg.WIN_CLOSED or event == '-SALIR-':
            break








def VentanaTicket():
    # Crearemos un ticket con los items que se encuentren en el inventario
    
    item_manager.cargar_items()




    OjetosInventario = []
    OjetosCarrito = []
    #   def mostrar_items(self):
    #table = ''
    #for item in self.items:
    #    table += f"Item: {item.nombre} - {item.codigo} - {item.estado} - {item.tipo} \n"
    #return table

    for item in item_manager.items:
        OjetosInventario.append(
            f'Nombre: {item.nombre} | Estado: {item.estado} | Tipo: {item.tipo} | Código: {item.codigo}')
        


    layoutTicket = [
        [sg.Text('Ticket')],
        # barra de busqueda
        [sg.Text('Buscar: '), sg.Input(key='-BUSQUEDA-'), sg.Button('Buscar', key='-BUSCAR-')],
        # On duble click se agrega al carrito
        [sg.Listbox(values=OjetosInventario, size=(60, 10), key='-INVENTARIO-')],
        # Carrito de compras
        [sg.Text('Carrito de Compras')],
        [sg.Listbox(values=OjetosCarrito, size=(60, 10), key='-CARRITO-')],
        # No. Control
        [sg.Text('No. Control: '), sg.Input(key='-CONTROL-')],
        # Extras (Text Box, para agregar cosas como: Material que no tenga codigo de barras, Herramientas, etc)
        [sg.Text('Extras: '), sg.InputText(key='-EXTRAS-')],
        # Botones
        [sg.Button('Agregar al Carrito', key='-AGREGAR_CARRITO-'),
            sg.Button('Quitar del Carrito', key='-QUITAR-')],
        [sg.Button('Generar Ticket', key='-GENERAR-'),
            sg.Button('Cancelar', key='-CANCELAR-')],
        # Text Box para usar lector de codigo de barras
        [sg.Text('Codigo de Barras: '), sg.Input(key='-BARRA-'), sg.Button('Agregar', key='-AGREGAR-BARRA-', bind_return_key=True)],
    ]
    VentanaTicket = sg.Window('Ticket', layoutTicket, modal=True)

    while True:
        event, values = VentanaTicket.read()

        VentanaTicket['-AGREGAR-BARRA-'].BindReturnKey = True
        if event == sg.WIN_CLOSED or event == '-SALIR-':
            break
        elif event == '-AGREGAR_CARRITO-':
            # El item seleccionado se agrega al carrito
            itemSeleccionado = values['-INVENTARIO-']
            
            # Si no hay nada seleccionado, no se hace nada
            if len(itemSeleccionado) == 0:
                itemSeleccionado = None
            else:
                itemSeleccionado = itemSeleccionado[0]

            OjetosCarrito.append(itemSeleccionado)
            VentanaTicket['-CARRITO-'].update(OjetosCarrito)
            # Se elimina del inventario y del array
            OjetosInventario.remove(itemSeleccionado)
            VentanaTicket['-INVENTARIO-'].update(OjetosInventario)



        elif event == '-QUITAR-':
            # Aplica lo contrario a -AGREGAR- pero solo si el carrito no esta vacio
            if len(OjetosCarrito) > 0:
                itemSeleccionado = values['-CARRITO-']
                itemSeleccionado = itemSeleccionado[0]
                OjetosInventario.append(itemSeleccionado)
                VentanaTicket['-INVENTARIO-'].update(OjetosInventario)
                OjetosCarrito.remove(itemSeleccionado)
                VentanaTicket['-CARRITO-'].update(OjetosCarrito)


        elif event == '-GENERAR-':
            # Validar que el usuario haya ingresado un No. Control
            if values['-CONTROL-'] == '':
                sg.popup('No. Control no ingresado', title='Error')
            else:
                # Validar que el numero de control sea valido
                if ValidarControl(values['-CONTROL-']):
                    # Generar el ticket de item
                    # 
                    #         self.usuario = usuario
                    #         self.fecha = fecha
                    #         self.estado = estado
                    #         self.items = items 
                    # Crear un objeto ticket y guardarlo con el ticket
                
                    ticket = it.Ticket(values['-CONTROL-'], datetime.datetime.now(), 'Abierto', OjetosCarrito)
                    ticket_manager.agregar_ticket(ticket)
                    # Actualizar el inventario usando los manejadores
                    print(item_manager.mostrar_items())
                    items_a_actualizar = OjetosCarrito
                    for item in items_a_actualizar:
                        # Actualizar el estado de los 
                        # Convertir el item a un objeto Item
                        item = it.Item(item[0], item[1], item[2], item[3])
                        item_manager.cambiar_estado(item, 'Prestado')
                        print(item.estado)
                        item_manager.actualizar_item(item, item.nombre, item.estado, item.tipo, item.codigo)
                        item_manager.guardar_items()
                        print(item_manager.mostrar_items())



                    # Reinicia el inventario 
                    OjetosCarrito = []
                    VentanaTicket['-CARRITO-'].update(OjetosCarrito)
                    OjetosInventario = []
                    for item in item_manager.items:
                        OjetosInventario.append(
                            f'Nombre: {item.nombre} | Estado: {item.estado} | Tipo: {item.tipo} | Código: {item.codigo}')
                    VentanaTicket['-INVENTARIO-'].update(OjetosInventario)
                    ticket_manager.guardar_tickets()


                    sg.popup('Ticket generado', title='Ticket')
                    VentanaTicket.close()
                else:
                    sg.popup('No. Control no valido', title='Error')
                    VentanaUsuario()


                
        elif event == '-CANCELAR-':
            # Reinicia el inventario y manda el carrito a 0
            OjetosCarrito = []
            VentanaTicket['-CARRITO-'].update(OjetosCarrito)
            OjetosInventario = []
            for item in item_manager.items:
                OjetosInventario.append(
                    f'Nombre: {item.nombre} | Estado: {item.estado} | Tipo: {item.tipo} | Código: {item.codigo}')
            VentanaTicket['-INVENTARIO-'].update(OjetosInventario)
        elif event == '-BUSCAR-':
            # Muestra solo los items que contengan parte del texto ingresado
            # Si el item esta en el carrito no se muestra

            OjetosInventario = []
            for item in item_manager.items:
                OjetosInventario.append(
                    f'Nombre: {item.nombre} | Estado: {item.estado} | Tipo: {item.tipo} | Código: {item.codigo}')
            texto = values['-BUSQUEDA-']
            # La busqueda no es sensible a mayusculas
            texto = texto.lower()
            # Si el item esta en el carrito no se muestra
            for item in OjetosCarrito:
                if item in OjetosInventario:
                    OjetosInventario.remove(item)
            # Si el item no contiene el texto ingresado no se muestra
            for item in OjetosInventario:
                if texto not in item.lower():
                    OjetosInventario.remove(item)
            VentanaTicket['-INVENTARIO-'].update(OjetosInventario)
        elif event == '-AGREGAR-BARRA-':
            
            # Agregar al carrito si esta en el inventario
            # Y hacer lo mismo que -AGREGAR-
            # y si ya esta en el carrito Regresar al inventario
            # y hacer lo mismo que -QUITAR-

            # Obtener el codigo de barras
            codigo = values['-BARRA-']
            # Elimina el ultimo digito del numero
            codigo = codigo[:-1]
            # Reinicia el input
            VentanaTicket['-BARRA-'].update('')
            
            # Determina si el codigo esta en el inventario y asigna el item a itemGuardar
            itemGuardar = ''
            for item in items:
                if codigo == item[1]:
                    itemGuardar = item
                    break
            
            # Si el item esta en el inventario agregarlo al carrito
            if itemGuardar != '':
                # Usamos el for para que el item se agregue al carrito
                # con el formato que se muestra en la lista
                for item in OjetosInventario:
                    if itemGuardar[0] in item:
                        itemGuardar = item
                        break
                OjetosCarrito.append(itemGuardar)
                VentanaTicket['-CARRITO-'].update(OjetosCarrito)
                # Se elimina del inventario y del array
                OjetosInventario.remove(itemGuardar)
                VentanaTicket['-INVENTARIO-'].update(OjetosInventario)
            # Si el item no esta en el inventario mandar un popup
            else:
                sg.popup('Codigo no encontrado', title='Error')

def VentanaUsuario():
    layoutUsuario = [
        [sg.Text('Nuevo Usuario', font='Any 15')],
        [sg.Text('Nombre: '), sg.Input(key='-NOMBRE-')],
        #Apellidos
        [sg.Text('Apellidos: '), sg.Input(key='-APELLIDOS-')],
        #No. de Control
        [sg.Text('No. de Control: '), sg.Input(key='-CONTROL-')],
        #Carrera
        # Electronica, Electrica, Mecatronica, Sistemas Computaconales, Logistica, Materiales, Industrial, Mecanica, Gestion Empresarial, Arquitectura, Maestria
        [sg.Text('Carrera: '), sg.InputCombo(('Electronica', 'Electrica', 'Mecatronica', 'Sistemas Computaconales', 'Logistica', 'Materiales', 'Industrial', 'Mecanica', 'Gestion Empresarial', 'Arquitectura', 'Maestria'), key='-CARRERA-')],
        #Semestre
        [sg.Text('Semestre: '), sg.InputCombo(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11','12','NA'), key='-SEMESTRE-')],
        [sg.Button('Guardar', key='-GUARDAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]
    VentanaUsuario = sg.Window('Nuevo Usuario', layoutUsuario, modal=True)

    while True:
        event, values = VentanaUsuario.read()
        if event == sg.WIN_CLOSED or event == '-CANCELAR-':
            break
        elif event == '-GUARDAR-':
            # Guarda los datos del usuario csv Linea por linea
            # Nombre, Apellidos, No. de Control, Carrera, Semestre
            # Si el usuario ya existe no se guarda

            for line in open('Usuarios.csv'):
                if values['-CONTROL-'] in line:
                    sg.popup('El usuario ya existe', title='Error')
                    break
            else:
                with open('Usuarios.csv', 'a') as file:
                    file.write(f"{values['-NOMBRE-']},{values['-APELLIDOS-']},{values['-CONTROL-']},{values['-CARRERA-']},{values['-SEMESTRE-']}\n")
                VentanaUsuario.close()


            break
        elif event == '-CANCELAR-':
            # Resetea los campos
            VentanaUsuario['-NOMBRE-'].update('')
            VentanaUsuario['-APELLIDOS-'].update('')
            VentanaUsuario['-CONTROL-'].update('')
            VentanaUsuario['-CARRERA-'].update('')
            VentanaUsuario['-SEMESTRE-'].update('')
            VentanaUsuario.close()
            break
        





while True:
    event, values = VentanaPrincipal.read()
    if event == sg.WIN_CLOSED or event == '-SALIR-':
        break
    elif event == '-AGREGAR-':
        VentanaAgregar()
    elif event == '-INVENTARIO-':
        VentanaInventario()
    elif event == '-TICKETS-ABIERTOS-':
        VentanaTicketsAbiertos()
    elif event == '-TICKET-':
        VentanaTicket()
    elif event == '-USUARIO-':
        VentanaUsuario()
