import csv

# Declare constants for the file names in case we want to use
# other inputs more easily.
LOOKUP_TABLE_FILE = "lookuptable.csv"
FLOW_LOG_FILE = "generated-flow-log.txt"
RESULTS_FILE = "results.txt"


# This function will read in the data from the LOOKUP_TABLE_FILE file into a dictionary
# It assumes the column order is: dstport,protocol,tag
def open_lookup_table(file):
    # Declaring an empty dictionary to read in the content of the lookup table file
    data = {}

    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        # Assuming the order of the columns is correct, the contents are iterated through each row of the file
        # and put into the 'data' dictionary in this format: {('25', 'tcp'): 'sv_P1',}
        for row in reader:
            port = row[0]
            protocol = row[1]
            tag = row[2]
            data[(port, protocol)] = tag

    # print("Data: ", data)
    return data


# The field indexes from the AWS flow log documentation with the count starting at 0
# https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
#
# The protocol information can be found here: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
def parser(flow_log_file, lookup_table_data):
    # declare empty dictionaries to write the count data
    tag_counter = {}
    port_and_protocol_counter = {}

    # a constant dictionary with the protocol numbers (in string format)
    PROTOCOLS = {
        "6": "tcp",
        "17": "udp",
        "1": "icmp",
    }

    with open(flow_log_file, "r") as f:
        for line in f:
            field = line.split()  # since the log is space separated
            dstport = field[6]  # look at the 7th field of the row based on the AWS docs
            protocol = PROTOCOLS.get(
                field[7]
            )  # using the protocols dictionary key, get the value i.e. "6" -> "tcp"

            key = (dstport, protocol)
            value = lookup_table_data.get(key, "Untagged")

            # Counting for the tags and the port/protocols
            # and writing the data to their dictionaries
            if value.lower() in tag_counter:
                tag_counter[value.lower()] += 1
            else:
                tag_counter[value.lower()] = 1

            if key in port_and_protocol_counter:
                port_and_protocol_counter[key] += 1
            else:
                port_and_protocol_counter[key] = 1

    return tag_counter, port_and_protocol_counter


def write_results(tag_counter, port_and_protocol_counter, file):
    # Declaring the headers as string lists to avoid the csv writer from adding quotes
    tag_count_header = ["Tag", "Count"]
    port_and_protocol_header = ["Port", "Protocol", "Count"]

    with open(file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Tag Counts:"])
        writer.writerow(tag_count_header)

        # iterate over and write the Tag,Count rows
        for tag, count in tag_counter.items():
            writer.writerow([tag, count])

        writer.writerow(["---------------"])
        writer.writerow(["Port/Protocol Counts:"])
        writer.writerow(port_and_protocol_header)

        # iterate over and write the Port,Protocol,Count rows
        for (port, protocol), count in port_and_protocol_counter.items():
            writer.writerow([port, protocol, count])


def main():
    # Read in the data from the lookup table file and pass it to the parser function
    lookup_table_data = open_lookup_table(LOOKUP_TABLE_FILE)
    # assign the returned parsed data
    tag_count, port_and_protocol_count = parser(FLOW_LOG_FILE, lookup_table_data)
    write_results(tag_count, port_and_protocol_count, RESULTS_FILE)
    print(
        f"The flow log has been parsed. Check the {RESULTS_FILE} file for the results."
    )


"""
Run the main function when executing the python main.py command
"""
main()
