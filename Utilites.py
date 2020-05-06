import csv


# def write_string_as_csv(data: bytes, file):
#     credential_report_csv = bytes(data).decode('ascii')
#     reader = csv.DictReader(credential_report_csv.splitlines())
#     with open(file, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=reader.__next__())
#         writer.writeheader()
#         for row in reader:
#             writer.writerow(row)

# Multiline file with child account numbers
def load_accounts_list(accountsFile):
    with open(accountsFile, 'r') as f:
        return f.read().splitlines()


def write_meta(filePrefix, metaData):
    with open(filePrefix + '_meta', 'w') as f:
        for name, value in metaData.items():
            f.writelines(name + ":" + value + '\n')


def write_data(filePrefix, data, type="json"):
    with open(filePrefix + "." + type, 'w') as f:
        f.writelines(data)
