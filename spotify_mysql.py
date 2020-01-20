import mysql.connector
import json
import pandas as pd

mysql_credentials = json.load(open("mysql_credentials.json"))

conn = mysql.connector.connect(
    user = mysql_credentials["user"], 
    password = mysql_credentials["password"], 
    host = mysql_credentials["host"], 
    database = mysql_credentials["database"],
    auth_plugin = mysql_credentials["auth_plugin"],
)

cur = conn.cursor()

tracks_df = pd.read_csv("files/tracks_df.csv")

lines = []
for key, row in tracks_df.iterrows():
    lines.append(str(list(row)).replace('[','(').replace("]",")"))

insert_query = "INSERT INTO tracks VALUES\n"
insert_query += (",\n".join([line for line in lines]) + ";")

cur.execute(insert_query)

conn.commit()
cur.close()
conn.close()