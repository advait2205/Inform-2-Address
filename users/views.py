from operator import mod
import re
from django.shortcuts import render, HttpResponse,redirect
from decouple import config
from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
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
    if request.method == "POST":
        mobile = request.POST.get('username')
        password = request.POST.get('password')

        conn = connect()
        c = conn.cursor()

        # Check for admin

        c.execute(f'''
            SELECT *
            FROM my_db.admin
            WHERE mobile_number = '{mobile}' and password = '{password}'
        ''')

        user = c.fetchone()
        groupName = "admin"
        next = "/admin/statistics"

        if user is None:
            # Check for authority

            c.execute(f'''
                SELECT *
                FROM my_db."authority "
                WHERE mobile_number = '{mobile}' and password = '{password}'
            ''')

            user = c.fetchone()
            groupName = "authority"
            next = "/authority/assigned_complains"

        if user is None:
            # Check for citizen

            c.execute(f'''
                SELECT *
                FROM my_db.user
                WHERE mobile_number = '{mobile}' and password = '{password}'
            ''')

            user = c.fetchone()
            groupName = "citizen"
            next = "/citizen/"

        if user is not None:
            conn.close()
            model_user = User.objects.filter(username=mobile)

            if model_user.count() == 0:
                model_user = User(username=mobile)
                model_user.set_password(password)
                model_user.save()
                Group.objects.get(name=groupName).user_set.add(model_user)
            else:
                model_user = model_user[0]
                model_user.set_password(password)
                model_user.save()
            
            user = authenticate(request, username=mobile, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect(next)
                else:
                    return render(request, "login.html", {"message": "User logged out, please login again"})
            else:
                return render(request, "login.html", {"message": "Invalid creentials"})
        
        else:
            print("Invalid user")
            return render(request, "login.html",{"message": "User not exist"})

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

