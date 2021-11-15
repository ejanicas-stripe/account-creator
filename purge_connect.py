#!/usr/bin/env python

"""Purge Connect Accounts for Testing.

The aim of this script is to quickly delete Connect Express test accounts for BWI. 
It deletes all accounts previously generated with the create_express_connect.py script.

The output from create_express_connect.py is stored in a file express_accounts.txt on the same directory of this script with the format:
[(account_id_1, onboarding_url_1), ..., (account_id_n, onboarding_url_n)]
"""

import ast
import os
import stripe

stripe.api_key = os.getenv('STRIPE_API_KEY')

__author__ = "Eduardo Janicas"
__copyright__ = "2021 Stripe, Inc."
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Eduardo Janicas"
__email__ = "ejanicas@stripe.com"
__status__ = "Prototype"

if __name__ == '__main__':
    if os.path.exists("express_accounts.txt"):
        print("Reading express_account.txt file...")
        with open('express_accounts.txt') as f:
            accounts = ast.literal_eval(f.read())
            # accounts is of format [(account_id_1, onboarding_url_1), ..., (account_id_n, onboarding_url_n)]
            for account in accounts:
                print("Deleting account " + account[0])
                # account is of format (account_id_n, onboarding_url_n)
                stripe.Account.delete(account[0])
        print("All accounts deleted. Preparing to remove express_accounts.txt")
        os.remove("express_accounts.txt")
        print("express_accounts.txt removed")

    else:
        print("No express_accounts.txt file to delete from. Try running create_express_connect.py first")
