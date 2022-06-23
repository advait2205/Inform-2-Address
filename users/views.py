from django.shortcuts import render, HttpResponse
from decouple import config
import psycopg2
import json

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
    return render(request, "user_home.html")

def categorywise_complaints(request):
    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT *
        FROM my_db.complains
    ''')

    colnames = [desc[0] for desc in c.description]
    print(colnames)

    complains = c.fetchall()
    complains = [dict(zip(colnames, complain)) for complain in complains]
    print(complains)

    complains = json.dumps(complains, indent=4, sort_keys=True, default=str)
    conn.close()

    return render(request, "complains.html", {"complains" : complains})