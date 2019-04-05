import urllib.request, json

def llista_platjes(latitude, longitude):
    print("http://meteoapi.systemadmin.es/platges/geosearch/"+str(longitude)+"/"+str(latitude))
    with urllib.request.urlopen("http://meteoapi.systemadmin.es/platges/geosearch/"+str(longitude)+"/"+str(latitude)) as url:
        data = json.loads(url.read().decode())
        return str(data)
