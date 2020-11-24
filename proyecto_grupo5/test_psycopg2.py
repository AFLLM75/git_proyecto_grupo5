import psycopg2
conn = psycopg2.connect(dbname="wifi_db", user="grupo5_user", password="patata")
print("Funciona!")