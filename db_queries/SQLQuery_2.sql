CREATE TABLE IF NOT EXISTS Tasks(
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description TEXT,
    isPurchased BOOLEAN NOT NULL,
    doneAt DATE
);