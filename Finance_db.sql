CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(10) UNIQUE,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    passcode VARCHAR(100),
    role VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE records (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(10),
    amount FLOAT,
    type VARCHAR(20),
    category VARCHAR(50),
    date DATE,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

