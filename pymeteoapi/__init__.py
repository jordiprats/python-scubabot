# -*- coding: utf-8 -*-
import MySQLdb

meteoapi_user=''
meteoapi_password=''
meteoapi_db=''

def setup(user,password,db):
    global meteoapi_user,meteoapi_password, meteoapi_db
    meteoapi_user=user
    meteoapi_password=password
    meteoapi_db=db

# per previsio - últims 24*dies

def platja_id_to_descripcio(id):
    global meteoapi_user,meteoapi_password, meteoapi_db
    db_query = """
            SELECT CONCAT(municipis.nom,', Platja ',platges.nom) as descripcio FROM platges JOIN municipis ON platges.municipi_id=municipis.id WHERE platges.id={id}
       """.format(id=id)
    db = MySQLdb.connect(host="localhost",
                         user=meteoapi_user,
                         passwd=meteoapi_password,
                         db=meteoapi_db)
    cur = db.cursor()

    print(db_query)
    cur.execute(db_query)

    platges=[]
    row = cur.fetchone()

    cur.close()
    db.close()

    return row[0]

def platja_slug_to_platja_id(slug):
    global meteoapi_user,meteoapi_password, meteoapi_db
    db_query = """
            SELECT id FROM platges WHERE slug='{slug}'
       """.format(slug=slug)
    db = MySQLdb.connect(host="localhost",
                         user=meteoapi_user,
                         passwd=meteoapi_password,
                         db=meteoapi_db)
    cur = db.cursor()

    print(db_query)
    cur.execute(db_query)

    platges=[]
    row = cur.fetchone()

    cur.close()
    db.close()

    return row[0]

def llista_platjes(latitude, longitude, limit=4, distancia=15):
    global meteoapi_user,meteoapi_password, meteoapi_db
    # $platges_raw = DB::table('platges')
    #   ->select(DB::raw('*, 6371 * acos (
    #     cos ( radians('.$latitude.') )
    #   * cos( radians( platges.latitude ) )
    #   * cos( radians( platges.longitude ) - radians('.$longitude.') )
    #   + sin ( radians('.$latitude.') )
    #   * sin( radians( platges.latitude ) )
    #   ) as distance'))
    #   ->havingRaw('distance < ?', [15])
    #   ->orderByRaw('distance')
    #   ->take($limit)
    #   ->get();
    db_query = """
        SELECT
            CONCAT(municipis.nom,', Platja ',platges.nom) as descripcio,
            platges.slug,
            6371 * acos (
             cos ( radians({latitude}) )
           * cos( radians( platges.latitude ) )
           * cos( radians( platges.longitude ) - radians({longitude}) )
           + sin ( radians({latitude}) )
           * sin( radians( platges.latitude ) )
           ) as distance
       FROM platges JOIN municipis ON platges.municipi_id=municipis.id
       GROUP BY descripcio, platges.slug, distance
       HAVING distance < {distancia}
       ORDER BY distance
       LIMIT {limit}
       """.format(longitude=longitude, latitude=latitude, limit=limit, distancia=distancia)
    db = MySQLdb.connect(host="localhost",
                         user=meteoapi_user,
                         passwd=meteoapi_password,
                         db=meteoapi_db)
    cur = db.cursor()

    print(db_query)
    cur.execute(db_query)

    platges=[]
    for row in cur.fetchall():
        platja={}
        platja['nom']=row[0]
        platja['slug']=row[1]
        platja['distancia']=row[2]
        platges.append(platja)

    cur.close()
    db.close()
    return platges
