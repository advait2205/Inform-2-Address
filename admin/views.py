from django.shortcuts import render
from users.views import connect
import json
# Create your views here.

def get_statistics(request):
    conn = connect()
    c = conn.cursor()

    c.execute(f'''
        SELECT * FROM my_db."authority "
    ''')

    colnames = [desc[0] for desc in c.description]

    authorities = c.fetchall()
    authorities = [dict(zip(colnames, authority)) for authority in authorities]
    authorities = json.dumps(authorities, indent=4, sort_keys=True, default=str)
    
    conn.close()
    
    return render(request, "admin_page.html", {"authorities": authorities})

