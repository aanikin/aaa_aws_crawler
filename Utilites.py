import csv
import datetime
import json


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
            f.writelines(name + ":" + json.dumps(value, default=datetime_handler) + '\n')


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def write_data(filePrefix, data, type="json"):
    if type == "json":
        with open(filePrefix + "." + type, 'w') as f:
            json.dump(data, f, default=datetime_handler)
    else:
        with open(filePrefix + "." + type, 'w') as f:
            f.writelines(data)
