from faker import Faker
from datetime import datetime
import random
import time

#LINE = """\
#{remote_addr} - - [{time_local} +0000] "{request_type} {request_path} HTTP/1.1" {status} {body_bytes_sent} "{http_referer}" "{http_user_agent}"\
#"""

LINE = """\
{first_name} {last_name} - - [{entry_date} +0000] {occupation} {origin_country} {current_residence}\
"""

LOG_FILE_A = "public/pipeline/log_a.txt"
LOG_FILE_B = "public/pipeline/log_b.txt"
#LOG_FILE_A = "log_a.txt"
#LOG_FILE_B = "log_b.txt"
LOG_MAX = 100

def generate_log_line():
    fake = Faker()
    now = datetime.now()
    time_local = now.strftime('%d/%b/%Y:%H:%M:%S')
    first_name = fake.first_name().replace(" ", ".")
    last_name = fake.last_name().replace(" ", ".")
    occupation = fake.job().replace(" ", ".")
    origin_country = fake.country().replace(" ", ".")
    current_residence = fake.state().replace(" ", ".")

    log_line = LINE.format(
        first_name = first_name,
        last_name = last_name,
        entry_date=time_local,
        occupation = occupation,
        origin_country = origin_country,
        current_residence = current_residence
    )

    return log_line

def write_log_line(log_file, line):
    with open(log_file, "a") as f:
        f.write(line)
        f.write("\n")

def clear_log_file(log_file):
    with open(log_file, "w+") as f:
        f.write("")

if __name__ == "__main__":
    current_log_file = LOG_FILE_A
    lines_written = 0

    clear_log_file(LOG_FILE_A)
    clear_log_file(LOG_FILE_B)

    while True:
        line = generate_log_line()

        write_log_line(current_log_file, line)
        lines_written += 1

        if lines_written % LOG_MAX == 0:
            new_log_file = LOG_FILE_B
            if current_log_file == LOG_FILE_B:
                new_log_file = LOG_FILE_A

            clear_log_file(new_log_file)
            current_log_file = new_log_file

        sleep_time = random.choice(range(1, 5, 1))

        time.sleep(sleep_time)


