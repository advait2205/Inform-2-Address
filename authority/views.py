from django.shortcuts import render
from users.views import connect

# Create your views here.

def login(request):
    return render(request, "authority_login.html")

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