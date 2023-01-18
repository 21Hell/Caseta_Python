
import item
import codigobarra as cb
import PySimpleGUI as sg
import random

sg.theme('DarkAmber')   # Add a touch of color


layoutPrincipal = [
    [sg.Text('App Caseta')],
    # Agregar Item al Inventario con Código de Barras
    [sg.Button('Agregar Item', key='-AGREGAR-', size=(60, 5),)],
    # Ver Inventario
    [sg.Button('Ver Inventario', key='-INVENTARIO-', size=(60, 5))],
    # Generar Ticket
    [sg.Button('Generar Ticket', key='-TICKET-', size=(60, 5))],
    # Salir
    [sg.Button('Salir', key='-SALIR-', size=(60, 5))]
]
VentanaPrincipal = sg.Window('App Caseta', layoutPrincipal, modal=True)


def VentanaAgregar():
    layoutAgregar = [
        [sg.Text('Agregar Item')],
        [sg.Text('Nombre: '), sg.Input(key='-NOMBRE-')],
        # Código de Barras generado automáticamente
        [sg.Text('Código de Barras: '), sg.Input(key='-BARRA-',
                                                 default_text=random.randint(1000000000000, 9999999999999))],
        # Descrición del Item
        [sg.Text('Descripción: '), sg.Input(key='-DESCRIPCION-')],
        # Estado del Item (Ej: Prestado, Disponible, Dañado)
        [sg.Text('Estado: '), sg.Listbox(values=('Disponible', 'Dañado', 'Prestado'), size=(
            20, 3), key='-ESTADO-', default_values=['Disponible'])],
        [sg.Button('Agregar', key='-AGREGAR-'),
         sg.Button('Cancelar', key='-CANCELAR-')]
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
            Ojeto = item.Item(nombre, codigo, estado, descripcion_tipo)
            Ojeto.agregar_item(nombre, codigo, estado, descripcion_tipo)
            sg.popup('Item Agregado')
            break


def ObtenerInventario():
    # Obtener el Inventario del csv
    items = []
    open('inventario.csv', 'r')
    for line in open('inventario.csv', 'r'):
        line = line.strip()
        line = line.split(',')
        items.append(line)
    return items


def VentanaInventario():
    items = ObtenerInventario()
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


def FormateoBonito(items):
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
    return Ojetos




def VentanaTicket():
    # Crearemos un ticket con los items que se encuentren en el inventario
    items = ObtenerInventario()
    nombresItems = []
    estadosItems = []
    tiposItems = []
    codigoItems = []
    for item in items:
        nombresItems.append(item[0])
        codigoItems.append(item[1])
        estadosItems.append(item[2])
        tiposItems.append(item[3])
    OjetosInventario = []
    OjetosCarrito = []
    
    ObjetosBonitos = FormateoBonito(items)


    layoutTicket = [
        [sg.Text('Ticket')],
        # barra de busqueda
        [sg.Text('Buscar: '), sg.Input(key='-BUSCAR-')],
        # On duble click se agrega al carrito
        [sg.Listbox(values=ObjetosBonitos, size=(60, 10), key='-INVENTARIO-')],
        # Carrito de compras
        [sg.Text('Carrito de Compras')],
        [sg.Listbox(values=[], size=(60, 10), key='-CARRITO-')],
        # Botones
        [sg.Button('Agregar al Carrito', key='-AGREGAR-'),
            sg.Button('Quitar del Carrito', key='-QUITAR-')],
        [sg.Button('Generar Ticket', key='-GENERAR-'),
            sg.Button('Cancelar', key='-CANCELAR-')],
        [sg.Button('Salir', key='-SALIR-')]
    ]
    VentanaTicket = sg.Window('Ticket', layoutTicket, modal=True)

    while True:
        event, values = VentanaTicket.read()
        if event == sg.WIN_CLOSED or event == '-SALIR-':
            break
        elif event == '-AGREGAR-':
            # Del Arrerlo de objetos del inventario de aquel que se selecciono se agrega al carrito
            item = values['-INVENTARIO-']
            OjetosCarrito = OjetosCarrito.append(item)
            # Se actualiza el estado del item en el inventario pero no se elimina


            VentanaTicket.update()



while True:
    event, values = VentanaPrincipal.read()
    if event == sg.WIN_CLOSED or event == '-SALIR-':
        break
    elif event == '-AGREGAR-':
        VentanaAgregar()
    elif event == '-INVENTARIO-':
        VentanaInventario()
    elif event == '-TICKET-':
        VentanaTicket()
