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

def read_file(file_name):
    with open(file_name, 'r') as load_f:
        json_data = json.load(load_f)
    return json_data

def get_keys(json_data, conn, tb_raw_entities):
    keys_header = list(set(json_data["header"].keys()))
    keys_tables = list(set(json_data["tables"].keys()))
    keys_blocks = list(set(json_data["blocks"].keys()))

    entities = json_data["entities"]
    key_list_buf = []
    for row in entities:
        keys_tmp = row.keys()
        for key in keys_tmp:
            key_list_buf.append(key)
    keys_entities_dxf = list(set(key_list_buf))
    
    sql_query = "select column_name from information_schema.columns where table_name='%s'"
    cursor = conn.cursor()
    cursor.execute(sql_query % (tb_raw_entities))
    rows = cursor.fetchall()
    keys_entities_db = []
    for row in rows:
        key = row[0]
        if "sn" == key or "project_id" == key or "file_id" == key:
            continue
        else:
            keys_entities_db.append(key)
    cursor.close()

    keys_entities = []
    for key in keys_entities_dxf:
        if key in keys_entities_db:
            keys_entities.append(key)
        else:
            print("\n Warning: This key is not exist in DB:", tb_raw_entities, ", key:", key)

    keys_header.sort()
    keys_tables.sort()
    keys_blocks.sort()
    keys_entities.sort()
    return keys_header, keys_tables, keys_blocks, keys_entities

def save_header(conn, tb_name, json_data, keys_header, project_id, file_id):
    header = json_data["header"]
    cursor = conn.cursor()
    sql_insert = "INSERT INTO %s (project_id, file_id, key, value) VALUES('%s', '%s', '%s', '%s')"
    for key in keys_header:
        value_str = str(header[key])
        value_str = value_str.replace("'", '"')
        cursor.execute(sql_insert % (tb_name, project_id, file_id, key, value_str))
    conn.commit()
    cursor.close()

def save_tables(conn, tb_name, json_data, keys, project_id, file_id):
    json_data_sub = json_data["tables"]
    sql_insert = "INSERT INTO %s (project_id, file_id, viewPort, lineType, layer) VALUES('%s', '%s', '%s', '%s', '%s')"
    
    viewPort = str(json_data_sub["viewPort"])
    viewPort = viewPort.replace("'", '"')
    viewPort = viewPort.replace(": True", ": true")
    viewPort = viewPort.replace(": False", ": false")

    lineType = str(json_data_sub["lineType"])
    lineType = lineType.replace("'", '"')
    lineType = lineType.replace(": True", ": true")
    lineType = lineType.replace(": False", ": false")
    
    layer = str(json_data_sub["layer"])
    layer = layer.replace("'", '"')
    layer = layer.replace(": True", ": true")
    layer = layer.replace(": False", ": false")
    
    cursor = conn.cursor()
    cursor.execute(sql_insert % (tb_name, project_id, file_id, viewPort, lineType, layer))
    conn.commit()
    cursor.close()

def save_blocks(conn, tb_name, json_data, keys, project_id, file_id):
    json_data_sub = json_data["blocks"]
    cursor = conn.cursor()
    sql_insert = "INSERT INTO %s (project_id, file_id, key, value) VALUES('%s', '%s', '%s', '%s')"
    for key in keys:
        value_str = str(json_data_sub[key])
        value_str = value_str.replace("'", '"')
        value_str = value_str.replace(": True", ": true")
        value_str = value_str.replace(": False", ": false")
        cursor.execute(sql_insert % (tb_name, project_id, file_id, key, value_str))
    conn.commit()
    cursor.close()

def save_entities(conn, tb_name, json_data, keys, project_id, file_id):
    sql_head = 'INSERT INTO ' + tb_name + ' ("project_id", "file_id", '
    for key in keys:
        key = '"' + key + '", '
        sql_head += key
    sql_head = sql_head[:-2]
    sql_head += ') '
    
    entities = json_data["entities"]
    cursor = conn.cursor()
    for row in entities:
        sql_insert = ""
        values = " VALUES('" + project_id + "', '" + file_id + "', "
        for key in keys:
            if key in row:
                val = str(row[key])
                if -1 != val.find("{"):
                    val = val.replace("'", '"')  # process json string for saving into postgreSQL.
            else:
                val = "{}"
            values += "'" + val + "',"
        values = values[:-1]
        values += ")"
        sql_insert = sql_head + values
        cursor.execute(sql_insert)
    conn.commit()
    cursor.close()
    
def json_2_db(project_id, file_id, file_name):
    print("\n", time.asctime( time.localtime(time.time())), file_name)
    tb_raw_header = "tb_raw_header"
    tb_raw_tables = "tb_raw_tables"
    tb_raw_blocks = "tb_raw_blocks"
    tb_raw_entities = "tb_raw_entities"
    
    json_data = read_file(file_name)
    conn = init_db()
    keys_header, keys_tables, keys_blocks, keys_entities = get_keys(json_data, conn, tb_raw_entities)
    save_header(conn, tb_raw_header, json_data, keys_header, project_id, file_id)
    save_tables(conn, tb_raw_tables, json_data, keys_tables, project_id, file_id)
    save_blocks(conn, tb_raw_blocks, json_data, keys_blocks, project_id, file_id)
    save_entities(conn, tb_raw_entities, json_data, keys_entities, project_id, file_id)
    conn.close()
    print(" ", time.asctime( time.localtime(time.time())))

def test():
    project_id = "p2"
    file_id = "f2"    
    file_name = "./json/p007_42.json"
    json_2_db(project_id, file_id, file_name)

    project_id = "p2"
    file_id = "f3"    
    file_name = "./json/p007_43.json"
    json_2_db(project_id, file_id, file_name)

    project_id = "p2"
    file_id = "f4"    
    file_name = "./json/p007_44.json"
    json_2_db(project_id, file_id, file_name)
    
    project_id = "p2"
    file_id = "f5"    
    file_name = "./json/p007_45.json"
    json_2_db(project_id, file_id, file_name)
    
def main():
    for i in range(0, 500):
        test()
    print("finished")
    
if __name__ == "__main__":
    main()
    