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
    cursor.execute("SELECT * FROM wifi;")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'wifi.html', params)