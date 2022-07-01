from unicodedata import category
from django.shortcuts import render,redirect
from users.views import connect
from django.contrib import messages
from django.contrib.auth.models import Group, User
import json
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
# Create your views here.

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response

def get_statistics(request):

    # auth_logout(request)
    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return render(request, "login.html")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    
    if request.method == "POST":
        mobile = request.POST.get('mobile')

        conn = connect()
        c = conn.cursor()

        c.execute(f'''
            SELECT * 
            FROM my_db."authority "
            where mobile_number = '{mobile}'
        ''')

        colnames = [desc[0] for desc in c.description]

        authority = c.fetchone()

        if authority is None:
            conn.close()
            messages.error(request, 'No user with given username')
            return render(request, "admin_page.html")

        authority = dict(zip(colnames, authority))
        
        c.execute(f'''
            SELECT *
            FROM my_db.complains
            where resolve_authority_number = '{mobile}'
        ''')

        colnames = [desc[0] for desc in c.description]

        complains = c.fetchall()
        complains = [dict(zip(colnames, complain)) for complain in complains]
        complains = json.dumps(complains, indent=4, sort_keys=True, default=str)

        conn.close()
        
        return render(request, "admin_page.html", {"authority":authority, "complains": complains})

    return render(request, "admin_page.html")

def add_authority(request):

    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return render(request, "login.html")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        department = request.POST.get('department')
        region = request.POST.get('region')
        city = request.POST.get('city')
        state = request.POST.get('state')
        password = request.POST.get('password')

        conn = connect()
        c = conn.cursor()

        c.execute(f'''
            INSERT INTO my_db."authority "(
                name, mobile_number, department, region, city, state, password)
                VALUES ('{name}', '{mobile}', '{department}', '{region}', '{city}', '{state}', '{password}');
        ''')

        conn.commit()
        conn.close()
            
    return render(request, "add_authority.html")

def manage_category(request):

    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return render(request, "login.html")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    

    if request.method == "POST":
        mobile = request.POST['mobile']
        category = request.POST['category']
        submit = request.POST['submit']
        print(mobile, category, submit)

        conn = connect()
        c = conn.cursor()

        c.execute(f'''
            select *
            from my_db."authority "
            where mobile_number = '{mobile}'
        ''')

        colnames = [desc[0] for desc in c.description]
        user = c.fetchone()
        
        if user is None:
            messages.error(request, "No user with given id")
        else:
            user = dict(zip(colnames, user))

            if submit == "Add to the Category":
                if category == user['department']:
                    messages.error(request, "Given user is already in the category " + user['department'])
                else:
                    c.execute(f'''
                        UPDATE my_db."authority "
                        SET department = '{category}'
                        where mobile_number = '{mobile}'
                    ''')
                    messages.success(request, "Authority added to the department")
            
            else:
                if category != user['department']:
                    messages.error(request, "Given user is in the given category " +user['department'])
                else:
                    c.execute(f'''
                        UPDATE my_db."authority "
                        SET department = 'Not assigned'
                        where mobile_number = '{mobile}'
                    ''')
                    messages.success(request, "Authority removed from department")

        conn.commit()
        conn.close()

    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        select distinct department
        from my_db.complains
    ''')

    categories = c.fetchall()
    categories = [t[0] for t in categories]

    conn.close()

    return render(request, "manage_category.html", {"categories": categories})