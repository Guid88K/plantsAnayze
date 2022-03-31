import mysql.connector
from mysql.connector import Error

TABLES = {'plats_analyze': (
    "CREATE TABLE `plats_analyze` ("
    "  `id` int(20) NOT NULL AUTO_INCREMENT,"
    "  `plant_id` varchar(128) NOT NULL,"
    "  `name` varchar(128) NOT NULL,"
    "  `cloud_coverage` varchar(128) NOT NULL,"
    "  `avg_ndvi` varchar(128) NOT NULL,"
    "  `variability_index` varchar(128) NOT NULL,"
    "  `analyzed_date` varchar(128) NOT NULL,"
    "  `created_date` date NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY unique_plant_id (name)"
    ") ENGINE=InnoDB")}


def my_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test"
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def migrate():
    conn = my_db_connection()

    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")

    tables = cursor.fetchall()

    for table in tables:
        print(table)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            sql = "DROP TABLE IF EXISTS {}".format(table_name)
            cursor.execute(sql)
            print("deleted")

            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")

    cursor.close()


if __name__ == "__main__":
    migrate()

#
# cursor.execute(
#     "CREATE TABLE students (name VARCHAR(255), rollno INTEGER(100), branch VARCHAR(255), address VARCHAR(255))")

# insert to table
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
#
# data_plats = (
#     meta_data['id'],
#     item,
#     meta_data['cloud_coverage'],
#     meta_data['avg_ndvi'],
#     variability_index,
#     datetime.datetime.now()
# )
#
