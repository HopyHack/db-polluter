#!/usr/bin/env python3
import json
import random
import argparse
import os

import yaml
import requests
from faker import Faker

fake = Faker()


def run(data, use_burp):
    while True:
        try:
            session = requests.Session()

            if use_burp:
                session.proxies = {
                    "http": "http://127.0.0.1:8080",
                    "https": "http://127.0.0.1:8080",
                }

            session.headers.update(
                {
                    "User-Agent": fake.user_agent(),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                }
            )

            print("GET", data["base_url"])
            session.get(data["base_url"], verify=not use_burp)

            # Init global variable use in multi fields
            birthday = fake.date_between(start_date="-70y", end_date="-18y")

            for form in data["forms"]:
                data_to_post = {}

                for field_name, field_type in form["fields"].items():
                    if type(field_type) is dict:
                        if field_type.get("select", None):
                            variable_name = "%s_%s" % (field_name, "select")

                            vars()[variable_name] = random.choice(field_type["select"])

                            data_to_post[field_name] = vars()[variable_name]

                        if field_type.get("concat", None):
                            data_to_post[field_name] = ""
                            for var in field_type["concat"]:
                                data_to_post[field_name] += str(vars()[var]) + " "

                        if field_type.get("random_int", None):
                            data_to_post[field_name] = fake.random_int(
                                min=field_type["random_int"][0],
                                max=field_type["random_int"][1],
                            )

                    if type(field_type) is str:
                        if field_type == "first_name":
                            first_name = fake.first_name()
                            data_to_post[field_name] = first_name

                        elif field_type == "last_name":
                            last_name = fake.first_name()
                            data_to_post[field_name] = last_name

                        elif field_type == "birthday_day":
                            data_to_post[field_name] = birthday.day

                        elif field_type == "birthday_month":
                            data_to_post[field_name] = birthday.month

                        elif field_type == "birthday_year":
                            data_to_post[field_name] = birthday.year

                        elif field_type == "email":
                            email = fake.ascii_free_email()
                            data_to_post[field_name] = email

                        elif field_type == "street_address":
                            street_address = fake.street_address()
                            data_to_post[field_name] = street_address

                        elif field_type == "postcode":
                            postcode = fake.postcode()
                            data_to_post[field_name] = postcode

                        elif field_type == "city":
                            city = fake.city()
                            data_to_post[field_name] = city

                        elif field_type == "phone_number":
                            phone_number = fake.msisdn()
                            data_to_post[field_name] = phone_number

                        elif field_type == "credit_card_number":
                            card_type = random.choice(
                                ["mastercard", "visa", "visa16", "visa19"]
                            )
                            credit_card_number = fake.credit_card_number(
                                card_type=card_type
                            )
                            data_to_post[field_name] = credit_card_number

                        elif field_type == "credit_card_expire":
                            credit_card_expire = fake.credit_card_expire(end="+3y")
                            data_to_post[field_name] = credit_card_expire

                        elif field_type == "credit_card_security_code":
                            credit_card_security_code = fake.credit_card_security_code()
                            data_to_post[field_name] = credit_card_security_code

                url = data["base_url"] + form["path"]
                print("POST", url)
                session.post(
                    url=url,
                    data=data_to_post,
                    verify=not use_burp,
                )

        except KeyboardInterrupt as interuption:
            raise interuption

        except Exception as exception:
            print("Exception", url)
            print(exception)


def main():
    parser = argparse.ArgumentParser(
        description="e.g. python3 %s -file data_steps.json"
        % (os.path.basename(__file__))
    )
    parser.add_argument(
        "-file",
        required=True,
        help="File that describe form steps",
    )
    parser.add_argument(
        "--burp",
        action="store_true",
        help="Use Burp to localy analyse requests",
    )

    args = parser.parse_args()
    file_name = args.file
    use_burp = args.burp

    file = open(file_name)

    if ".json" in file_name:
        data = json.load(file)

    elif ".yml" in file_name or ".yaml" in file_name:
        data = yaml.safe_load(file)

    run(data, use_burp)


if __name__ == "__main__":
    main()
