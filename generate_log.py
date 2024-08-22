import random

# 1 = icmp, 6 = tcp, 17 = udp
PROTOCOL_NUMBERS = [1, 6, 17]
PORT_NUMBERS = [49154, 49155, 49156, 49157, 443, 80, 1024, 23, 25, 110, 68, 143]
LOG_STATUS = ["ACCEPTED", "REJECTED"]
LINES_TO_GENERATE = 10000
GENERATED_LOG_FILE = "generated-flow-log.txt"


# 10,000 lines is roughly 1.1MB
def generate(lines, file):
    generated_log = open(file, "w")
    for _ in range(lines):
        protocol = random.choice(PROTOCOL_NUMBERS)
        port = random.choice(PORT_NUMBERS)
        log_status = random.choice(LOG_STATUS)

        generated_log.write(
            f"2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 {port} {port} {protocol} 25 20000 1620140761 1620140821 {log_status} OK\n"
        )
    generated_log.close()


def main():
    generate(LINES_TO_GENERATE, GENERATED_LOG_FILE)


main()
