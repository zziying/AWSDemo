import pymysql
import json

# config

# connection
connection = pymysql.connect(host=endpoint, user=username, password=password, db=database_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

def read_req(list_of_ids):
    '''read a list of ids from database'''
    format_strings = ','.join(['%s'] * len(list_of_ids))
    cursor = connection.cursor()
    cursor.execute('Select * from Characters WHERE id IN (%s)' % format_strings, tuple(list_of_ids))
    rows = cursor.fetchall()
    return rows


def write_req(vals):
    '''Write a json object into database'''
    cursor = connection.cursor()
    sql = 'Insert into Characters(hero, name, power, color, xp) values (%s, %s, %s, %s, %s)'
    cursor.execute(sql, (vals["hero"], vals["name"], vals["power"], vals["color"], vals["xp"]))
    connection.commit()
    return "done"


def lambda_handler(event, context):
    if (event["REQUEST"] == "read"): 
        id_list = event['SQLS']
        rows = read_req(id_list)
        return {
            "statusCode": 200,
            "body": rows
        }
    else:
        json_obj = event['SQLS']
        
        for obj in json_obj:
            write_req(obj)
            
        return {
            "statusCode": 200,
            "body": "write success"
        }
