from utilites import log_output, write_data
import ec2


def before_run(provider):
    pass


def after_run(provider):
    pass


def worker(provider, account):
    support = provider.get_client_for_root('support')
    response = support.describe_trusted_advisor_checks(language="en")
    checks = []
    for check in response["checks"]:
        if check["category"] == "security":
            # checks.append(check["id"])
            response = support.describe_trusted_advisor_check_result(checkId=check["id"], language="en")
            if response["result"]["hasFlaggedResources"] == "True":
                for flResource in response["result"]["flaggedResources"]:
                    print("{} {} {}".format(flResource["resourceId"], flResource["status"]))

    response = support.describe_trusted_advisor_check_summaries(checkIds=checks)
    print(response["summaries"])
