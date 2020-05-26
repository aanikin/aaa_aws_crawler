import datetime

from utilites import log_output

REPORT_UNACCOCIATED_IPS = "Reports/all_unaccociated_IPs.txt"


def before_run(provider):
    with open(REPORT_UNACCOCIATED_IPS, 'w') as f:
        f.write("[" + datetime.datetime.now().isoformat() + "] \n")


def after_run(provider):
    pass


def worker(provider, account):
    org = provider.get_client_for_root('organizations')
    describeAccount = org.describe_account(AccountId=account)
    networkTitle = account + " " + describeAccount["Account"]["Name"]
    log_output(networkTitle)

    ips = get_ips_for_account(provider, account, association="NOT ASSOCIATED")
    log_output(str(ips))

    if len(ips) > 0:
        with open(REPORT_UNACCOCIATED_IPS, 'a') as f:
            f.write(networkTitle + "\n")
            f.write(str(ips) + "\n")


def get_ips_for_account(provider, account, association="ALL"):
    ips = []
    for (region, client) in provider.get_clients_for_all_regions(account, 'ec2'):
        addresses_dict = client.describe_addresses()

        for eip_dict in addresses_dict['Addresses']:
            ip = eip_dict['PublicIp']

            if association == "ALL":
                ips.append(ip)
                continue

            if association == "ASSOCIATED":
                if 'AssociationId' in eip_dict:
                    ips.append(ip)
                    continue

            if association == "NOT ASSOCIATED":
                if 'AssociationId' not in eip_dict:
                    ips.append(ip)
                    continue

    return ips


if __name__ == '__main__':
    # You can debug your module here

    # api = shodan.Shodan(get_api_key())
    # scans = api.scans()
    #
    # for scan in scans["matches"]:
    #     print(scan["id"] + " - " + str(scan["size"]) + " - " + scan["status"])
    pass
