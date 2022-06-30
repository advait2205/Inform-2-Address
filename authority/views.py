from django.shortcuts import render
from users.views import connect
import json

# Create your views here.

def login(request):
    return render(request, "authority_login.html")

def assigned_complains(request):
    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT *
        FROM my_db.complains
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
