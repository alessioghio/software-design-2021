create TABLE stockerUser (
    userName VARCHAR(100),
    userLastName VARCHAR(100),
    email VARCHAR(100),
    account VARCHAR(50),
    passkey VARCHAR(100)
);

create TABLE administrator (
    id BIGSERIAL NOT NULL PRIMARY KEY
)inherits(stockerUser);

create TABLE client (
    id BIGSERIAL NOT NULL PRIMARY KEY
)inherits(stockerUser);

create TABLE adminURL (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    webName VARCHAR(50),
    webURL VARCHAR(200)
    admin_id BIGINT REFERENCES administrator(id),
    UNIQUE(admin_id)
);

create TABLE supply(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    supplyName VARCHAR(100),
    price NUMERIC NOT NULL DEFAULT 0,
    unit VARCHAR(50),
    quantity INT,
    category VARCHAR(100),
    visibility BOOLEAN
);

create TABLE shoppingCart(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    shopDate DATETIME,
    supply_id BIGINT REFERENCES supply(id),

);