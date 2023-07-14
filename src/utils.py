import re


def read_credentials() -> list[str]:
    '''Reads the database credentials from the config.ini file and returns them as a list{username, password}.'''
    with open('config.ini') as f:
        credentials = f.read()

    username_match = re.search(
        r"^(username)[ ]*=(?=\s*(\w+))", credentials, re.IGNORECASE)
    if username_match:
        username = username_match.group(2)

    password_match = re.search(
        r"^(password)[ ]*=(?=\s*(\w+))", credentials, re.IGNORECASE)
    if password_match:
        password = password_match.group(2)

    return [username, password]
