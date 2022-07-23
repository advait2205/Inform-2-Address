from django.shortcuts import render,redirect
from users.views import connect
from django.contrib import messages
from django.contrib.auth.models import Group, User
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

# Create your views here.
from django.template import RequestContext


def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response

def assigned_complains(request):

    if request.user.is_authenticated == False:
        messages.error(request, 'Login first to view assigned complaints')
        return redirect("/login")

    if not User.objects.get(username=request.user.username).groups.all().filter(name__in=['admin', 'authority']):
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
        FROM my_db.complains
        WHERE resolve_authority_number = '{request.user.username}' and state LIKE '{state}' and city LIKE '{city}' and region LIKE '{region}' and start_time > '{start_date}' and end_time > '{end_date}' 
    ''')
    
    colnames = [desc[0] for desc in c.description]

    complains = c.fetchall()
    complains = [dict(zip(colnames, complain)) for complain in complains]
    
    empty = "There are no complains assigned to you"
    if complains.__len__() != 0:
        empty = ""
    
    complains = json.dumps(complains, indent=4, sort_keys=True, default=str)
    conn.close()

    return render(request, "authority_complains.html", {"complains" : complains, "empty" : empty})
