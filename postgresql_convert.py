import sqlite3
import psycopg2

#sqlite connect
sqlite_connection = sqlite3.connect('cafes.db')
sqlite_cursor = sqlite_connection.cursor()

#postgresql connect
postgresql_conn = psycopg2.connect(database="d5ige2q6li0rfd", user="krsnfxdhjwelxg", password="0e40d205537d91ed6d9d8d563cbbc573b0c41b59cc55874ecf32753b999b674c", host="ec2-23-20-124-77.compute-1.amazonaws.com", port="5432")
postgresql_cursor = postgresql_conn.cursor()

data = sqlite_cursor.execute('SELECT * FROM cafe')
cafes = data.fetchall()
for i in cafes:
    id = i[0]
    name = i[1]
    map_url = i[2]
    img_url = i[3]
    location = i[4]
    has_sockets = bool(i[5])
    has_toilet = bool(i[6])
    has_wifi = bool(i[7])
    can_take_calls = bool(i[8])
    seats = i[9]
    coffee_price = i[10]
    postgresql_cursor.execute(f"INSERT INTO cafe (id,name,map_url,img_url,location,has_sockets,has_toilet,has_wifi,can_take_calls,seats,coffee_price) VALUES ({id}, '{name}', '{map_url}', '{img_url}', '{location}', {has_sockets}, {has_toilet}, {has_wifi}, {can_take_calls}, '{seats}', '{coffee_price}')")

postgresql_conn.commit()

sqlite_connection.close()
postgresql_conn.close()