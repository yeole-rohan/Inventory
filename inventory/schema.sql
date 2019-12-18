DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS product_movement;

CREATE TABLE product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_quantity INTEGER NOT NULL
);

CREATE TABLE location(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loc_name TEXT NOT NULL
);

CREATE TABLE product_movement(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_id INTEGER NOT NULL,
    from_loc TEXT,
    to_loc TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (prod_id) REFERENCES product(id),
    FOREIGN KEY (from_loc) REFERENCES location(id)
    FOREIGN KEY (to_loc) REFERENCES location(id)
);