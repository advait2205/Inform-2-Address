from django.shortcuts import render, HttpResponse
from decouple import config
import psycopg2

def connect():
    return psycopg2.connect(
            database=config('DB_NAME'), 
            user=config('DB_USER'), 
            password=config('DB_PASSWORD'), 
            host=config('HOST'), 
            port= config('PORT')
        )

# Create your views here.
def show_categories(request):
    return render(request, "index.html")

def categorywise_complaints(request):
    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT *
        FROM my_db.complains
    ''')

    
    complains = c.fetchall()
    conn.close()

    return render(request, "category.html", {"complains" : complains})