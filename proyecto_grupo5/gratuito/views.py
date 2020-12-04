from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import psycopg2.extras
# Create your views here.

def wifi(request):
    conn = psycopg2.connect(dbname="wifi_db",
                            user="grupo5_user",
                            password="patata")
    with open("debug.log", "a+") as debug_file:
        print("Funciona!", file=debug_file)
    return HttpResponse('Funciona!')

def select(request):
    conn = psycopg2.connect(dbname="wifi_db",
                            user="grupo5_user",
                            password="patata")
    cursor = conn.cursor()
    cursor.execute("SELECT ETRS89_COORD_X,ETRS89_COORD_Y,LONGITUD,LATITUD FROM wifi;")
    html = '<html>'
    columns = [col[0] for col in cursor.description]
    for column in columns:
        html += str(column) + '|'
    html += '<br>'
    for empleado in cursor.fetchall():
        for columna in empleado:
            html += str(columna) + '|'
        html += '<br>'
    html += '</html>'
    cursor.close()
    conn.close()
    return HttpResponse(html)

'''=========================Ver Coordenadas==============================='''
def selectcoordenadas(request):
    conn = psycopg2.connect(dbname="wifi_db", user="grupo5_user",password="patata")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    equipament = request.GET.get('get_equipament', default='%')
    cursor.execute(f'SELECT * FROM wifi WHERE equipament LIKE %s; ',(equipament,))
    result = cursor.fetchall()
    cursor.execute(f"SELECT equipament FROM wifi;")
    resultall = cursor.fetchall()
    params = {
        'wifi':result,
        'equipamentall':resultall,
    }
    cursor.close()
    conn.close()
    # print (result)
    crear_mapa(result[0]['latitud'], result[0]['longitud'])
    return render(request, 'wifiBCNcabecera.html', params)

'''=================================Crear Mapa==========================='''
def crear_mapa(x,y):
    import gmplot
    # Create the map plotter:

    APIKEY = 'AIzaSyD3SJ0Z-jhr5Y-PmW2Pe5CelLt2pKDTwdg'  # (your API key here)
    gmap = gmplot.GoogleMapPlotter(41.38714, 2.17006, 13, Apikey=APIKEY)

    # Mark a hidden gem:
    gmap.marker(x, y, color='cornflowerblue')
    gmap.draw('gratuito/templates/map.html')
    # insertamos dos lineas de codigo en el archivo generado automaticamente
    with open('gratuito/templates/map.html', 'r') as fichero_entrada, \
         open('gratuito/templates/map_modificado.html', 'w') as fichero_salida:
        i = 0
        for linea in fichero_entrada:
            if i == 28:
                print('{% block cabecera %}', file=fichero_salida)
                print('{% endblock %}', file=fichero_salida)
                print('{% block buscar_coordenadas %}', file=fichero_salida)
                print('{% endblock %}', file=fichero_salida)
            print(linea, file=fichero_salida, end='')
            i = i + 1


    # abrir mapa y modificar map.html en el body antes del  añadir
def prueba(request):

    conn = psycopg2.connect(dbname="wifi_db", user="grupo5_user",password="patata")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    nom_barris = request.GET.get('get_nom_barri', default='%')
    cursor.execute(f"SELECT * FROM barris WHERE nom_barri LIKE %s; ",(nom_barris,))
    result = cursor.fetchall()
    id_barris = request.GET.get('get_id_barri', default='%')
    cursor.execute(f"SELECT idbarri FROM barris WHERE nom_barri LIKE %s; ",(id_barris,))
    resulidbarri = cursor.fetchall()
    cursor.execute(f"SELECT nom_barri FROM barris ORDER BY nom_barri ASC;")
    resultall = cursor.fetchall()
    params = {
        'nom_barris':result,
        'barrisall':resultall,
        'id_barris':resulidbarri,
            }
    cursor.close()
    conn.close()
    return render(request, 'formWifi.html', params)

def insert(request):
    #print('insertando ando')
    conn = psycopg2.connect(dbname="wifi_db",
                            user="grupo5_user",
                            password="patata")
    cursor = conn.cursor()
    coordenada_x= request.POST["etrs89_coord_x"]
    coordenada_y = request.POST["etrs89_coord_y"]
    longitud= request.POST["longitud"]
    latitud = request.POST["latitud"]
    equipament = request.POST["equipament"]
    nom_barri = request.POST["barri"]
    cursor.execute(f"SELECT idbarri FROM barris  WHERE nom_barri  = %s; ",(nom_barri,))
    idbarri = cursor.fetchone()[0]
    adreca = request.POST["adreca"]
    telefon = request.POST["telefon"]
    cursor.execute(f"INSERT INTO wifi VALUES (default,'{coordenada_x}','{coordenada_y}','{longitud}','{latitud}','{equipament}','{idbarri}','{adreca}','{telefon}');")
    conn.commit()                                    
    cursor.close()
    conn.close()
    return redirect(prueba)




"""
def prueba(request):
    barri= request.GET.get('get_nom_barri', default='%')

    conn = psycopg2.connect(dbname="wifi_db",
                            user="grupo5_user",
                            password="patata")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f"SELECT nom_barri FROM barris';")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    params = {'barris': result}
    return render(request, 'wifi.html', params)
"""
def home_page(request):
   return render(request, 'wifi.html')

'''=========================Ver por Barris ==============================='''
def selectbarris(request):
    conn = psycopg2.connect(dbname="wifi_db", user="grupo5_user",password="patata")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    nom_barri = request.GET.get('get_barris', default='%')
    print(nom_barri)
    cursor.execute('SELECT wifi.equipament, adreca, telefon FROM wifi, barris'
                   f' WHERE  barri=idBarri and idbarri=(SELECT idbarri FROM barris WHERE nom_barri=%s);',(nom_barri,))
    result = cursor.fetchall()
    cursor.execute(f"SELECT nom_barri FROM barris;")
    resultodos = cursor.fetchall()

    params = {
        'dadesBarri':result,
        'todosbarri':resultodos,
    }
    cursor.close()
    conn.close()
    # print (result)

    return render(request, 'dadesperbarris.html', params)