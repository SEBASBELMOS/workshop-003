CREATE DATABASE IF NOT EXISTS happiness_db;

\c happiness_db;

CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100),
    continent VARCHAR(50),
    year INTEGER,
    economy FLOAT,
    health FLOAT,
    social_support FLOAT,
    freedom FLOAT,
    corruption_perception FLOAT,
    generosity FLOAT,
    happiness_rank INTEGER,
    happiness_score FLOAT,
    predicted_happiness_score FLOAT
);