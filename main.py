import Audit
import sys


print("Please enter root account number:")
rootAccount = sys.stdin.readline()

Audit.IAMAudit(rootAccount, 'data/all_accounts.txt')
