CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    status TEXT,
    notes TEXT,
    created date DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id INTEGER,
    feedback TEXT,
    status TEXT,
    created date DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE qa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    feedback TEXT,
    created date DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE demand (
    product_id INTEGER PRIMARY KEY,
    quantity INTEGER,
    created date DEFAULT CURRENT_TIMESTAMP,
    due date NULL
);

INSERT INTO demand VALUES(1,200,datetime(),datetime());
INSERT INTO demand VALUES(2,200,datetime(),datetime());
INSERT INTO demand VALUES(3,200,datetime(),datetime());

CREATE TABLE schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    start_date date NULL,
    end_date date NULL
);

CREATE TABLE schedule_labour (
    schedule_id INTEGER,
    labour_id INTEGER
);

CREATE TABLE labour (
    id INTEGER PRIMARY KEY,
    name TEXT
);

INSERT INTO labour VALUES(1,'Frank');
INSERT INTO labour VALUES(2,'Bill');
INSERT INTO labour VALUES(3,'John');
INSERT INTO labour VALUES(4,'Doug');
INSERT INTO labour VALUES(5,'Steve');
INSERT INTO labour VALUES(6,'Tim');

CREATE TABLE schedule_machine (
    schedule_id INTEGER,
    machine_id INTEGER
);

CREATE TABLE machines (
    id INTEGER PRIMARY KEY
);

INSERT INTO machines VALUES(1);
INSERT INTO machines VALUES(2);
INSERT INTO machines VALUES(3);
INSERT INTO machines VALUES(4);
INSERT INTO machines VALUES(5);
INSERT INTO machines VALUES(6);


CREATE TABLE product (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantity INTEGER
);

INSERT INTO product VALUES(1,'Pen',200);
INSERT INTO product VALUES(2,'Pencil',100);
INSERT INTO product VALUES(3,'Fancy Pen',0);
INSERT INTO product VALUES(4,'Gold Pen',0);
INSERT INTO product VALUES(5,'Silver Pen',10);

CREATE TABLE rawmaterials (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantity INTEGER
);

INSERT INTO rawmaterials VALUES(1,'INK',100);
INSERT INTO rawmaterials VALUES(2,'LEAD',200);
INSERT INTO rawmaterials VALUES(3,'WOOD',500);
INSERT INTO rawmaterials VALUES(4,'GOLD',50);
INSERT INTO rawmaterials VALUES(5,'SILVER',20);
INSERT INTO rawmaterials VALUES(6,'STEEL',300);
INSERT INTO rawmaterials VALUES(7,'PLASTIC',500);

CREATE TABLE product_rawmaterials (
    product_id INTEGER,
    rawmaterial_id INTEGER,
    quantity INTEGER
);

-- PEN
INSERT INTO product_rawmaterials VALUES(1,1,5);
INSERT INTO product_rawmaterials VALUES(1,6,10);
INSERT INTO product_rawmaterials VALUES(1,7,7);
-- PENCIL
INSERT INTO product_rawmaterials VALUES(2,2,1);
INSERT INTO product_rawmaterials VALUES(2,3,10);
-- FANCY PEN
INSERT INTO product_rawmaterials VALUES(3,1,5);
INSERT INTO product_rawmaterials VALUES(3,5,5);
INSERT INTO product_rawmaterials VALUES(3,6,5);
-- GOLD PEN
INSERT INTO product_rawmaterials VALUES(4,1,5);
INSERT INTO product_rawmaterials VALUES(4,4,10);
INSERT INTO product_rawmaterials VALUES(4,7,7);
-- SILVER PEN
INSERT INTO product_rawmaterials VALUES(5,1,5);
INSERT INTO product_rawmaterials VALUES(5,5,10);
INSERT INTO product_rawmaterials VALUES(5,7,7);
