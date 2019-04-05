import urllib.request, json

def llista_platjes(latitude, longitude):
    query_url = "http://meteoapi.systemadmin.es/platges/geosearch/"+str(latitude)+"/"+str(longitude)
    print(query_url)
    with urllib.request.urlopen(query_url) as url:
        data = json.loads(url.read().decode())
        return str(data)
