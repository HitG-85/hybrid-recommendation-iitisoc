CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    item_id INT REFERENCES items(id),
    interaction_type VARCHAR(20),
    interaction_strength FLOAT,
    watch_percentage FLOAT,
    rewatch_count INT,
    timestamp TIMESTAMP
);

CREATE TABLE recommendations (
    user_id INT REFERENCES users(id),
    item_id INT REFERENCES items(id),
    score FLOAT,
    rank INT,

    PRIMARY KEY (user_id, rank)
);