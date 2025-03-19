-- Create users table if not exists
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    password TEXT NOT NULL,
    darkMode BOOLEAN NOT NULL
);

INSERT INTO users (email, firstName, lastName, password, darkMode)
VALUES
    ('info@rian.fyi', 'Rian', 'Atri', 'Rian1234', 0),
    ('rocky@gmail.com', 'Rocky', 'K', 'Rocky1234', 1),
    ('carol@gmail.com', 'Carol', 'Brown', 'Carol1234', 0),
    ('david@gmail.com', 'David', 'Wilson', 'David1234', 1);

