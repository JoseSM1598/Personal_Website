import time
import sys
import sqlite3
from datetime import datetime

DB_NAME = "public/pipeline/db.sqlite"

def create_table():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS logs (
      raw_log TEXT NOT NULL UNIQUE,
      first_name TEXT,
      last_name TEXT,
      time_local TEXT,
      occupation TEXT,
      origin TEXT,
      residence TEXT,
      created DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """)
    conn.close()

def parse_line(line):
    split_line = line.split(" ")
    if len(split_line) < 7:
        return []
    first_name = split_line[0].replace(".", " ")
    last_name = split_line[1].replace(".", " ")
    time_local = (split_line[4] + " " + split_line[5]).replace(".", " ")
    occupation = split_line[6].replace(".", " ")
    origin = split_line[7].replace(".", " ")
    residence = split_line[8].replace(".", " ")

    created = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    return [
        first_name,
        last_name,
        time_local,
        occupation,
        origin,
        residence,
        created
    ]

def insert_record(line, parsed):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    args = [line] + parsed
    cur.execute('INSERT INTO logs VALUES (?,?,?,?,?,?,?,?)', args)
    conn.commit()
    conn.close()

LOG_FILE_A = "public/pipeline/log_a.txt"
LOG_FILE_B = "public/pipeline/log_b.txt"

if __name__ == "__main__":
    create_table()
    try:
        f_a = open(LOG_FILE_A, 'r')
        f_b = open(LOG_FILE_B, 'r')
        while True:
            where_a = f_a.tell()
            line_a = f_a.readline()
            where_b = f_b.tell()
            line_b = f_b.readline()

            if not line_a and not line_b:
                time.sleep(1)
                f_a.seek(where_a)
                f_b.seek(where_b)
                continue
            else:
                if line_a:
                    line = line_a
                else:
                    line = line_b

                line = line.strip()
                parsed = parse_line(line)
                if len(parsed) > 0:
                    insert_record(line, parsed)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        f_a.close()
        f_b.close()
        sys.exit()