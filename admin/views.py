from re import sub
from unicodedata import category
from django.shortcuts import render,redirect
from users.views import connect
from django.contrib import messages
from django.contrib.auth.models import Group, User
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
# Create your views here.

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response

def get_statistics_util(request, mobile):

    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return redirect("/login")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    
    state = "%"
    city = "%"
    region = "%"
    start_date = datetime.now() + relativedelta(months=-3)
    end_date = start_date
    
    if request.method == "POST":
        if request.POST.get('state') != "":
            state = request.POST.get('state')
        if request.POST.get('city') != "":
            city = request.POST['city']
        if request.POST.get('region') != "":
            region = request.POST['region']
        if request.POST.get('UnresolvedOnly'):
            end_date = datetime.now()
        
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
            start_date = datetime.now() + relativedelta(years=-100)

    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT * 
        FROM my_db."authority"
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
        WHERE resolve_authority_number = '{mobile}' and state LIKE '{state}' and city LIKE '{city}' and region LIKE '{region}' and start_time > '{start_date}' and end_time > '{end_date}'
    ''')

    colnames = [desc[0] for desc in c.description]

    complains = c.fetchall()
    complains = [dict(zip(colnames, complain)) for complain in complains]
    complains = json.dumps(complains, indent=4, sort_keys=True, default=str)

    conn.close()
    
    return render(request, "admin_page.html", {"authority":authority, "complains": complains})

def get_statistics(request):

    # auth_logout(request)
    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return redirect("/login")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    
    state = "%"
    city = "%"
    region = "%"
    position = "%"

    if request.method == "POST":
        if request.POST.get('state') != "":
            state = request.POST.get('state')
        if request.POST.get('city') != "":
            city = request.POST['city']
        if request.POST.get('region') != "":
            region = request.POST['region']
        if request.POST.get('position') != "":
            position = "%" + request.POST['position'] + "%"
        
        conn = connect()
        c = conn.cursor()

        c.execute(f'''
            SELECT * 
            FROM my_db."authority"
            where lower(region) like '{region.lower()}' and lower(city) like '{city.lower()}' and lower(state) like '{state.lower()}' and lower(position) like '{position}'
        ''')

        colnames = [desc[0] for desc in c.description]

        authorities = c.fetchall()

        if authorities is None:
            conn.close()
            messages.error(request, 'No user with given filter')
            return render(request, "admin_page.html")

        authorities = [dict(zip(colnames, authority)) for authority in authorities]
        
        conn.close()

        return render(request, "admin_page.html", {"authorities" : authorities})

    return render(request, "admin_page.html")

def add_authority(request):

    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return redirect("/login")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    
    conn = connect()
    c = conn.cursor()

    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        department = request.POST.get('department')
        region = request.POST.get('region')
        city = request.POST.get('city')
        state = request.POST.get('state')
        position = request.POST.get('position')
        password = request.POST.get('password')

        
        c.execute(f'''
            DELETE from
            my_db.authority
            where mobile_number = '{mobile}'
        ''')

        c.execute(f'''
            INSERT INTO my_db."authority"(
                name, mobile_number, department, region, city, state, password, position,chat_id)
                VALUES ('{name}', '{mobile}', '{department}', '{region}', '{city}', '{state}', '{password}', '{position}', '123456789');
        ''')

    c.execute(f'''
        select category
        from my_db.categories
    ''')

    categories = c.fetchall()
    categories = [t[0] for t in categories]

    conn.commit()
    conn.close()
            
    return render(request, "add_authority.html", {"categories": categories})

def edit_authority(request):

    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return redirect("/login")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    
    state = "%"
    city = "%"
    region = "%"
    position = "%"

    conn = connect()
    c = conn.cursor()

    if request.method == "POST":
        if request.POST.get('state') != "":
            state = request.POST.get('state')
        if request.POST.get('city') != "":
            city = request.POST['city']
        if request.POST.get('region') != "":
            region = request.POST['region']
        if request.POST.get('position') != "":
            position = "%" + request.POST['position'] + "%"
        
        c.execute(f'''
            SELECT * 
            FROM my_db."authority"
            where lower(region) like '{region.lower()}' and lower(city) like '{city.lower()}' and lower(state) like '{state.lower()}' and lower(position) like '{position}'
        ''')

        colnames = [desc[0] for desc in c.description]

        authorities = c.fetchall()

        if authorities is None:
            conn.close()
            messages.error(request, 'No user with given filter')
            return redirect("/admin/edit_authority")

        authorities = [dict(zip(colnames, authority)) for authority in authorities]
        
        conn.close()
        
        return render(request, "add_authority.html", {"edit":1, "authorities": authorities})

    c.execute(f'''
        select category
        from my_db.categories
    ''')

    categories = c.fetchall()
    categories = [t[0] for t in categories]
    conn.close()
    
    return render(request, "add_authority.html", {"edit":1, "categories": categories})

def edit_authority_util(request, mobile):
    
    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return redirect("/login")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    
    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT * 
        FROM my_db."authority"
        where mobile_number = '{mobile}'
    ''')

    colnames = [desc[0] for desc in c.description]

    authority = c.fetchone()

    if authority is None:
        conn.close()
        messages.error(request, 'No user with given username')
        return render(request, "admin_page.html")

    authority = dict(zip(colnames, authority))
    
    if request.method == "POST":
        conn.close()
        submit = request.metho.get('submit')
        if submit == "add_authority":
            return redirect("/admin/add_authority")

    c.execute(f'''
        select category
        from my_db.categories
    ''')

    categories = c.fetchall()
    categories = [t[0] for t in categories]
    
    conn.close()
    
    return render(request, "add_authority.html", {"authority": authority, "editing":1, "categories":categories})

def manage_category(request):
    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return redirect("/login")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    
    state = "%"
    city = "%"
    region = "%"
    position = "%"

    if request.method == "POST":
        if request.POST.get('state') != "":
            state = request.POST.get('state')
        if request.POST.get('city') != "":
            city = request.POST['city']
        if request.POST.get('region') != "":
            region = request.POST['region']
        if request.POST.get('position') != "":
            position = "%" + request.POST['position'] + "%"
        
        conn = connect()
        c = conn.cursor()

        c.execute(f'''
            SELECT * 
            FROM my_db."authority"
            where lower(region) like '{region.lower()}' and lower(city) like '{city.lower()}' and lower(state) like '{state.lower()}' and lower(position) like '{position}'
        ''')

        colnames = [desc[0] for desc in c.description]

        authorities = c.fetchall()

        if authorities is None:
            conn.close()
            messages.error(request, 'No user with given filter')
            return render(request, "admin_page.html")

        authorities = [dict(zip(colnames, authority)) for authority in authorities]
        
        conn.close()
        
        return render(request, "manage_category.html", {"authorities": authorities})

    return render(request, "manage_category.html")
        

def manage_category_util(request, mobile):

    if request.user.is_authenticated == False:
        messages.error(request, 'Login to proceed further')
        return redirect("/login")

    if not User.objects.get(username=request.user.username).groups.all().filter(name='admin'):
        return handler404(request)
    
    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT * 
        FROM my_db."authority"
        where mobile_number = '{mobile}'
    ''')

    colnames = [desc[0] for desc in c.description]

    authority = c.fetchone()

    if authority is None:
        conn.close()
        messages.error(request, 'No user with given username')
        return render(request, "admin_page.html")

    authority = dict(zip(colnames, authority))
    
    if request.method == "POST":
        category = request.POST.get('category')
        submit = request.POST['submit']
        
        c.execute(f'''
            select *
            from my_db."authority"
            where mobile_number = '{mobile}'
        ''')

        colnames = [desc[0] for desc in c.description]
        user = c.fetchone()
        user = dict(zip(colnames, user))
        
        if user is None:
            messages.error(request, "No user with given id")
        else:
            
            if submit == "Add to the Department":
                if category == user['department']:
                    messages.error(request, "Given user is already in the category " + user['department'])
                else:
                    c.execute(f'''
                        UPDATE my_db."authority"
                        SET department = '{category}'
                        where mobile_number = '{mobile}'
                    ''')
                    messages.success(request, "Authority added to the department")
            
            else:
                c.execute(f'''
                    UPDATE my_db."authority"
                    SET department = 'Not assigned'
                    where mobile_number = '{mobile}'
                ''')
                messages.success(request, "Authority removed from department")


    # c.execute(f'''
    #     select distinct department
    #     from my_db.complains
    # ''')

    c.execute(f'''
        select category
        from my_db.categories
    ''')

    categories = c.fetchall()
    categories = [t[0] for t in categories]
    
    c.execute(f'''
        select *
        from my_db."authority"
        where mobile_number = '{mobile}'
    ''')

    colnames = [desc[0] for desc in c.description]
    user = c.fetchone()
    user = dict(zip(colnames, user))
    
    conn.commit()
    conn.close()

    return render(request, "manage_category.html", {"authority": user, "categories": categories})