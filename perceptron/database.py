import os
import sqlite3 as sql


def create_db(db_name, destroy_existing=True):
    """
    @description: Try and create a sqlite3 db if it does not exist
    @args:
        - db_name: the name of the database file without the .db extension
        - destroy_existing (bool) - if True, and the file exists, it will destroy and create the db again. Otherwise returns false
    """
    db_name = db_name + ".db"
    if os.path.isfile(db_name):
        if destroy_existing:
            destroy_db(db_name)
        else:
            return False  # DB exists. Cannot create the db

    c = sql.connect(db_name)
    c.close()
    return True


def destroy_db(db_name):
    """
    @description: Destroy a given .db file
    """
    db = db_name + ".db"
    os.remove(db)
    return True


def get_db_connection(db_name):
    """
    @description: Get a db connection object
    """

    try:
        conn = sql.connect(db_name + '.db')
        conn.row_factory = sql.Row
        return conn
    except:
        return False


def create_tables(db_name, classes, features, iterations):
    conn = get_db_connection(db_name)
    if not conn:
        return False

    # Create the iteration table
    sql = """CREATE TABLE perceptron_details(
                id INTEGER PRIMARY KEY,
                iterations INT
        );"""
    conn.execute(sql)
    conn.commit()

    # Insert details into table
    sql = "INSERT INTO perceptron_details (iterations) VALUES (?);"
    args = (iterations, )

    conn.execute(sql, args)
    conn.commit()

    # Create the class table
    sql = """CREATE TABLE classes(
                id INTEGER PRIMARY KEY,
                class TEXT
        );"""
    conn.execute(sql)
    conn.commit()

    # Insert into classes table
    for klass in classes:
        sql = "INSERT INTO classes (class) VALUES (?)"
        args = (klass, )
        conn.execute(sql, args)
        conn.commit()

    # Create features table
    sql = """CREATE table features(
                id INTEGER PRIMARY KEY,
                feature TEXT
        );"""
    conn.execute(sql)
    conn.commit()

    # Insert features
    for feature in features:
        sql = "INSERT INTO features (feature) VALUES (?)"
        args = (feature, )
        conn.execute(sql, args)
        conn.commit()

    # Create training data table
    sql = """CREATE TABLE training_datas(
                id INTEGER PRIMARY KEY,
                class INT
        """

    feature_sql = ""
    for feature in features:
        feature_sql += ", %s REAL" % feature

    sql += feature_sql + ");"
    conn.execute(sql)
    conn.commit()

    # Create the weights table
    sql = "CREATE TABLE weights(\
                id INTEGER PRIMARY KEY,\
                class_id INTEGER\
                %s);" % feature_sql
    conn.execute(sql)
    conn.commit()

    # Insert temporary weights into table
    #i = 0
    #for klass in classes:
    #    i += 1
    #    sql = "INSERT INTO weights (class_id, weight) VALUES (%d, 0.0)" % i
    #    conn.execute(sql)
    #    conn.commit()

    conn.close()
    return True


def add_training_data(db_name, data):
    """
    @description: add a training data item
    """
    conn = get_db_connection(db_name)
    klass = data['class']
    del(data['class'])

    sql = "INSERT INTO training_datas (%s, class) VALUES (%s, %s)"
    fields_sql = ",".join(data.keys())
    value_sql = ""
    values = []

    for key in data.keys():
        values.append(data[key])
    value_sql = ",".join(values)

    # get class id
    c = conn.cursor()
    c.execute("SELECT id FROM classes WHERE class =?", (klass, ))
    r = c.fetchone()
    class_id = r['id']

    sql = sql % (fields_sql, value_sql, class_id)
    conn.execute(sql)
    conn.commit()
    conn.close()
    return True

