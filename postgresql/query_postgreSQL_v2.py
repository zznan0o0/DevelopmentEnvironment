import time
import json
import psycopg2

def db_conn(host_val, user_val, password_val, dbname_val):
    connect_info = "host='%s' dbname='%s' user='%s' password='%s'"
    db_conn = psycopg2.connect(connect_info %(host_val, dbname_val, user_val, password_val))
    return db_conn

def init_db():
    db_domain = "localhost"
    db_user = "dbuser"
    db_passwd = "dbuser"
    db_name = "exampledb"
    conn = db_conn(db_domain, db_user, db_passwd, db_name)
    return conn

def query_psql(conn, tb_name):
    sql_query = "select sn, vertices, vertices->0->>'x' as v1_x from %s where type='LINE' limit 5"
    cursor = conn.cursor()
    cursor.execute(sql_query %(tb_name))
    rows = cursor.fetchall()
    for row in rows:
        val_1 = row[0]
        val_2 = row[1]
        val_3 = row[2]
        print("\n", val_1, val_2, val_3)
        
        print("len(val_2):", len(val_2))
        vertices = val_2
        v1 = vertices[0]
        v2 = vertices[1]
        print(v1)
        print(v2)
        
        v1_x = v1['x']
        v1_y = v1["y"]
        print("v1_x:", v1_x)
        print("v1_y:", v1_y)
    cursor.close()
    
def main():
    tb_raw_entities = "tb_raw_entities"
    conn = init_db()
    query_psql(conn, tb_raw_entities)
    conn.close()
    print("finished")
    
if __name__ == "__main__":
    main()
    