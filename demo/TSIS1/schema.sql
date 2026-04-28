-- groups table
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

-- phonebook table
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    name TEXT,
    phone TEXT UNIQUE,
    email TEXT,
    birthday DATE,
    group_id INTEGER REFERENCES groups(id)
);