CREATE TABLE products (
    product_no integer,
    name text,
    price numeric
);


CREATE TABLE voice_data
(
    Id SERIAL PRIMARY KEY,
    unique_id INTEGER,
    datta integer,
    etap_1 CHARACTER VARYING(30), 
    etap_2 INTEGER,
    phone_number VARCHAR(15),
    texxt CHARACTER VARYING(30),
    duration INTEGER
);
INSERT INTO voice_data (unique_id, datta, etap_1, etap_2, phone_number, texxt, duration) VALUES (12345, 2020-08-27, 94674, 0, 7689967, 'ya slushayu', 432); 