# DB Polluter

An anti phishing tool to pollute database

## Installation

### Pipenv

You could use [Pipenv](https://pipenv.pypa.io/en/latest/install/) to install dependencies.

Install python dependencies:

```bash
pipenv install
```

Pipenv will create a virtual env.

Activate the virtual env

```bash
pipenv shell
```

### Classic installation

You can use the `requirements.txt` file to install dependencies in your favorite virtual env.

## How to run

The script uses a config file in JSON or YAML format

Run the project like this

```bash
python main.py -file example.json
```

or with the `--burp` flag to analyse the requests send by the script with [Burp Suite COmmunity Edition](https://portswigger.net/burp/communitydownload)

```bash
python main.py -file example.json --burp
```

## Config file

```json
{
    "base_url": "https://www.example.com",
    "forms": [
        {
            "path": "/actions/login.php",
            "fields": {
                "prenom": "first_name",
                "nom": "last_name",
                "day": "birthday_day",
                "month": "birthday_month",
                "year": "birthday_year",
                "mail": "email"
            }
        },
        {
            "path": "/actions/card.php",
            "fields": {
                "input_cc_name": {
                    "concat": ["last_name", "first_name"]
                },
                "input_cc_num": "credit_card_number",
                "input_cc_exp": "credit_card_expire",
                "input_cc_cvv": "credit_card_security_code"
            }
        }
    ]
}
```

- `base_url`: is the domain of the phishing website, the target.
- `forms`: list of forms send to the phishing website. This list can has only one element.
  - `path`: is the website's path where le form is POST. Path variable is combine with `base_url` to make the complite URL.
  - `fields`: list of form fields where you have to define keys and types of values. Key is the field name in form of the target. Type value is a string reconize by the script to file the form field with a fake vale.  

### Type value

- `first_name`: set a fake first name
- `last_name`: set a fake last name
- `birthday_day`: set a fake  day of a fake birthday
- `birthday_month`: set a fake month of a fake birthday
- `birthday_year`: set a fake  year of a fake birthday
- `email`: set a fake email
- `street_address`: set a fake street address
- `postcode`: set a fake postcode
- `city`: set a fake city
- `phone_number`: set a fake phone number
- `credit_card_number`: set a fake mastercard, visa, visa16, visa19 number
- `credit_card_expire`: set a fake credit card expire date
- `credit_card_security_code`: set a fake credit card security code (CCV)

### Specific Type value

- `select`: set a random choice in the given list
- `concat`: concat pre define variable in a string
- `random_int`: set a random int in min and max range given limit
