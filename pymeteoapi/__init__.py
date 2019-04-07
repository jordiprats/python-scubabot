import MySQLdb

meteoapi_user=''
meteoapi_password=''
meteoapi_db=''

def setup(user,password,db):
    global meteoapi_user,meteoapi_password, meteoapi_db
    meteoapi_user=user
    meteoapi_password=password
    meteoapi_db=db

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
        SELECT nom, slug, 6371 * acos (
             cos ( radians({latitude}) )
           * cos( radians( platges.latitude ) )
           * cos( radians( platges.longitude ) - radians({longitude}) )
           + sin ( radians({latitude}) )
           * sin( radians( platges.latitude ) )
           ) as distance
       FROM platges
       GROUP BY nom, slug, distance
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

    for row in cur.fetchall() :
        print(row[0], " ", row[2])
    return db_query
