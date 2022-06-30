from django.shortcuts import render
from users.views import connect
import json
# Create your views here.

def get_statistics(request):

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

        print(complains)
        
        conn.close()
        
        return render(request, "admin_page.html", {"authority":authority, "complains": complains})

    return render(request, "admin_page.html")

def add_authority(request):
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