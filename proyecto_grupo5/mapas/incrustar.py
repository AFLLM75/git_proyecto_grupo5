with open('/home/oc-admin/Escritorio/txtinsertar.txt', 'r') as fichero_entrada,\
        open('/home/oc-admin/Escritorio/txtsalida.txt', 'w') as fichero_salida:
    print('hola', file=fichero_salida)
    i=0
    for linea in fichero_entrada:
        print(linea, file=fichero_salida, end='')
        if i == 2:
            print('fila3', file=fichero_salida, end = '')
        i =i+1
    print('adios', file=fichero_salida)