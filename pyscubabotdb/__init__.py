# -*- coding: utf-8 -*-
import MySQLdb

scubabotdb_user=''
scubabotdb_password=''
scubabotdb_db=''

def setup(user,password,db):
    global scubabotdb_user,scubabotdb_password, scubabotdb_db
    scubabotdb_user=user
    scubabotdb_password=password
    scubabotdb_db=db

def setUserPlatja(user_id,platja_id):
    try:
        db_query = """
                INSERT INTO bussejadors (telegram_id, platja_id) VALUES ({user_id},{platja_id})
                    ON DUPLICATE KEY UPDATE platja_id={platja_id};
           """.format(user_id=user_id,platja_id=platja_id)
        db = MySQLdb.connect(host="localhost",
                             user=scubabotdb_user,
                             passwd=scubabotdb_password,
                             db=scubabotdb_db)
        cur = db.cursor()

        #print(db_query)
        cur.execute(db_query)

        db.commit()

        cur.close()
        db.close()

        return True
    except:
        return False
