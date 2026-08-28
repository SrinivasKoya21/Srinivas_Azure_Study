-- sql/01_seed_source_db.sql
-- Run against the northwind database on pg-northwind-retail

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id     SERIAL PRIMARY KEY,
    first_name      VARCHAR(50)  NOT NULL,
    last_name       VARCHAR(50)  NOT NULL,
    email           VARCHAR(120) NOT NULL,
    region          VARCHAR(20)  NOT NULL,   -- 'North America','Europe','APAC','LATAM'
    signup_date     DATE         NOT NULL,
    updated_at      TIMESTAMP    NOT NULL DEFAULT now()
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
    product_id      SERIAL PRIMARY KEY,
    product_name    VARCHAR(120) NOT NULL,
    category        VARCHAR(40)  NOT NULL,   -- 'Electronics','Home','Apparel','Sports','Books'
    unit_price      NUMERIC(10,2) NOT NULL,
    updated_at      TIMESTAMP    NOT NULL DEFAULT now()
);

INSERT INTO customers (first_name, last_name, email, region, signup_date) VALUES
 ('Aria','Nakamura','aria.nakamura@example.com','APAC','2023-02-11'),
 ('Liam','O''Connor','liam.oconnor@example.com','Europe','2022-11-02'),
 ('Sofia','Reyes','sofia.reyes@example.com','LATAM','2023-06-19'),
 ('Ethan','Walker','ethan.walker@example.com','North America','2021-09-14'),
 ('Noor','Haddad','noor.haddad@example.com','Europe','2023-01-05'),
 ('Priya','Shah','priya.shah@example.com','APAC','2022-04-27'),
 ('Marco','Rossi','marco.rossi@example.com','Europe','2023-08-30'),
 ('Chidi','Okonkwo','chidi.okonkwo@example.com','North America','2022-12-15'),
 ('Isla','Campbell','isla.campbell@example.com','North America','2023-03-22'),
 ('Diego','Fernandez','diego.fernandez@example.com','LATAM','2021-07-08'),
 ('Yuki','Tanaka','yuki.tanaka@example.com','APAC','2023-05-01'),
 ('Emma','Schmidt','emma.schmidt@example.com','Europe','2022-02-19'),
 ('Kwame','Mensah','kwame.mensah@example.com','North America','2023-07-11'),
 ('Valentina','Moreno','valentina.moreno@example.com','LATAM','2022-10-06'),
 ('Hana','Kobayashi','hana.kobayashi@example.com','APAC','2021-12-25');

INSERT INTO products (product_name, category, unit_price) VALUES
 ('Wireless Earbuds Pro','Electronics', 89.99),
 ('4K Streaming Stick','Electronics', 39.99),
 ('Mechanical Keyboard','Electronics', 74.50),
 ('Espresso Machine','Home', 199.00),
 ('Non-Stick Cookware Set','Home', 129.99),
 ('Memory Foam Pillow','Home', 34.99),
 ('Running Shoes','Sports', 84.99),
 ('Yoga Mat','Sports', 24.99),
 ('Adjustable Dumbbell Set','Sports', 149.00),
 ('Men''s Denim Jacket','Apparel', 59.99),
 ('Women''s Wool Coat','Apparel', 129.00),
 ('Graphic T-Shirt','Apparel', 19.99),
 ('Data Engineering with Databricks','Books', 44.99),
 ('The Pragmatic Programmer','Books', 34.50),
 ('Designing Data-Intensive Applications','Books', 49.99);
