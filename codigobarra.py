import treepoem


# Generar Codigo de Barras

def generar_codigo_barras(codigo, nombre_archivo):
    barcode = treepoem.generate_barcode(barcode_type='code128', data=codigo)
    barcode.save(nombre_archivo + '.png')




