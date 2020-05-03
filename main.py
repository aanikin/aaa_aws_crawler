import Audit
import sys

Audit.IAMAudit('975464189649', 'data/all_accounts.txt')

exit()

print("Please enter root account number:")
rootAccount = sys.stdin.readline()

Audit.IAMAudit(rootAccount, 'data/all_accounts.txt')
