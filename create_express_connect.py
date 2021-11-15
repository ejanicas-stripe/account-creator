#!/usr/bin/env python

"""Create Connect Express Accounts for Testing.

The aim of this script is to quickly generate Connect Express test accounts for BWI.

Testing is important to make sure your Connect integration handles different flows correctly. 
Use test mode to simulate live mode while taking advantage of Stripe-provided special tokens to make testing easier.

We use test tokens to pre-fill success verification statuses.
The following tokens can be used to test verification with Custom and Express accounts. 

Details on the account’s acceptance of the Stripe Services Agreement from Connect Express accounts needs to happen via the dashboard.
For that reason the output of this script needs to be manually accessed to accept the TOS. The output is of format:
account_id_1: Onboarding URL 1
account_id_2: Onboarding URL 2
...
account_id_n: Onboarding URL N

The output is also stored in a file express_accounts.txt on the same directory of this script with the format:
[(account_id_1, onboarding_url_1), ..., (account_id_n, onboarding_url_n)]

Useful resources:
https://stripe.com/docs/connect/testing-verification
https://stripe.com/docs/connect/testing
https://stripe.com/docs/api/accounts
"""

import json
import os
import sys
import stripe

stripe.api_key = os.getenv('STRIPE_API_KEY')

__author__ = "Eduardo Janicas"
__copyright__ = "2021 Stripe, Inc."
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Eduardo Janicas"
__email__ = "ejanicas@stripe.com"
__status__ = "Prototype"


def import_hotels(path):
    """
    Returns a dictionary of hotels to create

    Keyword Arguments:
    path -- path of the hotels JSON
    """
    f = open(path,)
    hotels = json.load(f)
    f.close()
    return hotels


def create_express_account(name, number, country):
    """
    Returns a tuple with an account id and an onboarding account link

    Keyword Arguments:
    name -- resort name
    number -- resort number
    country -- country code (ISO 3166-1 alpha-2 country code - US only at the moment)
    """
    # email is of format <name>@example.com
    account_email = "{}@example.com".format(name.lower().replace(" ", ""))
    # name is of format <number> <name>
    account_name = "{} {}".format(number, name)
    print("Creating " + account_name)
    # pre-polutate account with test data as per https://stripe.com/docs/connect/testing
    account = stripe.Account.create(
        type="express",
        country=country,
        email=account_email,
        business_type="company",
        company={
            "address": {
                "line1": "address_full_match",
                "city": "Schenectady",
                "postal_code": "12345",
                "state": "NY"
            },
            "structure": "sole_proprietorship",
            "name": account_name,
            "tax_id": "000000000",
            "phone": "0000000000",
        },
        external_account={
            "object": "bank_account",
            "country": "US",
            "currency": "usd",
            "routing_number": "110000000",
            "account_number": "000123456789",
        },
        business_profile={
            "mcc": "7011",
            "url": "https://www.bestwestern.com/",
            "name": account_name
        }
    )
    # You need to use the Persons API to collect information on the business owners
    stripe.Account.create_person(
        account.id,
        first_name="Jenny",
        last_name="Rosen",
        relationship={
            "owner": "true",
            "executive": "true",
            "representative": "true",
            "percent_ownership": "100",
            "title": "CEO",
        },
        address={
            "line1": "address_full_match",
            "city": "Schenectady",
            "postal_code": "12345",
            "state": "NY",
        },
        dob={
            "day": "01",
            "month": "01",
            "year": "1901",
        },
        ssn_last_4="0000",
        phone="000 000 0000",
        email=account_email,
    )
    stripe.Account.modify(
        account.id,
        company={
            "owners_provided": "true",
            "executives_provided": "true"
        },
    )
    # Account Links are the means by which an express connected account can accept its TOS
    account_link = stripe.AccountLink.create(
        account=account.id,
        refresh_url="https://dashboard.stripe.com/",
        return_url="https://dashboard.stripe.com/",
        type="account_onboarding",
    )
    return (account.id, account_link.url)


def create_express_accounts(hotels):
    """
    Returns a list of tuples wit an account ids and onboarding account links

    Keyword Arguments:
    hotels -- JSON of hotels to create
    """
    result = []
    for hotel in hotels["data"]:
        result.append(create_express_account(
            hotel["name"], hotel["number"], hotel["country"]))
    return result


if __name__ == '__main__':
    if not os.path.exists("account_info.json"):
        print("No account_info.json file to import hotels from. Try creating the account_info file first")
        sys.exit(0)

    print("Importing hotels from account_info.json...")
    hotels = import_hotels('account_info.json')
    # account_info.json expected format:
    # {
    #     "data": [
    #         {
    #             "number": 1,
    #             "name": "Hotel Name",
    #             "country": "US"  // ISO 3166-1 alpha-2 country code
    #         },
    #         ...
    #     ]
    # }
    print("account_info.json imported!")
    print("Creating Express Connect Accounts")
    accounts = create_express_accounts(hotels)
    print("All hotels created!")
    print("Creating express_account.txt file")
    # [(account_id_1, onboarding_url_1), ..., (account_id_n, onboarding_url_n)]
    with open('express_accounts.txt', 'a') as f:
        print(accounts, file=f)

    print("express_account.txt file created!")
    print()
    print("Final output:")
    # account_id_1: Onboarding URL 1
    # account_id_2: Onboarding URL 2
    # ...
    # account_id_n: Onboarding URL N
    for account in accounts:
        print(account[0] + ": " + account[1])