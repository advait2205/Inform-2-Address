from email import message
from tracemalloc import start
from django.contrib import messages
from operator import mod
import re
from django.shortcuts import render, HttpResponse,redirect
from decouple import config
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import Group, User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
import psycopg2
import json
from users.send_message_telegram_group import send_message

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response

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
    
def logout(request):
    if request.user.is_authenticated == True:
        auth_logout(request)
        messages.success(request, "Good bye ! You are logged out now")

    return redirect("/login")

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
                FROM my_db."authority"
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
        
        print(request.GET.get('next'))

        conn.close()
        
        if user is not None:
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

            if user.is_active:
                auth_login(request, user)
                return redirect(next)
            else:
                messages.error(request, "User logged out, please login again")
                return render(request, "login.html")
        
        else:

            messages.error(request, "Invalid credentials")
            return render(request, "login.html")

    return render(request, "user_home.html")


def categorywise_complaints(request, category):

    state = "%"
    city = "%"
    region = "%"
    user_mobile_number = "%"
    start_date = datetime.now() + relativedelta(months=-3)
    filtered = False

    if request.method == "POST":
        filtered = True
        if request.POST.get('state') != "":
            state = request.POST.get('state')
        if request.POST.get('city') != "":
            city = request.POST['city']
        if request.POST.get('region') != "":
            region = request.POST['region']
        if request.POST.get('myOnly'):
           user_mobile_number = request.user.username
        
        time = request.POST['time']

        if time == "1week":
            start_date = datetime.now() + relativedelta(days=-7)
        elif time == "15days":
            start_date = datetime.now() + relativedelta(days=-15)
        elif time == "1month":
            start_date = datetime.now() + relativedelta(months=-1)
        elif time == "6months":
            start_date = datetime.now() + relativedelta(months=-6)
        elif time == "1year":
            start_date = datetime.now() + relativedelta(years=-1)
        elif time == "showall":
            start_date = datetime.now() + relativedelta(years=-1)
        
    print(state, city, region, user_mobile_number, start_date)
    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT *
        FROM my_db.complains
        WHERE lower(department) = lower('{category}') and state LIKE '{state}' and city LIKE '{city}' and region LIKE '{region}' and user_mobile_number LIKE '{user_mobile_number}' and start_time > '{start_date}'
    ''')
    
    colnames = [desc[0] for desc in c.description]

    complains = c.fetchall()
    complains = [dict(zip(colnames, complain)) for complain in complains]
    
    empty = "There are no complains with given category"
    if complains.__len__() != 0:
        empty = ""
    
    complains = json.dumps(complains, indent=4, sort_keys=True, default=str)
    conn.close()

    return render(request, "complains.html", {"complains" : complains, "empty" : empty, "filtered":filtered})

def add_complain(request, category):

    if request.user.is_authenticated == False:
        messages.error(request, 'Login first to file a complaint')
        return redirect("/login")
    
    if request.method == "POST":
        text = request.POST.get('details')
        user_mobile_number = request.POST.get('mobile')
        department = category
        region = request.POST.get('region')
        city = request.POST.get('city')
        state = request.POST.get('state')
        upvotes = 0

        # HAVE TO CHANGE THIS
        resolve_authority_number = "9687999393" 
        
        conn = connect()
        c = conn.cursor()

        # c.execute(f'''
        #     INSERT INTO my_db.complains(
        #         text, image_url, start_time, end_time, user_mobile_number, department, region, city, state, resolve_authority_number, upvotes)
        #         VALUES ('{text}', NULL, NOW(), NULL, '{user_mobile_number}', '{department}', '{region}', '{city}', '{state}', '{resolve_authority_number}', {upvotes});
        # ''')

        c.execute(f'''
            SELECT * 
            FROM my_db."authority"
            where mobile_number = '{resolve_authority_number}'
        ''')

        colnames = [desc[0] for desc in c.description]
        authority = c.fetchone()
        authority = dict(zip(colnames, authority))
            
        conn.commit()
        conn.close()

        send_message( authority["chat_id"] , "complaint title", text, "", region, city, resolve_authority_number)
        


    return render(request, "add_complain.html")

def upvote_complain(request, category, id):
    
    if request.user.is_authenticated == False:
        messages.error(request, "Login to upvote a complain")
        return redirect("/login")

    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        UPDATE my_db.complains
        SET upvotes = upvotes+1
        WHERE id = {id};
    ''')

    conn.commit()
    conn.close()

    path = request.path
    path = path[:path.rindex("/")]
    return redirect(path+"/complains")