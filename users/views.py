import re
from django.shortcuts import render, HttpResponse
from decouple import config
from datetime import datetime
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
def login(request):
    return render(request, "login.html")
    
def show_categories(request):
    return render(request, "user_home.html")

def categorywise_complaints(request, category):

    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT *
        FROM my_db.complains
        WHERE lower(department) = lower('{category}')
    ''')

    colnames = [desc[0] for desc in c.description]

    complains = c.fetchall()
    complains = [dict(zip(colnames, complain)) for complain in complains]

    complains = json.dumps(complains, indent=4, sort_keys=True, default=str)
    conn.close()

    empty = "There are no complains with given category"

    if complains.__len__() == 0:
        empty = ""

    return render(request, "complains.html", {"complains" : complains, "empty" : empty})

def add_complain(request, category):

    if request.method == "POST":
        text = request.POST.get('details')
        user_mobile_number = request.POST.get('mobile')
        department = category
        region = request.POST.get('region')
        city = request.POST.get('city')
        state = request.POST.get('state')
        upvotes = 0
        resolve_authority_number = "214-224-1501"
        
        conn = connect()
        c = conn.cursor()

        c.execute(f'''
            INSERT INTO my_db.complains(
                text, image_url, start_time, end_time, user_mobile_number, department, region, city, state, resolve_authority_number, upvotes)
                VALUES ('{text}', NULL, NOW(), NULL, '{user_mobile_number}', '{department}', '{region}', '{city}', '{state}', '{resolve_authority_number}', {upvotes});
        ''')

        conn.commit()
        conn.close()

    return render(request, "add_complain.html")