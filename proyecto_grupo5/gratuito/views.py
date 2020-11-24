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
    cursor.execute("SELECT ETRS89_COORD_X , ETRS89_COORD_Y , LONGITUD , LATITUD FROM wifi;")
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


