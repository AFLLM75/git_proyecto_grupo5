from django.shortcuts import render
from django.http import HttpResponse
import psycopg2.extras
# Create your views here.
"""
def wifi(request):
    conn = psycopg2.connect(dbname="wifi_db",
                            user="grupo5_user",
                            password="patata")
    with open("debug.log", "a+") as debug_file:
    print("Funciona!", file=debug_file)
    return HttpResponse('Funciona!')
"""
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
    return render(request, 'VerCoordenadas.html', params)




def insert(request):
    conn = psycopg2.connect(dbname="wifi_db",
                            user="grupo5_user",
                            password="patata")
    cursor = conn.cursor()
    coordenada_x= request.POST["coordenada_x"]
    coordenada_y= request.POST["coordenada_y"]
    cursor.execute(f"INSERT INTO wifi VALUES (default,'{coordenada_x}','{coordenada_y}');")
    conn.commit()                                    
    cursor.close()
    conn.close()
    return HttpResponse("Insertado")


def prueba(request):
    conn = psycopg2.connect(dbname="wifi_db",
                            user="grupo5_user",
                            password="patata")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    iddistricte= request.GET.get('get_iddistricte', default='%')
    with open("debug.log", "w") as debug_file:
        print(f"SELECT * FROM barris WHERE idDistricte = '{iddistricte}';", file=debug_file)
    if iddistricte == 'Todas':
        iddistricte = '%'
    cursor.execute(F"SELECT * FROM barris WHERE idDistricte = '{iddistricte}';")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    params = {'barris': result}
    return render(request, 'wifi.html', params)

def home_page(request):
   return render(request,'wifi.html')