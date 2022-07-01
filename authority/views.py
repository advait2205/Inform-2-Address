from django.shortcuts import render
from users.views import connect
from django.contrib import messages
from django.contrib.auth.models import Group, User
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
        return render(request, "login.html")

    if not User.objects.get(username=request.user.username).groups.all().filter(name__in=['admin', 'authority']):
        return handler404(request)
        
    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT *
        FROM my_db.complains        
        where resolve_authority_number = '{request.user.username}'
    ''')

    colnames = [desc[0] for desc in c.description]

    complains = c.fetchall()
    complains = [dict(zip(colnames, complain)) for complain in complains]

    complains = json.dumps(complains, indent=4, sort_keys=True, default=str)
    conn.close()

    empty = "There are no complains with given category"

    if complains.__len__() == 0:
        empty = ""

    return render(request, "authority_complains.html", {"complains": complains})
