
import item
import codigobarra as cb
import PySimpleGUI as sg
import random

sg.theme('DarkAmber')   # Add a touch of color



# Generador de Codigo de Barras Layout

layoutBarcode = [[sg.Text('Generador de Codigo de Barras', size=(30, 1), justification='center', font=("Helvetica", 25))],
[sg.Text('Nombre del item', size=(30, 1), justification='center', font=("Helvetica", 15))],
[sg.InputText()],
[sg.Text('Tipo del item', size=(30, 1), justification='center', font=("Helvetica", 15))],
[sg.InputText()],
[sg.Text('Codigo', size=(30, 1), justification='center', font=("Helvetica", 15))],
[sg.InputText(str(random.randint(1000000000000, 9999999999999)))],
[sg.Button('Generar Codigo', size=(30, 2), font=("Helvetica", 15))],
[sg.Button('Return', size=(30, 2), font=("Helvetica", 15))]]

# Ticket generator

layoutTicket = []
# Ticket Deleter

layoutDelete = []

# show all open tickets

layoutShow = []

# Main layout

layoutMain = [[sg.Text('Generador de Codigo de Barras', size=(30, 1), justification='center', font=("Helvetica", 25))],
[sg.Button('Generar Codigo de Barras', size=(30, 2), font=("Helvetica", 15))],
[sg.Button('Generar Ticket', size=(30, 2), font=("Helvetica", 15))],
[sg.Button('Cerrar Ticket', size=(30, 2), font=("Helvetica", 15))],
[sg.Button('Mostrar Tickets Abiertos', size=(30, 2), font=("Helvetica", 15))],
[sg.Button('Salir', size=(30, 2), font=("Helvetica", 15))]]

# Create the window

window = sg.Window('Generador de Codigo de Barras', layoutMain, size=(600, 600), element_justification='center')


# Event Loop to process "events" and get the "values" of the inputs












while True:

    event, values = window.read()

    if event in (None, 'Exit'):
        break


    if event == 'Generar Codigo de Barras':
        window = sg.Window('Generador de Codigo de Barras', layoutBarcode, size=(500, 500), element_justification='center')
    elif event == 'Generar Ticket':
        window.close()
        window = sg.Window('Generador de Codigo de Barras', layoutTicket, size=(500, 500), element_justification='center')
    elif event == 'Cerrar Ticket':
        window.close()
        window = sg.Window('Generador de Codigo de Barras', layoutDelete, size=(500, 500), element_justification='center')
    elif event == 'Mostrar Tickets Abiertos':
        window.close()
        window = sg.Window('Generador de Codigo de Barras', layoutShow, size=(500, 500), element_justification='center')
    
    
    
    elif event == 'Generar Codigo':
        print(values[0])
        print(values[1])
        print(values[2])


    
    elif event == 'Return':
        window.close()
        window = sg.Window('Generador de Codigo de Barras', layoutMain, size=(600, 600), element_justification='center')
    else:
        window.close()
        break


