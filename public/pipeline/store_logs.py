import time
import sys
import sqlite3
from datetime import datetime

DB_NAME = "db.sqlite"

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
    first_name = split_line[0]
    last_name = split_line[1]
    time_local = split_line[4] + " " + split_line[5]
    occupation = 
    origin = 
    residence = 

    created = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    return [
        remote_addr,
        time_local,
        request_type,
        request_path,
        status,
        body_bytes_sent,
        http_referer,
        http_user_agent,
        created
    ]

def insert_record(line, parsed):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    args = [line] + parsed
    cur.execute('INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?,?)', args)
    conn.commit()
    conn.close()

LOG_FILE_A = "log_a.txt"
LOG_FILE_B = "log_b.txt"

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