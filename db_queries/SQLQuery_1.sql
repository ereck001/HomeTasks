CREATE TABLE PurchasedProducts(
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    isPurchased BOOLEAN NOT NULL,
    doneAt DATE
);