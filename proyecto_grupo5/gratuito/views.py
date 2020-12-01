from django.shortcuts import render
from django.http import HttpResponse
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
    cursor.execute(f"SELECT * FROM wifi WHERE equipament LIKE '{equipament}';")
    result = cursor.fetchall()
    cursor.execute(f"SELECT equipament FROM wifi;")
    resultall = cursor.fetchall()
    params = {
        'wifi':result,
        'equipamentall':resultall,
    }
    cursor.close()
    conn.close()
    crear_mapa()
    return render(request, 'testvercoordenadas.html', params)

def crear_mapa():
    import gmplot
    # Create the map plotter:
    apikey = ''  # (your API key here)
    gmap = gmplot.GoogleMapPlotter(41.38714, 2.17006, 13, apikey=apikey)

    # Mark a hidden gem:
    gmap.marker(41.38714, 2.17006, color='cornflowerblue')
    gmap.draw('gratuito/templates/map.html')
    with open('gratuito/templates/map.html', 'r') as fichero_entrada, \
            open('gratuito/templates/map_modificado.html', 'w') as fichero_salida:

        i = 0
        for linea in fichero_entrada:
            if i == 28:
                print('{% block buscar_coordenadas %}', file=fichero_salida)
                print('{% endblock %}', file=fichero_salida)
            print(linea, file=fichero_salida, end='')
            i = i + 1




    # abrir mapa y modificar map.html en el body antes del  añadir
def prueba(request):
    conn = psycopg2.connect(dbname="wifi_db", user="grupo5_user",password="patata")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    nom_barris = request.GET.get('get_nom_barri', default='%')
    cursor.execute(f"SELECT * FROM barris WHERE nom_barri LIKE '{nom_barris}';")
    result = cursor.fetchall()
    cursor.execute(f"SELECT nom_barri FROM barris ORDER BY nom_barri ASC;")
    resultall = cursor.fetchall()
    cursor.execute(f"SELECT idbarri FROM barris;")
    resulbarri = cursor.fetchall()
    params = {
        'nom_barris':result,
        'barrisall':resultall,
        'resulbarri':resulbarri,
            }
    cursor.close()
    conn.close()
    return render(request, 'formWifi.html', params)

def insert(request):
    print('insertando ando')
    conn = psycopg2.connect(dbname="wifi_db",
                            user="grupo5_user",
                            password="patata")
    cursor = conn.cursor()
    coordenada_x= request.POST["etrs89_coord_x"]
    coordenada_y = request.POST["etrs89_coord_y"]
    longitud= request.POST["longitud"]
    latitud = request.POST["latitud"]
    equipament = request.POST["equipament"]
    barri = request.POST["resulbarri"]
    adreca = request.POST["adreca"]
    telefon = request.POST["telefon"]
    cursor.execute(f"INSERT INTO wifi VALUES (default,'{coordenada_x}','{coordenada_y}','{longitud}','{latitud}','{equipament}','{barri}','{adreca}','{telefon}');")
    conn.commit()                                    
    cursor.close()
    conn.close()
    return render(request, 'formWifi.html')
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
