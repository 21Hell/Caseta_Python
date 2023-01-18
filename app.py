
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
    
    OjetosInventario = FormateoBonito(items)

    layoutTicket = [
        [sg.Text('Ticket')],
        # barra de busqueda
        [sg.Text('Buscar: '), sg.Input(key='-BUSQUEDA-'), sg.Button('Buscar', key='-BUSCAR-')],
        # On duble click se agrega al carrito
        [sg.Listbox(values=OjetosInventario, size=(60, 10), key='-INVENTARIO-')],
        # Carrito de compras
        [sg.Text('Carrito de Compras')],
        [sg.Listbox(values=OjetosCarrito, size=(60, 10), key='-CARRITO-')],
        # Botones
        [sg.Button('Agregar al Carrito', key='-AGREGAR-'),
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
        elif event == '-AGREGAR-':
            # El item seleccionado se agrega al carrito
            itemSeleccionado = values['-INVENTARIO-']
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
            # TODO Genera el ticket
            pass
        elif event == '-CANCELAR-':
            # Reinicia el inventario y manda el carrito a 0
            OjetosCarrito = []
            VentanaTicket['-CARRITO-'].update(OjetosCarrito)
            OjetosInventario = FormateoBonito(items)
            VentanaTicket['-INVENTARIO-'].update(OjetosInventario)
        elif event == '-BUSCAR-':
            # Muestra solo los items que contengan parte del texto ingresado
            items = ObtenerInventario()
            OjetosInventario = FormateoBonito(items)
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
