import sqlite3 as lite
import sys, com

con = None

def connect_db():
    return

def insert_order(product_id, quantity):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        params = (product_id,  quantity, "Not Started", "No Notes")
        cur.execute("INSERT INTO orders VALUES(NULL,?,?,?,?,datetime())", params)
        return cur.lastrowid

def update_order(order_id, order_status, notes):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        cur.execute("UPDATE orders SET STATUS = '" + order_status + "' WHERE id = " + str(order_id))
        cur.execute("UPDATE orders SET NOTES = '" + notes + "' WHERE id = " + str(order_id))


def insert_maintenance(machine_id, feedback):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        params = (machine_id, feedback);
        cur.execute("INSERT INTO maintenance VALUES(NULL,?,?,datetime())", params)
        return cur.lastrowid

def insert_qa(product_id, feedback):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        params = (product_id, feedback);
        cur.execute("INSERT INTO qa VALUES(NULL,?,?,datetime())", params)
        return cur.lastrowid

# dummy
def insert_demand(product_id, quantity):
    return

def get_product_name(product_id):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT name FROM product WHERE id = " + str(product_id))
        return cur.fetchone()

def create_schedule(order_id, labour_ids, machine_ids, start_date, finish_date):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        params = (order_id, start_date, finish_date)
        cur.execute("INSERT INTO schedule VALUES(NULL,?,?,?)", params)
        schedule_id = cur.lastrowid
        labour_ids = [x.strip() for x in labour_ids.split()]
        for labour_id in labour_ids:
            params = (schedule_id, labour_id)
            cur.execute("INSERT INTO schedule_labour VALUES(?,?)", params)
        machine_ids = [x.strip() for x in machine_ids.split()]
        for machine_id in machine_ids:
            params = (schedule_id, machine_id)
            cur.execute("INSERT INTO schedule_machine VALUES(?,?)", params)
    return schedule_id

def select_all(table):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM " + table)
        return cur.fetchall()


def select_one(table, item_id):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM " + table + " WHERE id = " + str(item_id))
        return cur.fetchone()

def get_labour(schedule_id):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT labour_id FROM schedule_labour WHERE schedule_id = " + str(schedule_id))
        return cur.fetchall()
        
def get_machine(schedule_id):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT machine_id FROM schedule_machine WHERE schedule_id = " + str(schedule_id))
        return cur.fetchall()

def raw_materials_handler(product_id, quantity):
    con = lite.connect('prod.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT rawmaterial_id, quantity FROM product_rawmaterials WHERE product_id = " + str(product_id))
        rawmaterials = cur.fetchall()
        for rawmaterial in rawmaterials:
            rawmaterial_id = rawmaterial[0]
            required_quantity = rawmaterial[1] * quantity
            cur.execute("SELECT name, quantity FROM rawmaterials WHERE id = " + str(rawmaterial_id))
            rawmaterial_info = cur.fetchone()
            rawmaterial_name = rawmaterial_info[0]
            rawmaterial_quantity = rawmaterial_info[1]
            if rawmaterial_quantity < required_quantity:
                receive = com.order_raw_materials(required_quantity, rawmaterial_name, rawmaterial_id)
                cur.execute("UPDATE rawmaterials SET QUANTITY = " + str(rawmaterial_quantity)  + " WHERE id = " + str(rawmaterial_id))
            else:
                new_stock = rawmaterial_quantity - required_quantity 
                cur.execute("UPDATE rawmaterials SET QUANTITY = " + str(new_stock) + " WHERE id = " + str(rawmaterial_id))
                
            
        
