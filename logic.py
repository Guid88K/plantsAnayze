import time
import MySQLdb
import numpy as np
import os
import re
import rasterio
import json

from migrate import *


def insert_to_table(data_plats, conn):
    cursor = conn.cursor()

    add_plats = ("INSERT INTO plats_analyze "
                 "(plant_id, name, cloud_coverage, avg_ndvi, variability_index, analyzed_date, created_date) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    try:
        cursor.execute(add_plats, data_plats)
        conn.commit()
        print("success insert")
    except (MySQLdb.Error, MySQLdb.Warning, MySQLdb.IntegrityError) as e:
        print(e)
    except:
        print('duplicate order')
    cursor.close()


def get_from_table(conn, plant_id):
    cursor = conn.cursor()

    query = "SELECT * FROM plats_analyze WHERE plant_id = %s"

    cursor.execute(query, (plant_id,))

    result = cursor.fetchall()

    cursor.close()

    return result


def images_to_collection(in_directory, veg_index_name, conn):
    failures = []
    band_list = os.listdir(in_directory)

    ndvi_name_matcher = re.compile(r'\w*' + veg_index_name + '\w*.PNG')
    ndvi_name_list = {item.upper() for item in band_list if
                      (os.path.isfile(in_directory + "\\" + item) and ndvi_name_matcher.match(item.upper()))}
    json_name_matcher = re.compile(r'\w*' + veg_index_name + '\w*.json')
    json_name_list = {item.upper() for item in band_list if
                      (os.path.isfile(in_directory + "\\" + item) and json_name_matcher.match(item.upper()))}

    for item in ndvi_name_list:
        with rasterio.open(in_directory + "\\" + item, 'r') as im:
            im_array = im.read(1)  # reading raster PNG image as ONEband array
            im_array = im_array[np.nonzero(im_array)]  # clearing zero-values

            if np.count_nonzero(im_array != 254) / len(im_array) >= 0.65:
                trash_count = int(
                    np.count_nonzero(im_array != 254) * 0.95)  # calculating trash-hold level for variability index
                val_array = [{'value': i, 'count': 0} for i in range(0, 254)]

                for value in im_array:  # counting pixel_vales between unique
                    if value < 254:
                        val_array[value]['count'] = val_array[value]['count'] + 1

                val_array = sorted(val_array, key=lambda x: x['count'], reverse=True)
                check_sum = 0
                indexes = []

                for i in range(0, 254):
                    if check_sum <= trash_count:
                        check_sum = check_sum + val_array[i]['count']
                        if val_array[i]['value'] not in indexes:
                            indexes.append(val_array[i]['value'])
                    else:
                        break

                if os.path.isfile(in_directory + "\\" + item[:-4] + '_meta.json'):
                    # -------------------------------------------------------------------
                    variability_index = (255 - (max(indexes) - min(indexes))) / 255
                    print(variability_index)
                    print(min(indexes))
                    date = item.split("_")[0]
                    analyze_date = f'{date[:2]}-{date[:2]}-{date[4:]}'
                    print(max(indexes))
                    meta_json = open(in_directory + "\\" + item[:-4] + '_meta.json', 'rb')
                    meta_str = meta_json.read()

                    try:
                        meta_data = json.loads(meta_str)
                    except:
                        print('json malformed')
                        continue

                    meta_data['variability_index'] = round(variability_index, 4)
                    meta_json.close()

                    data_plats = (
                        meta_data['id'],
                        item,
                        meta_data['cloud_coverage'],
                        meta_data['avg_ndvi'],
                        variability_index,
                        analyze_date,
                        time.strftime('%Y-%m-%d %H:%M:%S')
                    )

                    insert_to_table(data_plats, conn)
                    with open(in_directory + "\\" + item[:-4] + '_meta.json', 'w') as f:
                        json.dump(meta_data, f)
                    # -------------------------------------------------------------------
                else:
                    failures.append(item)
            else:
                failures.append(item)

    return failures


def moveData():
    in_dir = '.\\data'
    # ------------------------------------------------------------------------------------------------------------------

    # vi_list = ['NDVI', 'NDWI', 'AVI']
    vi_list = ['NDVI']
    failure_list = []

    dir_list = os.listdir(in_dir)
    connection = my_db_connection()

    if_get_data = input("Імпортуавти дані в базу даних?(так/ні) ")
    if if_get_data == "так":
        for vi in vi_list:
            for directory in dir_list:
                final_dir = in_dir + "\\" + directory + '\\result'
                if os.path.exists(final_dir):
                    fails = images_to_collection(final_dir, vi, connection)
                    if len(fails) != 0:
                        failure_list.append(fails)


if __name__ == '__main__':

    # -----------------------------------------------------------INPUT-DIRECTORY-FOR-VARIABILITY-INDEX-CALCULATIONS-----


    print()
