import csv
import sqlite3

DB = "ECE401 Project Database.db"
RACES_CSV = "races.csv"
RESULTS_CSV = "results-selected-columns.csv"

SCHEMA = """
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS races;

CREATE TABLE races(
    raceId INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,
    round INTEGER NOT NULL,
    circuitId INTEGER NOT NULL,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT,
    url TEXT,
    fp1_date TEXT, fp1_time TEXT, fp2_date TEXT, fp2_time TEXT,
    fp3_date TEXT, fp3_time TEXT, quali_date TEXT, quali_time TEXT,
    sprint_date TEXT, sprint_time TEXT,
    UNIQUE(year, round)
    );

CREATE TABLE results(
    resultId INTEGER PRIMARY KEY,
    raceId INTEGER NOT NULL REFERENCES races(raceId),
    driverId INTEGER NOT NULL,
    constructorId INTEGER NOT NULL,
    number INTEGER,
    grid INTEGER NOT NULL,
    position INTEGER,
    positionText TEXT NOT NULL,
    positionOrder INTEGER NOT NULL,
    points REAL NOT NULL
    );
CREATE INDEX idx_results_raceId ON results(raceId);
"""

def rows(path):
    """Yield CSV rows as lists, converting the dump's '\\N' marker to None (SQL NULL)."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        yield header
        for row in reader:
            yield [None if v == r"\N" else v for v in row]

def load(con, table, path):
    data = rows(path)
    header = next(data)
    sql = f"INSERT INTO {table} ({','.join(header)}) VALUES ({','.join('?' * len(header))})"
    con.executemany(sql, data)

con = sqlite3.connect(DB)
con.executescript(SCHEMA)
load(con, "races", RACES_CSV)
load(con, "results", RESULTS_CSV)
con.commit()

print("FK violations:", con.execute("PRAGMA foreign_key_check").fetchall())
for t in ("races", "results"):
    print(t, con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0], "rows")
con.close()
