import pandas as pd
# import sqlite3
import csv
import mysql.connector # mysql-connector-python ==    8.0.23

def flood_items(file_name):
    # con = sqlite3.connect("db.sqlite3")
    con = mysql.connector.connect(
    user="root",
    password = "",
    host = "localhost",
    database="demo_IMS_db")
    cur = con.cursor()
    a_file = open(file_name,"r")
    rows = csv.reader(a_file)
    header = next(rows)
    print(next(rows))
    query2 = cur.executemany("INSERT INTO core_item (item_code,item_description,MOQ,brand) VALUES (%s, %s, %s, %s)",rows)
    print("insertion complete")
    con.commit()
    con.close()

if __name__ == '__main__':
    # flood_items("T2_PriceList.csv")
    # flood_items("ABB_PriceList_Cleaned_2.csv")
    # flood_items("items_scame.csv")
    # flood_items("itemSOCOMEC.csv")
    # flood_items("itemEATON.csv")
    # flood_items("itemst1.csv") 
    # flood_items("itemsPHOENIXMECANO.csv")
    # flood_items("itemsABB.csv")
    pass
# query2 = cur.executemany("INSERT INTO core_item (item_code,item_description,MOQ,brand) VALUES (?,?,?,?)",rows) # for db.sqlite3