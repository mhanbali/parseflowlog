PURPOSE:

This application will take in two files. A VPC flow log (version 2) file and a lookup table, parsing through the log with the lookup table as reference for matches. Then it will output the results to a plain text file.

USAGE:

python main.py

The results will be in a results.txt file in the same directory

ASSUMPTIONS:

- The flow log file has all the required fields. For example, no empty fields which would likely be replaced with a "-" according to the AWS docs
- The columns in the lookup table are in the correct order: dstport,protocol,tag
- This currently just supports version 2 of the VPC Flow Log
- The protocol decimals are from the referenced link in the AWS documentation: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
- Running Python 3.11.8 as the only tested version with the csv.py default library, and MacOS 14.5

MY NOTES:

- I knew I could use csv.py, but it's been almost two years since I had used it, so I referenced: https://docs.python.org/3/library/csv.html
- I wasn't familiar with flow log files, but the AWS documentation was very clear and on the field table within the docs I found it very helpful to have an external link to listing out the protocol decimals.
- I'm not sure if it was a requirement to have a larger log file of up to 10MB, or if it's just assumed to be able to handle that
- The data I used was from the assignment email found in the assignment.txt file
- I left some commented out print statements in case the reviewer finds that helpful
