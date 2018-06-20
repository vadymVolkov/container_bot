import mysql.connector
from config import config


def connection():
    conn = mysql.connector.connect(
        host=config.host,
        user=config.user,
        passwd=config.password,
        database=config.db,
        use_unicode=True,
        charset="utf8")

    return conn


def create_new_table(table_name):
    conn = connection()
    cursor = conn.cursor()
    sql = '''
        CREATE TABLE {table} (
        `id` INT NOT NULL AUTO_INCREMENT,
        `arr_date` VARCHAR(255) NULL,
        `dep_date` VARCHAR(255) NULL,
        `car_num` VARCHAR(255) NULL,
        `truck_num` VARCHAR(255) NULL,
        `driver` VARCHAR(255) NULL,
        `direction` VARCHAR(255) NULL,
        `forwarder` VARCHAR(255) NULL,
        `cont_num` VARCHAR(255) NULL,
        `cont_size` VARCHAR(255) NULL,
        `line_name` VARCHAR(255) NULL,
        `cargo` VARCHAR(255) NULL,
        `cargo_det` VARCHAR(255) NULL,
        `weight` VARCHAR(255) NULL,
        `sender_reciever` VARCHAR(255) NULL,
        `city` VARCHAR(255) NULL,
        `country` VARCHAR(255) NULL,
        `transporter` VARCHAR(255) NULL,
        `mode` VARCHAR(255) NULL,
        `oreinter` VARCHAR(255) NULL,
        FULLTEXT KEY `ft1` (city),
        PRIMARY KEY (`id`));
        '''
    cursor.execute(sql.format(table=table_name))
    conn.commit()
    conn.close()


def insert_data_in_table(table_name, data):
    conn = connection()
    cursor = conn.cursor()
    sql = 'insert into {table} (arr_date, dep_date, car_num, truck_num, driver, direction, `forwarder`, cont_num, cont_size, line_name, cargo, cargo_det, weight, sender_reciever, city, country, transporter, `mode`, oreinter ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql.format(table=table_name), data)
    conn.commit()
    conn.close()


def get_tables_list():
    conn = connection()
    cursor = conn.cursor()
    sql = 'select * from tables_list'
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return data


def get_table_by_name_from_table_list(db_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'select * from tables_list where table_name = %s'
    cursor.execute(sql, (db_name,))
    data = cursor.fetchone()
    conn.close()
    return data


def get_table_data_by_table_name(table_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'select * from {table}'
    cursor.execute(sql.format(table=table_name))
    data = cursor.fetchall()
    conn.close()
    return data


def insert_table_name_in_table_list(name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'insert into tables_list (table_name) VALUES (%s)'
    cursor.execute(sql, (name,))
    conn.commit()
    conn.close()


def arched_table_by_name(name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'delete from tables_list where table_name = %s'
    cursor.execute(sql, (name,))
    conn.commit()
    conn.close()


def drop_table_by_name(name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'DROP TABLE IF EXISTS {table}'
    cursor.execute(sql.format(table=name))
    conn.commit()
    conn.close()


def check_if_table_empty_byt_name(table_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'select file_upload from tables_list where table_name = %s'
    cursor.execute(sql, (table_name,))
    result = cursor.fetchone()
    conn.close()
    return result


def delete_empty_records(table_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'delete  from {tabel} where city is null'
    cursor.execute(sql.format(tabel=table_name))
    conn.commit()
    conn.close()


def change_city_name_by_id(id, table_name, new_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'update {table} set city = %s where id = %s'
    cursor.execute(sql.format(table=table_name), (new_name, id,))
    conn.commit()
    conn.close()


def set_file_upload_status_in_table_list(status, table_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'update tables_list set file_upload = %s where table_name = %s'
    cursor.execute(sql, (status, table_name,))
    conn.commit()
    conn.close()


def search_city(city_name):
    conn = connection()
    cursor = conn.cursor()
    sql = """
    SELECT *, MATCH (possible_city_name) AGAINST (%s) as REL
    FROM city_names
    WHERE MATCH (possible_city_name) AGAINST (%s)
    """
    cursor.execute(sql, (city_name, city_name))
    data = cursor.fetchone()
    conn.close()
    return data


def set_file_format_status_in_table_list(status, table_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'update tables_list set file_format = %s where table_name = %s'
    cursor.execute(sql, (status, table_name,))
    conn.commit()
    conn.close()


def find_original_city_by_name(entered_original_city_name):
    conn = connection()
    cursor = conn.cursor()
    sql = """
        SELECT *, MATCH (city_name) AGAINST (%s) as REL
        FROM city_names
        WHERE MATCH (city_name) AGAINST (%s)
        """
    cursor.execute(sql, (entered_original_city_name, entered_original_city_name))
    data = cursor.fetchone()
    conn.close()
    return data


def get_possible_city_names_by_city_name(city_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'select possible_city_name from city_names where city_name = %s'
    cursor.execute(sql, (city_name,))
    data = cursor.fetchone()
    conn.close()
    return data[0]


def add_possible_city_name_by_original_city_name(original_city_name_from_city_list, unknown_city_name):
    possible_names = get_possible_city_names_by_city_name(original_city_name_from_city_list)
    if possible_names is None:
        possible_names = ''
    unknown_city_name = possible_names + ', ' + unknown_city_name
    conn = connection()
    cursor = conn.cursor()
    sql = 'update city_names set possible_city_name = %s where city_name = %s'
    cursor.execute(sql, (unknown_city_name, original_city_name_from_city_list,))
    conn.commit()
    conn.close()



def add_new_original_city_name_and_possible_city_name(entered_original_city_name, unknown_city_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'insert into container.city_names(city_name, possible_city_name) VALUES (%s, %s)'
    cursor.execute(sql, (entered_original_city_name, unknown_city_name))
    conn.commit()
    conn.close()


def set_table_status_in_table_list(status, table_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'update tables_list set table_status = %s where table_name = %s'
    cursor.execute(sql, (status, table_name,))
    conn.commit()
    conn.close()


def get_tables_list_for_client():
    conn = connection()
    cursor = conn.cursor()
    sql = 'select * from tables_list where table_status = %s'
    cursor.execute(sql, (True,))
    data = cursor.fetchall()
    conn.close()
    return data


def get_container_list_by_city_name(table_name, city_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'select * from {table}  where city = %s'
    cursor.execute(sql.format(table=table_name), (city_name,))
    data = cursor.fetchall()
    conn.close()
    return data


def set_file_in_db_stAtus_in_table_list(status, table_name):
    conn = connection()
    cursor = conn.cursor()
    sql = 'update tables_list set file_in_db = %s where table_name = %s'
    cursor.execute(sql, (status, table_name,))
    conn.commit()
    conn.close()