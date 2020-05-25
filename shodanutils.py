import shodan
from shodan.cli.helpers import get_api_key
import Utilites
import time


def before_run(provider):
    pass


def after_run(provider):
    pass


# Shodan CLI should be setup to store an Access Key
def worker(provider, account):
    org = provider.get_client_for_root('organizations')
    describeAccount = org.describe_account(AccountId=account)
    networkTitle = account + " " + describeAccount["Account"]["Name"]
    print(networkTitle)

    ips = get_ips_for_account(provider, account)
    if len(ips) == 0:
        print(account + ": No public IP addresses in account.")
        return

    save_ips_to_file(accountId=account, ips=ips)

    api = shodan.Shodan(get_api_key())
    alerts = api.alerts(include_expired=True)

    alertId = get_alert(alerts, networkTitle)

    if not alertId:
        alert = api.create_alert(name=networkTitle, ip=ips)
        triggers = api.alert_triggers()
        for trigger in triggers:
            if trigger["name"] == "any":
                continue
            api.enable_alert_trigger(alert["id"], trigger["name"])

        api.add_alert_notifier(alert["id"], get_slack_notifier_id(api))
        print(account + ": Alert " + networkTitle + " created with IPs " + str(ips))
    else:
        api.edit_alert(alertId, ip=ips)
        print(account + ": Alert " + networkTitle + " updated with IPs " + str(ips))


def get_alert(alerts, networkTitle):
    for alert in alerts:
        if alert["name"] == networkTitle:
            return alert["id"]

    return ""


def get_slack_notifier_id(api):
    notifiers = api.notifier.list_notifiers()
    for notifier in notifiers["matches"]:
        if notifier["provider"] == "slack":
            return notifier["id"]

    # if no slack integration setup - return default notifier
    return "default"


def get_ips_for_account(provider, account):
    ips = list()
    for (region, client) in provider.get_clients_for_all_regions(account, 'ec2'):
        addresses_dict = client.describe_addresses()

        for eip_dict in addresses_dict['Addresses']:
            ip = eip_dict['PublicIp']

            # is_ip_found = find_alert(alerts, ip)
            #
            # if is_ip_found:
            #     continue

            ips.append(ip)

    return ips


def find_alert(alerts, ip):
    found_in_alert = ""
    for alert in alerts:

        if ip in alert["filters"]["ip"]:
            found_in_alert = alert
            break

    return found_in_alert


def find_ips(api, alerts):
    ips = []
    with open("Data/aws_elastic_ips.txt", 'r') as f:
        ips = f.readlines()
    ips_clear = [x.strip() for x in ips]

    for alert in alerts:
        if alert["name"] == "Networks":
            for ip in alert["filters"]['ip']:
                if ip not in ips_clear:

                    try:
                        print(api.host(ips=ip))
                    except:
                        print("No information available for that IP.")
                    continue
    #
    # for ip in ips:
    #     ip = ip.strip()
    #
    #     alert = find_alert(alerts, ip)
    #
    #     if alert:
    #         print(ip) # + " found in " + alert["name"])


def delete_alert_for_network(api, alerts, networkTitle):
    for alert in alerts:
        if alert["name"] == networkTitle:
            api.delete_alert(alert["id"])


def save_ips_to_file(accountId, ips):
    fileName = "Reports/" + accountId + "/" + accountId + "_all_public_ips"
    Utilites.write_data(fileName, ips)


if __name__ == '__main__':
    # You can debug your module here

    # api = shodan.Shodan(get_api_key())
    # scans = api.scans()
    #
    # for scan in scans["matches"]:
    #     print(scan["id"] + " - " + str(scan["size"]) + " - " + scan["status"])
    pass
