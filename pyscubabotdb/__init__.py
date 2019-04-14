# -*- coding: utf-8 -*-
import MySQLdb

scubabotdb_user=''
scubabotdb_password=''
scubabotdb_db=''
scubabotdb_host='localhost'

def setup(user,password,db,host='localhost'):
    global scubabotdb_user,scubabotdb_password, scubabotdb_db, scubabotdb_host
    scubabotdb_user=user
    scubabotdb_password=password
    scubabotdb_db=db
    scubabotdb_host=host

def runDBquery(db_query):
    global scubabotdb_user,scubabotdb_password, scubabotdb_db, scubabotdb_host
    try:
        db = MySQLdb.connect(host=scubabotdb_host,
                             user=scubabotdb_user,
                             passwd=scubabotdb_password,
                             db=scubabotdb_db)
        cur = db.cursor()

        cur.execute(db_query)

        db.commit()

        cur.close()
        db.close()

        return True
    except:
        return False

def setUserPlatja(user_id,platja_id):
    db_query = """
            INSERT INTO bussejadors (telegram_id, platja_id) VALUES ({user_id},{platja_id})
                ON DUPLICATE KEY UPDATE platja_id={platja_id};
       """.format(user_id=user_id,platja_id=platja_id)
    return runDBquery(db_query)
