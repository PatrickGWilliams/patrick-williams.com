DROP TABLE IF EXISTS bees;
DROP TABLE IF EXISTS boxes;

CREATE TABLE bees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    print_date TIMESTAMP UNIQUE NOT NULL,
    letters TEXT NOT NULL,
    accepted TEXT NOT NULL,
    pangrams TEXT
);


CREATE TABLE boxes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    print_date TIMESTAMP UNIQUE NOT NULL,
    sides TEXT NOT NULL,
    one_word TEXT,
    two_word TEXT,
    dictionary TEXT NOT NULL
);
