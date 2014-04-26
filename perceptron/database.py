import os
import sqlite3 as sql


"""
Basic Database wrapper Functions
"""


def create_db(db_name, destroy_existing=True):
    """
    @description: Try and create a sqlite3 db if it does not exist
    @args:
        - db_name: the name of the database file without the .db extension
        - destroy_existing (bool) - if True, and the file exists, it will destroy and create the db again. Otherwise returns false
    """
    db = db_name + ".db"
    if os.path.isfile(db):
        if destroy_existing:
            destroy_db(db_name)
        else:
            return False  # DB exists. Cannot create the db

    c = sql.connect(db)
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


def _simple_query_wrapper(db_name, sql, args=None):
    """
    @description: wraps the database query in a nice function to stop code duplication
    @TODO: make this so it returns data?
    """  # TODO
    try:
        conn = get_db_connection(db_name)
        if not conn:
            return False
        c = conn.cursor()

        if args:
            c.execute(sql, args)
        else:
            c.execute(sql)

        conn.commit()
        conn.close()
        return True
    except Exception, e:
        print e
        try:  # Incase that the connection was established and another error occured,
              # close the connection before returning
            conn.close()
        except:
            pass
        return False


def _simple_select_query_wrapper(db_name, sql, args=None):
    """
    @description: wrapes the select queries around this function to handle exceptions, etc.
    @returns - False OR Array of Row objects
    """
    try:
        conn = get_db_connection(db_name)
        if not conn:
            return False
        c = conn.cursor()

        if args:
            c.execute(sql, args)
        else:
            c.execute(sql)
        r = c.fetchall()
        conn.close()
        if len(r) == 0:
            return None
        return r
    except:
        try:  # Incase that the connection was established and another error occured,
              # close the connection before returning
            conn.close()
        except:
            pass
        return False


"""
Singular Database Create Table Functions
    - table definitions can be found in sql/base_schema.sql
"""


def _create_perceptron_details_table(db_name):
        sql = """
            CREATE TABLE perceptron_details (
                id INTEGER PRIMARY KEY,
                iterations INTEGER
            );
        """
        return _simple_query_wrapper(db_name, sql, None)


def _create_classes_table(db_name):
        sql = """
            CREATE TABLE classes (
                id INTEGER PRIMARY KEY,
                class TEXT
            );
        """
        return _simple_query_wrapper(db_name, sql, None)


def _create_features_table(db_name):
        sql = """
            CREATE TABLE features (
                id INTEGER PRIMARY KEY,
                feature TEXT
            );
        """
        return _simple_query_wrapper(db_name, sql, None)


def _create_training_datas_table(db_name, features):
    sql = "CREATE TABLE training_datas (\
            id INTEGER PRIMARY KEY,\
            class TEXT\
            %s);"
    feature_sql = ""
    for feature in features:
        feature_sql += ", %s REAL" % feature
    sql = sql % feature_sql
    return _simple_query_wrapper(db_name, sql, None)


def _create_weights_table(db_name, features):
    sql = "CREATE TABLE weights (\
            id INTEGER PRIMARY KEY,\
            class TEXT\
            %s);"
    feature_sql = ""
    for feature in features:
        feature_sql += ", %s REAL" % feature
    sql = sql % feature_sql

    return _simple_query_wrapper(db_name, sql, None)


def _create_historical_weights_table(db_name, features):
    sql = "CREATE TABLE historical_weights (\
            id INTEGER PRIMARY KEY,\
            training_data_id INTEGER,\
            class TEXT\
            %s);"
    feature_sql = ""
    for feature in features:
        feature_sql += ", %s REAL" % feature
    sql = sql % feature_sql

    return _simple_query_wrapper(db_name, sql, None)


def _create_classification_data_table(db_name, features):
    sql = "CREATE TABLE classification_data (\
            id INTEGER PRIMARY KEY,\
            class TEXT\
            %s);"
    feature_sql = ""
    for feature in features:
        feature_sql += ", %s REAL" % feature
    sql = sql % feature_sql

    return _simple_query_wrapper(db_name, sql, None)


"""
Insert Database Functions
    - functions to insert data into the tables
"""


def _insert_perceptron_details(db_name, iterations):
    if type(iterations) is int:
        sql = "INSERT INTO perceptron_details (iterations) VALUES (?);"
        args = (iterations, )
        return _simple_query_wrapper(db_name, sql, args)


def _insert_classes(db_name, classes):
    sql = "INSERT INTO classes (class) VALUES (?)"
    error_classes = []  # stores all error inserts
    for k in classes:
        if not _simple_query_wrapper(db_name, sql, (k, )):
            error_classes.append(k)
    if len(error_classes) > 0:
        return False, error_classes
    return True, None


def _insert_features(db_name, features):
    sql = "INSERT INTO features (feature) VALUES (?)"
    error_classes = []  # stores all error inserts
    for k in features:
        if not _simple_query_wrapper(db_name, sql, (k, )):
            error_classes.append(k)
    if len(error_classes) > 0:
        return False, error_classes
    return True, None


def _insert_training_data(db_name, klass, feature_dict):
    sql = "INSERT INTO training_datas (class %s) VALUES (? %s);"
    args = [klass]
    feature_key_sql = ""
    feature_arg_sql = ""

    for k in feature_dict.keys():
        args.append(feature_dict[k])
        feature_arg_sql += ", ? "
        feature_key_sql += ", %s" % k
    sql = sql % (feature_key_sql, feature_arg_sql)
    args = tuple(args)

    return _simple_query_wrapper(db_name, sql, args)


def _insert_weights(db_name, klass, feature_dict):
    sql = "INSERT INTO weights (class %s) VALUES (? %s);"
    args = [klass]
    feature_key_sql = ""
    feature_arg_sql = ""

    for k in feature_dict.keys():
        args.append(feature_dict[k])
        feature_arg_sql += ", ? "
        feature_key_sql += ", %s" % k
    sql = sql % (feature_key_sql, feature_arg_sql)
    args = tuple(args)
    return _simple_query_wrapper(db_name, sql, args)


def _insert_historical_weights(db_name, klass, training_id, feature_dict):
    sql = "INSERT INTO historical_weights (class, training_data_id %s) VALUES (?, ? %s);"
    args = [klass, int(training_id)]
    feature_key_sql = ""
    feature_arg_sql = ""

    for k in feature_dict.keys():
        args.append(feature_dict[k])
        feature_arg_sql += ", ? "
        feature_key_sql += ", %s" % k
    sql = sql % (feature_key_sql, feature_arg_sql)
    args = tuple(args)

    return _simple_query_wrapper(db_name, sql, args)


def _insert_classification_data(db_name, klass, feature_dict):
    sql = "INSERT INTO classification_data (classified_class %s) VALUES (? %s);"
    args = [klass]
    feature_key_sql = ""
    feature_arg_sql = ""

    for k in feature_dict.keys():
        args.append(feature_dict[k])
        feature_arg_sql += ", ? "
        feature_key_sql += ", %s" % k
    sql = sql % (feature_key_sql, feature_arg_sql)
    args = tuple(args)

    return _simple_query_wrapper(db_name, sql, args)


"""
Select Database Functions
    - functions to select data from tables
"""


def get_iterations(db_name):
    sql = "SELECT iterations FROM perceptron_details LIMIT 1"  # since only one row should exist per perceptron
    res = _simple_select_query_wrapper(db_name, sql, None)
    if res:
        return int(res['iterations'])
    return False


def get_classes(db_name):
    sql = "SELECT id, class FROM classes"
    res = _simple_query_wrapper(db_name, sql, 0)

    if res:
        ret_list = []
        for r in res:
            ret_list.append(r['class'])
        return ret_list
    return False


def get_features(db_name):
    sql = "SELECT id, feature FROM features"
    res = _simple_query_wrapper(db_name, sql, 0)

    if res:
        ret_list = []
        for r in res:
            ret_list.append(r['feature'])
        return ret_list
    return False





# def create_tables(db_name, classes, features, iterations):
#     conn = get_db_connection(db_name)
#     if not conn:
#         return False

#     # Create the iteration table
#     sql = """CREATE TABLE perceptron_details(
#                 id INTEGER PRIMARY KEY,
#                 iterations INT
#         );"""
#     conn.execute(sql)
#     conn.commit()

#     # Insert details into table
#     sql = "INSERT INTO perceptron_details (iterations) VALUES (?);"
#     args = (iterations, )

#     conn.execute(sql, args)
#     conn.commit()

#     # Create the class table
#     sql = """CREATE TABLE classes(
#                 id INTEGER PRIMARY KEY,
#                 class TEXT
#         );"""
#     conn.execute(sql)
#     conn.commit()

#     # Insert into classes table
#     for klass in classes:
#         sql = "INSERT INTO classes (class) VALUES (?)"
#         args = (klass, )
#         conn.execute(sql, args)
#         conn.commit()

#     # Create features table
#     sql = """CREATE table features(
#                 id INTEGER PRIMARY KEY,
#                 feature TEXT
#         );"""
#     conn.execute(sql)
#     conn.commit()

#     # Insert features
#     for feature in features:
#         sql = "INSERT INTO features (feature) VALUES (?)"
#         args = (feature, )
#         conn.execute(sql, args)
#         conn.commit()

#     # Create training data table
#     sql = """CREATE TABLE training_datas(
#                 id INTEGER PRIMARY KEY,
#                 class INT
#         """

#     feature_sql = ""
#     for feature in features:
#         feature_sql += ", %s REAL" % feature

#     sql += feature_sql + ");"
#     conn.execute(sql)
#     conn.commit()

#     # Create the weights table
#     sql = "CREATE TABLE weights(\
#                 id INTEGER PRIMARY KEY,\
#                 class_id INTEGER\
#                 %s);" % feature_sql
#     conn.execute(sql)
#     conn.commit()

#     # Insert temporary weights into table
#     #i = 0
#     #for klass in classes:
#     #    i += 1
#     #    sql = "INSERT INTO weights (class_id, weight) VALUES (%d, 0.0)" % i
#     #    conn.execute(sql)
#     #    conn.commit()

#     conn.close()
#     return True


# def add_training_data(db_name, data):
#     """
#     @description: add a training data item
#     """
#     conn = get_db_connection(db_name)
#     klass = data['class']
#     del(data['class'])

#     sql = "INSERT INTO training_datas (%s, class) VALUES (%s, %s)"
#     fields_sql = ",".join(data.keys())
#     value_sql = ""
#     values = []

#     for key in data.keys():
#         values.append(data[key])
#     value_sql = ",".join(values)

#     # get class id
#     c = conn.cursor()
#     c.execute("SELECT id FROM classes WHERE class =?", (klass, ))
#     r = c.fetchone()
#     class_id = r['id']

#     sql = sql % (fields_sql, value_sql, class_id)
#     conn.execute(sql)
#     conn.commit()
#     conn.close()
#     return True

