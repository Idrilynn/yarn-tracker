CREATE TYPE yarn_availability AS ENUM ('available', 'available online' 'out of stock', 'discontinued');

CREATE TABLE catalog_yarn (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product VARCHAR(30) NOT NULL,
    brand VARCHAR(30) NOT NULL,
    dye VARCHAR(45),
    colour VARCHAR(30) NOT NULL,
    material VARCHAR(30) NOT NULL,
    weight NUMERIC(5,2) NOT NULL,
    length NUMERIC(5,2) NOT NULL,
    availability yarn_availability NOT NULL DEFAULT 'available',
    misc VARCHAR(100)
);

CREATE TABLE stock_yarn (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    catalog_id UUID NOT NULL REFERENCES catalog_yarn(id),
    dye_lot VARCHAR(20),
    initial_weight NUMERIC(5,2) NOT NULL,
    current_weight NUMERIC(5,2),
    misc VARCHAR(100)
);