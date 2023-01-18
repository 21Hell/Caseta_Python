import treepoem


# Generar Codigo de Barras

def generar_codigo_barras(codigo, nombre_archivo):
    barcode = treepoem.generate_barcode(
        barcode_type='ean13',
        data=codigo,
        # include_text and guardwhitespace
        options=dict(includetext=True)
    )


    barcode.save(nombre_archivo + '.png')
    
# https://github.com/bwipp/postscriptbarcode/wiki/Options-Reference




