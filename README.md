# Express Connect Account Creator

The aim of this script is to quickly generate Connect Express test accounts.

## Description

Testing is important to make sure your Connect integration handles different flows correctly.
Use test mode to simulate live mode while taking advantage of Stripe-provided special tokens to make testing easier.

We use test tokens to pre-fill success verification statuses.
The following tokens can be used to test verification with Custom and Express accounts.

Details on the account’s acceptance of the Stripe Services Agreement from Connect Express accounts needs to happen via the dashboard.
For that reason the output of this script needs to be manually accessed to accept the TOS. The output is of format:
```
account_id_1: Onboarding URL 1
account_id_2: Onboarding URL 2
...
account_id_n: Onboarding URL N
```

The output is also stored in a file express_accounts.txt on the same directory of this script with the format:
```
[(account_id_1, onboarding_url_1), ..., (account_id_n, onboarding_url_n)]
```

## Getting Started

### Dependencies

- Python 3.4+
- Stripe Python Library
- [Register your platform](https://dashboard.stripe.com/account/applications/settings)

### Installing

- Just fill the `account_info.json` with the account information you want to create. The file has the following format:
```
{
    "data": [
        {
            "number": 1,
            "name": "Resort Name 1",
            "country": "US"
        },
        {
            "number": 2,
            "name": "Resort Name 2",
            "country": "US"        
        },
        ...
        {
            "number": resort_number,
            "name": "Resort Name",
            "country": "US"        
        }
    ]
}
```

### Executing program

1. Give executable privilege to `create_express_connect.py` and `purge_connect.py`

```
chmod +x create_express_connect.py
chmod +x purge_connect.py
```

2. Export your secret key as the STRIPE_API_KEY environment variable. Test mode secret keys have the prefix `sk_test*`

```
EXPORT STRIPE_API_KEY=sk_test_?????
```

3. Run the Account Creator

```
./create_express_connect.py
```

4. **MAKE SURE YOU LOGGED OUT OF YOUR CONSOLE BEFORE THIS STEP**. The output is displayed both in the console while running and in the `express_accounts.txt` file. Make sure to go through each of the URLs there to accept the TOS.

5. (Optional) If you want to delete all accounts created using this script, run the `purge_connect.py` script

```
./purge_connect.py
```

## Help

Any advise for common problems or issues contact me on ejanicas@stripe.com.

## Authors

Eduardo Janicas (ejanicas@stripe.com)

## Version History

- 0.1
  - Initial Release

## License

MIT License

Copyright (c) 2021 Stripe, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Useful Resources

- https://stripe.com/docs/connect/testing-verification
- https://stripe.com/docs/connect/testing
- https://stripe.com/docs/api/accounts
